import json
import datetime

class Logger:
    def __init__(self, log_file):
        self.log_file = log_file
        self.session_log = []
    
    def log_command(self, command):
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'command': command
        }
        self.session_log.append(log_entry)
        self._save_log()
    
    def _save_log(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.session_log, f, indent=2)