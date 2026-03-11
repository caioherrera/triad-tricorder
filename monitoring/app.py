import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
import uuid
import json
import psutil
import threading
import time
import requests
import subprocess
import argparse

from flask import Flask, jsonify, request
from flask_cors import CORS

from core.logger import Logger
from core.message import MonitorRequestMessage, MonitorResultMessage, MonitorStatusMessage, Message
from core.setup import Setup

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

Setup.initialize_from_env()

def send_message(endpoint: str, message: Message):
    
    """
    Sends a JSON-encoded message to a specified backend API endpoint via HTTP POST.
    Args:
        endpoint (str): The API endpoint to send the message to.
        message (Message): The message object to be sent, which must implement a `to_json()` method.
    Returns:
        requests.Response: The response object returned by the POST request.
    Logs:
        - Sending message details including thread ID.
        - Response status code.
    """    

    Logger.write_log(f"Sending message to {endpoint} with thread_id {threading.get_ident()}", level_details = 2)

    response = requests.post(
        url = f'http://{Setup.backend_hostname}:{Setup.backend_port}/api/monitor/{endpoint}',
        data = message.to_json(),
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    )

    Logger.write_log(f"Response status code: {response.status_code}", level_details = 2)

    return response

def is_process_still_running(processes: list):

    process = psutil.Process(processes[0].pid)

    is_running: bool = process.is_running() and process.status() != psutil.STATUS_ZOMBIE
    if not is_running:
        Logger.write_log(f'Process with PID {processes[0].pid} has terminated, status = {process.status()}.', level_details = 1)

    return is_running

def collect_data_point(processes: list, interval: float, last_io: int, last_io_bytes: int):
    
    """
    Collects a data point from the specified processes at a given interval.
    Args:
        processes: A list of psutil.Process objects to collect data from.
        interval: The time interval (in seconds) to wait between data collection.
        last_io: The last recorded I/O counter value.
        last_io_bytes: The last recorded I/O bytes value.
    Returns:
        A tuple containing the collected data point values.
    """

    process = psutil.Process(processes[0].pid)

    raw_cpu = process.cpu_percent(interval)
    raw_cpu = raw_cpu / psutil.cpu_count()  # Normalize by number of CPU cores

    raw_mem = process.memory_info().rss
    sample_io = process.io_counters()
    raw_io_diff = (sample_io.read_count + sample_io.write_count) - last_io
    curr_io = sample_io.read_count + sample_io.write_count

    # io bytes
    io_bytes_diff = (sample_io.read_bytes + sample_io.write_bytes) - last_io_bytes
    curr_io_bytes = sample_io.read_bytes + sample_io.write_bytes

    return raw_cpu, raw_mem, raw_io_diff, io_bytes_diff, curr_io, curr_io_bytes

def execute_artifact(command: list, replicate_app_logs_to_stdout: bool = False):
    
    """
    Executes a command as a subprocess and returns the process handle.
    Args:
        command (list): The command to execute, including the application path and arguments.
        replicate_app_logs_to_stdout (bool): If True, replicates application logs to stdout.
    Returns:
        A list of processes representing the started processes.
    Logs:
        - Started process details including process ID and thread ID.
    """

    is_network_telemetry: bool = "/tmp/bin" in command

    client_command: list = []

    # TO-DO: Handle command line parsing better
    if is_network_telemetry:

        application_path, artifact_file_path, workload_input_value = command
        
        subprocess.run(["rm","-Rf","/usr/lib/x86_64-linux-gnu/libdataprocessing.so.1"])
        subprocess.run(["ln","-s", artifact_file_path,"/usr/lib/x86_64-linux-gnu/libdataprocessing.so.1"])

        command = [ application_path, workload_input_value ]
        Logger.write_log(f'Server command: {command}', level_details = 1)

        client_command = [ application_path.replace('server', 'client'), workload_input_value ]
        Logger.write_log(f'Client command: {client_command}', level_details = 1)

    process = subprocess.Popen(command, stdout = sys.stdout if replicate_app_logs_to_stdout else subprocess.PIPE, stderr=subprocess.STDOUT)

    processes = [ process ]
    Logger.write_log(f'Started process with PID: {processes[0].pid}', level_details = 2)

    if is_network_telemetry:
        
        client_process = subprocess.Popen(client_command)
        
        processes.append(client_process)
        Logger.write_log(f'Started client process with PID: {processes[1].pid}', level_details = 2)
            
    return processes

