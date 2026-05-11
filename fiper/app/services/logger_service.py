import json
import os
from datetime import datetime
from flask import request

class LoggerService:
    def __init__(self, log_file='activity_logs.json'):
        self.log_file = log_file

    def log_action(self, action, db_alias):
        """Mencatat aktivitas user ke file JSON"""
        new_entry = {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "ip": request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0],
            "action": action,
            "db": db_alias,
            "status": "SUCCESS"
        }

        try:
            logs = []
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    try:
                        logs = json.load(f)
                    except json.JSONDecodeError:
                        logs = []
                        
            logs.insert(0, new_entry)

            # PERBAIKAN: Ambil 50 teratas, BUKAN buang 50 teratas!
            logs = logs[:50]

            with open(self.log_file, 'w') as f:
                json.dump(logs, f, indent=4)
                
        except Exception as e:
            print(f"Failed to write log: {e}")

logger_service = LoggerService()