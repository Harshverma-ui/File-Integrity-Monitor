from PyQt5.QtCore import QObject, pyqtSignal

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

import os

from core.hash_manager import HashManager
from core.database import DatabaseManager
from core.logger import ActivityLogger


# =====================================================
# SIGNAL MANAGER
# =====================================================

class MonitorSignals(QObject):

    file_modified = pyqtSignal(str)
    file_deleted = pyqtSignal(str)
    file_restored = pyqtSignal(str)
    integrity_alert = pyqtSignal(str, str)
    refresh_required = pyqtSignal()


# =====================================================
# EVENT HANDLER
# =====================================================

class IntegrityEventHandler(
    FileSystemEventHandler
):

    def __init__(
        self,
        signals
    ):

        super().__init__()

        self.signals = signals

        self.db = DatabaseManager()

        self.logger = ActivityLogger()

    # =================================================
    # MODIFIED
    # =================================================

    def on_modified(self, event):
        

        

        if event.is_directory:
            return

        try:

            file_path = os.path.normpath(
                event.src_path
            )

            data = self.db.get_all_files()

            

            if file_path not in data:


                return

            
            current_hash = (
                HashManager.generate_sha256(
                    file_path
                )
            )

            stored_hash = (
                data[file_path]["hash"]
            )

            

            if current_hash != stored_hash:

                self.db.update_status(
                    file_path,
                    "MODIFIED"
                )

                self.logger.log(
                    f"Integrity Violation: "
                    f"{file_path}"
                )

                

                self.signals.integrity_alert.emit(
                    "Integrity Alert",
                    f"File Modified:\n\n{file_path}"
                )

                self.signals.file_modified.emit(
                    file_path
                )

                self.signals.refresh_required.emit()

            else:

                self.db.update_status(
                    file_path,
                    "SAFE"
                )

        except Exception as e:

            print("ERROR:", e)

            self.logger.log(
                f"Monitor Error: {str(e)}"
            )

    # =================================================
    # DELETED
    # =================================================

    def on_deleted(self, event):

        if event.is_directory:
            return

        file_path = os.path.normpath(
            event.src_path
        )

        data = self.db.get_all_files()

        if file_path not in data:
            return

        self.db.update_status(
            file_path,
            "MISSING"
        )

        self.logger.log(
            f"File Deleted: {file_path}"
        )

        self.signals.integrity_alert.emit(
            "File Missing",
            f"Monitored file deleted:\n\n"
            f"{file_path}"
        )

        self.signals.file_deleted.emit(
            file_path
        )

        self.signals.refresh_required.emit()

    # =================================================
    # CREATED
    # =================================================

    def on_created(self, event):

        if event.is_directory:
            return

        file_path = os.path.normpath(
            event.src_path
        )

        data = self.db.get_all_files()

        if file_path not in data:
            return

        try:

            current_hash = (
                HashManager.generate_sha256(
                    file_path
                )
            )

            stored_hash = (
                data[file_path]["hash"]
            )

            if current_hash == stored_hash:

                self.db.update_status(
                    file_path,
                    "SAFE"
                )

                self.logger.log(
                    f"File Restored: "
                    f"{file_path}"
                )

                self.signals.file_restored.emit(
                    file_path
                )

                self.signals.refresh_required.emit()

        except Exception:
            pass

    # =================================================
    # MOVED / RENAMED
    # =================================================

    def on_moved(self, event):

        if event.is_directory:
            return

        old_path = os.path.normpath(event.src_path)

        data = self.db.get_all_files()

        if old_path not in data:
            return

        self.db.update_status(
            old_path,
            "MISSING"
        )

        self.logger.log(
            f"File Renamed/Moved: "
            f"{old_path}"
        )

        self.signals.integrity_alert.emit(
            "File Renamed",
            f"Monitored file moved:\n\n"
            f"{old_path}"
        )

        self.signals.refresh_required.emit()


# =====================================================
# REAL TIME MONITOR
# =====================================================

class RealTimeMonitor(QObject):

    def __init__(self):

        super().__init__()

        self.signals = MonitorSignals()

        self.observers = []

    # =================================================
    # START
    # =================================================

    def start(self, folder):

        if not os.path.exists(folder):
            return

        event_handler = (
            IntegrityEventHandler(
                self.signals
            )
        )

        observer = Observer()

        observer.schedule(
            event_handler,
            folder,
            recursive=True
        )
        print("Observer Started:", folder)
        observer.start()

        self.observers.append(
            observer
        )

    # =================================================
    # STOP
    # =================================================

    def stop(self):

        for observer in self.observers:

            try:

                observer.stop()

                observer.join()

            except Exception:
                pass

        self.observers.clear()

    # =================================================
    # IS RUNNING
    # =================================================

    def is_running(self):

        return len(
            self.observers
        ) > 0