import time
import json
import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

watch_directory = "/home/ubuntu/bsm/test"
log_directory = "/home/ubuntu/bsm/logs/changes.json"

class LogHandler(FileSystemEventHandler):
    def on_modified(self, event):
        self.log_event(event)
        
    def on_created(self, event):
        self.log_event(event)
        
    def on_deleted(self, event):
        self.log_event(event)
    
    def log_event(self, event):
        log_entry = {
            "event_type": event.event_type, 
            "src_path": event.src_path,
            "is_directory": event.is_directory,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(log_directory, "a") as log_file:
            json.dump(log_entry, log_file)
            log_file.write("\n")

if __name__ == "__main__":
    event_handler = LogHandler()
    observer = Observer()
    observer.schedule(event_handler, watch_directory, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop() 
        observer.join()  
