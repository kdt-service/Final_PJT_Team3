import  mysql.connector
import pandas as pd
from crawling_funcs import *
from extra_funcs import *
import pymysql.cursors
import datetime as dt

# DB 연결s
def init_mysql():
    aws = pymysql.connect(
        database = 'final_project', host = "15.152.250.135", port = 3306, 
        user = 'remote_user',password = 'password' , cursorclass = pymysql.cursors.DictCursor)
    return aws

def excecuteDB(df, table_name):
    aws = init_mysql()
    cur = aws.cursor() # SQL 실행
    
    if table_name == 'channel': # 채널 테이블   
        cols = df.columns[:3]
        log_cols = df.columns[3:]
    
    elif table_name == 'video': # 동영상 테이블
        cols = df.columns[:7]
        log_cols = df.columns[7:]
    
    elif table_name == 'comment': # 동영상 테이블
        cols = df.columns[:6]
        log_cols = df.columns[6:]
        
    # 동영상 크롤링 로그 테이블
    insert_cols = ",".join(cols)
    insert_log_cols = ','.join(log_cols)

    for idx, row in df.iterrows():

        insert_value = ['"'+str(row[col])+'"' for col in cols]
        insert_id = insert_value[0]
        insert_value = ",".join(map(str,insert_value))

        # 채널 , 동영상, 댓글 테이블 
        # 쿼리 설명 : 이미 채널, 동영상, 댓글  테이블에 id가 존재한다면 no action, 존재하지 않는다면 insert
    
        query = f"""INSERT INTO tb_{table_name} ({insert_cols})
                    SELECT {insert_value} FROM DUAL 
                    WHERE NOT EXISTS (SELECT * FROM tb_{table_name} WHERE id = {insert_id}) """
        
        if query != '':
            try : 
                cur.execute(query) # 쿼리추가s
            except : 
                print(row) # content의 내용에 따라 query에 안 들어가기도 함

        # 로그 테이블 
        log_insert_value = ['"'+str(row[log_col])+'"' for log_col in log_cols]
        log_insert_value = ",".join(map(str,log_insert_value))
        log_query = f'INSERT INTO '+ f'tb_{table_name}_log' +'('+ insert_log_cols +') VALUES('+ log_insert_value +');'
        

        if log_query != '':
            try : 
                cur.execute(log_query) # 쿼리추가s
            except : 
                print(row) # content의 내용에 따라 query에 안 들어가기도 함
        
    aws.commit() # 추가한 쿼리 DB에 적용
    aws.close() # 연결 해제

def comment_by_videoid(video_id): # video_id를 인자로 넘겨주면 해당 해당 동영상의 댓글 df 넘겨줘
    aws = init_mysql()
    cur = aws.cursor() # SQL 실행
    query  = f'''select * from tb_comment where video_id = '{video_id}' ; '''
    query = query.replace("\n"," ").replace("\t"," ")
    cur.execute(query)
    recent_result = pd.DataFrame(cur.fetchall())# SQL 실행결과 가져와서 데이터프레임으로 변환
    aws.close()
    return recent_result



def get_data_to_csv(query):
    '''
    +-------------------------+
    | Tables_in_final_project |
    +-------------------------+
    | tb_channel              |
    | tb_channel_log          |
    | tb_comment              |
    | tb_comment_log          |
    | tb_video                |
    | tb_video_log            |
    +-------------------------+
    '''
    sql = init_mysql()
    df = pd.read_sql_query(query, sql)
    sql.close()

    return df

def make_channel_list(df):
    '''
    ---
    parameter : df(tb_channel Data)
    ---
    '''

    def checked_platform(name, channel_lst):
        check_name1 = name + '(유튜브)'
        check_name2 = name + '(틱톡)'

        if (check_name1 in channel_lst) and (check_name2 in channel_lst):
            return True
        else:
            return False
        
    
    names, platform, ids = df['channel_name'].values, df['platform'].values, df['id'].values

    channel_lst = [n + '(' + p + ')' for n, p in zip(names, platform)]
    name_to_id = {n : i for n, i in zip(channel_lst, ids)}
    for n in set(names):
        if checked_platform(n, channel_lst):
            channel_lst.append(n + '('+ '전체' +')')

    

    return channel_lst, name_to_id


def get_channel_list(where = ''):

    sql = init_mysql()
    query = 'select * from tb_channel' + where  
    df = pd.read_sql_query(query, sql)
    sql.close()
    
    return df

    

def get_channel_log_data(target, group_by = False):
    '''
    -----
    parameter : target -> channel_id / group_by -> True or False
    return : tb_channel_log
    -----
    '''
    
    sql = init_mysql()

    if group_by: # 크롤링 한 것 중에서 처음 숫자가 바뀐 시간을 가져오긴 하는데 이 방법은 좋지 않음
        query = f"select * from tb_channel_log where channel_id = '{target}' group by video_count Order by crawled_at desc;"
    else:
        query = f'select * from tb_channel_log where channel_id = {target};'

    df = pd.read_sql_query(query, sql)
    sql.close()

    return df


def get_video_data(target, recent = False, limit = None):
    '''
    ----
    parameter : target -> channel_id
    ----
    '''
    sql = init_mysql()
    query = f"select * from tb_video where channel_id = '{target}'"
    
    if recent:
        query += f' order by uploaded_at desc'
    
    if limit:
        assert type(limit) is int, "limit는 숫자(정수)만 입력 할 수 있습니다. 매개변수 확인해주세요."
        query += f" limit {str(limit)}"

    query += ';'
    df = pd.read_sql_query(query, sql)
    sql.close()

    return df   


