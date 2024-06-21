from driveAPI import auth
from googleapiclient.http import MediaIoBaseDownload, MediaIoBaseUpload
import io

class driveFunctions():

    def list_files():
        
        service = auth()
        name_list = []
        
        response = service.files().list(
            q="name contains '.enc'",
            pageSize=100,
            fields="files(id, name)"
        ).execute()
        files = response.get('files', [])
        
        for file in files:
            name_list.append(file['name'])
            
        return name_list
    
    def search_files_by_name(file_name):
    
        service = auth()
        query = f"name = '{file_name}'"
        response = service.files().list(q=query, fields='files(id)').execute()
        files = response.get('files', [])
        file_ids = [file['id'] for file in files]
        return file_ids[0]
    
    
    def download_file_from_drive(file_id, file_path):
    
        service = auth()
        request = service.files().get_media(fileId=file_id)
        
        with open(file_path, 'wb') as f:
            downloader = MediaIoBaseDownload(f, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()


    def upload_file_to_drive(file_path, file_name):
        service = auth()

        file_metadata = {
            'name': file_name
        }

        media = MediaIoBaseUpload(io.FileIO(file_path, 'rb'), mimetype='application/octet-stream', resumable=True)
        file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print('File ID:', file.get('id'))
        
        
if __name__ == "__main__":
    print(driveFunctions.list_files())