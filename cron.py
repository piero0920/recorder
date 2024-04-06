import datetime, os, schedule, pathlib, time
from utils_local import moveVOD

root_path = str(pathlib.Path(__file__).parent)

def run_cronjob(days_ago: int) -> None:
    
    print(f'cron jon started at {datetime.datetime.now()}')

    file_id = datetime.datetime.strftime(datetime.datetime.now() - datetime.timedelta(days=days_ago), '%Y%m%d')

    files = os.listdir('./data/METADATA')

    unique_files = []

    for file in files:
        if f'live_{file_id}' in file:
            unique_files.append(file)
    
    if unique_files != []:
        print('Starting cron process')
        

        for unique in unique_files:

            #Move drive files
        
            for unique in unique_files:
                
                unique_file_id = unique[5:-5]

                moveVOD(unique_file_id, len(unique_files))

            print('process done!')

        else:
            print('theres not files for cron job')


schedule.every().day.at("08:00").do(lambda: run_cronjob(1))

while True:
    schedule.run_pending()
    time.sleep(1)