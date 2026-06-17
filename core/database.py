import json
import os
from datetime import datetime


class DatabaseManager:

    def __init__(self, db_file="data/baseline.json"):

        self.db_file = db_file

        os.makedirs(
            os.path.dirname(self.db_file),
            exist_ok=True
        )

        if not os.path.exists(self.db_file):

            with open(
                self.db_file,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    {},
                    file,
                    indent=4
                )

    # ==========================================
    # LOAD DATABASE
    # ==========================================

    def load(self):

        try:

            with open(
                self.db_file,
                "r",
                encoding="utf-8"
            ) as file:

                return json.load(file)

        except Exception:

            return {}

    # ==========================================
    # SAVE DATABASE
    # ==========================================

    def save(self, data):

        with open(
            self.db_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4
            )

    # ==========================================
    # ADD FILE
    # ==========================================

    def add_file(self, path, sha256):
        path = os.path.normpath(path)

        data = self.load()

        now = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        data[path] = {
            "hash": sha256,
            "date_added": now,
            "last_verified": now,
            "status": "SAFE"
        }

        self.save(data)

    # ==========================================
    # REMOVE FILE
    # ==========================================

    def remove_file(self, path):

        data = self.load()

        if path in data:

            del data[path]

            self.save(data)

            return True

        return False

    # ==========================================
    # UPDATE HASH
    # ==========================================

    def update_hash(self, path, new_hash):

        data = self.load()

        if path not in data:
            return False

        data[path]["hash"] = new_hash

        data[path]["last_verified"] = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        data[path]["status"] = "SAFE"

        self.save(data)

        return True

    # ==========================================
    # UPDATE STATUS
    # ==========================================

    def update_status(self, path, status):

        data = self.load()

        if path not in data:
            return False

        data[path]["status"] = status

        data[path]["last_verified"] = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        self.save(data)

        return True

    # ==========================================
    # UPDATE VERIFICATION TIME
    # ==========================================

    def update_verification_time(
        self,
        path
    ):

        data = self.load()

        if path not in data:
            return False

        data[path]["last_verified"] = (
            datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
        )

        self.save(data)

        return True

    # ==========================================
    # GET HASH
    # ==========================================

    def get_hash(self, path):

        data = self.load()

        if path in data:

            return data[path].get("hash")

        return None

    # ==========================================
    # GET FILE INFO
    # ==========================================

    def get_file_info(self, path):

        data = self.load()

        return data.get(path)

    # ==========================================
    # GET ALL FILES
    # ==========================================

    def get_all_files(self):

        return self.load()

    # ==========================================
    # FILE EXISTS
    # ==========================================

    def file_exists(self, path):

        data = self.load()

        return path in data

    # ==========================================
    # TOTAL FILES
    # ==========================================

    def total_files(self):

        return len(self.load())

    # ==========================================
    # SAFE FILES COUNT
    # ==========================================

    def count_safe(self):

        data = self.load()

        return sum(
            1
            for item in data.values()
            if item.get("status") == "SAFE"
        )

    # ==========================================
    # MODIFIED FILES COUNT
    # ==========================================

    def count_modified(self):

        data = self.load()

        return sum(
            1
            for item in data.values()
            if item.get("status") == "MODIFIED"
        )

    # ==========================================
    # MISSING FILES COUNT
    # ==========================================

    def count_missing(self):

        data = self.load()

        return sum(
            1
            for item in data.values()
            if item.get("status") == "MISSING"
        )

    # ==========================================
    # CLEAR DATABASE
    # ==========================================

    def clear_database(self):

        self.save({})

    # ==========================================
    # EXPORT DATABASE
    # ==========================================

    def export_database(
        self,
        export_path
    ):

        try:

            with open(
                export_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    self.load(),
                    file,
                    indent=4
                )

            return True

        except Exception:

            return False