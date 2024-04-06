import subprocess, os, pathlib
import utils_local
from dotenv import load_dotenv

root_path = str(pathlib.Path(__file__).parent)

load_dotenv(dotenv_path=os.path.join(root_path, '.env'))

def recordStream(meta: dict):
    
    file_id = utils_local.getFileID(meta["createdAt"], True)

    filename_mp4 = f'{file_id}.mp4'
    
    filename_ts = f'{file_id}.ts'
    
    file_path_mp4 = os.path.join(root_path,'data/VOD', filename_mp4)
    
    file_path_ts = os.path.join(root_path, 'data/TS', filename_ts)
    
    print('Recording Stream')
    
    subprocess.call([
        'streamlink', 
        f'twitch.tv/{os.getenv("STREAMER")}', os.getenv("QUALITY"), 
        '--twitch-api-header', f'Authorization=OAuth {os.getenv("AUTHTOKEN")}',
        '--hls-segment-threads', '3',
        '--hls-live-restart',
        '--retry-streams', '5',
        '--twitch-disable-reruns',
        '-o', file_path_ts
    ])
    
    print('Stream ended, converting to mp4')
    
    if(os.path.exists(file_path_ts) is True):
    
        subprocess.call([
            'ffpb',
            '-y', '-i', file_path_ts,
            '-analyzeduration', '2147483647',
            '-probesize', '2147483647',
            '-c:v', 'copy', 
            '-c:a', 'copy',
            '-start_at_zero', 
            '-copyts', file_path_mp4
        ])
        
        print('Stream was converted')