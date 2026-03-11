import logging
import os
import sys
from core.setup import Setup

class Logger:

    Setup.initialize_from_env()

    log_file_path = Setup.log_file_path
    if os.path.exists(log_file_path):
        os.remove(log_file_path)    

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s | %(levelname)-4s | %(message)s')

    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    # 0: no logs, 1: minimum amount of logs, 2: all logs
    log_details: int = 2

    replicate_to_stdout: bool = True

    @staticmethod
    def set_log_details(details: int = 2):
        Logger.log_details = max(0, min(2, details))

    @staticmethod
    def set_replicate_to_stdout(replicate: bool = True):

        if replicate and not Logger.replicate_to_stdout:
            Logger.logger.addHandler(Logger.stream_handler)
        
        elif not replicate and Logger.replicate_to_stdout:
            Logger.logger.removeHandler(Logger.stream_handler)

        Logger.replicate_to_stdout = replicate

    @staticmethod
    def write_log(message: str, level_details: int = 2):
        
        if level_details <= Logger.log_details:

            logging.info(message)
