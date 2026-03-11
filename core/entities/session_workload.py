from core.connection_manager import ConnectionManager
from core.entities.session import DBSession, SessionService
from core.entities.workload import DBWorkload, WorkloadService
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = ConnectionManager.get_connection()
db_session = ConnectionManager.get_session

class DBSessionWorkload(db.Model):

  __tablename__ = "session_workload"

  id: Mapped[int] = mapped_column(db.Integer, primary_key = True)
  session_id: Mapped[int] = mapped_column(ForeignKey("session.id"), nullable = False)
  session: Mapped["DBSession"] = relationship()
  workload_id: Mapped[int] = mapped_column(ForeignKey("workload.id"), nullable = False)
  workload: Mapped["DBWorkload"] = relationship()
  monitoring_status: Mapped[str] = mapped_column(db.String, nullable = False)
  analysis_status: Mapped[str] = mapped_column(db.String, nullable = False)
  monitoring_start_time_seconds: Mapped[float] = mapped_column(db.Float)
  monitoring_end_time_seconds: Mapped[float] = mapped_column(db.Float)
  analysis_start_time_seconds: Mapped[float] = mapped_column(db.Float)
  analysis_end_time_seconds: Mapped[float] = mapped_column(db.Float)
  verdict: Mapped[int] = mapped_column(db.Integer)
  iterations_to_detect: Mapped[int] = mapped_column(db.Integer)
  total_iterations: Mapped[int] = mapped_column(db.Integer)

class SessionWorkloadService:
  
  @staticmethod
  def get_session_workloads(session_workload_id: int = None):

    if session_workload_id is None:
      return db_session().query(DBSessionWorkload).all()
    
    return db_session().query(DBSessionWorkload).filter_by(id = session_workload_id).one_or_none()
  
  @staticmethod
  def get_session_workload(session_id: int = None, workload_id: int = None):

    if session_id is None and workload_id is None:
      return SessionWorkloadService.get_session_workload()

    if session_id is None:
      return db_session().query(DBSessionWorkload).filter_by(workload_id = workload_id).all()
    
    if workload_id is None:
      return db_session().query(DBSessionWorkload).filter_by(session_id = session_id).all()

    return db_session().query(DBSessionWorkload).filter_by(session_id = session_id, workload_id = workload_id).one_or_none()

  @staticmethod
  def get_workloads_for_session(session_id: int, monitoring_status: str = None, analysis_status: str = None):

    results_query = db_session().query(DBWorkload).\
      select_from(DBSessionWorkload).\
      filter_by(session_id = session_id)
    
    if monitoring_status is not None:
      results_query = results_query.filter_by(monitoring_status = monitoring_status)

    if analysis_status is not None:
      results_query = results_query.filter_by(analysis_status = analysis_status)

    return results_query.join(DBWorkload, DBWorkload.id == DBSessionWorkload.workload_id).all()

  @staticmethod
  def insert_session_workload(session_id: int, workload_id: int, monitoring_status: str = 'not_started', analysis_status: str = 'not_started',
    monitoring_start_time_seconds: float = None, monitoring_end_time_seconds: float = None, analysis_start_time_seconds: float = None, analysis_end_time_seconds: float = None,
    verdict: int = None, iterations_to_detect: int = None, total_iterations: int = None):

    new_session_workload: DBSessionWorkload = DBSessionWorkload(
      id = None,
      session_id = session_id,
      session = SessionService.get_sessions(session_id),
      workload_id = workload_id,
      workload = WorkloadService.get_workloads(workload_id),
      monitoring_status = monitoring_status,
      analysis_status = analysis_status,
      monitoring_start_time_seconds = monitoring_start_time_seconds,
      monitoring_end_time_seconds = monitoring_end_time_seconds,
      analysis_start_time_seconds = analysis_start_time_seconds,
      analysis_end_time_seconds = analysis_end_time_seconds,
      verdict = verdict,
      iterations_to_detect = iterations_to_detect,
      total_iterations = total_iterations
    )

    print(new_session_workload)

    db_session().add(new_session_workload)
    db_session().commit()

  @staticmethod
  def update_session_workload(session_workload_id: int, session_id: int, workload_id: int, monitoring_status: str, analysis_status: str,
    monitoring_start_time_seconds: float, monitoring_end_time_seconds: float, analysis_start_time_seconds: float, analysis_end_time_seconds: float,
    verdict: int, iterations_to_detect: int, total_iterations: int):

    curr_session_workload: DBSessionWorkload = SessionWorkloadService.get_session_workloads(session_workload_id)
    if curr_session_workload is None:
      return None
    
    curr_session_workload.session_id = session_id
    curr_session_workload.workload_id = workload_id
    curr_session_workload.monitoring_status = monitoring_status
    curr_session_workload.analysis_status = analysis_status
    curr_session_workload.monitoring_start_time_seconds = monitoring_start_time_seconds
    curr_session_workload.monitoring_end_time_seconds = monitoring_end_time_seconds
    curr_session_workload.analysis_start_time_seconds = analysis_start_time_seconds
    curr_session_workload.analysis_end_time_seconds = analysis_end_time_seconds
    curr_session_workload.verdict = verdict
    curr_session_workload.iterations_to_detect = iterations_to_detect
    curr_session_workload.total_iterations = total_iterations

    db_session().commit()
    return curr_session_workload