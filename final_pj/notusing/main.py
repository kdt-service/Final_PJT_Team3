from crawling_funcs import *
from extra_funcs import *
from db_connect import * 
from video_list import *
from recent_highview_list import * 
import pandas as pd
import re 
import pandas as pd
from gyoungwon_main.preprocess_lang import * 
from gyoungwon_main.emotion import * 


# Crontab 활용해서 4시간마다 periodically_crawl.py에서 실행된다. -> 실행 결과는 video_list.csv에 저장 되어 있다. 
#list_df = pd.read_csv('/home/ubuntu/final_pj/video_list_csvs/video_list_STUDIO_SUZE.csv')
# 인자 : 리스트 항목개수, 채널ID, 데이터프레임(video_id만 갖고있음)
#recent_top_list, high_diff_list= recent_highview_func(5, 'UC4ZA57iJrf73bJlApKFeLRw',list_df)

# # 댓글 여러분석기능 만들기
# #1. 감정분석 하려면 content가 필요해 => SQL문으로 video_id가 ~~인 최신 댓글 갖고와. 
# for idx, video_id in enumerate(recent_top_list): # recent_df1, ,,, recent_df5 생성
#         globals() ['recent_df{}'.format(idx+1)]= comment_by_videoid(video_id) # video_id로 댓글 가져와서 
#         globals() ['recent_df{}'.format(idx+1)]['writed_at']=pd.to_datetime(globals() ['recent_df{}'.format(idx+1)]['writed_at']) # writed_at type 변경
#         globals() ['recent_df_dt{}'.format(idx+1)] = globals() ['recent_df{}'.format(idx+1)].set_index('writed_at') # 날짜 데이터를 인덱스로 설정
#         globals() ['recent_df_fn{}'.format(idx+1)]= globals() ['recent_df_dt{}'.format(idx+1)].resample('D').count()['id'].cumsum().to_frame() # 하루별로 세서, 누적
# for idx, video_id in enumerate(high_diff_list): # highview_df1, ,,, highview_df5 생성
#     globals() ['highview_df{}'.format(idx+1)]= comment_by_videoid(video_id)

emotion_chart('eU0b0BgrfsE')
model, device = load_model()
model.eval()
