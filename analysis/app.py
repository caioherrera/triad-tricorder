import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import json
import uuid
import threading
import shutil
import requests
import argparse

from flask import Flask, jsonify, request
from flask_cors import CORS

from core.logger import Logger
from core.message import AnalysisRequestMessage, AnalysisResultMessage, AnalysisStatusMessage, Message
from core.utils.execution_utils import ExecutionUtils
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

    Logger.write_log(f"Sending message to {endpoint} with thread_id {threading.get_ident()}")
    response = requests.post(
        url = f'http://{Setup.backend_hostname}:{Setup.backend_port}/api/analysis/{endpoint}',
        data = message.to_json(),
        headers = {'Content-Type': 'application/json', 'Accept': 'application/json'}
    )
    return response

def generate_temp_folder():

    """
    Generates a temporary folder for storing intermediate files.
    Returns:
        str: The path to the created temporary folder.
    """

    folder = f'/tmp/{uuid.uuid4()}'
    os.makedirs(folder)

    return folder

def check_for_new_groups(damicore_groups: dict, ref_profiles: dict):

    """
    Checks for new groups in the DAMICORE output by comparing with reference profiles.
    Args:
        damicore_groups (dict): The generated groups to check.
        ref_profiles (dict): The reference profiles to compare against.
    Returns:
        list: A list of new group IDs found in the DAMICORE output, without any reference profile.
    """

    new_groups: list = []

    for group_id in damicore_groups.keys():

        found_new_group: bool = True
        for profile_id in damicore_groups[group_id]:

            ref_keys: list = [ str(x) for x in ref_profiles.keys() ]
            if str(profile_id) in ref_keys:
                Logger.write_log(f'Profile {profile_id} on group {group_id} belongs to reference session.', True)
                found_new_group = False
                break

        if found_new_group:
            new_groups.append(group_id)
    
    if len(new_groups) > 0:
        Logger.write_log(f'Found new groups: {new_groups}', True)

    return new_groups 

def process_damicore_groups(damicore_output_file: str) -> dict:

    """
    Processes the DAMICORE output file and extracts group information.
    Args:
        damicore_output_file (str): The path to the DAMICORE output file.
    Returns:
        dict: A dictionary mapping group IDs to lists of profile IDs.
    """

    groups: dict = {}

    with open(damicore_output_file, 'r') as file:
        damicore_output = file.readlines()

    Logger.write_log(f'damicore output file content: {damicore_output}')

    for line in damicore_output:

        profile_id, group_id = int(line.split('.')[0]), int(line.split(',')[1].replace('\n', ''))
        Logger.write_log(f'Group: {group_id}, profile: {profile_id}')

        if not group_id in groups:
            groups[group_id] = []
        groups[group_id].append(profile_id)

    Logger.write_log("Finished file lines. Returning result")
    
    return groups

def run_analysis(session_workload_id: int, session_id: int, workload_id: int, profiles: dict, ref_profiles: dict, restrictive: bool, report_status: bool = True) -> dict:

    """
    Runs the analysis for the given session and workload.
    Args:
        session_workload_id (int): The session workload ID.
        session_id (int): The session ID.
        workload_id (int): The workload ID.
        profiles (dict): The profiles to analyze.
        ref_profiles (dict): The reference profiles for comparison.
        report_status (bool): Whether to report status updates.
    Returns:
        dict: The analysis results.
    """

    Logger.write_log(f"Restrictive mode: {restrictive}", level_details = 1)

    Logger.write_log('Starting analysis step', level_details = 1)

    temp_folder = generate_temp_folder()
    Logger.write_log(f"Created temp folder {temp_folder}", level_details = 2)
    
    output_temp_folder = generate_temp_folder()
    Logger.write_log(f"Created output temp folder {output_temp_folder}", level_details = 2)

    for profile_id in ref_profiles.keys():
        shutil.copy(ref_profiles[profile_id], f'{temp_folder}/{profile_id}.csv')

    anomaly_detected: bool = False
    anomaly_confirmed: bool = False
    total_executions: int = len(profiles.keys())
    curr_execution: int = 1
    first_profile: bool = None

    for profile_id in profiles.keys():

        Logger.write_log(f'Including profile {profile_id}', level_details = 2)
        shutil.copy(profiles[profile_id], f'{temp_folder}/{profile_id}.csv')

        first_profile = True if first_profile == None else False

        if first_profile and len(ref_profiles.keys()) == 0:
            continue
        
        if report_status:

            status = AnalysisStatusMessage(
                session_workload_id = session_workload_id,
                session_id = session_id,
                workload_id = workload_id,
                curr_execution = curr_execution,
                total_executions = total_executions,
                is_last_message = curr_execution == total_executions
            )

            response = send_message('status', status)
            Logger.write_log(f'Status response: {response}', level_details = 2)

        damicore_output = f'{output_temp_folder}/damicore.out'   

        cmd = f'{sys.executable} {Setup.damicore_path} --compressor {Setup.damicore_compressor} --model-order {Setup.damicore_model_order} --memory {Setup.damicore_memory}'\
            + f' --tree-output {output_temp_folder}/damicore.newick --graph-image {output_temp_folder}/damicore.png' \
            + f' -o {damicore_output} {temp_folder}'

        Logger.write_log(f'Running command: {cmd}', level_details = 1)

        # TODO This FileNotFoundError is not known but has been ocasionaly happening on latest Damicore version
        # TODO Check whether error Weights must not be negative is expected
        ExecutionUtils.resilient_execute(cmd, tolerated_exceptions=['FileNotFoundError', 'Weights must not be negative'], timeout_in_seconds = 600)

        Logger.write_log(f"Damicore result generated on {damicore_output}", level_details = 2)

        damicore_groups = process_damicore_groups(damicore_output)
        Logger.write_log(f'Damicore groups: {damicore_groups}', level_details = 2)

        if ref_profiles is None or len(ref_profiles) == 0:
            Logger.write_log('There is no reference session to search for anomalies', level_details = 1)
        elif len(check_for_new_groups(damicore_groups, ref_profiles)) > 0:
            
            Logger.write_log('Detected anomaly!', level_details = 1)
            
            if restrictive:
                if anomaly_detected:
                    anomaly_confirmed = True
                    break
            
            anomaly_detected = True
            
            if not restrictive:
                anomaly_confirmed = True
                break
        else:
            Logger.write_log('Did not detect anomaly', level_details = 1)
            anomaly_detected = False

        curr_execution += 1

    Logger.write_log('Finishing analysis step', level_details = 1)

    return damicore_groups, anomaly_confirmed, curr_execution, total_executions

