import os
import time

class FileWatcher():
    def __init__(self, filepath):
        self._cached_stamp = 0
        self.filename = filepath
        self.remove_file_if_exists()

    def remove_file_if_exists(self):
        try:
            os.remove(self.filename)
        except OSError:
            pass

    def check_file_changed(self, did_change_callback):
        try:
            stamp = os.stat(self.filename).st_mtime
            if stamp == self._cached_stamp: return
            self._cached_stamp = stamp
            did_change_callback()
        except FileNotFoundError:
            pass


