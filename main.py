import time, asyncio
from twitch_api import getStream, getIDs, getVOD
from logger import logStream, setLiveBoolean, saveMetadata
from runner import recordStream
from utils_local import deleteTS
from dirs import CreateFolders
#from threading import Thread

print('Process started')

CreateFolders()

while True:
    is_live = getStream()

    if is_live is not None and logStream(is_live):
        print('live started')

        setLiveBoolean(True)
        recordStream(is_live)
        setLiveBoolean(False)
        ids = asyncio.run(getIDs(is_live))
        vod_metadata = asyncio.run(getVOD(ids))
        deleteTS(is_live)
        saveMetadata(is_live, vod_metadata)

        print('live ended')
    else:
        time.sleep(30)