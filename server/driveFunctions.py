from driveAPI import auth
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
from google.oauth2.credentials import Credentials
from flask import session
from googleapiclient.discovery import build
import tempfile
from werkzeug.utils import secure_filename
import io, os

class driveFunctions():

    @staticmethod
    def list_files():
        
        service = auth()[0]
        files_info = []
        
        response = service.files().list(
            q="name contains '.enc' and trashed = false",
            pageSize=100,
            fields="files(id, name, size, modifiedTime)"
        ).execute()
        files = response.get('files', [])
        
        if not files:
            print("No files found.")
        else:
            for file in files:
                file_info = {'name': file['name'][:-4], 'id': file['id'], 'size': file.get('size', 'Unknown'), 'mimeType': file.get('mimeType', 'Unknown'), 'modifiedTime': file.get('modifiedTime', 'Unknown')}
                files_info.append(file_info)
        return files_info
    
    @staticmethod
    def search_files_by_name(file_name):
    
        service = auth()[0]
        query = f"name = '{file_name}'"
        response = service.files().list(q=query, fields='files(id)').execute()
        files = response.get('files', [])
        file_ids = [file['id'] for file in files]
        return file_ids[0]
    
    @staticmethod
    def download_file_from_drive(file_id, file_name):
    
        service = auth()[0]
        request = service.files().get_media(fileId=file_id)
        
        ##tempfile
        temp_dir = tempfile.mkdtemp()

        sec_filename = secure_filename(file_name)
        
        temp_file_path = os.path.join(temp_dir, sec_filename)
        ##

        with open(temp_file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()
                
        # print(temp_file_path)
        return temp_file_path

    @staticmethod
    def upload_file_to_drive(file_path, file_name):
        service = auth()[0]

        file_metadata = {
            'name': file_name
        }

        media = MediaIoBaseUpload(io.FileIO(file_path, 'rb'), mimetype='application/octet-stream', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print('File ID:', file.get('id'))
        
    @staticmethod  
    def delete_file(file_name):
        
        file_id = driveFunctions.search_files_by_name(file_name)

        print(file_id)
        
        service = auth()[0]
        try:
            service.files().delete(fileId=file_id).execute()
            print(f'File with ID: {file_id} deleted successfully.')
        except Exception as e:
            print(f'An error occured: {e}')
    
if __name__ == "__main__":
    # temp_path = driveFunctions.download_file_from_drive("1UcD7L0m2E0mxuHyqxr90cxIyU99xlWdf", "InfoBytes GS_8.png.enc")

    print(driveFunctions.delete_file('EttyDB.zip.enc'))