CREATE TABLE IF NOT EXISTS application (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  application_name TEXT NOT NULL,
  command_line TEXT
);

CREATE TABLE IF NOT EXISTS artifact (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  artifact_name TEXT NOT NULL,
  application_id INTEGER NOT NULL,
  is_reference INTEGER NOT NULL,
  file_path TEXT,
  FOREIGN KEY (application_id) REFERENCES application (id)
);

CREATE TABLE IF NOT EXISTS workload (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  application_id INTEGER NOT NULL,
  workload_name TEXT NOT NULL,
  workload_desc TEXT NOT NULL,
  input_value TEXT,
  FOREIGN KEY (application_id) REFERENCES application (id)
);

CREATE TABLE IF NOT EXISTS session (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  artifact_id INTEGER NOT NULL,
  session_type TEXT NOT NULL,
  num_executions INTEGER,
  sample_interval FLOAT,
  sample_count INTEGER,
  reference_session_id INTEGER,
  status TEXT NOT NULL,
  continuous_execution INTEGER NOT NULL,
  restrictive INTEGER NOT NULL DEFAULT 0,
  FOREIGN KEY (artifact_id) REFERENCES artifact (id),
  FOREIGN KEY (reference_session_id) REFERENCES session (id)
);

CREATE TABLE IF NOT EXISTS session_workload (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_id INTEGER NOT NULL,
  workload_id INTEGER NOT NULL,
  monitoring_status TEXT NOT NULL,
  analysis_status TEXT NOT NULL,
  monitoring_start_time_seconds REAL,
  monitoring_end_time_seconds REAL,
  analysis_start_time_seconds REAL,
  analysis_end_time_seconds REAL,
  verdict TEXT,
  iterations_to_detect INTEGER,
  total_iterations INTEGER,
  FOREIGN KEY (session_id) REFERENCES session (id),
  FOREIGN KEY (workload_id) REFERENCES workload (id)
);

CREATE TABLE IF NOT EXISTS session_group (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_workload_id INTEGER NOT NULL,
  identifier INTEGER NOT NULL,
  FOREIGN KEY (session_workload_id) REFERENCES session_workload (id)
);

CREATE TABLE IF NOT EXISTS profile (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  session_workload_id INTEGER NOT NULL,
  group_id INTEGER,
  file_path TEXT,
  FOREIGN KEY (session_workload_id) REFERENCES session_workload (id),
  FOREIGN KEY (group_id) REFERENCES session_group (id)
);