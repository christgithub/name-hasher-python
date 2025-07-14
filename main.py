import time
from sftp_client import SFTPClient
from mysql_indexer import MySQLIndexer
from file_hasher import FileHasher
import os

def main():
    sftp = SFTPClient(
        host="sftp",
        port=22,
        username="devuser",
        password="devpass"
    )

    files = sftp.download_files(remote_dir="upload")

    hasher = FileHasher(files)
    indexer = MySQLIndexer(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_ROOT_PASSWORD", "mypass"),
        database=os.getenv("MYSQL_DATABASE", "sftp_index")
    )

    for record in hasher.hash_lines():
        indexer.insert_record(record)

    indexer.close()
    print("✅ All files hashed and indexed into MySQL.")
    

if __name__ == "__main__":
    main()