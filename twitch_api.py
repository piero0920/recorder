import requests, pathlib, os
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first, limit
from dotenv import load_dotenv

root_path = str(pathlib.Path(__file__).parent)

load_dotenv(dotenv_path=os.path.join(root_path, '.env'))

gql_url = "https://gql.twitch.tv/gql"

def GQL_Request(query: str, variables: dict) -> dict | None: 
    gql_query = {
        "query": query,
        "variables": variables
    }

    headers = {
        "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
        "Cache-Control": "no-cache",
        "Pragma": "no-cache"
    }

    response = requests.post(gql_url, headers=headers, json=gql_query)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def getStream(streamer: str) -> dict | None:

    query = """
        query getStream($user: String){
            user(login: $user){
                stream{
                    id
                    title
                    createdAt
                }
            }
        }
    """

    variables = {
        "user": streamer
    }

    response = GQL_Request(query, variables)
    
    if response:

        data = response["data"]

        return data["user"]["stream"]
    
    else:
    
        return None


async def getIDs(meta: dict) -> list | None:
    
    twitch = await Twitch(os.getenv("APP_ID"), os.getenv("APP_SECRET"))

    user = await first(twitch.get_users(logins=os.getenv("STREAMER")))
    user_id = user.id

    videos = twitch.get_videos(user_id=user_id)

    if videos is not None:
        ids = []
        async for video in limit(videos, 10):
            if video.stream_id == meta["id"]: 
                ids.append({
                    "stream_id": video.stream_id,
                    "vod_id": video.id,
                    "createdAt": video.created_at
                })
                break
        
        if ids != []: 
            
            await twitch.close()
            return ids
    
    await twitch.close()    
    return None


async def getVOD(meta: dict) -> list | None:
    
    twitch = await Twitch(os.getenv("APP_ID"), os.getenv("APP_SECRET"))

    video = await first(twitch.get_videos(ids=[meta["id"]]))

    if video is not None:
        await twitch.close()  
        return video.to_dict()

    await twitch.close()    
    return None