import requests
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from datetime import date, datetime, timedelta
import os
import io
from Google import Create_Service
from googleapiclient.http import MediaIoBaseDownload
import Google_download
CLIENT_SECRET_FILE = 'client_secrets.json'
API_NAME = 'drive'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/drive']

service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

gauth = GoogleAuth()
# gauth.LocalWebserverAuth()


def date_list(start_date='01.01.01', end_date='02.02.02', word='Приходы'):
    start = datetime.strptime(start_date, '%d.%m.%y')
    end = datetime.strptime(end_date, '%d.%m.%y')
    delta = end - start
    folders_names_list = []
    if delta.days<=0:
        print('Нет диапзона')
    for i in range(delta.days + 1):
        date = start + timedelta(i)
        file_date = date.strftime("%m %d")
        file_name = f'{word}  {file_date}'
        folders_names_list.append(file_name)
    return folders_names_list
# return folders names for search in list


def get_files_names_and_ids(gauth, folder_id='1n6R50IOR3eTFcIDVbZ-jBBs-HXLYC2yt'):
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    files_names = []
    files_id = []
    for file in file_list:
        name = file['title']
        id = file['id']
        files_names.append(name)
        files_id.append(id)
    return [files_names, files_id]



def get_folders_dic(gauth, folder_id='1n6R50IOR3eTFcIDVbZ-jBBs-HXLYC2yt'):
    drive = GoogleDrive(gauth)
    file_list = drive.ListFile({'q': f"'{folder_id}' in parents and trashed=false"}).GetList()
    files_names = {}
    for file in file_list:
        title = file['title']
        id = file['id']
        files_names[f'{title}'] = f'{id}'
    return files_names


def find_folders_ids_and_mkdir():
    folder_names = []
    finding_folders_id = {}
    folders_list = []
    folders_dic = get_folders_dic(gauth, '1n6R50IOR3eTFcIDVbZ-jBBs-HXLYC2yt')
    date_delta = date_list(start_date='14.11.22', end_date='20.11.22', word='Приходы')
    for date in date_delta:     # цикл пробежки по названиям сгенерированных папок
        # print(f'Цикл переборки сгенерированных названий папок. Папка {date}')
        for key in folders_dic: # цикл поиска и получения по сгенерированным названиям
            # print(f'Цикл поиска совпадений из сгенерированного списка и папки. Название папки на диске {key}')
            if key == date:
                # print('Совпадение найдено!')
                item = folders_dic.get(key)
                finding_folders_id[f'{key}'] = f'{item}'
                os.mkdir(f"C:\Приходы\{key}")
                folders_list.append(item)
                folder_names.append(key)
    return finding_folders_id


def main():
    list = find_folders_ids_and_mkdir()
    print(list)
    # for folder_id in folders_ids:
    #     files_dic = get_files_names_and_ids(gauth, folder_id=folder_id)
    #     print(files_dic)
    for key in list:
        item = list.get(key)
        print(item)
        files_to_download = get_files_names_and_ids(gauth, folder_id=item)
        # print(f'{files_to_download} Скачать в папку {key}')
        files_names, files_ids = files_to_download
        for file_id, file_name in zip(files_ids, files_names):
            request = service.files().export_media(fileId=file_id,
                                                   mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fd=fh, request=request)
            done = False

            while not done:
                status, done = downloader.next_chunk()
            fh.seek(0)

            with open(os.path.join(f'C:\Приходы\{key}', f'{file_name}.xlsx'), 'wb') as f:
                f.write(fh.read())
                f.close()


# def noname():
#     dic = get_folders_dic(gauth, folder_id='1eLIxNdUhNaUVi2rlNNF5ekhZGHlRP6rb')
#     date_delta = date_list(start_date='14.11.22', end_date='17.11.22', word='разблюдовка')


    #
    # folder_names=[]
    # finding_folders_id = {}
    # folders_list = []
    # folders_dic = get_folders_dic(gauth, '1n6R50IOR3eTFcIDVbZ-jBBs-HXLYC2yt')
    # # print(f'Получаю словарь из папки {folders_dic}')
    # date_delta = date_list(start_date='14.11.22', end_date='20.11.22')
    # for date in date_delta:     # цикл пробежки по названиям сгенерированных папок
    #     print(f'Цикл переборки сгенерированных названий папок. Папка {date}')
    #     for key in folders_dic: # цикл поиска и получения по сгенерированным названиям
    #         print(f'Цикл поиска совпадений из сгенерированного списка и папки. Название папки на диске {key}')
    #         if key == date:
    #             print('Совпадение найдено!')
    #             item = folders_dic.get(key)
    #             finding_folders_id[f'{key}'] = f'{item}'
    #             os.mkdir(f"C:\Приходы\{key}")
    #             folders_list.append(item)
    #             folder_names.append(key)
    #             for folder in folders_list:
    #                 files_dic = get_files_names_and_ids(gauth, folder_id=folder)
    #                 print(files_dic)
    #
    #             names_and_ids = files_dic
    #             files_names = names_and_ids[0]
    #             print(files_names)
    #             files_ids = names_and_ids[1]
    #             print(files_ids)
    #
    #             for file_id, file_name in zip(files_ids, files_names):
    #                 request = service.files().export_media(fileId=file_id,
    #                                                        mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    #
    #                 fh = io.BytesIO()
    #                 downloader = MediaIoBaseDownload(fd=fh, request=request)
    #                 done = False
    #
    #                 while not done:
    #                     status, done = downloader.next_chunk()
    #                     print(f'Download progress {file_name} {0}'.format(status.progress() * 100))
    #
    #                 fh.seek(0)
    #
    #                 for key in folder_names:
    #                     print(f'Папка в которую качаю: {key}')
    #                     with open(os.path.join(f"C:\Приходы\{key}", file_name), 'wb') as f:
    #                         f.write(fh.read())
    #                         f.close()






    # date_list(start_date='10.11.22', end_date='13.11.22')
    # drive = GoogleDrive(gauth)
    # file_list = drive.ListFile({'q': "'1n6R50IOR3eTFcIDVbZ-jBBs-HXLYC2yt' in parents and trashed=false"}).GetList()
    # files_names = {
    #
    # }
    # for file in file_list:
    #     title = file['title']
    #     id = file['id']
    #     files_names[f'{title}'] = f'{id}'
    # print(files_names)
    # print(create_and_upload(file_name='hello.txt', file_content='Hello world!'))


if __name__ == '__main__':
    main()
