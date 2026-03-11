from core.connection_manager import ConnectionManager
from core.entities.session_workload import DBSessionWorkload, SessionWorkloadService
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = ConnectionManager.get_connection()
db_session = ConnectionManager.get_session

class DBGroup(db.Model):

  __tablename__ = "session_group"

  id: Mapped[int] = mapped_column(db.Integer, primary_key = True)
  session_workload_id: Mapped[int] = mapped_column(ForeignKey("session_workload.id"), nullable = False)
  session_workload: Mapped["DBSessionWorkload"] = relationship()
  identifier: Mapped[int] = mapped_column(db.Integer, nullable = False)

class GroupService:
  
  @staticmethod
  def get_groups(group_id: int = None):

    if group_id is None:
      return db_session().query(DBGroup).all()
  
    return db_session().query(DBGroup).filter_by(id = group_id).one_or_none()
  
  @staticmethod
  def get_session_groups(session_id: int):

    return db_session().query(DBGroup).filter_by(session_id = session_id).all()

  @staticmethod
  def insert_group(session_workload_id: int, identifier: int):
    
    new_group: DBGroup = DBGroup(
      id = None,
      session_workload_id = session_workload_id,
      session_workload = SessionWorkloadService.get_session_workloads(session_workload_id),
      identifier = identifier
    )

    db_session().add(new_group)
    db_session().commit()

    return new_group
  
  @staticmethod
  def update_group(group_id: int, session_workload_id: int, identifier: int):

    curr_group: DBGroup = GroupService.get_groups(group_id)
    if curr_group is None:
      return None
    
    curr_group.session_workload_id = session_workload_id
    curr_group.identifier = identifier

    db_session().commit()
    return curr_group