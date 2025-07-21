import time
import mysql.connector
from mysql.connector import Error

class MySQLIndexer:
    def __init__(self, host="localhost", user="root", password="", database="sftp_index", retries=10, delay=3):
        self.conn = None
        self.cursor = None

        for attempt in range(retries):
            try:
                self.conn = mysql.connector.connect(
                    host=host,
                    user=user,
                    password=password
                )
                if self.conn.is_connected():
                    print(f"✅ Connected to MySQL on attempt {attempt + 1}")
                    self.cursor = self.conn.cursor()
                    self.create_database(database)
                    self.conn.database = database
                    self.create_table()
                    return
            except Error as e:
                print(f"⏳ Waiting for MySQL... ({attempt + 1}/{retries}): {e}")
                time.sleep(delay)

        raise RuntimeError("❌ Could not connect to MySQL after multiple attempts")

    def create_database(self, db_name):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_hashes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename TEXT,
                hash_value VARCHAR(64)
            )
        """)

    def insert_record(self, file_name, hash_value):
        try:
            with self.conn.cursor() as cursor:
                query = "INSERT INTO file_hashes (filename, hash_value) VALUES (%s, %s)"
                cursor.execute(query, (file_name, hash_value))
            self.conn.commit()
        except Exception as e:
            raise RuntimeError(f"❌ Failed to insert into MySQL: {e}")

    def close(self):
        self.cursor.close()
        self.conn.close()