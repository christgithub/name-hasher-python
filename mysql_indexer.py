import mysql.connector

class MySQLIndexer:
    def __init__(self, host="localhost", user="root", password="", database="sftp_index"):
        self.conn = mysql.connector.connect(
            host=host,
            user=user,
            password=password
        )
        self.cursor = self.conn.cursor()
        self.create_database(database)
        self.conn.database = database
        self.create_table()

    def create_database(self, db_name):
        self.cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS file_hashes (
                id INT AUTO_INCREMENT PRIMARY KEY,
                filename TEXT,
                original_line TEXT,
                hash_value VARCHAR(64)
            )
        """)

    def insert_record(self, doc):
        sql = "INSERT INTO file_hashes (filename, original_line, hash_value) VALUES (%s, %s, %s)"
        values = (doc["filename"], doc["original"], doc["hash"])
        self.cursor.execute(sql, values)
        self.conn.commit()

    def close(self):
        self.cursor.close()
        self.conn.close()