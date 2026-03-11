from core.connection_manager import ConnectionManager
from core.entities.session_workload import DBSessionWorkload, SessionWorkloadService
from core.entities.group import DBGroup, GroupService
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = ConnectionManager.get_connection()
db_session = ConnectionManager.get_session

class DBProfile(db.Model):

  __tablename__ = "profile"

  id: Mapped[int] = mapped_column(db.Integer, primary_key = True)
  session_workload_id: Mapped[int] = mapped_column(ForeignKey("session_workload.id"), nullable = False)
  session_workload: Mapped["DBSessionWorkload"] = relationship()
  group_id: Mapped[int] = mapped_column(ForeignKey("session_group.id"), nullable = True)
  group: Mapped["DBGroup"] = relationship()
  file_path: Mapped[str] = mapped_column(db.String, nullable = False)

class ProfileService:
  
  @staticmethod
  def get_profiles(profile_id: int = None):

    if profile_id is None:
      return db_session().query(DBProfile).all()
  
    return db_session().query(DBProfile).filter_by(id = profile_id).one_or_none()
  
  @staticmethod
  def get_session_workload_profiles(session_workload_id: int):

    return db_session().query(DBProfile).filter_by(session_workload_id = session_workload_id).all()

  @staticmethod
  def get_session_profiles(session_id: int):

    return db_session().query(DBProfile)\
      .join(DBSessionWorkload, DBProfile.session_workload_id == DBSessionWorkload.id)\
      .filter(DBSessionWorkload.session_id == session_id).all()
  
  @staticmethod
  def get_group_profiles(group_id: int):

    return db_session().query(DBProfile).filter_by(group_id = group_id).all()
  
  @staticmethod
  def insert_profile(session_workload_id: int, file_path: str, group_id: int = None):
    
    new_profile: DBProfile = DBProfile(
      id = None,
      session_workload_id = session_workload_id,
      session_workload = SessionWorkloadService.get_session_workloads(session_workload_id),
      group_id = group_id,
      group = None if group_id is None else GroupService.get_groups(group_id),
      file_path = file_path
    )

    db_session().add(new_profile)
    db_session().commit()

    return new_profile
  
  @staticmethod
  def upload_profile(session_workload_id: int, file_path: str, group_id: int = None):
    
    new_profile: DBProfile = DBProfile(
      id = None,
      session_workload_id = session_workload_id,
      session_workload = SessionWorkloadService.get_session_workloads(session_workload_id),
      group_id = group_id,
      group = None if group_id is None else GroupService.get_groups(group_id),
      file_path = file_path
    )

    db_session().add(new_profile)
    db_session().commit()

    return new_profile

  @staticmethod
  def update_profile(profile_id: int, session_workload_id: int, file_path: str, group_id: int = None):

    curr_profile: DBProfile = ProfileService.get_profiles(profile_id)
    if curr_profile is None:
      return None
    
    curr_profile.session_workload_id = session_workload_id
    curr_profile.file_path = file_path
    curr_profile.group_id = group_id

    db_session().commit()
    return curr_profile