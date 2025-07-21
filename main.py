import sys
from file_downloader import FileDownloader
from mysql_indexer import MySQLIndexer
from file_hasher import FileHasher
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

def main():
    
    logging.info("🚀 Starting process")

    downloader = FileDownloader(
        host="sftp",
        port=22,
        username="devuser",
        password="devpass"
    )

    try:
        downloader.connect()
    except RuntimeError as e:
        print(e)
        sys.exit(1)

    logging.info("✅ Connected to sftp server")
    files = downloader.download_files(remote_dir="upload")
    logging.info(f"📥 Downloaded {len(files)} file(s)")

    try:
        hasher = FileHasher(files)
        hashedRows = hasher.hash_lines()
        logging.info(f"🔑 Hashed {len(hashedRows)} lines")
    except Exception as e:
        logging.error(f"❌ Error during hashing: {e}")
        return

    try:
        indexCounter = 0
        indexer = MySQLIndexer(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", "mypass"),
            database=os.getenv("MYSQL_DATABASE", "sftp_index")
        )
        logging.info("✅ Connect to MySQL")
        
        for row in hashedRows:
            indexer.insert_record(row["fileName"], row["hashValue"])
            indexCounter+=1
        logging.info("✅ All records inserted into MySQL")
        indexer.close()
    except Exception as e:
        logging.error(f"❌ Error inserting into MySQL: {e}")
    
    logging.info(f"✅ Indexed {indexCounter} row(s) into MySQL")
    logging.info("🏁 Process ran successfully.")

if __name__ == "__main__":
    main()