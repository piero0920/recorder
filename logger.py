import os, json, pathlib
import utils_local

root_path = str(pathlib.Path(__file__).parent)

def logStream(metadata: dict) -> bool :
    
    log_file = f'{root_path}/data/LOG/log-stream.log'

    if os.path.isfile(log_file) is False:
    
        with open(log_file, 'w') as f:
    
            f.close()

    log_line = f'{metadata["createdAt"]} - {metadata["id"]}\n'
    
    with open(log_file, 'r', encoding='utf-8') as f:
    
        exits = any(x == log_line for x in f)
    
    if not exits:
    
        with open(log_file, 'a', encoding='utf-8') as f:
    
            f.write(log_line)
    
        return True
    
    else:
    
        return False

def setLiveBoolean(is_live: bool) -> None:

    log_file = f'{root_path}/data/LOG/isLive.json'
    
    if os.path.isfile(log_file) is False:
    
        with open(log_file, 'w', encoding='utf-8') as f:
    
            json.dump({"isLive": False},f, ensure_ascii=False, indent=4)

    with open(log_file, 'r', encoding='utf-8') as f:
    
        data = json.loads(f.read())
    
    if is_live is True:
    
        data["isLive"] = True
    
    else:
    
        data["isLive"] = False
    
    with open(log_file, 'w', encoding='utf-8') as f:
    
        json.dump(data, f, ensure_ascii=False, indent=4)


def saveMetadata(metadata_live: dict, metadata_vod:dict) -> None:
    
    file_id = utils_local.getFileID(metadata_live["createdAt"], False)
    
    metadata_live_file = f'{root_path}/data/METADATA/live_{file_id}.json'
    
    metadata_vod_file = f'{root_path}/data/METADATA/vod_{file_id}.json'

    with open(metadata_live_file, 'w', encoding='utf-8') as f:
    
        json.dump(metadata_live, f, ensure_ascii=False, indent=4)
    
    if metadata_vod is not None: 
    
        with open(metadata_vod_file, 'w', encoding='utf-8') as f:
    
            json.dump(metadata_vod, f, ensure_ascii=False, indent=4)