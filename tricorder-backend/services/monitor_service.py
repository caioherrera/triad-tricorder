import requests

from core.entities.session import DBSession, SessionService
from core.message import MonitorRequestMessage, MonitorResultMessage, MonitorStatusMessage
from core.entities.session_workload import DBSessionWorkload, SessionWorkloadService
from core.entities.workload import DBWorkload
from core.entities.profile import ProfileService
from core.logger import Logger
from core.setup import Setup

from services.analysis_service import AnalysisService

class MonitorService:

    @staticmethod
    def trigger_monitor(session: DBSession, workload: DBWorkload, is_last_workload: bool = False, full_process: bool = False):

        session_workload: DBSessionWorkload = SessionWorkloadService.get_session_workload(session.id, workload.id)
        message: MonitorRequestMessage = MonitorRequestMessage(
            session_workload_id = session_workload.id,
            session_id = session.id,
            workload_id = workload.id,
            num_executions = session.num_executions,
            sample_interval = session.sample_interval,
            sample_count = session.sample_count,
            app_command_line = session.artifact.application.command_line,
            artifact_file_path = session.artifact.file_path,
            workload_input_value = workload.input_value,
            reading_types = ["cpu", "ram", "io_data", "io_bytes"],
            is_last_message = is_last_workload,
            continuous_execution = False,
            full_process = full_process
        )

        response = requests.post(f'http://{Setup.monitor_hostname}:{Setup.monitor_port}/api/monitor', json=message.to_json(), headers = {'Content-Type': 'application/json', 'Accept': 'application/json'})
        Logger.write_log(f"Response: {response}")

        SessionWorkloadService.update_session_workload(
            session_workload.id,
            session_workload.session_id,
            session_workload.workload_id,
            f'in_progress_0/{session.num_executions}',
            session_workload.analysis_status,
            session_workload.monitoring_start_time_seconds,
            session_workload.monitoring_end_time_seconds,
            session_workload.analysis_start_time_seconds,
            session_workload.analysis_end_time_seconds,
            session_workload.verdict,
            session_workload.iterations_to_detect,
            session_workload.total_iterations
        )

    @staticmethod
    def process_monitor_result(type: str, data: dict):

        Logger.write_log(f"Received message from topic {type}: {data}")

        if type == 'status':
            message = MonitorStatusMessage(
                session_id = data['session_id'],
                workload_id = data['workload_id'],
                session_workload_id = data['session_workload_id'],
                curr_execution = data['curr_execution'],
                total_executions = data['total_executions'],
                is_last_message = data['is_last_message']
            )
            session_workload: DBSessionWorkload = SessionWorkloadService.get_session_workloads(message.session_workload_id)
            SessionWorkloadService.update_session_workload(
                message.session_workload_id,
                message.session_id,
                message.workload_id,
                f'in_progress_{message.curr_execution}/{message.total_executions}',
                session_workload.analysis_status,
                session_workload.monitoring_start_time_seconds,
                session_workload.monitoring_end_time_seconds,
                session_workload.analysis_start_time_seconds,
                session_workload.analysis_end_time_seconds,
                session_workload.verdict,
                session_workload.iterations_to_detect,
                session_workload.total_iterations
            )
            return
        
        message = MonitorResultMessage(
            session_workload_id = data['session_workload_id'],
            session_id = data['session_id'],
            workload_id = data['workload_id'],
            file_paths = data['file_paths'],
            start_times = data['start_times'],
            end_times = data['end_times'],
            is_last_message = data['is_last_message'],
            monitor_start_time = data['monitor_start_time'],
            monitor_end_time = data['monitor_end_time'],
            full_process = data['full_process']
        )
        session_workload: DBSessionWorkload = SessionWorkloadService.get_session_workloads(message.session_workload_id)

        for i in range(len(message.file_paths)):

            ProfileService.insert_profile(
                message.session_workload_id,
                message.file_paths[i]
            )        
        
        SessionWorkloadService.update_session_workload(
            session_workload.id,
            session_workload.session_id,
            session_workload.workload_id,
            'completed',
            session_workload.analysis_status,
            message.monitor_start_time,
            message.monitor_end_time,
            session_workload.analysis_start_time_seconds,
            session_workload.analysis_end_time_seconds,
            session_workload.verdict,
            session_workload.iterations_to_detect,
            session_workload.total_iterations
        )

        Logger.write_log(f"Saved profiles and updated session_workload")

        if message.is_last_message:
            SessionService.update_session(
                session_workload.session_id,
                session_workload.session.artifact_id,
                session_workload.session.session_type,
                session_workload.session.num_executions,
                session_workload.session.sample_interval,
                session_workload.session.sample_count,
                session_workload.session.reference_session_id,
                'monitoring_completed',
                session_workload.session.continuous_execution,
                session_workload.session.restrictive
            )

            if message.full_process:
                Logger.write_log("Starting analysis as part of full process")
                AnalysisService.start(session_workload.session.id)

        else:
            MonitorService.prepare_monitor(session_workload.session, full_process = message.full_process)

    @staticmethod
    def prepare_monitor(session: DBSession, full_process: bool = False):

        workloads = SessionWorkloadService.get_workloads_for_session(session.id, monitoring_status = "not_started")

        if len(workloads) > 0:
            Logger.write_log(f"Triggering monitor for workload {workloads[0].workload_name}")
            MonitorService.trigger_monitor(session, workloads[0], len(workloads) == 1, full_process = full_process)

    @staticmethod
    def start(session_id: int, full_process: bool = False):
        
        Logger.write_log("Starting monitoring service")
        
        session: DBSession = SessionService.get_sessions(session_id)
        SessionService.update_session(
            session_id,
            session.artifact_id,
            session.session_type,
            session.num_executions,
            session.sample_interval,
            session.sample_count,
            session.reference_session_id,
            'monitoring_in_progress',
            session.continuous_execution,
            session.restrictive
        )

        MonitorService.prepare_monitor(session, full_process = full_process)