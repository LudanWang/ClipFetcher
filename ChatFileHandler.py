from pydrive.auth import GoogleAuth
from pydrive.auth import ServiceAccountCredentials
from pydrive.drive import GoogleDrive
import os

VIDEO_FOLDER_ID = '1tcs1nW3eWhXhC150nJhRK_g-KyH1d6Nr'
CHAT_FOLDER_ID = '1np-YmrUitiIoenl7hWuzgHYVQOTfK3k2'

def UploadChat(vod_id,abs_path):
    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('ClipFetcher-SERVICE-ACCOUNT.json', scope)
    drive = GoogleDrive(gauth)

    file_name = vod_id + '.json' #
    with open(abs_path, "r") as file:
        file_drive = drive.CreateFile({'title': os.path.basename(file.name),
                                       'parents': [{'kind': 'drive#fileLink',
                                                    'id': CHAT_FOLDER_ID}]})
        file_drive.SetContentFile(abs_path)
        file_drive.Upload()

def UploadVideo(vod_id,abs_path):
    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('ClipFetcher-SERVICE-ACCOUNT.json', scope)
    drive = GoogleDrive(gauth)

    file_name = vod_id + '.mp4'
    with open(abs_path, "r") as file:
        file_drive = drive.CreateFile({'title': os.path.basename(file.name),
                                        'parents': [{'kind': 'drive#fileLink',
                                                     'id': VIDEO_FOLDER_ID}]})
        file_drive.SetContentFile(abs_path)
        file_drive.Upload()

def ListFile(folder_id):
    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('ClipFetcher-SERVICE-ACCOUNT.json', scope)
    drive = GoogleDrive(gauth)

    query = '\'' + folder_id + '\' in parents and trashed=false'
    file_list = drive.ListFile({'q': query}).GetList()
    for file in file_list:
        print('Title: %s, ID: %s' % (file['title'], file['id']))

def GetFileID(file_name,folder_id):
    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('ClipFetcher-SERVICE-ACCOUNT.json', scope)
    drive = GoogleDrive(gauth)

    query = '\'' + folder_id + '\' in parents and trashed=false'  # root OR chat OR video
    file_list = drive.ListFile({'q': query}).GetList()
    for file in file_list:
        if file['title'] == file_name:
            return file['id']
    return None