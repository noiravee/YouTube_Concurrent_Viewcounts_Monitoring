import os
import sys
import pandas as pd
import re
import json
import time
from requests.models import Response
from tqdm import tqdm
from datetime import datetime
import requests as req
from bs4 import BeautifulSoup
from collections import OrderedDict
#from common.telegramMSG import send_telegram_msg

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import JobLookupError


TODAY = datetime.now().strftime('%y%m%d')
NOW = datetime.now().strftime('%y%m%d_%H%M')
RESULT = []
channelId ='UChlgI3UHCOnwUGzWzbJ3H5w'

with open ('./apikey.json', 'r', encoding='UTF-8') as f:
    key= json.load(f)




def get_videoId(channelId, key, type= 'video', eventType= 'live' ):
    videoIds= []
    url= f'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId={channelId}&type={type}&key={key}&eventType={eventType}'
    response= req.get(url)
    source= json.loads(response.text)

    for i in range(len(source['items'])):
        videoId= source['items'][i]['id']['videoId']
        videoIds.append(videoId)
        

    return videoIds
    


def get_concurrent_viewers(videoIds, key):
    source=[]
    result=[]
    for videoId in videoIds: 
        url = f'https://www.googleapis.com/youtube/v3/videos?&part=snippet,liveStreamingDetails&id={videoId}&key={key}'
        response= req.get(url)
        temp= json.loads(response.text)
        source.append(temp)



    for video in source:
        data=OrderedDict()
        data['timestamp']= datetime.now()
        data['videoId'] = video['items'][0]['id']
        data['title'] = video['items'][0]['snippet']['title']
        data['concurrentViewers'] = video['items'][0]['liveStreamingDetails']['concurrentViewers']
        data['actualStartTime'] = video['items'][0]['liveStreamingDetails']['actualStartTime']
        data['scheduledStartTime'] = video['items'][0]['liveStreamingDetails']['scheduledStartTime']
        
        
        result.append(data)
    

    df=pd.DataFrame(result)
    if not os.path.exists('concurrent_viewers.csv'):
        df.to_csv('concurrent_viewers.csv', index=False, mode='w')

    else:
        df.to_csv('concurrent_viewers.csv', index=False, mode='a', header=False)



def main():
    
    videoIds= get_videoId(channelId, key, type= 'video', eventType= 'live' )
    
    sched= BackgroundScheduler()
    sched.start()
    sched.add_job(get_concurrent_viewers, 'interval', minutes=1, id='step2', args=[videoIds, key])



    count=0
    while True:
        print('running main process...')
        time.sleep(55)

if __name__ == '__main__':

    main()



sys.exit(0)
