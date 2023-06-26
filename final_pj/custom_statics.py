import pandas as pd
import numpy as np
from db_connect import *

def make_line_df(video_lst, id_to_name, view_type = '조회수'):
    '''
    ---
    view_type : Base - 조회수
    [조회수, 좋아요, 댓글]
    ---
    '''

    result = pd.DataFrame()
    query = "select * from tb_video_log where video_id = "

    df_lst = []
    sql = init_mysql()
    for v_id in video_lst:
        # print(v_id)
        f_query = query + "'" + v_id + "'" + ';'
        df_lst.append(pd.read_sql_query(f_query, sql))

    sql.close()
    df = pd.concat(df_lst)
    df['crawled_at'] = [pd.to_datetime(t).strftime('%Y-%m-%d %H:00:00') for t in df['crawled_at']]


    df.drop_duplicates(subset=['video_id', 'crawled_at'], inplace=True)

    time_index = df['crawled_at'].unique()
    cols = df['video_id'].unique()

    if view_type =='조회수':
        target_type = 'view_count'
    elif view_type == '좋아요':
        target_type = 'like_count'
    elif view_type == '댓글':
        target_type = 'comment_count'

    target_values = [df[df['video_id'] == id][target_type].values for id in cols]

    cols = [id_to_name[str(n)] for n in cols]

    for i in range(len(cols)):
        result = pd.concat([result, pd.DataFrame({cols[i] : target_values[i]}, index = [idx for idx in time_index[:len(target_values[i])]])], axis=1)
    

    return result


def filter_top_limit(df_lst, top_limit = 5):

    result_idx = []
    result_idx = sorted(range(len(df_lst)),key= lambda i: df_lst[i])[::-1]

    return result_idx[:top_limit]


def make_viewDiff(df):
  cols = df.columns

  result = []

  for col in cols:
    tmp = []
    data = df[col]
    for i in range(len(data)-1,0,-1):
      if not pd.isna(data[i]) and not pd.isna(data[i-1]):
        tmp.append(data[i] - data[i-1])
      else:
        tmp.append(0)
    result.append(tmp[::-1])
  return result
    
def make_line_df_topVideo(video_lst, id_to_name):
    result = pd.DataFrame()

    query = "select * from tb_video_log where video_id = "

    df_lst = []
    df_lst_resample = []

    video_viewDiff = []
    sql = init_mysql()
    for idx, v_id in enumerate(video_lst):
        # print(v_id)
        f_query = query + "'" + v_id + "'" + ' order by crawled_at;'
        tmp = (pd.read_sql_query(f_query, sql))
        if idx == 0 : print(f_query)
        time_df = tmp.set_index('crawled_at')[['view_count']].resample('4H').max()[-4:]
        view_diff = time_df[-2:]['view_count'].values[1] - time_df[-2:]['view_count'].values[0]
        video_viewDiff.append(view_diff)
        df_lst.append(time_df)
        df_lst_resample.append(time_df)

    sql.close()

    idxs = filter_top_limit(video_viewDiff)

    top_df = [df_lst[idx] for idx in idxs]
    top_df_resample = [df_lst_resample[idx] for idx in idxs]

    df = pd.concat(top_df, axis=1)
    df_resample = pd.concat(top_df_resample , axis=1)

    df.columns = [id_to_name[video_lst[idx]] for idx in idxs]
    df_resample.columns = [id_to_name[video_lst[idx]] for idx in idxs]

    # test = df_resample.iloc[1:]
    # print(video_viewDiff)
    test = pd.DataFrame(np.array(make_viewDiff(df_resample)).transpose(), columns = df_resample.columns, index=df_resample.iloc[1:].index)

    return test

# 채널 ID 넘겨주면 video_list 갖고온다
def get_video_list(channel_id):
   query = "select * from tb_video where channel_id = "+'"'+channel_id+'"'+";"
   sql = init_mysql()
   result = pd.read_sql_query(query, sql)
   result = result.sort_values('uploaded_at', ascending=False) # 최신순으로 넘기기
   return result 



def title_to_id(name):
    query = "select id from tb_video where title = "+'"'+name+'"'+";"
    sql = init_mysql()
    df = pd.read_sql_query(query, sql)
    result = df['id'][0]
    return result


