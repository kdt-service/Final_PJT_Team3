from crawling_funcs import *
from extra_funcs import *
from db_connect import * 
from video_list import *
import pandas as pd
import time
import datetime as dt
url_list = [
 'https://www.youtube.com/@cu.official','https://www.youtube.com/@official_GS25',
 'https://www.youtube.com/@STUDIO_SUZE',"https://www.youtube.com/@dex101",'https://www.youtube.com/@user-kr3if6xn3g',#지상렬
   'https://www.youtube.com/@user-ou9fg3bg1v'#me
]

all_list = ['https://www.youtube.com/@STUDIO_SUZE','https://www.youtube.com/@user-kr3if6xn3g',"https://www.youtube.com/@user-ou9fg3bg1v"]

for url in url_list :
    print(url+"크롤링 시작!")
    url_id = url.split("@")[1]
    list_df = video_list(url)
    every_video_list = list_df['video_id']

    if url in all_list : # 부정어 사전 구축 관련 채널이면 모든 동영상 다 크롤링하지만
        every_video_list = every_video_list[:]
    else :
        every_video_list = every_video_list[:5] # 그게 아니라면 최신 동영상 5개만 크롤링.

    for videoid in every_video_list:  # DB에 INSERT하는 코드
        
        # 예시 코드
        DeleteAllFiles() # csv 안 파일 정리
        want_URL = f'https://www.youtube.com/watch?v={videoid}'
        
        # 채널 관련
        try :
            channel_csv = channel_table(want_URL)
            channel_df =  pd.read_csv(f'/home/ubuntu/final_pj/csvs/{channel_csv}')
            channel_id = channel_df['id']
            excecuteDB(channel_df, 'channel')
        except : 
            print(f'처리하지 못한 video_id는 {videoid}입니다\n')

        # 영상관련 
        try :
            video_csv = video_table(want_URL)
            video_df = pd.read_csv(f'/home/ubuntu/final_pj/csvs/{video_csv}')
            excecuteDB(video_df, 'video')
        except :
             with open('log_file.log','a') as f:
                f.write(f'처리하지 못한 video_id는 {videoid}입니다\n')

           
        if today_comment_crawl(videoid) : 
            # 댓글 관련 
            try :
                comment_csv = comment_table(want_URL)
                comment_df = pd.read_csv(f'/home/ubuntu/final_pj/csvs/{comment_csv}',  lineterminator='\n') 
                excecuteDB(comment_df, 'comment')
                time.sleep(2)
            except :
                with open('log_file.log','a') as f:
                    f.write(f'처리하지 못한 video_id는 {videoid}입니다\n')
        time.sleep(2)
    print(f'{url} 크롤링 완료! ')
   
    
