import os

class Setup:

    database_path: str = ""
    database_init_script: str = ""
    
    backend_hostname: str = ""
    backend_port: int = 0
    
    monitor_hostname: str = ""
    monitor_port: int = 0
    
    analysis_hostname: str = ""
    analysis_port: int = 0
    
    damicore_path: str = ""
    damicore_compressor: str = ""
    damicore_model_order: int = 0
    damicore_memory: int = 0
    
    log_file_path: str = ""

    @staticmethod
    def initialize_from_env():

        Setup.database_path = os.getenv("TRICORDER_DATABASE_PATH", "/opt/tricorder/data/tricorder.db")
        Setup.database_init_script = os.getenv("TRICORDER_DATABASE_INIT_SCRIPT", "/opt/tricorder/data/init_script.sql")
        
        Setup.backend_hostname = os.getenv("TRICORDER_BACKEND_HOSTNAME", "localhost")
        Setup.backend_port = int(os.getenv("TRICORDER_BACKEND_PORT", 5000))
        
        Setup.monitor_hostname = os.getenv("TRICORDER_MONITOR_HOSTNAME", "localhost")
        Setup.monitor_port = int(os.getenv("TRICORDER_MONITOR_PORT", 5100))
        
        Setup.analysis_hostname = os.getenv("TRICORDER_ANALYSIS_HOSTNAME", "localhost")
        Setup.analysis_port = int(os.getenv("TRICORDER_ANALYSIS_PORT", 5200))

        Setup.damicore_path = os.getenv("TRICORDER_DAMICORE_PATH", "/tmp/damicore-python3/damicore/damicore.py")
        Setup.damicore_compressor = os.getenv("TRICORDER_DAMICORE_COMPRESSOR", "ppmd")
        Setup.damicore_model_order = int(os.getenv("TRICORDER_DAMICORE_MODEL_ORDER", 12))
        Setup.damicore_memory = int(os.getenv("TRICORDER_DAMICORE_MEMORY", 100))

        Setup.log_file_path = os.getenv("TRICORDER_LOG_FILE_PATH", "./details.log")