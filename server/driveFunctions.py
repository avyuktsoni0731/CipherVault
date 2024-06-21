from driveAPI import auth
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import io

class driveFunctions():

    def list_files():
        
        service = auth()[0]
        files_info = []
        # name_list = []
        
        response = service.files().list(
            q="name contains '.enc'",
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
    
    def search_files_by_name(file_name):
    
        service = auth()[0]
        query = f"name = '{file_name}'"
        response = service.files().list(q=query, fields='files(id)').execute()
        files = response.get('files', [])
        file_ids = [file['id'] for file in files]
        return file_ids[0]
    
    
    def download_file_from_drive(file_id, file_path):
    
        service = auth()[0]
        request = service.files().get_media(fileId=file_id)
        
        with open(file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()


    def upload_file_to_drive(file_path, file_name):
        service = auth()[0]

        file_metadata = {
            'name': file_name
        }

        media = MediaIoBaseUpload(io.FileIO(file_path, 'rb'), mimetype='application/octet-stream', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print('File ID:', file.get('id'))
        
        
if __name__ == "__main__":
    print(driveFunctions.list_files())