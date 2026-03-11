from core.connection_manager import ConnectionManager
from core.entities.artifact import DBArtifact, ArtifactService
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = ConnectionManager.get_connection()
db_session = ConnectionManager.get_session

class DBSession(db.Model):

  __tablename__ = "session"

  id: Mapped[int] = mapped_column(db.Integer, primary_key = True)
  artifact_id: Mapped[int] = mapped_column(ForeignKey("artifact.id"), nullable = False)
  artifact: Mapped["DBArtifact"] = relationship()
  session_type: Mapped[str] = mapped_column(db.String, nullable = False)
  num_executions: Mapped[int] = mapped_column(db.Integer, nullable = True)
  sample_interval: Mapped[float] = mapped_column(db.Float, nullable = True)
  sample_count: Mapped[int] = mapped_column(db.Integer, nullable = True)
  reference_session_id: Mapped[int] = mapped_column(ForeignKey("session.id"), nullable = True)
  reference_session: Mapped["DBSession"] = relationship(remote_side=id)
  associated_sessions = relationship("DBSession", back_populates="reference_session")
  status: Mapped[str] = mapped_column(db.String, nullable = False)
  continuous_execution: Mapped[bool] = mapped_column(db.Boolean, nullable = False)
  restrictive: Mapped[bool] = mapped_column(db.Boolean, nullable = False, default = False)

class SessionService:
  
  @staticmethod
  def get_sessions(session_id: int = None):
    
    if session_id is None:
      return db_session().query(DBSession).all()
    
    return db_session().query(DBSession).filter_by(id = session_id).one_or_none()

  @staticmethod
  def get_application_sessions(application_id: int):

    return db_session().query(DBSession).\
      select_from(DBArtifact).\
      filter_by(application_id = application_id).\
      join(DBSession, DBSession.artifact_id == DBArtifact.id).all()

  @staticmethod
  def insert_session(artifact_id: int, session_type: str, num_executions: int = None, sample_interval: float = None, sample_count: int = None, reference_session_id: int = None, status: str = "not_started", continuous_execution: bool = False, restrictive: bool = False):
    
    new_session: DBSession = DBSession(
      id = None,
      artifact_id = artifact_id,
      artifact = ArtifactService.get_artifacts(artifact_id),
      session_type = session_type,
      num_executions = num_executions,
      sample_interval = sample_interval,
      sample_count = sample_count,
      reference_session_id = reference_session_id,
      reference_session = None if reference_session_id is None else SessionService.get_sessions(reference_session_id),
      status = status,
      continuous_execution = continuous_execution,
      restrictive = restrictive
    )

    db_session().add(new_session)
    db_session().commit()

    return new_session

  @staticmethod
  def update_session(session_id: int, artifact_id: int, session_type: str, num_executions: int = None, sample_interval: float = None, sample_count: int = None, reference_session_id: int = None, status: str = None, continuous_execution: bool = False, restrictive: bool = False):

    curr_session: DBSession = SessionService.get_sessions(session_id)
    if curr_session is None:
      return None
    
    curr_session.artifact_id = artifact_id
    curr_session.session_type = session_type
    curr_session.num_executions = num_executions
    curr_session.sample_interval = sample_interval
    curr_session.sample_count = sample_count
    curr_session.reference_session_id = reference_session_id
    curr_session.status = status
    curr_session.continuous_execution = continuous_execution
    curr_session.restrictive = restrictive

    db_session().commit()
    return curr_session