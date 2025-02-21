# services/cloud_service.py
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
import os
import pickle
import io

class GoogleDriveService:
    def __init__(self):
        # If modifying these scopes, delete the token.pickle file
        self.SCOPES = ['https://www.googleapis.com/auth/drive.file']
        self.creds = None
        self.service = None
        self.token_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'token.pickle')
        self.credentials_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'credentials.json')
        
    def authenticate(self):
        """Handles the OAuth2 authentication flow with Google"""
        # Load existing credentials if available
        if os.path.exists(self.token_path):
            with open(self.token_path, 'rb') as token:
                self.creds = pickle.load(token)
        
        # If credentials are invalid or don't exist, get new ones
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Save the credentials for future use
            with open(self.token_path, 'wb') as token:
                pickle.dump(self.creds, token)
        
        # Build the Drive API service
        self.service = build('drive', 'v3', credentials=self.creds)
        
    def upload_file(self, file_path, file_name=None):
        """
        Uploads a file to Google Drive
        Args:
            file_path (str): Path to the file to upload
            file_name (str, optional): Name to give the file in Drive
        Returns:
            str: ID of the uploaded file
        """
        if not self.service:
            self.authenticate()
            
        if not file_name:
            file_name = os.path.basename(file_path)
            
        file_metadata = {'name': file_name}
        media = MediaFileUpload(file_path, resumable=True)
        
        file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        
        return file.get('id')
        
    def download_file(self, file_id, save_path):
        """
        Downloads a file from Google Drive
        Args:
            file_id (str): ID of the file to download
            save_path (str): Where to save the downloaded file
        """
        if not self.service:
            self.authenticate()
            
        request = self.service.files().get_media(fileId=file_id)
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            
        fh.seek(0)
        with open(save_path, 'wb') as f:
            f.write(fh.read())
            
    def list_files(self, query=None):
        """
        Lists files in Google Drive
        Args:
            query (str, optional): Search query to filter files
        Returns:
            list: List of file metadata dictionaries
        """
        if not self.service:
            self.authenticate()
            
        results = self.service.files().list(
            pageSize=10,
            fields="nextPageToken, files(id, name, mimeType, createdTime)",
            q=query
        ).execute()
        
        return results.get('files', [])