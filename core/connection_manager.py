import threading
from sqlalchemy.orm import DeclarativeBase, MappedAsDataclass, scoped_session, sessionmaker
from sqlalchemy.sql import text
from flask_sqlalchemy import SQLAlchemy
      
class ConnectionManager():

   connection = None
   db_session = None
   session_per_thread = dict()
   app = None

   @staticmethod
   def create_connection():

      class Base(DeclarativeBase, MappedAsDataclass):
         pass

      if ConnectionManager.connection is None:
         ConnectionManager.connection = SQLAlchemy(ConnectionManager.app, model_class = Base, engine_options={'pool_pre_ping': True})

         with ConnectionManager.app.app_context():
            ConnectionManager.db_session = scoped_session(sessionmaker(
               autocommit = False, 
               autoflush = False, 
               bind = ConnectionManager.connection.engine,
               query_cls = ConnectionManager.connection.Query
            ))
         
         return True
      
      return False

   @staticmethod
   def set_connection(app, init_script: str):
      
      ConnectionManager.app = app
      ConnectionManager.create_connection()

      with ConnectionManager.db_session() as session:
         for partial_script in init_script.split(';'):
            session.execute(text(partial_script.strip()))
         session.commit()

   @staticmethod
   def get_connection():
      return ConnectionManager.connection
   
   @staticmethod
   def get_session():

      thread_id: int = threading.get_ident()
      
      if not thread_id in ConnectionManager.session_per_thread: 
         ConnectionManager.session_per_thread[thread_id] = ConnectionManager.db_session()
      
      return ConnectionManager.session_per_thread[thread_id]