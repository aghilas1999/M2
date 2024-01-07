# import os
# import json
# import base64
# import urllib.request
# from urllib.error import HTTPError

# # constants, configure to match your environment
# HOST = 'https://localhost:9200'
# INDEX = 'monindex'
# TYPE = '_doc'
# TMP_FILE_NAME = 'tmp.json'
# # for supported formats, see apache tika - http://tika.apache.org/1.4/formats.html
# INDEX_FILE_TYPES = ['json']


# def main():
#     index_directory = input('Index entire directory [Y/n]: ')

#     if not index_directory:
#         index_directory = 'y'

#     if index_directory.lower() == 'y':
#         directory = input('Directory to index (relative to script): ')
#         index_dir(directory)
#     else:
#         file_name = input('File to index (relative to script): ')
#         index_file(file_name)


# def index_file(file_name):
#     print('\nIndexing ' + file_name)
#     create_encoded_temp_file(file_name)
#     post_file_to_the_index()
#     os.remove(TMP_FILE_NAME)
#     print('\n-----------')


# def index_dir(directory):
#     print('Indexing dir ' + directory)
#     for path, dirs, files in os.walk(directory):
#         for file in files:
#             file_name = os.path.join(path, file)

#             base, extension = file.rsplit('.', 1)

#             if extension.lower() in INDEX_FILE_TYPES:
#                 index_file(file_name)

# def post_file_to_the_index():
#     cmd = 'curl -H "Content-Type: application/json" -XPOST "{}/{}/{}" -d @'.format(HOST, INDEX, TYPE) + TMP_FILE_NAME
#     print(cmd)
#     os.system(cmd)


# def create_encoded_temp_file(file_name):
#     file_content = open(file_name, "rb").read()
#     file_base64 = base64.b64encode(file_content).decode('utf-8')

#     print('writing JSON with base64 encoded file to temp file {}'.format(TMP_FILE_NAME))

#     with open(TMP_FILE_NAME, 'w') as f:
#         data = {'file': file_base64, 'title': file_name}
#         json.dump(data, f)


# # kick off the main function when script loads
# main()

import os
import json
import base64
import urllib.request

# constants, configure to match your environment
HOST = 'http://localhost:9200'
INDEX = 'monindex'
TYPE = '_doc'
TMP_FILE_NAME = 'tmp.json'
# for supported formats, see apache tika - http://tika.apache.org/1.4/formats.html
INDEX_FILE_TYPES = ['json']


def main():
    indexDirectory = input('Index entire directory [Y/n]: ')

    if not indexDirectory:
        indexDirectory = 'y'

    if indexDirectory.lower() == 'y':
        dir_path = input('Directory to index (relative to script): ')
        index_dir(dir_path)

    else:
        file_name = input('File to index (relative to script): ')
        index_file(file_name)


def index_file(file_name):
    print('\nIndexing ' + file_name)
    create_encoded_temp_file(file_name)
    post_file_to_the_index()
    os.remove(TMP_FILE_NAME)
    print('\n-----------')


def index_dir(dir_path):
    print('Indexing dir ' + dir_path)

    for path, dirs, files in os.walk(dir_path):
        for file in files:
            file_path = os.path.join(path, file)
            base, extension = file.rsplit('.', 1)

            if extension.lower() in INDEX_FILE_TYPES:
                index_file(file_path)


def post_file_to_the_index():
    cmd = 'curl -H "Content-Type: application/json" -XPOST "{}/{}/{}" -d @{}'.format(HOST, INDEX, TYPE, TMP_FILE_NAME)
    print(cmd)
    os.system(cmd)


def create_encoded_temp_file(file_name):
    file_content = open(file_name, "rb").read()
    encoded_file = base64.b64encode(file_content).decode('utf-8')

    print('writing JSON with base64 encoded file to temp file {}'.format(TMP_FILE_NAME))

    with open(TMP_FILE_NAME, 'w') as f:
        data = {'file': encoded_file, 'title': file_name}
        json.dump(data, f)  # dump json to tmp file


# kick off the main function when script loads
main()