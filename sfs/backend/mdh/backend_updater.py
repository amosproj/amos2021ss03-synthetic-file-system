import threading
import time
import logging


class MDHBackendUpdater:

    def __init__(self, mdh_backend):
        self.mdh_backend = mdh_backend
        update_thread = threading.Thread(target=self.update_loop)
        update_thread.start()

    def update_loop(self):
        while True:
            if len(self.mdh_backend.file_path_cache) != 0:
                self.mdh_backend.rescan()
            time.sleep(60)  # poll every 1 minutes
