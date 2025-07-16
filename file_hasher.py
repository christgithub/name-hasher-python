import hashlib

class FileHasher:
    def __init__(self, files):
        self.files = files

    def hash_lines(self):
        for file_path in self.files:
            with open(file_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        hash_value = hashlib.sha256(line.encode("utf-8")).hexdigest()
                        yield {
                            "filename": file_path,
                            "hash": hash_value
                        }