def save_csv_file(execution_results: dict, root_folder: str = "../profiles", folder_name: str = None):
    
    """
    Saves the execution results to a CSV file.
    Args:
        execution_results (dict): The execution results to save.
        root_folder (str): The root folder to save the CSV file in.
        folder_name (str): The name of the folder to save the CSV file in.
    Returns:
        The file path of the saved CSV file.
    """

    if folder_name is None:

        if not os.path.exists(root_folder):
            os.makedirs(root_folder)

        while True:
            folder_name = f'{root_folder}/{uuid.uuid4()}'
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)
                break

    while True:
        file_name = f'{folder_name}/{uuid.uuid4()}.csv'
        if not os.path.exists(file_name):
            break
    
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(execution_results.keys())
        writer.writerows(zip(*execution_results.values()))

    return file_name

def run_monitoring(session_workload_id: int, session_id: int, workload_id: int, command: list, num_executions: int, 
                   sample_interval: float, sample_count: int, reading_types: list, continuous_execution: bool = False,
                   report_status: bool = True, replicate_app_logs_to_stdout: bool = False):
    
    """
    Executes the monitoring of a workload.
    Args:
        session_workload_id (int): The session workload ID.
        session_id (int): The session ID.
        workload_id (int): The workload ID.
        command (list): The command to execute.
        num_executions (int): The number of executions to perform.
        sample_interval (float): The interval between samples.
        sample_count (int): The number of samples to collect.
        reading_types (list): The types of readings to collect.
        continuous_execution (bool): Whether to keep the processes running after data collection.
        report_status (bool): Whether to report the status.
        replicate_app_logs_to_stdout (bool): Whether to replicate application logs to stdout.
    Returns:
        A tuple containing the result file paths, start times, and end times.
    Logs:
        - Starting monitoring and execution steps
        - Command to be executed
    """

    file_paths = ['' for i in range(num_executions)]
    start_times = [0.0 for i in range(num_executions)]
    end_times = [0.0 for i in range(num_executions)]

    Logger.write_log('Starting monitoring step', level_details = 1)

    Logger.write_log(f'Command: {command}', level_details = 1)

    folder_name: str = None
    processes = None

    for execution in range(num_executions):

        if report_status:
            status = MonitorStatusMessage(
                session_workload_id = session_workload_id,
                session_id = session_id,
                workload_id = workload_id,
                is_last_message = execution == num_executions - 1,
                curr_execution = execution,
                total_executions = num_executions
            )

            response = send_message('status', status)
            Logger.write_log(f'Status response: {response}', level_details = 2)

        Logger.write_log(f'Starting execution #{execution}', level_details = 2)

        results = { reading_type: [] for reading_type in reading_types }

        start_times[execution] = time.time()

        if processes == None or not continuous_execution:
            processes = execute_artifact(command, replicate_app_logs_to_stdout)

        last_io, last_io_bytes = 0, 0

        Logger.write_log(f'Checking process {processes[0].pid} for collection of {sample_count} data samples', level_details = 2)

        for sample in range(sample_count):

            ## Removing this for now, as the previous experiments didn't preempt the application
            # if not is_process_still_running(processes):
            #     break

            cpu, ram, io_data, io_bytes, last_io, last_io_bytes = collect_data_point(processes, sample_interval, last_io, last_io_bytes)

            if "cpu" in results:
                results["cpu"].append(cpu)

            if "ram" in results:
                results["ram"].append(ram)

            if "io_data" in results:
                results["io_data"].append(io_data)

            if "io_bytes" in results:
                results["io_bytes"].append(io_bytes)

        if not continuous_execution:

            Logger.write_log("Killing processes after data collection", level_details = 2)

            for process in processes:
                process.kill()

        end_times[execution] = time.time()

        file_paths[execution] = save_csv_file(results, folder_name = folder_name)

        if folder_name is None:
            folder_name = os.path.dirname(file_paths[execution])

        Logger.write_log(f'Saving results for execution #{execution} at {file_paths[execution]}', level_details = 2)

        Logger.write_log(f'Ending execution #{execution}', level_details = 2)

    Logger.write_log('Finishing monitoring step', level_details = 1)

    return file_paths, start_times, end_times

