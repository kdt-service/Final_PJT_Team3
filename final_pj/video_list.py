from extra_funcs import *
from bs4 import BeautifulSoup
from selenium import webdriver #4.9.1 Version 사용
import time
import pandas as pd
import warnings 
warnings.filterwarnings(action  = 'ignore')

def video_list(channel_url): #https://www.youtube.com/@wavve
       
    #세팅
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument("--single-process")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome('/home/ubuntu/final_pj/chrome/chromedriver', chrome_options=chrome_options)
    driver.set_window_size(800, 600)
    # 유튜브 페이지 열기 
    #channel_url = 'https://www.youtube.com/@wavve'
    channel_url = channel_url.replace("/featured","")+"/videos"
    driver.get(channel_url)
    time.sleep(3)
    # 유튜브 더이상 로딩되지 않을 때까지 스크롤 아래로 내리기
    last_page_height = driver.execute_script("return document.documentElement.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
        time.sleep(3.0)
        new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
        if new_page_height == last_page_height:
            break
        last_page_height = new_page_height
    time.sleep(10.0)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    video_lists = soup.find_all("ytd-rich-item-renderer", class_ = "style-scope ytd-rich-grid-row")
    video_df = pd.DataFrame(columns = ['video_id' , 'view_count'])
    for video in video_lists :
        # video_id 가져오고
        video_id= video.find("a", id = "video-title-link").get('href').split("?v=")[1]
        # 조회수 가져오고 
        video_view = video.find(class_= 'inline-metadata-item style-scope ytd-video-meta-block').text.replace("조회수 ","").replace("회","")
        video_df = video_df.append({'video_id':video_id, 'view_count':video_view} , ignore_index=True)
    
    video_df['view_count']= video_df['view_count'].apply(lambda x: clean_viewcount(x))
    return video_df # 최신 순서대로 들어가있음

