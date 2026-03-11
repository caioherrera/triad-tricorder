import sys
sys.path.append('../')

from flask import Flask, jsonify, request
from flask_cors import CORS
import json
import uuid
import os

from core.connection_manager import ConnectionManager 
from core.setup import Setup
from core.logger import Logger

app = Flask(__name__)

Setup.initialize_from_env()

app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{Setup.database_path}"
CORS(app, resources={r"/api/*": {"origins": "*"}})

with open(Setup.database_init_script, 'r') as file:
  sql_script = file.read()

ConnectionManager.set_connection(app, sql_script)

from core.entities.application import ApplicationService
from core.entities.artifact import ArtifactService
from core.entities.workload import WorkloadService
from core.entities.profile import ProfileService
from core.entities.session import SessionService
from core.entities.session_workload import SessionWorkloadService
from services.monitor_service import MonitorService
from services.analysis_service import AnalysisService

##################### /api/applications

@app.get("/api/applications")
@app.get("/api/applications/<int:application_id>")
def get_applications(application_id: int = None):
  
  applications = ApplicationService.get_applications(application_id)
  return jsonify(applications)

@app.get("/api/applications/<int:application_id>/artifacts")
def get_application_artifacts(application_id: int):

  artifacts = ArtifactService.get_application_artifacts(application_id)
  return jsonify(artifacts)

@app.get("/api/applications/<int:application_id>/reference_artifact")
def get_reference_artifact(application_id: int):

  artifact = ArtifactService.get_reference_artifact(application_id)
  return jsonify(artifact)

@app.get("/api/applications/<int:application_id>/workloads")
def get_application_workloads(application_id: int):

  workloads = WorkloadService.get_application_workloads(application_id)
  return jsonify(workloads)

@app.get("/api/applications/<int:application_id>/sessions")
def get_application_sessions(application_id: int):

  sessions = SessionService.get_application_sessions(application_id)
  return jsonify(sessions)

@app.post("/api/applications/upsert")
def upsert_application():

  data = json.loads(request.data.decode())

  id = data['id']
  application_name = data['application_name']
  command_line = data['command_line']

  if id is None:
    application = ApplicationService.insert_application(application_name, command_line)
  else:
    application = ApplicationService.update_application(id, application_name, command_line)

  return jsonify(application)

##################### /api/artifacts

@app.get("/api/artifacts")
@app.get("/api/artifacts/<int:artifact_id>")
def get_artifacts(artifact_id: int = None):

  artifacts = ArtifactService.get_artifacts(artifact_id)
  return jsonify(artifacts)

@app.post("/api/artifacts/upsert")
def upsert_artifact():

  data = json.loads(request.data.decode())

  id = data['id']
  artifact_name = data['artifact_name']
  application_id = data['application']['id']
  file_path = data['file_path']
  is_reference = 1 if data['is_reference'] else 0

  if id is None:
    artifact = ArtifactService.insert_artifact(artifact_name, application_id, is_reference, file_path) 
  else:
    artifact = ArtifactService.update_artifact(id, artifact_name, application_id, is_reference, file_path)

  return jsonify(artifact)

##################### /api/workloads

@app.get("/api/workloads")
@app.get("/api/workloads/<int:workload_id>")
def get_workloads(workload_id: int = None):

  workloads = WorkloadService.get_workloads(workload_id)
  return jsonify(workloads)

@app.post("/api/workloads/upsert")
def upsert_workload():

  data = json.loads(request.data.decode())

  id = data['id']
  workload_name = data['workload_name']
  application_id = data['application']['id']
  workload_desc = data['workload_desc']
  input_value = data['input_value']

  if id is None:
    workload = WorkloadService.insert_workload(workload_name, workload_desc, application_id, input_value)
  else:
    workload = WorkloadService.update_workload(id, workload_name, workload_desc, application_id, input_value)

  return jsonify(workload)

##################### /api/sessions

@app.get("/api/sessions")
@app.get("/api/sessions/<int:session_id>")
def get_sessions(session_id: int = None):

  sessions = SessionService.get_sessions(session_id)
  return jsonify(sessions)

@app.get("/api/sessions/<int:session_id>/workloads")
def get_session_workloads(session_id: int):
  
  workloads = SessionWorkloadService.get_workloads_for_session(session_id)
  return jsonify(workloads)

@app.get("/api/sessions/<int:session_id>/details")
def get_session_details(session_id: int):

  session_workloads = SessionWorkloadService.get_session_workload(session_id)
  return jsonify(session_workloads)

@app.get  ("/api/sessions/<int:session_id>/profiles")
def get_session_profiles(session_id: int):

  profiles = ProfileService.get_session_profiles(session_id)
  return jsonify(profiles)

