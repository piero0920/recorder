import os, pathlib, json, re, calendar, shutil
from datetime import datetime, timedelta
from pytz import timezone
from dotenv import load_dotenv

root_path = str(pathlib.Path(__file__).parent)
load_dotenv(dotenv_path=os.path.join(root_path, '.env'))

def getFileID(metadata_time: str, new: bool) -> str:
    
    live_date = datetime.strptime(metadata_time,'%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone('UTC')).astimezone(tz=None).replace(tzinfo=None)
    
    live_date = live_date - timedelta(hours=10)
    
    filename = datetime.strftime(live_date,'%Y%m%d')
    
    files = os.listdir(f'{root_path}/data/VOD')
    
    new_files=[]
    
    for file in files:
    
        if filename in file:
    
            new_files.append(filename)
    
    if new:
    
        file_id = f'{filename}-{len(new_files)+1}'
    
    else:
    
        file_id = f'{filename}-{len(new_files)}'
    
    return file_id

def deleteTS(metadata: dict) -> None:
    
    file_id = getFileID(metadata["createdAt"], False)
    
    file_path = f'{root_path}/data/TS/{file_id}.ts'
    
    if os.path.isfile(file_path) is True:
    
        os.remove(file_path)

def formatFilename(file_date: datetime) -> dict:
    
    month_last = calendar.monthrange(file_date.year, file_date.month)[1]
    month_first = set(calendar.monthcalendar(file_date.year, file_date.month)[0])
    month_first.discard(0)

    if file_date.day <= len(month_first):
        week_first = file_date.replace(day=1)
        week_last = file_date.replace(day=len(month_first))
    else:
        week_first = file_date - timedelta(days=file_date.weekday())
        week_last = week_first + timedelta(days=6)


    week_first = week_first.day 
    week_last = week_last.day

    if week_last < week_first:
        week_last = month_last

    return {
        "week_first": week_first,
        "week_last":  week_last
    }

def moveVOD(file_id: str, total: int) -> None:
    
    with open(f'{root_path}/data/METADATA/live_{file_id}.json', 'r', encoding='utf-8') as f:
        
        metadata = json.loads(f.read())

    title = re.sub(r'[/\\:*?"<>|]', '_', metadata["title"])
    
    if len(title) > 220:
        
        dif = len(title) - 220
    
        title = title[:-dif]
    
    if total == 1:
    
        filename = f'{file_id[:-2]}_{title}.mp4'
    
    else:
    
        filename = f'{file_id[:-2]}_{title} ({file_id[-1:]}-{total}).mp4'

    file_date = datetime.strptime(file_id[:-2], '%Y%m%d').date()
    week = formatFilename(file_date)
    
    if week["week_first"] == week['week_last']:
        week_path = f'{week["week_first"]}'
    else:
        week_path = f'{week["week_first"]}-{week["week_last"]}'

    current_path = f'{root_path}/data/VOD/{file_id}.mp4'
    next_path = f'/videos/VOD - {file_date.year}/{file_date.month:02d} - {file_date.strftime("%B").upper()}/{file_date.strftime("%B").capitalize()} {week_path}/{filename}'
    print('Moving vod files to Drive')
    shutil.move(current_path, next_path)
