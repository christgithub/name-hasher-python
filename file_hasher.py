import hashlib

class FileHasher:
    def __init__(self, files):
        self.files = files

    # Open each file in array files for reading
    # Trim each row, hash and encode
    def hash_lines(self):
        results = []

        for file_path in self.files:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            hash_value = hashlib.sha256(line.encode("utf-8")).hexdigest()
                            results.append({
                                "fileName": file_path,
                                "hashValue": hash_value
                            })
            except Exception as e:
                raise RuntimeError(f"❌ Failed to open or read file '{file_path}': {e}")

        return results

