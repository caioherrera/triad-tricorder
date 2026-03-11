import json
from dataclasses import dataclass, asdict

@dataclass
class Message:
    session_workload_id: int
    session_id: int
    workload_id: int
    is_last_message: bool

    def to_json(self):
        return json.dumps(asdict(self))

@dataclass
class MonitorRequestMessage(Message):
    num_executions: int
    sample_interval: float
    sample_count: int
    app_command_line: str
    artifact_file_path: str
    workload_input_value: str
    reading_types: list
    continuous_execution: bool
    full_process: bool

@dataclass
class MonitorResultMessage(Message):
    monitor_start_time: float
    monitor_end_time: float
    file_paths: list
    start_times: list
    end_times: list
    full_process: bool

@dataclass
class MonitorStatusMessage(Message):
    curr_execution: int
    total_executions: int

@dataclass
class AnalysisRequestMessage(Message):
    profiles: dict
    ref_profiles: dict
    restrictive: bool

@dataclass
class AnalysisResultMessage(Message):
    analysis_start_time: float
    analysis_end_time: float
    groups: dict
    total_executions: int
    actual_executions: int
    verdict: bool

@dataclass
class AnalysisStatusMessage(Message):
    curr_execution: int
    total_executions: int