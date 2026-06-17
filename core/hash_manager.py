import hashlib


class HashManager:

    @staticmethod
    def generate_sha256(file_path):
        sha256 = hashlib.sha256()

        try:
            with open(file_path, "rb") as file:
                while chunk := file.read(4096):
                    sha256.update(chunk)

            return sha256.hexdigest()

        except Exception as e:
            print(f"Hash Error: {e}")
            return None