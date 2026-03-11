from core.connection_manager import ConnectionManager
from sqlalchemy.orm import Mapped, mapped_column

db = ConnectionManager.get_connection()
db_session = ConnectionManager.get_session

class DBApplication(db.Model):

  __tablename__ = "application"

  id: Mapped[int] = mapped_column(db.Integer, primary_key = True)
  application_name: Mapped[str] = mapped_column(db.String, nullable = False)
  command_line: Mapped[str] = mapped_column(db.String, nullable = True)

class ApplicationService:
  
  @staticmethod
  def get_applications(application_id: int = None):

    if application_id is None:
      return db_session().query(DBApplication).all()
    
    return db_session().query(DBApplication).filter_by(id = application_id).one_or_none()
  
  @staticmethod
  def insert_application(application_name: str, command_line: str):
    
    new_application: DBApplication = DBApplication(
      id = None,
      application_name = application_name,
      command_line = command_line
    )

    db_session().add(new_application)
    db_session().commit()

    return new_application
  
  @staticmethod
  def update_application(application_id: int, application_name: str, command_line: str):

    curr_application: DBApplication = ApplicationService.get_applications(application_id)
    if curr_application is None:
      return None

    curr_application.application_name = application_name
    curr_application.command_line = command_line

    db_session().commit()
    return curr_application