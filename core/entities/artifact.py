from core.connection_manager import ConnectionManager
from core.entities.application import DBApplication, ApplicationService
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = ConnectionManager.get_connection()
db_session = ConnectionManager.get_session

class DBArtifact(db.Model):

  __tablename__ = "artifact"

  id: Mapped[int] = mapped_column(db.Integer, primary_key = True)
  artifact_name: Mapped[str] = mapped_column(db.String, nullable = False)
  application_id: Mapped[int] = mapped_column(ForeignKey("application.id"))
  application: Mapped["DBApplication"] = relationship()
  is_reference: Mapped[int] = mapped_column(db.Integer, nullable = False)
  file_path: Mapped[str] = mapped_column(db.String, nullable = False)

class ArtifactService:
  
  @staticmethod
  def get_artifacts(artifact_id: int = None):

    if artifact_id is None:
      return db_session().query(DBArtifact).all()
    
    return db_session().query(DBArtifact).filter_by(id = artifact_id).one_or_none()
  
  @staticmethod
  def get_application_artifacts(application_id: int):

    return db_session().query(DBArtifact).filter_by(application_id = application_id).all()
  
  @staticmethod
  def get_reference_artifact(application_id: int):

    return db_session().query(DBArtifact).filter_by(application_id = application_id, is_reference = 1).one_or_none()
  
  @staticmethod
  def insert_artifact(artifact_name: str, application_id: int, is_reference: int, file_path: str):
    
    new_artifact: DBArtifact = DBArtifact(
      id = None,
      artifact_name = artifact_name,
      application_id = application_id,
      application = ApplicationService.get_applications(application_id),
      is_reference = is_reference,
      file_path = file_path
    )

    if is_reference == 1:

      old_reference = ArtifactService.get_reference_artifact(application_id)
      if old_reference is not None:
        old_reference.is_reference = 0

    db_session().add(new_artifact)
    db_session().commit()

    return new_artifact
  
  @staticmethod
  def update_artifact(artifact_id: int, artifact_name: str, application_id: int, is_reference: int, file_path: str):

    curr_artifact: DBArtifact = ArtifactService.get_artifacts(artifact_id)
    if curr_artifact is None:
      return None
    
    curr_artifact.artifact_name = artifact_name
    curr_artifact.application_id = application_id
    curr_artifact.file_path = file_path

    if is_reference == 1:

      old_reference = ArtifactService.get_reference_artifact(application_id)
      if old_reference is not None and old_reference.id != curr_artifact.id:
        old_reference.is_reference = 0

    curr_artifact.is_reference = is_reference

    db_session().commit()
    return curr_artifact