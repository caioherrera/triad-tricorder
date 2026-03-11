from core.connection_manager import ConnectionManager
from core.entities.application import DBApplication, ApplicationService
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = ConnectionManager.get_connection()
db_session = ConnectionManager.get_session

class DBWorkload(db.Model):

  __tablename__ = "workload"

  id: Mapped[int] = mapped_column(db.Integer, primary_key = True)
  workload_name: Mapped[str] = mapped_column(db.String, nullable = False)
  workload_desc: Mapped[str] = mapped_column(db.String, nullable = False)
  application_id: Mapped[int] = mapped_column(ForeignKey("application.id"))
  application: Mapped["DBApplication"] = relationship()
  input_value: Mapped[str] = mapped_column(db.String, nullable = True)

class WorkloadService:
  
  @staticmethod
  def get_workloads(workload_id: int = None):
    
    if workload_id is None:
      return db_session().query(DBWorkload).all()
    
    return db_session().query(DBWorkload).filter_by(id = workload_id).one_or_none()
  
  @staticmethod
  def get_application_workloads(application_id: int):

    return db_session().query(DBWorkload).filter_by(application_id = application_id).all()
  
  @staticmethod
  def insert_workload(workload_name: str, workload_desc: str, application_id: int, input_value: str):
    
    new_workload: DBWorkload = DBWorkload(
      id = None,
      workload_name = workload_name,
      application_id = application_id,
      application = ApplicationService.get_applications(application_id),
      workload_desc = workload_desc,
      input_value = input_value
    )

    db_session().add(new_workload)
    db_session().commit()

    return new_workload
  
  @staticmethod
  def update_workload(workload_id: int, workload_name: str, workload_desc: str, application_id: int, input_value: str):

    curr_workload: DBWorkload = WorkloadService.get_workloads(workload_id)
    if curr_workload is None:
      return None
    
    curr_workload.workload_name = workload_name
    curr_workload.workload_desc = workload_desc
    curr_workload.application_id = application_id
    curr_workload.input_value = input_value

    db_session().commit()
    return curr_workload