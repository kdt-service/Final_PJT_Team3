from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer as new_vader
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
from gyoungwon_main.preprocess_lang import * 
import sys
sys.path.append('/home/ubuntu/final_pj') # 같은 선상에 있는 파일이 아니기 때문에
from crawling_funcs import *
from extra_funcs import *
from db_connect import * 
from video_list import *
from recent_highview_list import * 
import pandas as pd
from datetime import datetime, timedelta 
import plotly.graph_objects as go

# 영어 감성 분류
def analyze_english_sentiment(comment): #영어 댓글 감성 분석 처리 
    new_c_a = new_vader()
    content_sentiment = new_c_a.polarity_scores(comment) #감성점수(neg, neu, pos, compound) 계산
    compound = content_sentiment['compound'] #compound 점수 가져오기
    
    #추출된 감성 점수로 감성 분류 
    if compound <= -0.05: 
        result =  'neg'  
    else:
        result =  'pos'
    return result 

# 한국어 감성 분류
def load_model():
    device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu') 
    model = AutoModelForSequenceClassification.from_pretrained("beomi/KcELECTRA-base-v2022")
    model.load_state_dict(torch.load("/home/ubuntu/final_pj/gyoungwon_main/pytorch_model_0615.bin", map_location=device))
    tokenizer = AutoTokenizer.from_pretrained("beomi/KcELECTRA-base-v2022")
    model.to(device)  # 모델 gpu로 전송
    return model, device, tokenizer

def analyze_korean_sentiment(sent,model,device, tokenizer):

    sent = str(sent)
    model.eval()

    tokenized_sent = tokenizer(
    sent,
    return_tensors = 'pt',
    truncation = True ,
    add_special_tokens = True,
    max_length = 128)

    tokenized_sent.to(device)

    with torch.no_grad():
        outputs = model(input_ids = tokenized_sent['input_ids'],
                    attention_mask = tokenized_sent['attention_mask'],
                    token_type_ids = tokenized_sent ['token_type_ids']
                    )

    logits = outputs[0]
    logits = logits.detach().cpu()
    result = logits.argmax(-1)

    if result == 0:
        result = "neg"
    elif result ==1 :
        result = 'pos'
    return result

#댓글별 감성 분석(pie_chart 생성)        
def emotion_all(video_id):
    df = comment_by_videoid(video_id)
    df1 = preprocessing(df)
    df2 = identify_lang(df1)
    df2 = df2[df2['lang'].isin(['en', 'ko'])] # lang에 en, ko 가 아닌 행은 다 삭제하기
    df2['sentiment'] = df2[df2['lang']=='en']['processed_content'].apply(analyze_english_sentiment)
    model, device, tokenizer = load_model()    
    # 시간 오래걸리는 부분!
    df2.loc[df2['lang'] == 'ko', 'sentiment'] = df2[df2['lang'] == 'ko']['demoji_text'].apply(analyze_korean_sentiment, args = (model, device,tokenizer)) 
    # 영어 댓글 감성분석 파이 차트
    eng_sentiment_chart = px.pie(df2[df2['lang'] == 'en'], 
                                values=[len(df2[(df2['lang'] == 'en') & (df2['sentiment'] == 'pos')]),
                                        len(df2[(df2['lang'] == 'en') & (df2['sentiment'] == 'neg')])], 
                                names=['긍정/중립', '부정'], 
                                title='영어 댓글 감성 분석', 
                                color=['긍정/중립', '부정'],
                                color_discrete_map={'긍정/중립': 'royalblue', '부정': 'indianred'})

    # 한국어 댓글 감성분석 파이 차트
    kor_sentiment_chart = px.pie(df2[df2['lang'] == 'ko'], 
                                values=[len(df2[(df2['lang'] == 'ko') & (df2['sentiment'] == 'pos')]),
                                        len(df2[(df2['lang'] == 'ko') & (df2['sentiment'] == 'neg')])], 
                                names=['긍정/중립', '부정'], 
                                title='한국어 댓글 감성 분석',
                                color=['긍정/중립', '부정'],
                                color_discrete_map={'긍정/중립': 'royalblue', '부정': 'indianred'}) 
    
    #언어/감성별 좋아요수 많은 대표 댓글(3개) 가져오기
    log_df = get_comment_log_data(df2) # DB 활용해서 로그데이터 (like_count) 데이터 가져오기 
    new_df = pd.merge(df2, log_df, left_on='id', right_on='comment_id') # comment_id를 공통으로 df, log_df 합치기
    
    ko_pos = new_df.loc[(new_df['lang'] == 'ko') & (new_df['sentiment'] == 'pos'), ['processed_content', 'writer', 'like_count']].sort_values('like_count', ascending=False).head(3)
    ko_neg = new_df.loc[(new_df['lang'] == 'ko') & (new_df['sentiment'] == 'neg'), ['processed_content', 'writer', 'like_count']].sort_values('like_count', ascending=False).head(3)
    
    #날짜별 감성분석 변화 바 그래프
    dates = df2['writed_at'].tolist()
    dates = sorted(list(set(dates)))
    pos_count = [] 
    neg_count = [] 

    for date in dates: 
        pos = len(df2[(df2['sentiment'] == 'pos') & (df2['writed_at'] == date)])
        pos_count.append(pos)
        
        neg = len(df2[(df2['sentiment'] == 'neg') & (df2['writed_at'] == date)])
        neg_count.append(neg)
        
    day_sentiment_chart= go.Figure(data=[
                    go.Bar(name='긍정/중립', x=dates, y=pos_count, text=pos_count, textposition='auto', marker=dict(color='royalblue')),
                    go.Bar(name='부정', x=dates, y=neg_count, text=neg_count, textposition='auto', marker=dict(color='indianred'))
                    ]) 
    day_sentiment_chart.update_layout(barmode='group', title='날짜별 댓글 감성 변화')
    
    return eng_sentiment_chart, kor_sentiment_chart, ko_pos, ko_neg, day_sentiment_chart
    
# 댓글별 언어 분석(pie_chart 생성)
def lang_pie(video_id):
    code_df = pd.read_excel('/home/ubuntu/final_pj/gyoungwon_main/언어코드 목록.xlsx')
    
    def code_change(x):
        try :
            idx = list(code_df['Code']).index(x)
            result = code_df['Kor_Lang'][idx]
        except :
            result = x
        return result
    
    df = comment_by_videoid(video_id)
    df1 = preprocessing(df)
    df2 = identify_lang(df1)
    lang_df = df2['lang'].value_counts().to_frame()
    lang_df['code']= lang_df.index
    lang_df['language']= lang_df['code'].apply(code_change)
    lang_df = lang_df.reset_index()
    hap = lang_df['lang'].sum()
    limit = hap * 0.001
    for i in range(len(lang_df)):
        if lang_df['lang'][i]<limit:
            lang_df['language'][i]='etc'
    id_idx = lang_df[lang_df['code']== 'id'].index
    lang_df=lang_df.drop(id_idx)
    fig = px.pie(lang_df, values = 'lang', names = 'language', color = 'language',
                 title = '댓글 언어 분석'    ,
             color_discrete_sequence = px.colors.qualitative.Pastel)
    
    fig.update_layout(legend=dict(
    orientation="h",
    yanchor="bottom",
    y=1.02,
    xanchor="right",
    x=1
))
    return lang_df, fig

