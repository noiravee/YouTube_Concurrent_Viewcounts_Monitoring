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
    info=[]
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
        df.to_excel('./concurrent_viewers.xlsx', index=False)
    


def main():
    schedule.every(5).minutes.do(videoIds= get_videoId('UChlgI3UHCOnwUGzWzbJ3H5w', key, type='video', eventType='live'),
    schedule.every(5).minutes.do(get_concurrent_viewers(videoIds, key))
    
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':

    main()



sys.exit(0)
