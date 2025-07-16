import string
import sys
from typing import List
import paramiko
import os

class SFTPClient:
    def __init__(self, host, port, username, password, download_dir="downloads"):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.download_dir = download_dir
        os.makedirs(download_dir, exist_ok=True)

    def connect(self):
        try:
            self.transport = paramiko.Transport((self.host, self.port))
            self.transport.connect(username=self.username, password=self.password)
            self.sftp = paramiko.SFTPClient.from_transport(self.transport)
        except Exception as e:
            raise RuntimeError(f"❌ Failed to connect to sftp server: {e}")

    def download_files(self, remote_dir="upload"): 
        try:
            files = self.sftp.listdir(remote_dir)
            downloaded = []
        
            for filename in files:
                remote_path = f"{remote_dir}/{filename}"
                local_path = os.path.join(self.download_dir, filename)
                self.sftp.get(remote_path, local_path)
                downloaded.append(local_path)
        except Exception as e:
            print(f"❌ Error listing files in {remote_dir}: {e}")
        
        self.disconnect()
        
        return downloaded

    def disconnect(self):
        self.sftp.close()
        self.transport.close()