def compare_df(channel_lst):

    df = pd.DataFrame()

    # video_id, channel_id, view, like, comment, platform
    # query = 'select tv.id video_id, tv.title title, tv.channel_id, max(tvl.view_count) views, max(tvl.like_count) likes, max(tvl.comment_count) comments, tc.platform, tv.uploaded_at upload_time, tc.channel_name channel, max(tcl.subscriber) subscriber from tb_video tv join tb_channel tc on tv.channel_id = tc.id join tb_video_log tvl on tv.id = tvl.video_id join tb_channel_log tcl on tc.id = tcl.channel_id where tv.channel_id = '
    query = 'select tv.id video_id, tv.title title, tv.channel_id, max(tvl.view_count) views, max(tvl.like_count) likes, max(tvl.comment_count) comments, tc.platform, tv.uploaded_at upload_time, tc.channel_name channel, tv.hashtag from tb_video tv join tb_channel tc on tv.channel_id = tc.id join tb_video_log tvl on tv.id = tvl.video_id where tv.channel_id = '
    query2 = 'group by video_id;'

    for channel in channel_lst:
        tmp = get_data_to_csv(query + "'" +channel + "'" + query2)     
        tmp     
        df = pd.concat([df, tmp])

    return df


def daily_compare_df(channel_lst, i, is_compare=True):
    df = pd.DataFrame()
 
    recent_query = 'select tv.id, tv.uploaded_at, max(tvl.view_count) views from tb_video tv join tb_video_log tvl on tv.id = tvl.video_id where channel_id =  '
    recent_ids = []

    for channel in channel_lst:
        tmp = get_data_to_csv(recent_query + "'" + channel + "'" + 'group by tv.id order by uploaded_at desc limit 5;')

        if len(tmp) < i : i = 0
        
        if is_compare:
            recent_ids.append(tmp.sort_values(['views']).iloc[i]['id'])
        else:
            recent_ids.append(tmp.iloc[i]['id'])

    # recent_ids = tmp['id'].unique()
    #video_id, channel_id, view, like, comment, platform
    query = 'select tv.id video_id, tv.title title, tv.channel_id, (tvl.view_count) views, (tvl.like_count) likes, (tvl.comment_count) comments, tv.uploaded_at, tc.platform, tc.channel_name, tvl.crawled_at time from tb_video tv join tb_channel tc on tv.channel_id = tc.id join tb_video_log tvl on tv.id = tvl.video_id  where tvl.video_id = '
    query2 = ';'

    for v_id in recent_ids:
        tmp = get_data_to_csv(query + "'" + v_id + "'" + query2)        
        df = pd.concat([df, tmp])

    return df

def daily_compare2(channel_lst):
    df = pd.DataFrame()
 
    recent_query = 'select tv.id, tv.uploaded_at, max(tvl.view_count) views from tb_video tv join tb_video_log tvl on tv.id = tvl.video_id where channel_id =  '
    recent_ids = []

    for channel in channel_lst:
        tmp = get_data_to_csv(recent_query + "'" + channel + "'" + 'group by tv.id order by uploaded_at desc limit 5;')
        for ids in tmp['id'].unique():
            recent_ids.append(ids)
                
    #video_id, channel_id, view, like, comment, platform
    query = 'select tv.id video_id, tv.title title, tv.channel_id, (tvl.view_count) views, (tvl.like_count) likes, (tvl.comment_count) comments, tv.uploaded_at, tc.platform, tc.channel_name, tvl.crawled_at time from tb_video tv join tb_channel tc on tv.channel_id = tc.id join tb_video_log tvl on tv.id = tvl.video_id     where tvl.video_id = '
    query2 = ';'

    for v_id in recent_ids:
        tmp = get_data_to_csv(query + "'" + v_id + "'" + query2)        
        df = pd.concat([df, tmp])

    return df

def mertic_number(num):

    # print(num)
    is_minus = True if num < 0 else False

    # B
    if abs(num) // 1000000000:
        # print(num)
        
        result = round((abs(num) / 1000000000),2)

        if is_minus:
            result = str(0 - result)

        result = str(result) + 'B'
    # M
    elif abs(num) // 1000000:
        result  =  round((abs(num) / 1000000),2)

        if is_minus:
            result = str(0 - result)

        result = str(result) + 'M'
    
    elif abs(num) // 1000:
        result = round((abs(num) /  1000),2)

        if is_minus:
            result = str(0 - result)

        result = str(result) + 'K'
    else:
        result =  str(num)

    return result    
        