def process_incoming_message(message_data: AnalysisRequestMessage):

    """
    Processes the messages received from the backend with the request for analysis, and sends the results back.
    Args:
        message_data: the analysis request message.
    Logs:
        - Message data
        - Analysis results and response
    """    

    Logger.write_log(f'Message data: {message_data}', level_details=2)
    analysis_start_time: float = time.time()

    damicore_groups: dict = {}
    anomaly_detected: bool = False

    damicore_groups, anomaly_detected, curr_execution, total_executions = run_analysis(
        message_data.session_workload_id, message_data.session_id, message_data.workload_id, message_data.profiles, message_data.ref_profiles, message_data.restrictive)

    analysis_end_time: float = time.time()

    results = AnalysisResultMessage(
        session_workload_id = message_data.session_workload_id,
        session_id = message_data.session_id,
        workload_id = message_data.workload_id,
        groups = damicore_groups,
        verdict = anomaly_detected,
        is_last_message = message_data.is_last_message,
        analysis_start_time = analysis_start_time,
        analysis_end_time = analysis_end_time,
        total_executions = total_executions,
        actual_executions = curr_execution,
    )

    Logger.write_log(f'Sending back results: {results}', level_details=2)

    response = send_message('result', results)
    Logger.write_log(f'Response: {response}', level_details=2)

# [POST] /api/analysis
@app.post('/api/analysis')
def analysis():

    """
        POST API to receive analysis requests from clients.
    """
    
    Logger.write_log('Received analysis request', level_details=2)

    request_data: dict = json.loads(request.get_json())
    if not request_data:
        return jsonify({"error": "Invalid JSON"}), 400

    Logger.write_log(request_data)

    message_data = AnalysisRequestMessage(
        session_workload_id = request_data['session_workload_id'],
        session_id = request_data['session_id'],
        workload_id = request_data['workload_id'],
        is_last_message = request_data['is_last_message'],
        profiles = request_data['profiles'],
        ref_profiles = request_data.get('ref_profiles', {}),
        restrictive = request_data['restrictive']
    )

    threading.Thread(target=process_incoming_message, args=(message_data, )).start()

    return jsonify({"status": "Analysis started"}), 202

if __name__ == "__main__":

    """
    This file will be executed as __main__ for independent executions. It can be instantiated through a terminal, by setting up the parameters
    described below. It will then execute the analysis and grouping of the specified resource consumption profiles.
    """

    parser = argparse.ArgumentParser()

    parser.add_argument('--profiles-folder', type=str, required=True, help='Path to the folder containing the profiles')
    parser.add_argument('--ref-folder', type=str, default='', help='Path to the folder containing the reference profiles')
    parser.add_argument("--log-detail-level", help = "Log detail level", type = int, choices = [0, 1, 2], default = 2)
    parser.add_argument('--restrictive', action='store_true', help='Enable restrictive mode for anomaly detection')

    args = parser.parse_args()
    Logger.set_log_details(args.log_detail_level)

    Logger.write_log(f'Starting analysis execution as __main__ with parameters {args}', level_details = 1)
    analysis_start_time = time.time()

    index: int = 0
    profiles: dict = {}
    ref_profiles: dict = {}

    for file_name in os.listdir(args.profiles_folder):
        if file_name.endswith('.csv'):
            profiles[index] = os.path.join(args.profiles_folder, file_name)
            index += 1
    
    if args.ref_folder:
        for file_name in os.listdir(args.ref_folder):
            if file_name.endswith('.csv'):
                ref_profiles[index] = os.path.join(args.ref_folder, file_name)
                index += 1

    restrictive: bool = args.restrictive

    damicore_groups, anomaly_detected, curr_execution, total_executions = run_analysis(
        -1, -1, -1, profiles, ref_profiles, restrictive, report_status=False)

    analysis_end_time = time.time()
    Logger.write_log(f'Analysis execution finished in {analysis_end_time - analysis_start_time} seconds', level_details = 1)

    Logger.write_log(f'Damicore groups: {damicore_groups}', level_details = 1)
    Logger.write_log(f'Anomaly detected: {anomaly_detected}', level_details = 1)