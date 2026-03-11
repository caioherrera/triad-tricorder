from core.entities.session import DBSession, SessionService
from core.message import AnalysisRequestMessage, AnalysisResultMessage, AnalysisStatusMessage
from core.entities.session_workload import DBSessionWorkload, SessionWorkloadService
from core.entities.workload import DBWorkload
from core.entities.profile import DBProfile, ProfileService
from core.entities.group import GroupService
from core.logger import Logger
from core.setup import Setup

import requests

class AnalysisService:

    @staticmethod
    def process_analysis_result(type: str, data: dict):

        Logger.write_log(f"Received message from topic {type}: {data}")

        if type == 'status':
            message = AnalysisStatusMessage(
                session_workload_id = data['session_workload_id'],
                session_id = data['session_id'],
                workload_id = data['workload_id'],
                curr_execution = data['curr_execution'],
                total_executions = data['total_executions'],
                is_last_message = data['is_last_message']            
            )
            session_workload: DBSessionWorkload = SessionWorkloadService.get_session_workloads(message.session_workload_id)
            SessionWorkloadService.update_session_workload(
                message.session_workload_id,
                message.session_id,
                message.workload_id,
                session_workload.monitoring_status,
                f'in_progress_{message.curr_execution}/{message.total_executions}',
                session_workload.monitoring_start_time_seconds,
                session_workload.monitoring_end_time_seconds,
                session_workload.analysis_start_time_seconds,
                session_workload.analysis_end_time_seconds,
                session_workload.verdict,
                session_workload.iterations_to_detect,
                session_workload.total_iterations
            )
            return
        
        message = AnalysisResultMessage(
            session_workload_id = data['session_workload_id'],
            session_id = data['session_id'],
            workload_id = data['workload_id'],
            groups = data['groups'],
            verdict = data['verdict'],
            is_last_message = data['is_last_message'],
            analysis_start_time = data['analysis_start_time'],
            analysis_end_time = data['analysis_end_time'],
            total_executions = data['total_executions'],
            actual_executions = data['actual_executions']
        )
        session_workload: DBSessionWorkload = SessionWorkloadService.get_session_workloads(message.session_workload_id)

        for group_identifier in message.groups.keys():
            group = GroupService.insert_group(session_workload.id, group_identifier)

            for profile_id in message.groups[group_identifier]:

                profile: DBProfile = ProfileService.get_profiles(profile_id)
                ProfileService.update_profile(profile.id, profile.session_workload_id, profile.file_path, group.id)
        
        SessionWorkloadService.update_session_workload(
            session_workload.id,
            session_workload.session_id,
            session_workload.workload_id,
            session_workload.monitoring_status,
            'completed',
            session_workload.monitoring_start_time_seconds,
            session_workload.monitoring_end_time_seconds,
            message.analysis_start_time,
            message.analysis_end_time,
            message.verdict,
            message.actual_executions,
            message.total_executions
        )

        Logger.write_log(f"Updated session_workload")

        if message.is_last_message:
            SessionService.update_session(
                session_workload.session_id,
                session_workload.session.artifact_id,
                session_workload.session.session_type,
                session_workload.session.num_executions,
                session_workload.session.sample_interval,
                session_workload.session.sample_count,
                session_workload.session.reference_session_id,
                'analysis_completed',
                session_workload.session.continuous_execution,
                session_workload.session.restrictive
            )
        else:
            AnalysisService.prepare_analysis(session_workload.session)

    @staticmethod
    def trigger_analysis(session: DBSession, workload: DBWorkload, is_last_workload: bool = False):

        session_workload: DBSessionWorkload = SessionWorkloadService.get_session_workload(session.id, workload.id)
        profiles: list = ProfileService.get_session_workload_profiles(session_workload.id)
        
        ref_profiles: list = []

        if session.reference_session != None:

            ref_session_workload: DBSessionWorkload = SessionWorkloadService.get_session_workload(session.reference_session.id, workload.id)
            ref_profiles = ProfileService.get_session_workload_profiles(ref_session_workload.id)

        message: AnalysisRequestMessage = AnalysisRequestMessage(
            session_workload_id = session_workload.id,
            session_id = session.id,
            workload_id = workload.id,
            profiles = { p.id: p.file_path for p in profiles },
            ref_profiles = { p.id: p.file_path for p in ref_profiles },
            is_last_message = is_last_workload,
            restrictive = session.restrictive
        )

        response = requests.post(f'http://{Setup.analysis_hostname}:{Setup.analysis_port}/api/analysis', json=message.to_json(), headers = {'Content-Type': 'application/json', 'Accept': 'application/json'})
        Logger.write_log(f"Response: {response}")

        SessionWorkloadService.update_session_workload(
            session_workload.id,
            session_workload.session_id,
            session_workload.workload_id,
            session_workload.monitoring_status,
            f'in_progress_0/{session.num_executions - 1}',
            session_workload.monitoring_start_time_seconds,
            session_workload.monitoring_end_time_seconds,
            session_workload.analysis_start_time_seconds,
            session_workload.analysis_end_time_seconds,
            session_workload.verdict,
            session_workload.iterations_to_detect,
            session_workload.total_iterations
        )

    @staticmethod
    def prepare_analysis(session: DBSession):

        workloads = SessionWorkloadService.get_workloads_for_session(session.id, analysis_status = "not_started")

        if len(workloads) > 0:
            Logger.write_log(f"Triggering analysis for workload {workloads[0].workload_name}")
            AnalysisService.trigger_analysis(session, workloads[0], len(workloads) == 1)

    @staticmethod
    def start(session_id: int):
        
        Logger.write_log("Starting analysis service")
        
        session: DBSession = SessionService.get_sessions(session_id)
        SessionService.update_session(
            session_id,
            session.artifact_id,
            session.session_type,
            session.num_executions,
            session.sample_interval,
            session.sample_count,
            session.reference_session_id,
            'analysis_in_progress',
            session.continuous_execution,
            session.restrictive
        )

        AnalysisService.prepare_analysis(session)