import os
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



TODAY = datetime.now().strftime('%y%m%d')
NOW = datetime.now().strftime('%y%m%d_%H%M')
RESULT = []

with open ('./apikey.csv', 'r', encoding='UTF-8') as f:
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

    


def get_concurrent_viewers(videoId, key):
    if pd.isnull(videoId):
        return 
    url = f'https://www.googleapis.com/youtube/v3/videos?&part=snippet,liveStreamingDetails&id={videoId}&key={key}'
    response= rq.get(url)
    live_streaming_details= json.loads(response.text)


get_videoId('UChlgI3UHCOnwUGzWzbJ3H5w', 'AIzaSyAraADzgRxHlDb_CgdtLpREn6uYI0FpziE')