import subprocess
import logging
import sys

class ExecutionUtils:

    @staticmethod
    def resilient_execute(cmd, retry_attempts = 5, tolerated_exceptions = [], timeout_in_seconds = 60):
        
        cmd_args = cmd.split(' ')
        curr_attempt = retry_attempts

        while curr_attempt > 0:
            
            try:
                subprocess.run(cmd_args, check=True, capture_output=True, timeout=timeout_in_seconds)
                
                break
            except subprocess.CalledProcessError as e:

                std_err = e.stderr.decode(sys.getfilesystemencoding()) if e.stderr else ''

                if any(ex in std_err for ex in tolerated_exceptions):
                    
                    logging.warning(f"Found tolerable exception: {std_err}")
                    curr_attempt -= 1
                    
                    if curr_attempt > 0:
                        logging.warning("Retrying latest cmd")
                    else:
                        logging.error("Retry policy for latest cmd ended")
                        break
                else:
                    logging.error(f"Found exception: {std_err}")
                    break

            except subprocess.TimeoutExpired:
                logging.error(f"Timeout when running latest cmd")
                break