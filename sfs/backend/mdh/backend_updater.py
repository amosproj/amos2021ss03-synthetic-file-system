import threading
import time
import os
from ...paths import CONFIG_PATH


class MDHBackendUpdater:
    """
    Class responsible for updating the MDH depending on the state of the cache.
    This class manages a cache file, where any changes are written to. On startup the backend checks
    this file for content, and sends a rescan to the MDH if needed.
    Otherwise, it also checks periodically for changes to the cache and sets an update request to the MDH
    TODO: what if the MDH gets closed before the first update request is handled?
    """

    def __init__(self, mdh_backend):
        self.mdh_backend = mdh_backend
        update_thread = threading.Thread(target=self.update_loop)
        self.cache_path = CONFIG_PATH / "mdh_cache.txt"
        self.check_cache()
        update_thread.start()

    def update_cache(self, cache: set[str]) -> None:
        """
        Updates the cache file using the given entries
        :param cache: the entries in the cache
        :return: None
        """
        with open(self.cache_path, "w") as cache_file:
            for line in cache:
                cache_file.write(line + "\n")
            cache_file.flush()

    def check_cache(self) -> None:
        """
        Checks whether the cache file contains any data or not. If it does this data is read into the
        cache of the backend
        :return: None
        """
        if not os.path.exists(self.cache_path):
            return
        with open(self.cache_path, "r") as cache_file:
            cache = set()
            for line in cache_file:
                cache.add(line.rstrip())
            self.mdh_backend.file_path_cache = cache.copy()
            cache_file.flush()

    def update_loop(self) -> None:
        """
        Periodically checks for updates to the cache of the MDH backend If there are entries
        send an rescan request to the MDH
        :return: None
        """
        while True:
            if len(self.mdh_backend.file_path_cache) != 0:
                self.mdh_backend.rescan()
            time.sleep(180)  # poll every 1 minutes