def process_incoming_message(message_data: MonitorRequestMessage):
    
    """
    Processes the messages received from the backend with the request for monitoring, and sends the results back.
    Args:
        message_data: the monitor request message.
    Logs:
        - Message data
        - Monitoring results and response
    """

    Logger.write_log(f'Message data: {message_data}', level_details = 2)
    monitor_start_time: float = time.time()

    # TO-DO: Better handle command line parsing
    command_line: list = [
        message_data.app_command_line or "",
        message_data.artifact_file_path or "",
        message_data.workload_input_value or ""
    ]

    file_paths, start_times, end_times = run_monitoring(
        message_data.session_workload_id,
        message_data.session_id,
        message_data.workload_id,
        ' '.join(command_line).split(' '),
        message_data.num_executions,
        message_data.sample_interval,
        message_data.sample_count,
        message_data.reading_types,
        message_data.continuous_execution
    )

    monitor_end_time: float = time.time()

    results = MonitorResultMessage(
        session_workload_id = message_data.session_workload_id,
        session_id = message_data.session_id,
        workload_id = message_data.workload_id,
        file_paths = file_paths,
        start_times = start_times,
        end_times = end_times,
        is_last_message = message_data.is_last_message,
        monitor_start_time = monitor_start_time,
        monitor_end_time = monitor_end_time,
        full_process = message_data.full_process
    )   

    Logger.write_log(f'Sending back results: {results}', level_details = 2)

    response = send_message('result', results)
    Logger.write_log(f'Response: {response}', level_details = 2)

# [POST] /api/monitor
@app.post('/api/monitor')
def monitor():

    """
        POST API to receive monitoring requests from clients.
    """
    
    Logger.write_log('Received monitor request', level_details = 2)

    request_data: dict = json.loads(request.get_json())
    if not request_data:
        return jsonify({"error": "Invalid JSON"}), 400

    Logger.write_log(request_data)

    message_data = MonitorRequestMessage(
        session_workload_id = request_data['session_workload_id'],
        session_id = request_data['session_id'],
        workload_id = request_data['workload_id'],
        is_last_message = request_data['is_last_message'],
        num_executions = request_data['num_executions'],
        sample_interval = request_data['sample_interval'],
        sample_count = request_data['sample_count'],
        app_command_line = request_data['app_command_line'],
        artifact_file_path = request_data['artifact_file_path'],
        workload_input_value = request_data['workload_input_value'],
        reading_types = request_data['reading_types'],
        continuous_execution = request_data['continuous_execution'],
        full_process = request_data['full_process']
    )

    threading.Thread(target=process_incoming_message, args = (message_data, )).start()    

    return jsonify({"status": "Monitoring started"}), 200

if __name__ == "__main__":

    """
    This file will be executed as __main__ for independent executions. It can be instantiated through a terminal, by setting up the parameters
    described below. It will then monitor the executions for the specified application and generate the corresponding profiles.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("--executions", help = "Number of executions", type = int, default = 10)
    parser.add_argument("--sample-interval", help = "Sample interval in seconds", type = float, default = 0.1)
    parser.add_argument("--sample-count", help = "Number of samples to collect", type = int, default = 30)
    parser.add_argument("--command-line", help = "Command line to be executed", type = str, nargs = '+', required = True)
    parser.add_argument("--reading-types", help = "Types of readings to collect", type = str, nargs = '+', default = ["cpu", "ram", "io_data", "io_bytes"])
    parser.add_argument("--replicate-application-logs-to-stdout", help = "Replicate application logs to stdout", action = "store_true", default = False)
    parser.add_argument("--log-detail-level", help = "Log detail level", type = int, choices = [0, 1, 2], default = 2)
    parser.add_argument("--continuous-execution", help = "Keep processes running after data collection", action = "store_true", default = False)

    args = parser.parse_args()
    Logger.set_log_details(args.log_detail_level)

    Logger.write_log(f'Starting monitor execution as __main__ with parameters: {args}', level_details = 1)
    monitor_start_time: float = time.time()

    file_paths, start_times, end_times = run_monitoring(
        -1, -1, -1,
        args.command_line,
        args.executions,
        args.sample_interval,
        args.sample_count,
        args.reading_types,
        report_status = False,
        continuous_execution = args.continuous_execution,
        replicate_app_logs_to_stdout = args.replicate_application_logs_to_stdout,
    )

    monitor_end_time: float = time.time()
    Logger.write_log(f'Monitoring execution finished in {monitor_end_time - monitor_start_time} seconds', level_details = 1)

    if len(file_paths) > 0:
        Logger.write_log(f'Profiles saved in: {os.path.dirname(file_paths[0])}', level_details = 1)