@app.post("/api/sessions/upsert")
def upsert_session():

  data = json.loads(request.data.decode())
  workloads: list = []
  existing_workloads: list = []

  if 'workloads' in data:
    workloads = data['workloads']
    data = data['session']

  id = data['id']
  artifact_id = data['artifact']['id']
  session_type = data['session_type']
  num_executions = data['num_executions']
  sample_interval = data['sample_interval']
  sample_count = data['sample_count']
  status = data['status']
  continuous_execution = data['continuous_execution']
  restrictive = data['restrictive']

  reference_session_id = None
  if data['reference_session'] is not None:
    reference_session_id = data['reference_session']['id']

  if id is None:
    session = SessionService.insert_session(artifact_id, session_type, num_executions, sample_interval, sample_count, reference_session_id, continuous_execution=continuous_execution, restrictive=restrictive)
  else:
    session = SessionService.update_session(id, artifact_id, session_type, num_executions, sample_interval, sample_count, reference_session_id, status, continuous_execution, restrictive=restrictive)
    existing_workloads = [ w.id for w in SessionWorkloadService.get_workloads_for_session(id)]
  
  for workload in workloads:
    workload_id: int = workload['id']
    if not workload_id in existing_workloads:
      SessionWorkloadService.insert_session_workload(session.id, workload_id)
  
  # TO-DO Delete workloads that do not show up on the new list

  return jsonify(session)

@app.get("/api/sessions/<int:session_id>/monitor")
def start_monitor(session_id: int):
  
  session = SessionService.get_sessions(session_id)
  MonitorService.start(session_id)
  
  return jsonify(session)

@app.get("/api/sessions/<int:session_id>/analyze")
def start_analyzer(session_id: int):
  
  session = SessionService.get_sessions(session_id)
  AnalysisService.start(session_id)
  
  return jsonify(session)

@app.get("/api/sessions/<int:session_id>/full_process")
def start_full_process(session_id: int):

  session = SessionService.get_sessions(session_id)
  MonitorService.start(session_id, full_process=True)

  return jsonify(session)

@app.post("/api/sessions/<int:session_id>/workload/<int:workload_id>/upload")
def upload_session_files(session_id: int, workload_id: int):

  Logger.write_log(f"Uploading files for session {session_id}, workload {workload_id}", level_details = 0)

  files = request.files.getlist('files')

  Logger.write_log(f"Received {len(files)} files", level_details = 0)

  if not files:
    return jsonify({"error": "Invalid request"}), 400

  session_workload = SessionWorkloadService.get_session_workload(session_id, workload_id)
  session = SessionService.get_sessions(session_id)

  try:

    folder: str = ""
    while True:
      folder = f'/opt/tricorder/profiles/{uuid.uuid4()}'
      if not os.path.exists(folder):
          break

    Logger.write_log(f"Creating folder {folder}", level_details = 0)
    os.makedirs(folder, exist_ok=True)

    for file in files:

      # move file to the correct directory
      path: str = ''

      while True:
        path = f'{folder}/{uuid.uuid4()}.csv'
        if not os.path.exists(path):
            break
        
      file.save(path)
      ProfileService.upload_profile(session_workload.id, path)

    SessionWorkloadService.update_session_workload(session_workload.id, session_workload.session_id, workload_id, 'manual', session_workload.analysis_status, session_workload.monitoring_start_time_seconds, session_workload.monitoring_end_time_seconds, session_workload.analysis_start_time_seconds, session_workload.analysis_end_time_seconds, session_workload.verdict, session_workload.iterations_to_detect, session_workload.total_iterations)
    SessionService.update_session(session.id, session.artifact_id, session.session_type, session.num_executions, session.sample_interval, session.sample_count, session.reference_session_id, 'manual_monitoring', session.continuous_execution, session.restrictive)

    return jsonify(session_workload), 200
    
  except Exception as e:
    return jsonify({"error": str(e)}), 500

##################### /api/monitor

@app.post('/api/monitor/status')
def monitor_status():
  
  data = request.get_json()
  if not data:
    return jsonify({"error": "Invalid JSON"}), 400
  
  MonitorService.process_monitor_result('status', data)

  return jsonify({"status": "Status received"}), 200

@app.post('/api/monitor/result')
def monitor_result():
  
  data = request.get_json()
  if not data:
    return jsonify({"error": "Invalid JSON"}), 400

  MonitorService.process_monitor_result('result', data)

  return jsonify({"status": "Result received"}), 200

##################### /api/analysis

@app.post('/api/analysis/status')
def analysis_status():
  
  data = request.get_json()
  if not data:
    return jsonify({"error": "Invalid JSON"}), 400
  
  AnalysisService.process_analysis_result('status', data)

  return jsonify({"status": "Status received"}), 200

@app.post('/api/analysis/result')
def analysis_result():
  
  data = request.get_json()
  if not data:
    return jsonify({"error": "Invalid JSON"}), 400

  AnalysisService.process_analysis_result('result', data)

  return jsonify({"status": "Status received"}), 200

if __name__ == "__main__":
  app.run(threaded = True)