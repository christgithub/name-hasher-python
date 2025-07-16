import sys
import time
from sftp_client import SFTPClient
from mysql_indexer import MySQLIndexer
from file_hasher import FileHasher
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    
    logging.info("🚀 Process running...")

    
    sftp = SFTPClient(
        host="sftp",
        port=22,
        username="devuser",
        password="devpass"
    )

    try:
        sftp.connect()
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    logging.info("✅ Connected to sftp server")
    files = sftp.download_files(remote_dir="upload")
    logging.info(f"📥 Downloaded {len(files)} file(s)")
    hasher = FileHasher(files)
    
    indexer = MySQLIndexer(
        host=os.getenv("MYSQL_HOST", "localhost"),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", "mypass"),
        database=os.getenv("MYSQL_DATABASE", "sftp_index")
    )

    try:
        indexer = MySQLIndexer(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "mypass"),
            database=os.getenv("MYSQL_DATABASE", "sftp_index")
        )
        logging.info("✅ Connect to MySQL")
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    indexCounter = 0
    for record in hasher.hash_lines():
        indexer.insert_record(record)
        indexCounter+=1

    indexer.close()
    logging.info(f"✅ Indexed {indexCounter} row(s) into MySQL")
    logging.info("🏁 Process ran successfully.")
    time.sleep(120)

if __name__ == "__main__":
    main()