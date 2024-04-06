import os, pathlib

root_folder = os.path.join(str(pathlib.Path(__file__).parent), "data")


TS_folder = os.path.join(root_folder, 'TS')
METADATA_folder = os.path.join(root_folder, 'METADATA')
LOG_folder = os.path.join(root_folder, 'LOG')

folders = [TS_folder, LOG_folder, METADATA_folder]

def CreateFolders():
    for folder in folders:
        if os.path.isdir(folder) is False:
            os.makedirs(folder)