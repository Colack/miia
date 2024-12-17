from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import logging

def backup_to_google_drive(file_path):
    """Back up the CSV file to Google Drive."""
    try:
        gauth = GoogleAuth()
        gauth.LocalWebserverAuth()
        drive = GoogleDrive(gauth)

        file_drive = drive.CreateFile({'title': file_path})
        file_drive.SetContentFile(file_path)
        file_drive.Upload()

        logging.info(f"{file_path} successfully backed up to Google Drive.")
    except Exception as e:
        logging.error(f"Failed to back up file: {e}")
