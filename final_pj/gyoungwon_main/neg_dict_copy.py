from mecab import MeCab
from konlpy.tag import Okt
from collections import Counter

from db_connect import *
from recent_highview_list import get_old_highcom_video
from custom_statics import get_video_list


#영상 댓글 받아오기 / 전시간 대비 댓글 변화가 가장 큰 댓글(high_diff_comments) vs 채널 영상 목록 중에서 가장 오래된 영상의 댓글(oldest_video_comments)
def negdict_get_comment(channel_id):
    result_df = get_video_list(channel_id) # 채널 id 넘겨받고
    oldest_videoid, high_diff_videoid=get_old_highcom_video(channel_id,result_df) # 제일 오래된 동영상 ID, 댓글수 차이 높은 video id가져오기
    oldest_video_comments = get_comment_data(oldest_videoid)[['id','video_id','content']]
    high_diff_comments = get_comment_data(high_diff_videoid)[['id','video_id','content']]
    return oldest_video_comments, high_diff_comments


def mecab_pos(df): #명사 추출, 불용어 제거해서 빈도수 계산 후 정렬
    mecab = MeCab()
    with open('/home/ubuntu/final_pj/gyoungwon_main/STOPWORD.txt', 'r') as f:
        stop_words = f.read().splitlines()

    with open('/home/ubuntu/final_pj/gyoungwon_main/EOMI.TXT', 'r') as f:
        eomi = f.read().splitlines()

    with open('/home/ubuntu/final_pj/gyoungwon_main/JOSA.TXT', 'r') as f:
        josa = f.read().splitlines()

    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    result = [] #형태소 분석으로 추출된 명사 넣을 리스트

    df['mecab_pos'] = ''
    for i, row in enumerate(df['processed_content']):
        if df['sentiment'][i] == 'neg': #neg로 분류된 댓글 명사만 추출 후 'mecab_pos'열에 할당
            nouns = mecab.nouns(row)
            filtered_nouns = []
            for noun in nouns:
                if noun not in stop_words and noun not in CHOSUNG_LIST and noun not in eomi and noun not in josa:
                    filtered_nouns.append(noun)
                    
            df.at[i, 'mecab_pos'] = filtered_nouns
            result.extend(filtered_nouns)

    word_counts = Counter(result)
    sorted_items = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return df, sorted_items


def mecab_diff_set(popular_mecab_nouns, unpopular_mecab_nouns):
    mecab = MeCab()
    popular_mecab_noun = [tup[0] for tup in popular_mecab_nouns]
    unpopular_mecab_noun = [tup[0] for tup in unpopular_mecab_nouns]
    set1 =set(popular_mecab_noun)
    set2 = set(unpopular_mecab_noun)
    diff = set1.difference(set2) # 'popular_mecab_noun - unpopular_mecab_noun'의 차집합
    diff_with_counts = [(value[0], value[1]) for value in popular_mecab_nouns if value[0] in diff] #diff에서 뽑힌 값과 popular_mecab_nouns 첫번째 값 비교해서 일치하면 빈도수 같이 가져오기
    mecab_list=diff_with_counts[:150] #상위 150개까지만 짜르기
    mecab_neg_list = []

    for word in mecab_list:
        if mecab.pos(word[0])[0][1] == 'NNG':
            if len(word[0])>=2:
                mecab_neg_list.append(word)

    return mecab_neg_list


def okt_pos(df):
    okt = Okt() 
    with open('/home/ubuntu/final_pj/gyoungwon_main/STOPWORD.txt', 'r') as f: 
        stop_words = f.read().splitlines()

    with open('/home/ubuntu/final_pj/gyoungwon_main/EOMI.TXT', 'r') as f:
        eomi = f.read().splitlines()

    with open('/home/ubuntu/final_pj/gyoungwon_main/JOSA.TXT', 'r') as f:
        josa = f.read().splitlines()

    CHOSUNG_LIST = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
    result = []

    df['okt_pos'] = ''
    for i, row in enumerate(df['processed_content']):
        if df['sentiment'][i] == 'neg':
            nouns = okt.nouns(row)
            filtered_nouns = []
            for noun in nouns:
                if noun not in stop_words and noun not in CHOSUNG_LIST and noun not in eomi and noun not in josa:
                    filtered_nouns.append(noun)

            df.at[i, 'okt_pos'] = filtered_nouns
            result.extend(filtered_nouns)

    word_counts = Counter(result)
    sorted_items = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return df, sorted_items

def okt_diff_set(popular_okt_nouns, unpopular_okt_nouns):
    okt = Okt() 
    popular_okt_noun = [tup[0] for tup in popular_okt_nouns]
    unpopular_okt_noun = [tup[0] for tup in unpopular_okt_nouns]
    set1 =set(popular_okt_noun)
    set2 = set(unpopular_okt_noun)
    diff = set1.difference(set2) # 'popular_Okt_noun - unpopular_Okt_noun'의 차집합
    diff_with_counts = [(value[0], value[1]) for value in popular_okt_nouns if value[0] in diff] #diff에서 뽑힌 값과 popular_okt_nouns 첫번째 값 비교해서 일치하면 빈도수 같이 가져오기
    okt_list=diff_with_counts[:150] #상위 150개까지만 짜르기
    okt_neg_list = []

    for word in okt_list:
        if len(word[0])>=2:
            okt_neg_list.append(word)

    return okt_neg_list

def mecab_okt_intersection(mecab_neg_list, okt_neg_list):
    mecab_word_list = [tup[0] for tup in mecab_neg_list]
    okt_word_list = [tup[0] for tup in okt_neg_list]
    mecab_set= set(mecab_word_list)
    okt_set = set(okt_word_list)
    meokt_inter_set = mecab_set.intersection(okt_set) #mecab과 okt에서 추출된 일반 명사(nng)의 교집합
    meokt_with_counts = [(value[0], value[1]) for value in mecab_neg_list if value[0] in meokt_inter_set and value[1] >= 10] #빈도수 10개 이상인 것만 추출
    return meokt_with_counts #빈도수는 mecab 기준


#부정어 사전 후보로 뽑힌 명사가 들어있는 댓글 가져오기 
def get_negdict_comment(meokt_with_counts, popular_mecab_df): #딕셔너리 형식으로 부정어 후보와 해당 댓글 짝지어짐
    words = [tup[0] for tup in meokt_with_counts]
    comment_list = {} 
    for word in words: 
        filtered_rows = popular_mecab_df[popular_mecab_df['mecab_pos'].apply(lambda x: word in x)]
        comments = filtered_rows['processed_content'].tolist()
        comment_list[word] = comments
    return comment_list