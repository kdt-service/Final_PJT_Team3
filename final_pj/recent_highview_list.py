from crawling_funcs import *
from custom_statics import *
from extra_funcs import *
from db_connect import * 
from video_list import *
import pandas as pd
import re 
import pandas as pd

def recent_highview_func(num, id_text,df):
    VIDEO_NUM = num # 비디오 개수 설정
    WANT_CHANNEL_ID = id_text
   
    list_df = df

    # 모든 동영상 ID 목록 가져오기
    every_video_list = list_df['id']
    # 최신 동영상 5개 video_id 가져오기
    recent_top_list = list_df['id'][:VIDEO_NUM].to_list()

    # # 조회수 차이 많이 나는 video_id 가져오기
    # 1. DB에서 제일 최신기준으로 tb_video_log들 가져오기
    aws = init_mysql()
    cur = aws.cursor() # SQL 실행
    recent_query = f'''
    select * from tb_video_log where (video_id, crawled_at)
    in ( select video_id, max(crawled_at) as crawled_at 
    from tb_video_log  where video_id in (select id from tb_video where channel_id = '{WANT_CHANNEL_ID}'
    ) group by video_id); '''

    recent_query = recent_query.replace("\n"," ").replace("\t"," ")
    cur.execute(recent_query)
    recent_result = pd.DataFrame(cur.fetchall())# SQL 실행결과 가져와서 데이터프레임으로 변환
    aws.close()


    #2. DB에서 두번째 최신기준으로 tb_video_log들 가져오기 #두번째가 없는 경우에는 Empty 
    aws = init_mysql()
    cur = aws.cursor()
    second_query = f'''SELECT * FROM tb_video_log k
    WHERE 2 = (SELECT COUNT( DISTINCT crawled_at) FROM tb_video_log u 
            WHERE k.crawled_at <= u.crawled_at AND k.video_id = u.video_id
            AND u.video_id in (select id from tb_video where channel_id = '{WANT_CHANNEL_ID}'
    )                    GROUP BY u.video_id) ;'''

    cur.execute(second_query)
    second_result = pd.DataFrame(cur.fetchall())# SQL 실행결과 가져와서 데이터프레임으로 변환
    aws.close()


    # 2-1. recent와 second의 교집합에서 조회수 차이 비교하기
    new_df = pd.merge(recent_result, second_result, on= ['video_id'])
    new_df['view_count_diff']= new_df['view_count_x']-new_df['view_count_y']
    new_df= new_df[['video_id', 'view_count_diff']].sort_values('view_count_diff' ,  ascending=False) # 조회수 차이 큰 것대로 정렬 완료! 
    
    high_diff_list = new_df['video_id'][:VIDEO_NUM].to_list()

    return recent_top_list, high_diff_list

def recent_top_list_info(recent_top_list):
    info_query = f"SELECT * from tb_video where id  in ('{recent_top_list[0]}','{recent_top_list[1]}' , '{recent_top_list[2]}', '{recent_top_list[3]}' , '{recent_top_list[4]}') order by uploaded_at desc;"
    df = pd.read_sql_query(info_query,init_mysql())
    info_log_query = f'''select * from tb_video_log where (video_id, crawled_at) in ( select video_id, max(crawled_at) as crawled_at 
        from tb_video_log  where video_id in ('{recent_top_list[0]}','{recent_top_list[1]}' , '{recent_top_list[2]}', '{recent_top_list[3]}' , '{recent_top_list[4]}')
        group by video_id);''' # 제일 최신 log
    info_log_query = info_log_query.replace("\n"," ").replace("\t"," ")
    log_df = pd.read_sql_query(info_log_query,init_mysql()).set_index('video_id', drop= True)   # viw_count, like_count, comment_count 
    return df, log_df