def get_video_log_data(target):
    '''
    -----
    parameter : target : video_id
    return : tb_video_log
    -----
    '''
    
    sql = init_mysql()

    query = f"select * from tb_video_log where video_id = '{target}' Order by crawled_at desc;"
    
    df = pd.read_sql_query(query, sql)
    sql.close()

    return df

def get_comment_data(target):
    ''''
    ----
    parameter : target : video_id
    ----
    '''
    sql = init_mysql()

    query = f"select * from tb_comment where video_id = '{target}';"

    df = pd.read_sql_query(query, sql)
    sql.close()

    return df


def get_comment_log_data(target):
    '''
    -----
    return : tb_video_log
    -----
    '''
    
    sql = init_mysql()

    query = f"select * from tb_video_log where video_id = '{target}' Order by crawled_at desc;"
    
    df = pd.read_sql_query(query, sql)
    sql.close()

    return df


def get_tiktok_views(name):
    
    sql = init_mysql()
    query = f"select total_view_count from tb_channel_log where channel_id = '{name}' order by crawled_at desc limit 1;"
    total_views = pd.read_sql_query(query, sql)['total_view_count'].iloc[0]
    sql.close()
    
    return total_views if total_views else 0

def today_comment_crawl(videoid):
    now = dt.datetime.now()
    # 해당 영상의 log 테이블이 오늘 크롤링한 기록이 있으면 하고, 아니면 넘어간다. 
    sql = init_mysql()
    query = f"select comment_id, max(crawled_at) as crawled_at from tb_comment_log where comment_id in (select id from tb_comment where video_id = '{videoid}') group by comment_id;"
    if len(pd.read_sql_query(query, sql)['crawled_at']) == 0 : # 새로운 비디오 
        result = True

    else :
        last_crawl = pd.read_sql_query(query, sql)['crawled_at'].iloc[0] #2023-06-17 12:23:02
        last_crawl = dt.datetime.strptime(str(last_crawl), '%Y-%m-%d %H:%M:%S') # datetime type으로 변경
        sql.close()
    
        result = False # 기본으로 default인데 
        if last_crawl.day == now.day : #날짜가 같아
            if last_crawl.hour <6 & last_crawl.hour < now.hour : # 마지막으로 크롤링 된게 새벽이고, 마지막 크롤잉이 오늘보다 beofre
                result = True
        elif last_crawl.day < now.day: #제일 최신 크롤링 날짜가 오늘보다 before. Then, Crawl! 
            result = True 
    print(result)
    return result

#부정어 사전 단어 등록 함수
def register_block_word(word, channel_title):
    aws = init_mysql()
    cur = aws.cursor() # SQL 실행
    query = f"""insert into tb_block_words (word, channel_title) select '{word}','{channel_title}' from dual
  WHERE NOT EXISTS (SELECT channel_title, word FROM tb_block_words WHERE channel_title = '{channel_title}' and word = '{word}')     ;
    ;"""
    query = query.replace("\n"," ").replace("\t"," ")
    if query != '':
                try : 
                    cur.execute(query) # 쿼리추가s
                    result = True
                except : 
                    print(query) # content의 내용에 따라 query에 안 들어가기도 함
                    result = False
    aws.commit() # 추가한 쿼리 DB에 적용
    aws.close() # 연결 해제
    return result

#부정어 사전 단어 제거 함수
def delete_block_word(word, channel_title):
    aws = init_mysql()
    cur = aws.cursor() # SQL 실행
    query = f"DELETE FROM tb_block_words where channel_title = '{channel_title}' and word = '{word}';"
    if query != '':
                try : 
                    cur.execute(query) # 쿼리추가s
                    result = True
                except : 
                    print(query) 
                    result = False # content의 내용에 따라 query에 안 들어가기도 함
    aws.commit() # 추가한 쿼리 DB에 적용
    aws.close() # 연결 해제
    return result

# 부정어 사전 단어 목록 반환 함수
def get_block_wordlist(channel_title):
    sql = init_mysql()
    query = f"SELECT * FROM tb_block_words where channel_title = '{channel_title}';"
    word_list= pd.read_sql_query(query, sql)['word'].to_list()
    sql.close()
    return word_list

def channel_name_to_id(channel_title):
    #재밌는 거 올라온다
    sql = init_mysql()
    query = f"select * from tb_channel where channel_name = '{channel_title}' ;" 
    id = pd.read_sql_query(query, sql)['id'][0]
    sql.close()
    return id

#해당 부정어가 포함된 댓글들 가져오기
def get_comments_with_word(channel_title, word):
    sql= init_mysql()
    channel_id = channel_name_to_id(channel_title)
    query =  "SELECT * FROM tb_comment WHERE video_id in (select id from tb_video where channel_id = '{channel_id}' ) and content LIKE '%{word}%' ;"
    df=pd.read_sql_query(query, sql)
    sql.close()
    result = df['id'].to_list()
    return result

def get_comment_log_data(df):
    #현재 데이터들의 id값을 갖고 있는 tb_comment_log 데이터들을 가져와서,
    #  그중에서 제일 최신 데이터 (로그 값들은 계속 변하니까) 를 반환
    temp = df['id'].to_list()
    temp= str(temp).replace('[','').replace(']','')
    sql = init_mysql()
    query = f'''select comment_id, like_count, max(crawled_at) as crawled_at from tb_comment_log where  comment_id in
    ({temp}) group by comment_id;'''
    query= query.replace("\n"," ").replace("\t"," ")
    df=pd.read_sql_query(query, sql)
    sql.close()
    return df