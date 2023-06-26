from extra_funcs import *
import pandas as pd
import datetime as dt
from googleapiclient.discovery import build
import re
import random
import time

# 채널 테이블 
def channel_table(url):
    
    # api_obj = build('youtube', 'v3', developerKey=open_key())

    # video_id = url.split("?v=")[-1]
    # response = api_obj.videos().list(part='snippet,statistics,contentDetails', id=video_id, maxResults=50).execute()

    api_key_lst = open_key2()
    api_idx = random.randint(0, len(api_key_lst)-1)

    while True:
        api_obj = build('youtube', 'v3', developerKey=api_key_lst[api_idx])
        # 댓글 정보 테이블 비디오 아이디
        video_id = url.split("?v=")[-1]
        
        try:
            response = api_obj.videos().list(part='snippet,statistics,contentDetails', id=video_id, maxResults=50).execute()   
            print(response)
            break
        except Exception as e: 
            print(f'{api_key_lst[api_idx]}channel_tb -> ',e)
            api_idx = random.randint(0, len(api_key_lst))

    # 채널 테이블 platformcr
    platform = '유튜브'
    # 채널 테이블 channel_name
    channel_name = response['items'][0]['snippet']['channelTitle']
    # 채널 ID channel_id
    channel_id = response['items'][0]['snippet']['channelId']
    # 구독자수 subscriber
    sub_response = api_obj.channels().list(part='statistics', id=channel_id, maxResults=50).execute()
    subscriber = sub_response ['items'][0]['statistics']['subscriberCount']
    # 동영상 개수 videoCount
    video_count = sub_response ['items'][0]['statistics']['videoCount']
    # 총 조회수 viewCount
    total_view_count =  sub_response ['items'][0]['statistics']['viewCount']
    # 크롤링한 시각 crawled_at
    crawled_at = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # print('cn : ', channel_name)
    # print('ci : ', channel_id)
    # print('sb : ', subscriber)
    # print('vc : ', video_count)
    # print('tvc : ', total_view_count)

    # print('SLEEP 10 SEC')
    # time.sleep(10)

    tb_channel = pd.DataFrame({'id':[channel_id], "platform":[platform], 'channel_name':[channel_name], 
                              'channel_id' :[channel_id], 'subscriber': [subscriber],'video_count':[video_count], 
                              'total_view_count':[total_view_count], 'crawled_at' : [crawled_at]
                             })
    # 앞부분은 하이픈, 뒷부분은 다른걸로 바꿔보자 
    now = str(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')).replace(":",".").replace(" ","_")
    tb_channel.to_csv(f"/home/ubuntu/final_pj/csvs/tb_channel_{now}.csv", index = False )
    # tb_channel.to_csv(f"/home/ubuntu/tb_channel_{now}.csv", index = False )
    file_name = f'tb_channel_{now}.csv'
    return file_name

# video 테이블 
def video_table(url):
    # api_obj = build('youtube', 'v3', developerKey=open_key())
    #  영상 크롤링 로그 테이블 비디오 아이디
    # video_id = url.split("?v=")[-1]
    # response = api_obj.videos().list(part='snippet,statistics,contentDetails', id=video_id, maxResults=50).execute()


    api_key_lst = open_key2()
    api_idx = random.randint(0, len(api_key_lst)-1)
    while True:
        api_obj = build('youtube', 'v3', developerKey=api_key_lst[api_idx])
        # 댓글 정보 테이블 비디오 아이디
        video_id = url.split("?v=")[-1]

        try:
            response = api_obj.videos().list(part='snippet,statistics,contentDetails', id=video_id, maxResults=50).execute()
            break
        except Exception as e:
            print(f'{api_key_lst[api_idx]} vide_tb -> ',e)
            api_idx = random.randint(0, len(api_key_lst)-1)

    # 영상 정보 테이블 채널아이디
    channel_id = response['items'][0]['snippet']['channelId']
    # 영상 정보 테이블 영상 제목
    title = response['items'][0]['snippet']['title']
    # 영상 정보 테이블 소개글
    intro = response['items'][0]['snippet']['description']
    # 영상 정보 테이블 해시태그
    try: 
        hashtag = response['items'][0]['snippet']['tags']
    except : 
        hashtag = []
    # 영상 정보 테이블 영상 길이
    running_time = running_time_func(response['items'][0]['contentDetails']['duration']) 
    # 영상 정보 테이블 업로드 날짜
    uploaded_at = response['items'][0]['snippet']['publishedAt'].split("T")[0]
    # 영상 크롤링 로그 테이블 조회수
    view_count =  response['items'][0]['statistics']['viewCount']
    # 영상 크롤링 로그 테이블 좋아요 수
    try :
        like_count = response['items'][0]['statistics']['likeCount']
    except:
        like_count = -1
    # 영상 크롤링 로그 테이블 댓글 수 commentCount
    comment_count =  response['items'][0]['statistics']['commentCount']
    # 영상 크롤링 로그 테이블 크롤링한 날짜 및 시간
    crawled_at = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    tb_video = pd.DataFrame({'id':[video_id], 'channel_id' :[channel_id], 'title': [title],
                               'intro':[intro], 'hashtag':[hashtag],
                               'running_time':[running_time], 'uploaded_at':[uploaded_at],
                             'video_id': [video_id], 'view_count':[view_count],
                             'like_count':[like_count],'comment_count':[comment_count],
                               'crawled_at' : [crawled_at]
                              })
    now = str(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')).replace(":",".").replace(" ","_")
    tb_video.to_csv(f"/home/ubuntu/final_pj/csvs/tb_video_{now}.csv", index = False )
    file_name = f'tb_video_{now}.csv'
    return file_name
   
   # 댓글 테이블 
   # 동영상 url 넘기기
def comment_table(url):
    comments = list()
    api_key_lst = open_key2()
    api_idx = random.randint(0, len(api_key_lst)-1)
    while True:
        api_obj = build('youtube', 'v3', developerKey=api_key_lst[api_idx])
        # 댓글 정보 테이블 비디오 아이디
        video_id = url.split("?v=")[-1]
        
        try:
            response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, maxResults=100).execute()
            break
        except Exception as e:
            print(f'{api_key_lst[api_idx]} comment_tb -> ',e)
            api_idx = random.randint(0, len(api_key_lst))

    crawled_at = dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    while response:
        for item in response['items']:
            item_id = item['id'] # 아이디
            parent_id = item_id # 부모 댓글 아이디 
            comment = item['snippet']['topLevelComment']['snippet']
            # id, parent_id(동일), video_id, content, writer , writed_at
            ct = comment['textDisplay']
            ct = re.sub('(?=\<a).+(?<=a>)', '' ,ct) # a태그
            ct = re.sub('[<br>]+', '' , ct) # <br>태그
            comment_text = re.sub('   ', ' ', ct) # 줄바꿈, 텝 -> 띄어쓰기로 대체

            comments.append([item_id,item_id,video_id,comment_text, comment['authorDisplayName'], comment['publishedAt'].split("T")[0], item_id,comment['likeCount'],crawled_at ])
            # 대댓글 추가! 
            if item['snippet']['totalReplyCount'] > 0:
                try : 
                    for reply_item in item['replies']['comments']:
                        parent_id = reply_item['id'].split(".")[0]
                        replie_id =reply_item['id'].split(".")[1]
                        reply = reply_item['snippet']
                        # id, parent_id, video_id, content, writer, writed_at 
                        rt = reply['textDisplay']
                        rt = re.sub('(?=\<a).+(?<=a>)', '' ,rt) # a태그
                        rt = re.sub('[<br>]+', '' , rt) # <br>태그
                        reply_text = re.sub('   ', ' ', rt) # 줄바꿈, 텝 -> 띄어쓰기로 대체
                        comments.append([replie_id, parent_id,video_id, reply_text, reply['authorDisplayName'], reply['publishedAt'].split("T")[0],replie_id,reply['likeCount'],crawled_at])
                except: # replies가 존재하지 않는 경우도 있네
                    pass
        if 'nextPageToken' in response:
            while True:
                try:
                    response = api_obj.commentThreads().list(part='snippet,replies', videoId=video_id, pageToken=response['nextPageToken'], maxResults=100).execute()
                    break
                except Exception as e:
                    print(f'{api_key_lst[api_idx]} newxPageToken - >', e)
                    api_idx = random.randint(0,len(api_key_lst)-1)
                    api_obj = build('youtube', 'v3', developerKey=api_key_lst[api_idx])

        else:
            break   
    tb_comments = pd.DataFrame(comments, columns = ['id','parent_id','video_id','content','writer', 'writed_at','comment_id','like_count','crawled_at'])       
    now = str(dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')).replace(":",".").replace(" ","_")
    tb_comments.to_csv(f"/home/ubuntu/final_pj/csvs/tb_comment_{now}.csv", index = False )
    file_name = f'tb_comment_{now}.csv'
    return file_name

# def open_key(): # youtube_api_key 따로 youtube_api_key.txt에 저장해놓은 내용 읽기
#     hour = dt.datetime.now().hour
#     f = open('/home/ubuntu/final_pj/youtube_api_key',"rt")
#     line = f.readline() # 다은's
#     if hour >10 and hour <14 : # 10시에서 13시 사이이면 석호님 googleapikey  
#         line = f.readline()
#     if hour >=14 and hour <19 : # 2시에서 5시 사이이면 수연님 googleapikey  
#         line = f.readline()
#         line = f.readline()
#     if hour >= 19 : # 오후 5시 이후이면 석호님 googleapikey  
#         line = f.readline()
#         line = f.readline()
#         line = f.readline()
#     f.close()
#     return line

def open_key2():
    with open('/home/ubuntu/final_pj/youtube_api_key',"r") as f:
        line = f.readlines()
        
    return line