def high_diff_list_info(high_diff_list):
   info_query = f"SELECT * from tb_video where id in ('{ high_diff_list[0]}','{ high_diff_list[1]}' , '{ high_diff_list[2]}', '{ high_diff_list[3]}' , '{ high_diff_list[4]}');"
   df = pd.read_sql_query(info_query,init_mysql())
   info_log_query = f'''select * from tb_video_log where (video_id, crawled_at) in ( select video_id, max(crawled_at) as crawled_at 
                from tb_video_log  where video_id in ('{high_diff_list[0]}','{high_diff_list[1]}' , '{high_diff_list[2]}', '{high_diff_list[3]}' , '{high_diff_list[4]}')
                group by video_id);''' # 제일 최신 log
   info_log_query = info_log_query.replace("\n"," ").replace("\t"," ")
   log_df = pd.read_sql_query(info_log_query,init_mysql()) # viw_count, like_count, comment_count 
   return df, log_df


# 제일 오래된 동영상 ID와, 댓글 수 차이가 가장 많이 나는 동영상 ID 제공해주는 함수
def get_old_highcom_video(id_text,df): 
    
    WANT_CHANNEL_ID= id_text
    list_df = df
    # 모든 동영상 ID 목록 가져오기
    every_video_list = list_df['id']
    
    # 가장 오래된 동영상 ID
    oldest_videoid = list_df.reset_index()['id'][len(list_df)-1]

    # # 댓글 수 차이 많이 나는 video_id 가져오기
    # 1. DB에서 제일 최신기준으로 tb_video_log들 가져오기
    aws = init_mysql()
    cur = aws.cursor() # SQL 실행
    recent_query = f'''
    select * from tb_video_log where (video_id, crawled_at)
    in ( select video_id, max(crawled_at) as crawled_at 
    from tb_video_log  where video_id in (select id from tb_video where channel_id = '{WANT_CHANNEL_ID}'
    ) group by video_id); '''

    recent_query = recent_query.replace("\n"," ").replace("\t"," ")
    cur.execute(recent_query)
    recent_result = pd.DataFrame(cur.fetchall())# SQL 실행결과 가져와서 데이터프레임으로 변환
    aws.close()


    #2. DB에서 두번째 최신기준으로 tb_video_log들 가져오기 #두번째가 없는 경우에는 Empty 
    aws = init_mysql()
    cur = aws.cursor()
    second_query = f'''SELECT * FROM tb_video_log k
    WHERE 2 = (SELECT COUNT( DISTINCT crawled_at) FROM tb_video_log u 
            WHERE k.crawled_at <= u.crawled_at AND k.video_id = u.video_id
            AND u.video_id in (select id from tb_video where channel_id = '{WANT_CHANNEL_ID}'
    )                    GROUP BY u.video_id) ;'''

    cur.execute(second_query)
    second_result = pd.DataFrame(cur.fetchall())# SQL 실행결과 가져와서 데이터프레임으로 변환
    aws.close()


    # 2-1. recent와 second의 교집합에서 조회수 차이 비교하기
    new_df = pd.merge(recent_result, second_result, on= ['video_id'])
    
    new_df['comment_diff']= new_df['comment_count_x']-new_df['comment_count_y']
    
    new_df= new_df[['video_id', 'comment_diff']].sort_values('comment_diff' ,  ascending=False) # 조회수 차이 큰 것대로 정렬 완료! 
    
    high_diff_videoid = new_df.iloc[0]['video_id']
    return oldest_videoid, high_diff_videoid

if __name__ == "__main__":
    channel_id = 'UC4ZA57iJrf73bJlApKFeLRw'
    result_df = get_video_list(channel_id) # 채널 id 넘겨받고 
   
    oldest_videoid, high_diff_videoid=get_old_highcom_video(channel_id,result_df)
    print(oldest_videoid, high_diff_videoid)
    oldest_video_comments = get_comment_data(oldest_videoid)[['id','video_id','content']]
    high_diff_comments = get_comment_data(high_diff_videoid)[['id','video_id','content']]
