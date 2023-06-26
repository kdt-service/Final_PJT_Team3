# import sys
# sys.path.append('/home/ubuntu/final_pj') # 같은 선상에 있는 파일이 아니기 때문에
# from crawling_funcs import *
# from extra_funcs import *
# from db_connect import * 
# from video_list import *
# from recent_highview_list import * 

# 여기서 사용 안하는 패키지들이라 주석 처리했습니다.

import pandas as pd
import re
import emoji #ec2 설치완료
from soynlp.normalizer import *
import langid #ec2 설치완료
import plotly.express as px

# 전처리 함수
def preprocessing(df):

    def process_text(text):
        result = re.sub('(?=\<a).+(?<=a>)', '' , text) # a태그 제거
        result = re.sub('(?=\<b).+(?<=b>)', '' , text) # b태그 제거
        result = re.sub('(<br>)+', '' , result) # <br>태그 제거
        result = re.sub('[\n\t]', ' ', result) # 줄바꿈, 텝 -> 띄어쓰기로 대체
        result = re.sub('(&quot;)', '' , result) # &quot; 제거
        result = re.sub(r'@[^ ]*', '', result) # 답댓글시 @닉네임 제거
        
        result = emoticon_normalize(result, num_repeats=2)  # 이모지, 특수문자 정규화
        result = repeat_normalize(result, num_repeats=2)
        
        return result.strip()

    #df = pd.read_csv(file_path) # 파일 위치 읽기
    df.dropna(inplace=True) # nan value 있는 행 제거
    df.drop_duplicates(inplace=True) #중복 행 제거 
    df = df[df['content'].str.len() > 1] # 댓글 길이가 한 글자면 제거
    df['processed_content'] = df['content'].apply(process_text)
    
    emoji_text = ''.join(set(list(emoji.EMOJI_DATA.keys()))) # 이모지 데이터

    #♥ ♡ .!,? 제외한 특수문자와 일반문자 수 비교 후 특수문자 더 많을 시 해당 댓글 제거
    indices_to_drop = []  # 제거할 데이터의 인덱스를 저장할 리스트
    
    for i, content in enumerate(df['processed_content']):
        normal_text = len(re.findall(f'[\w\s\{emoji_text}\♥ ♡ .!,?]', content))
        special_text = len(re.findall(f'[^\w\s\{emoji_text}\♥ ♡ .!,?]', content))

        if normal_text >= special_text:
            pass
        else:
            indices_to_drop.append(i)

    df = df.drop(indices_to_drop).reset_index(drop=True)

    #emoji, 특수문자로 구성된 댓글 etc로 필터링(추후에 kcelectra 감성 분류)
    for i, content in enumerate(df['processed_content']):
        if re.search(rf'^(?:[^\w\s]|{emoji_text})+$', content):
            df.loc[i, 'lang'] = 'etc'
            
    # 언어 판별 모듈 정확도 높이기 위하여 emoji, 특수문자 제거 후 언어판별용 칼럼인 for_langid에 할당
    df['for_langid'] = df['processed_content'].apply(lambda x: re.sub(rf'([^\w\s]|{emoji_text})', '', x))

    return df


# 언어 분류 함수
def identify_lang(df):
    df['lang'] = df.apply(lambda row: langid.classify(row['for_langid'])[0], axis=1) #langid 사용하여 댓글 언어 판별 

    # 따로 처리하겠음
    # df = df[df['lang'].isin(['en', 'ko', 'etc'])] # lang에 en, ko, etc 가 아닌 행은 다 삭제하기
    df = df.drop('for_langid', axis=1) #for_langid 삭제

    #알파벳, 한글 수 비교 후 한글이 더 많으면 ko, 영어가 더 많으면 en로 재분류
    for i, content in df[df['lang'].isin(['en', 'ko'])]['processed_content'].items():
        kor_text = len(re.findall('[ㄱ-ㅎ가-힣ㅏ-ㅣ]', content))
        eng_text = len(re.findall('[A-Za-z]', content))
    
        if kor_text >= eng_text:
            df.loc[i, 'lang'] = 'ko'
        else:
            df.loc[i, 'lang'] = 'en'

    for i, content in df[df['lang'].isin(['ja'])]['processed_content'].items():
       # 일본어로 분류된 댓글들 (ㅋㅋㅋㅋ, ㅇㅈ 으로 구성된 댓글 많음) 한국어로 재분류 
        kor_text = len(re.findall('[ㄱ-ㅎ가-힣ㅏ-ㅣ]', content))
        eng_text = len(re.findall('[A-Za-z]', content))
        jap_text = len(re.findall('[ぁ-ゔ]+|[ァ-ヴー]+[々〆〤]', content))
        text = len(content)
        if kor_text >= text*0.5: # 절반이상이 한글이면 
            df.loc[i, 'lang'] = 'ko'
          
        if jap_text == 0 : # 일본어가 없어 (영어, 한글 섞여 있는 경우 존재)
          if kor_text >= eng_text:
            df.loc[i, 'lang'] = 'ko'
          else:
            df.loc[i, 'lang'] = 'en'

    for i, content in df[df['lang'].isin(['zh'])]['processed_content'].items(): # 중국어로 분류된 댓글 중에서 한글 찾기
        kor_text = len(re.findall('[ㄱ-ㅎ가-힣ㅏ-ㅣ]', content))
        text = len(content)
        if kor_text >= text*0.5: # 절반이상이 한글이면 
            df.loc[i, 'lang'] = 'ko'
            
    for i in range(len(df)): #emoji-> 한글 변환
        if df.loc[i,'lang']=='ko':
            temp = df.loc[i,'processed_content']
            demoji_text = emoji.demojize(temp, language = 'ko')
            demoji_list = {"♡" : "하트", "🫶🏻" : "하트",  "🫰🏻" : "하트", "🫶🏽": "하트"} #emoji.demojize가 처리해주지 못하는 이모지 추가 처리
             
            for emoji_code, emoji_kor in demoji_list.items():
                demoji_text = demoji_text.replace(emoji_code, emoji_kor) 
            
            df.loc[i, 'demoji_text']=demoji_text

    return df


