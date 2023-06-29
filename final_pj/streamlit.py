import streamlit as st
# from stqdm import stqdm
from streamlit_option_menu import option_menu
#from crawling_funcs import *
from extra_funcs import *
from db_connect import * 
from custom_statics import *
from video_list import *
from recent_highview_list import * 
import pandas as pd
import plotly.express as px
from gyoungwon_main.preprocess_lang import * 
from gyoungwon_main.emotion import * 
import matplotlib.pyplot as pyplot
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math
from youtube_block.doc import *
from gyoungwon_main.neg_dict_copy import *


st.set_page_config(
    page_title="FinalProject_4",
    page_icon="✅",
    layout="wide",    
    )


def streamlit_menu():
    with st.sidebar:
        selected = option_menu(
            menu_title="메인메뉴",  
            options=["서비스 정보 소개", "개인채널(Youtube)", '채널비교(Youtube)', "부정어 블락처리"],  
            icons=["balloon-heart", "youtube", 'bar-chart-fill', 'database-fill-gear'],
            menu_icon="file-play",
            default_index=0,
            styles={ "icon": {"color": "red", "font-size": "25px"}, 
                    "nav-link-selected": {"background-color": "#b1c8fa"}}

        )
    return selected

selected = streamlit_menu()

if selected == '서비스 정보 소개':
    st.markdown("**<p align='center'> <font size = '8'> 서비스 정보 소개 </font></p>**", unsafe_allow_html=True)
    st.markdown("**<p align='left'> <font size = '6'> 서비스 목적 </font></p>**", unsafe_allow_html=True)
    ment = """많은 기업과 연예인이 본인 소유의 SNS 채널(Youtube, Instagram 등)을 운영하고 있다. 
    특정 기업과 연예인에 대해서 긍정적, 부정적 이슈가 발생했을 때 해당 채널의 댓글의 수가 폭발적으로 증가하는 모습을 발견할 수 있었고, 
    이 현상을 실시간 크롤링을 통해서 감지하여 긍정적 이슈라면 마케팅(광고, 보도자료)으로 활용하고,
      부정적 이슈라면 즉각적으로 대처할 수 있게끔 하는 프로그램을 만들려고 한다."""
    st.write(ment)

    st.markdown("**<p align='left'> <font size = '6'> 메뉴별 기능소개 </font></p>**", unsafe_allow_html=True)
    st.markdown("**<p align='left'> <font size = '5'> 1. 개인채널 </font></p>**", unsafe_allow_html=True)
    st.markdown("<p align='left'> <font size = '4'> 개인채널 페이지에서는 해당 채널에 대한 여러 분석결과를 제공해줍니다. </font></p>", unsafe_allow_html=True)
    st.markdown("**<p align='left'> <font size = '3'> 1️⃣최신 동영상 5개에 대한 시간대별 조회수 평균 상승률  </font></p>**", unsafe_allow_html=True)
    st.write('이전 시간대의 조회수 대비 기준 시간대의 조회수 상승률의 평균을 제공해줍니다.')
    st.markdown("**<p align='left'> <font size = '3'> 2️⃣시간대 별 업로드 N일차에 상승한 조회수  </font></p>**", unsafe_allow_html=True)
    st.write('시간대별로 업로드 된지 N일차에 얼만큼 조회수가 상승했는지를 보여줍니다.')
    st.markdown("**<p align='left'> <font size = '3'> 3️⃣댓글 언어 분석  </font></p>**", unsafe_allow_html=True)
    st.write('동영상의 댓글 언어 종류와 비율을 보여줍니다.')
    st.write('동영상의 댓글을 감성 분석 한 후 긍부정 비율과 날짜별 시계열 그래프를 보여줍니다.')




    st.markdown("**<p align='left'> <font size = '5'> 2. 채널비교 </font></p>**", unsafe_allow_html=True)
    st.markdown("<p align='left'> <font size = '4'> 채널비교 페이지에서는 기준 채널과 비교 채널에 대한 여러가지 비교 분석결과를 제공해줍니다. </font></p>", unsafe_allow_html=True)
    st.markdown("**<p align='left'> <font size = '3'> 1️⃣조회수 / 좋아요 / 댓글 추이 그래프  </font></p>**", unsafe_allow_html=True)
    st.write('구독자 대비 조회수 비율을 백분율로 보여드립니다.')
    st.write('좋아요 수와 댓글 수를 시계열 꺾은선 그래프로 보여드립니다. ')
    st.markdown("**<p align='left'> <font size = '3'> 2️⃣채널별 주요 해시태그 20개  </font></p>**", unsafe_allow_html=True)
    st.write('채널별로 주요 해시태그들을 워드클라우드 형태로 보여드립니다.')
    st.markdown("**<p align='left'> <font size = '3'> 3️⃣실시간 그래프 기능  </font></p>**", unsafe_allow_html=True)
    st.write('실시간 그래프를 체크하면 최신 업로드 동영상 5개에 대한 그래프를 연달아서 확인 할 수 있습니다.')






    st.markdown("**<p align='left'> <font size = '5'> 3. 부정어 블락처리 </font></p>**", unsafe_allow_html=True)
    st.markdown("<p align='left'> <font size = '4'> 부정어 블락처리 페이지에서는 채널별 부정어 목록 확인, 등록, 삭제 기능을 제공해줍니다. </font></p>", unsafe_allow_html=True)
    st.markdown("**<p align='left'> <font size = '3'> 1️⃣채널의 부정어 DB 목록 확인  </font></p>**", unsafe_allow_html=True)
    st.write('해당 채널의 부정어로 등록되어 DB에 쌓여있는 단어들을 확인 할 수 있습니다.')
    st.markdown("**<p align='left'> <font size = '3'> 2️⃣부정어 후보 단어 제시 & 해당 단어가 포함된 부정적 댓글 확인  </font></p>**", unsafe_allow_html=True)
    st.write('형태소 분석과 감성 분석을 진행하여 도출한 부정어를 후보로 제공해주고, 해당 단어가 포함된 실제 댓글을 보여줍니다.')
    st.markdown("**<p align='left'> <font size = '3'> 3️⃣부정어 등록 & 삭제  </font></p>**", unsafe_allow_html=True)
    st.write('부정어로 등록할 단어와 부정어에서 삭제할 단어를 사용자에게 입력받습니다. ')
    st.write('부정어로 등록된 단어가 포함된 댓글들은 최대 3분안에 화면에서 보여지지 않게 됩니다. 댓글 유형이 검토대기중으로 바뀌어 사용자의 승인 후에 댓글 화면에 보여지게 됩니다.')








if selected == 'Youtube 분석결과' :
    st.markdown("**<p align='center'> <font size = '8'> Youtube 채널 분석 결과</font></p>**", unsafe_allow_html=True)
    
    # 채널 선택 부분
    channel_df = get_channel_list()
    channel_list, name_to_id = make_channel_list(channel_df)
    select_channel = st.selectbox('채널을 선택해주세요.' , ([n for n in channel_list if '유튜브' in n ]))
    list_df = get_video_list(name_to_id[select_channel]) # 동영상 목록 가져오기
   
    # 인자 : 리스트 항목개수, 채널ID, 데이터프레임(video_id만 갖고있음)
    recent_top_list, high_diff_list= recent_highview_func(5, name_to_id[select_channel],list_df)

    channel_id = name_to_id[select_channel]
    line_df = get_video_data(channel_id, limit = 5, recent=True)
    id_to_name_dict = id_to_name(line_df) # id <-> 이름 사전

    order = st.selectbox('분석기준을 선택해주세요.' , ('최신 업로드 동영상 5개 기준', '조회수 상승순 동영상 5개 기준'))
    st.title('')
    st.text('')

    if order == '최신 업로드 동영상 5개 기준' :
           
        #1. 동영상 목록 보여주기
        col1, col2 = st.columns([8, 2])
        col1.markdown("<p align='left'> <font size = '4'> ⭐ 업로드 날짜 기준으로 최신 동영상 5개를 보여드립니다.  </font></p>", unsafe_allow_html=True)
        st.markdown('&emsp;&emsp;⭐ &emsp;제목을 클릭하면 해당 동영상 링크로 창이 생성됩니다. ')
        details = col2.checkbox('See Details')
        
        df, log_df= recent_top_list_info(recent_top_list)

        for i in range(len(df)):
            st.write(f"&emsp;&emsp;✔️&emsp; Video {i+1} : &emsp; [{df['title'][i]}](https://www.youtube.com/watch?v={df['id'][i]})")
            if details : # See Details 체크박스 누른 경우
                st. write(f"&emsp;&emsp;&emsp;&emsp;&emsp; ➕    업로드 날짜 : {df['uploaded_at'][i]} &emsp; 조회수 : {log_df.loc[df['id'][i]]['view_count']}  &emsp;  좋아요 수 : {log_df.loc[df['id'][i]]['like_count']} &emsp; 댓글 수 : {log_df.loc[df['id'][i]]['comment_count']}")
        
        st.title('')

        # 2. 로그 데이터 변화량 그래프
        st.markdown("<p align='left'> <font size = '4'> ⭐ 최신 동영상 5개에 대하여 변화량 추이를 꺾은선 그래프로 보여드립니다.  </font></p>", unsafe_allow_html=True)
        view_type = st.selectbox('분류 기준을 선택해주세요' , ('조회수', '좋아요', '댓글'))
        # video_names = line_df['title'].values
        list_df = make_line_df(line_df['id'].values, id_to_name_dict, view_type = view_type)
        
        # list_df.index = list_df.index[::-1]
        st.dataframe(list_df.reset_index().sort_values(['index']).set_index(['index']))

        fig = px.line(
             list_df
        )
        fig.update_layout(legend=dict(x=0, y=1.1, orientation="h"))
        # st.plotly_chart(fig)

        st.title('')

        #3.  댓글 언어별 PieChart
        
        st.markdown("<p align='left'> <font size = '4'> ⭐ 해당 동영상의 댓글 분석 결과를 보여드립니다.   </font></p>", unsafe_allow_html=True)
        video_select = st.selectbox('분석을 원하는 동영상을 선택해주세요.' , (df['title'][0], df['title'][1],df['title'][2],df['title'][3],df['title'][4]))
        
       # com_col1, com_col2 = st.columns([2,1])
       # com_col1.plotly_chart(lang_pie(title_to_id(video_select))) #댓글언어분석 파이차트 그리기
        #com_col2.plotly_chart(lang_pie(title_to_id(video_select))) #댓글언어분석 파이차트 그리기
        #4. 동영상 별 긍부중 비율 보여주기
        
    if order == '조회수 상승순 동영상 5개 기준':

        #1. 동영상 목록 보여주기
        col3, col4 = st.columns([8, 2])
        col3.markdown("<p align='left'> <font size = '4'> ⭐ 3시간 전과 비교하여 조회수 차이가 큰 동영상 5개를 보여드립니다.  </font></p>", unsafe_allow_html=True)
        st.write('')
        details = col4.checkbox('See Details')

        
        df, log_df= high_diff_list_info(recent_top_list)

        for i in range(len(df)):
            st.write(f"&emsp;&emsp;✔️&emsp; Video {i+1} : &emsp; [{df['title'][0]}](https://www.youtube.com/watch?v={df['id'][i]})")
            if details : 
                st. write(f"&emsp;&emsp;&emsp;&emsp;&emsp; ➕    업로드 날짜 : {df['uploaded_at'][i]} &emsp; 조회수 : {log_df['view_count'][i]}  &emsp;  좋아요 수 : {log_df['like_count'][i]} &emsp; 댓글 수 : {log_df['comment_count'][i]}")
        

        df = get_video_data(channel_id)
        id_to_name_dict = id_to_name(df)
        line_df = make_line_df_topVideo(df['id'].values, id_to_name_dict)

        st.dataframe(line_df)
        st.line_chart(line_df, use_container_width=True)
       

if  selected == '개인채널(Youtube)':
    st.markdown("**<p align='center'> <font size = '8'> Youtube 개인 채널 분석 </font></p>**", unsafe_allow_html=True)
    st.subheader('')

    channel_df = get_channel_list(where = " where platform = '유튜브'")
    check_lst = [0 for _ in range(len(channel_df))] 
    channels  = channel_df['channel_name'].values
    channel_ids = channel_df['id'].values

    channel1 = st.selectbox('채널 선택을 선택해주세요', channels)
    # selected_channels.append(channel_ids[np.where(channels == channel1)][0])
    st.subheader('')

    # channel_df = get_channel_list()
    _, name_to_id = make_channel_list(channel_df)

    list_df = get_video_list(name_to_id[channel1+'(유튜브)'])
    recent_top_list, high_diff_list= recent_highview_func(5, name_to_id[channel1+'(유튜브)'],list_df)
    df, log_df= recent_top_list_info(recent_top_list)
    title_to_idx = {title : idx for idx, title in enumerate(df['title'].values)}
    
    plot_df = daily_compare2([channel_ids[np.where(channels == channel1)][0]]).set_index('time')
    
    # st.dataframe(plot_df)
    show_df = plot_df.groupby(['video_id']).max()
    show_df = show_df[['title', 'views', 'likes', 'comments','uploaded_at']].sort_values('uploaded_at', ascending=False).reset_index(drop=True)
    show_df.columns = ['동영상 제목', '조회수', '좋아요', '댓글', '업로드 날짜']

    # 증가율 계산
    df4 = pd.DataFrame()
    for ids in plot_df['video_id'].unique():
        tmp = plot_df[plot_df['video_id'] == ids]
        tmp = tmp[tmp.index>'2023-06-08'].resample('2H').max().reset_index()
        
        tmp['uploaded_at'] = pd.to_datetime(tmp['uploaded_at'])
        
        tmp['diff_days'] = (tmp['time'] - tmp['uploaded_at']) / np.timedelta64(1, 'D')
        
        tmp.dropna(subset=['diff_days'], inplace=True)
        tmp['diff_days'] = tmp['diff_days'].apply(math.floor)
        # st.dataframe(tmp)
        start, end = int(min(tmp['diff_days'].values)), int(max(tmp['diff_days'].values)) + 1
        
        def hour(date):
            return date.hour
        tmp['hour'] = tmp['time'].apply(hour)
        
        max_view = (max(tmp['views']))
        for i in range(start, end):
            t = tmp[tmp['diff_days'] == i][['video_id','views','diff_days','hour']]
            ratio2 = []
            for j in range(len(t)-1, 0, -1):
                value = ((t['views'].iloc[j] - t['views'].iloc[j-1]) / max_view)
                ratio2.append(value)
            
            t = t[1:]
            t['ratio2'] = ratio2

            df4 = pd.concat([df4, t])


    
    # df4 = df4.groupby(['diff_days', 'hour'])['ratio2'].mean().reset_index()
    df4 = df4.groupby(['hour'])['ratio2'].mean().reset_index()
    
    # df4['ratio2'] =         (df4['ratio2']/len(df4['diff_days'].unique()))
    st.write("**<p style=\"font-size:26px;\"> 최신 업로드 동영상 5개 시간대별 조회수 평균 상승률</p>**", unsafe_allow_html=True)

    colorscales = px.colors.named_colorscales()
    fig = px.bar(
        data_frame = df4,
        x = 'hour',
        y = 'ratio2',
        color = 'hour', 
        color_continuous_scale='darkmint',
        text_auto = '.2%',
        labels = {'ratio2' : '상승률', 'hour' : '시간대'}
    )

    # fig.update_layout(showlegend = False)
    fig.update_layout(yaxis={'visible': True, 'showticklabels': False})
    fig.update_layout(
        uniformtext_minsize=10, uniformtext_mode='hide'
        )
    st.write("<p style=\"font-size:16px; \"> 📺이전 시간대에 비하여 기준 시간대에 조회수가 얼마나 상승했는지를 보여줍니다.  </p>", unsafe_allow_html=True)
    st.write("<p style=\"font-size:12px; \">  상승률은 [(기준 시간 - 이전 시간)조회수 / 최대 조회수]의 평균으로 계산되었습니다. 2시간 간격으로 시간대가 설정되어 있습니다.</p>", unsafe_allow_html=True)
    st.plotly_chart(fig,use_container_width=True)
    st.write("<p style=\"font-size:12px; \">  최신 업로드 동영상 5개에 대한 정보입니다. </p>", unsafe_allow_html=True)

    st.dataframe(show_df,use_container_width=True)
    st.subheader('')
    st.subheader('동영상 별 분석')
    video_select = st.selectbox('최신 업로드 동영상 5개 중에서 분석을 원하는 동영상을 선택해주세요.' , (df['title'][0], df['title'][1],df['title'][2],df['title'][3],df['title'][4]))
    # st.write("<p style=\"font-size:12px; \"> 최신 업로드 동영상 5개 정보를 참고하세요.</p>", unsafe_allow_html=True)

    
    recent_video = daily_compare_df([channel_ids[np.where(channels == channel1)][0]], title_to_idx[video_select], is_compare=False).set_index('time')

    # 증가율 계산
    tmp = recent_video[recent_video.index>'2023-06-08'].resample('2H').max().reset_index()
    
    tmp['uploaded_at'] = pd.to_datetime(tmp['uploaded_at'])
    
    tmp['diff_days'] = (tmp['time'] - tmp['uploaded_at']) / np.timedelta64(1, 'D')
    
    tmp.dropna(subset=['diff_days'], inplace=True)
    tmp['diff_days'] = tmp['diff_days'].apply(math.floor)
    # st.dataframe(tmp)
    start, end = int(min(tmp['diff_days'].values)), int(max(tmp['diff_days'].values)) + 1
    
    def hour(date):
        return date.hour
    tmp['hour'] = tmp['time'].apply(hour)

    df3 = pd.DataFrame()
    for i in range(start, end):

        t = tmp[tmp['diff_days'] == i][['views','diff_days','hour']]
        ratio = []
        view_cnt = []
        for i in range(len(t)-1, 0, -1):
            value = ((t['views'].iloc[i] / t['views'].iloc[i-1]) - 1)
            value2 = (t['views'].iloc[i] - t['views'].iloc[i-1])
            ratio.append(value)
            view_cnt.append(value2)

        t = t[1:]
        t['이전 시간대비 상승률'] = ratio
        t['상승 조회수'] = view_cnt

        df3 = pd.concat([df3, t])
    
    
    st.write("**<p style=\"font-size:26px;\"> 시간대별 조회수 증가량</p>**", unsafe_allow_html=True)
    st.write("<p style=\"font-size:16px; \"> 🎥 시간대 별 동영상 업로드 후 N일차에 따른 조회수 증가량을 보여줍니다.  </p>", unsafe_allow_html=True)

    video_id = recent_video[recent_video['title'] == video_select]['video_id'].unique()[0]
    upload_date = recent_video['uploaded_at'].unique()[0].strftime("%Y년 %m월 %d일")
    st.write(f"🎥  [{video_select}](https://www.youtube.com/watch?v={video_id}) 은  {upload_date}에 업로드 되었습니다.", unsafe_allow_html=True)
    
    
    df3.rename(columns={'diff_days' : '업로드 N일차'}, inplace=True)
    fig = px.bar(
        data_frame = df3,
        x = 'hour',
        y = '상승 조회수',
        color = '업로드 N일차',
        text = '상승 조회수',
        # text_auto = '',
        color_continuous_scale='darkmint',
        hover_data=['상승 조회수'],
        labels = {'상승 조회수' : '', 'hour' : '시간대'}
    )
    # fig.update_layout(showlegend)
    fig.update_layout(yaxis={'visible': True, 'showticklabels': False})
    fig.update_layout(
        # uniformtext_minsize=10, uniformtext_mode='hide'
        )
    fig.update_traces(textfont_size=12, 
                    # textfont_color='red',
                    # textfont_family = "Times", 
                    texttemplate='%{text:,}',
                    textangle=0, textposition="inside")

    st.plotly_chart(fig,use_container_width=True)

    st.write("**<p style=\"font-size:26px;\"> 댓글 분석 </p>**", unsafe_allow_html=True)
    st.write("**<p style=\"font-size:20px;\"> 1️⃣ 댓글 언어 분석 </p>**", unsafe_allow_html=True)
    st.write("<p style=\"font-size:16px;\">  동영상 댓글의  언어 종류와 비율을 보여줍니다.</p>", unsafe_allow_html=True)
    st.write("<p style=\"font-size:12px;\">  전체 댓글의 0.1% 미만의 언어인 경우 etc로 분류됩니다. </p>", unsafe_allow_html=True)

    #댓글 언어분석
    com_col1, com_col2 = st.columns([2,1])
    with st.spinner('댓글 언어 판별 중입니다. 잠시만 기다려주세요. '):
        lang_df, lang_fig = lang_pie(title_to_id(video_select))
        com_col1.plotly_chart((lang_fig),use_container_width=True) #댓글언어분석 파이차트 그리기
        total= lang_df['lang'].sum()
        com_col2.header("")
        com_col2.header("")
        com_col2.header("")
        com_col2.header("")
        com_col2.write(f'전체 댓글 수는 {total}개 입니다.')
        com_col2.write(f"한글 댓글 개수는 {int(lang_df[lang_df['index']=='ko']['lang'])}개 입니다.")
        com_col2.write(f"영어 댓글 개수는 {int(lang_df[lang_df['index']=='en']['lang'])}개 입니다.")
    
    # 댓글 감정분석
    st.write("**<p style=\"font-size:20px;\"> 2️⃣ 댓글 감성 분석 </p>**", unsafe_allow_html=True)
    st.write("<p style=\"font-size:16px;\"> 감성 분석 모델로 분석한 댓글의 감성 비율과 실제 댓글들을 보여줍니다. </p>", unsafe_allow_html=True)
    st.write("<p style=\"font-size:16px;\"> 날짜별 댓글 업로드 개수와 해당 댓글의 감성을 시계열 그래프로 제공합니다. </p>", unsafe_allow_html=True)

    st.write("<p style=\"font-size:12px;\">  현재는 한국어, 영어만 지원합니다. </p>", unsafe_allow_html=True) 
    
    com_col3, com_col4 = st.columns([1, 1])
    
    with st.spinner('댓글 감성 분석 중입니다. 잠시만 기다려주세요. '):

        charts_and_comments = emotion_all(title_to_id(video_select))
        eng_sentiment_chart, kor_sentiment_chart, ko_pos, ko_neg, day_sentiment_chart = charts_and_comments

        com_col3.plotly_chart(kor_sentiment_chart, use_container_width=True)
        com_col4.plotly_chart(eng_sentiment_chart, use_container_width=True) 
        
        my_expander_1 = st.expander(label=('긍정으로 분류된 좋아요 상위 댓글 3개')) 
        my_expander_2 = st.expander(label=('부정으로 분류된 좋아요 상위 댓글 3개'))
        
        with my_expander_1:
            if len(ko_pos) >= 1:
                ko_pos_index_reset = ko_pos.reset_index(drop=True)
                st.dataframe(ko_pos_index_reset, use_container_width=True)
            else:
                st.write('해당 댓글이 없습니다.')
        with my_expander_2:        
            if len(ko_neg) >= 1:
                ko_neg_index_reset = ko_neg.reset_index(drop=True)
                st.dataframe(ko_neg_index_reset, use_container_width=True)
            else:
                st.write('해당 댓글이 없습니다.')

    st.plotly_chart(day_sentiment_chart, use_container_width=True)
                
if selected == '채널비교(Youtube)':
    
    st.markdown("**<p align='center'> <font size = '8'> Youtube 채널 비교 분석 </font></p>**", unsafe_allow_html=True)
    st.subheader('')

    channel_df = get_channel_list(where = " where platform = '유튜브'")
    check_lst = [0 for _ in range(len(channel_df))] 
    channels  = channel_df['channel_name'].values
    channel_ids = channel_df['id'].values
    
    selected_channels = []
    select_channel1, select_channel2 = st.columns(2)
    with select_channel1:
        channel1 = st.selectbox('기준 채널을 선택해주세요.', channels)
        selected_channels.append(channel_ids[np.where(channels == channel1)][0])
    
    with select_channel2:
        pop_idx = np.where(channels == channel1)
        channel2 = st.selectbox('비교 채널을 선택해주세요.', (np.delete(channels, pop_idx)))
        selected_channels.append(channel_ids[np.where(channels == channel2)][0])

    a1,a2 = st.columns([1,6])
    if selected == "채널비교(Youtube)":
        real_time = a1.checkbox('실시간 그래프')
    else :
        real_time = False 
    a2.markdown("<p style=\"font-size:15px; \"> 실시간 그래프를 체크하면 최신 동영상 5개를 기준으로 한 그래프를 연달아서 확인 할 수 있습니다. 그래프는 10초후에 바뀝니다. </p>", unsafe_allow_html=True)


    st.subheader('')
    cc1,cc2,cc3 = st.columns([3,0.5,3])
    cc1.markdown(f"**<p align='center'> <font size = '18'><span style='color:green'> {channel1} </span></font></p>**", unsafe_allow_html=True)
    cc2.markdown(f"**<p align='center'> <font size = '18'><span style='color:black'> VS </span></font></p>**", unsafe_allow_html=True)
    cc3.markdown(f"**<p align='center'> <font size = '18'><span style='color:red'> {channel2} </span></font></p>**", unsafe_allow_html=True)
    #st.title(f":green[{channel1}]"+ '  VS  ' + f":red[{channel2}]")
    #st.markdown(f"**<p align='center'> <font size = '23'><span style='color:green'> {channel1} </span> &emsp; VS &emsp; <span style='color:red'> {channel2} </span></font></p>**", unsafe_allow_html=True)
    
    df = compare_df(selected_channels)
    
    channel_lst = list(df['platform'].unique())
    channel_lst.append('전체')
    
    placeholder = st.empty()
    filter = ['유튜브']

    # 비교균 df
    df = df[df['platform'].isin(filter)]

    # st.dataframe(df)
    df1 = df[df['channel_id'] == selected_channels[0]]
    df2 = df[df['channel_id'] == selected_channels[1]]

    # tb_channel_log join시 데이터 가져오는 시간이 너무 오래걸려서 따로 가져옴
    df1_sub = get_data_to_csv(f"select subscriber from tb_channel_log where channel_id = '{selected_channels[0]}' order by subscriber desc limit 1")
    df2_sub = get_data_to_csv(f"select subscriber from tb_channel_log where channel_id = '{selected_channels[1]}' order by subscriber desc limit 1")
    
    subscriber_info = { selected_channels[0] : df1_sub['subscriber'].iloc[0],
                        selected_channels[1] : df2_sub['subscriber'].iloc[0]                        }
    

    for i in range(200):
        # 대시보드 
        with placeholder.container():

            # create three columns
            line1_1, line1_2, line1_3, line1_4, line1_5 = st.columns(5)

            video_diff = len(df1) - len(df2)
            line1_1.metric(
                label = "영상수 :movie_camera:",
                value = len(df1),
                delta=(video_diff),
            )

            view_cnt1 = df1['views'].sum() 
            view_cnt2 = df2['views'].sum()
            views_diff = view_cnt1 - view_cnt2

            
            if view_cnt1 == 0 or view_cnt2 == 0:
                st.write("<p style=\"font-size:26px; color:red; font-weight:bold;\"> 요청하신 채널의 총시청수를 가져오지 못했습니다. </p>", unsafe_allow_html=True)

            line1_2.metric(
                label="조회수 :eyes:",
                value= mertic_number(view_cnt1),
                delta= mertic_number(views_diff),
            )
            
            likes_diff = df1['likes'].sum() - df2['likes'].sum()
            line1_3.metric(
                label="좋아요 :heart:",
                value=mertic_number(df1['likes'].sum()),
                delta= mertic_number(likes_diff),
            )

            comments_diff = df1['comments'].sum() - df2['comments'].sum()
            line1_4.metric(
                label="댓글 :speech_balloon:",    
                value=mertic_number(df1['comments'].sum()),
                delta=mertic_number(comments_diff),
            )
            
            subscriber_diff = df1_sub['subscriber'].iloc[0] - df2_sub['subscriber'].iloc[0]
            line1_5.metric(
                label = '구독자 👩‍👧‍👦',
                value = mertic_number(df1_sub['subscriber'].iloc[0]),
                delta = mertic_number(subscriber_diff)
            )
            st.markdown('')
            st.markdown(f"<p align='right'> <font size = '3'> 선택 채널의 지표수가 기준이 되고, 경쟁 채널과의 차이는 아래 숫자의 화살표로 보여줍니다. <br> ( K는 1,000 (1천), M은 1,000,000 (1백만) )  </font></p>", unsafe_allow_html=True)
            
            subplot_fig = make_subplots(rows=1, cols=3,
                                        subplot_titles=("구독자 대비 조회수 도달률  ", "좋아요", "댓글"))
            plot_df = daily_compare_df(selected_channels, i%5, is_compare = False).set_index('time')
            st.subheader('')
            st.markdown("<p style=\"font-size:26px; font-weight:bold;\"> 조회수 / 좋아요 / 댓글 추이 </p>", unsafe_allow_html=True)

            videos = '/\n'.join([p + '->' + t for p, t in zip(plot_df['platform'].unique(), plot_df['title'].unique())])
            # st.write("<p style=\"font-size:40px; font-weight:bold;\">최근 5개 영상 정보</p>", unsafe_allow_html=True)
            # st.write("<p style=\"font-size:12px;\">(최근 5개 영상중 조회수가 높은 영상 순서대로 비교 됩니다.)</p>", unsafe_allow_html=True)
            # st.write("<p style=\"font-size:26px; font-weight:bold;\">구독자 대비 조회수 변화</p>", unsafe_allow_html=True)
            # st.write(videos)

            def view_div_sub(df):
                tmp = [subscriber_info[n] for n in df['channel_id'].values]
                df['view/sub'] = (df['views'].values / np.array(tmp)) 
            view_div_sub(plot_df)         

            
            fig = go.Figure()
            fig_df1 = plot_df[plot_df['channel_id'] == selected_channels[0]]
            fig_df2 = plot_df[plot_df['channel_id'] == selected_channels[1]]
            fig.add_trace(go.Scatter(
                x= fig_df1.index,
                y= fig_df1['view/sub'],
                line_color='green',
                # showlegend=False,
                name = fig_df1['title'].unique()[0]
            ))
            fig.add_trace(go.Scatter(
                x= fig_df2.index,
                y= fig_df2['view/sub'],
                line_color='red',
                name = fig_df2  ['title'].unique()[0]
            ))
            subplot_fig.add_trace(go.Scatter(
                x= fig_df1.index,
                y= fig_df1['view/sub'],
                line_color='green',
                mode='lines+markers',
                # showlegend=False,
                name = fig_df1['title'].unique()[0]
            ), row =1, col=1)
            subplot_fig.add_trace(go.Scatter(
                x= fig_df2.index,
                y= fig_df2['view/sub'],
                line_color='red',
                mode='lines+markers',
                name = fig_df2  ['title'].unique()[0]
            ), row=1, col=1)
            
            subplot_fig.update_layout(yaxis_tickformat = '.2%')
            subplot_fig.update_layout(hovermode="x")


            fig.update_layout(legend=dict(x=0, y=1.2, orientation="h"),
                            legend_title_text = '구분')

            # fig.update_xaxes(title_text="")
            # fig.update_yaxes(title_text="")
            fig.update_traces(mode='lines')
            # st.plotly_chart(fig, use_container_width=True)    
            # st.dataframe(plot_df[['title', 'view/sub', 'channel_name']])

            
            # fig_t = go.Figure()
            # st.write("<p style=\"font-size:26px; font-weight:bold;\">좋아요 & 댓글 변화</p>", unsafe_allow_html=True)
            fig2 = make_subplots(specs=[[{"secondary_y": True}]])
            # colors = ['#FF3333', '#33FF99']
            colors = ['green', 'red']
            showlegend = True
            for i in range(2):
                tmp_df = plot_df[plot_df['channel_id'] == selected_channels[i]]

                for idx, (contestant, group) in enumerate(tmp_df.groupby("channel_name")):
                    # if idx == 1 :
                    #     showlegend = False
                    # fig2.add_trace(go.Histogram(x=group.index, y=group["likes"], name= '좋아요', showlegend = showlegend, marker={'color': colors[idx]}),secondary_y=False)
                    # fig2.add_trace(go.Scatter(x=group.index, y=group['comments'], name='댓글', showlegend = showlegend, line_color = colors[idx+2]),secondary_y=True)
                    subplot_fig.add_trace(go.Scatter(x=group.index, y=group["likes"], name= '좋아요', showlegend = False, mode='lines+markers', marker={'color': colors[i]}), row=1,col=2)
                    subplot_fig.add_trace(go.Scatter(x=group.index, y=group['comments'], name='댓글', showlegend = False, mode='lines+markers', line_color = colors[i]), row=1,col=3)
                

            fig2.update_layout(legend=dict(x=0, y=1.2, orientation="h"))

            # Set y-axes titles
            fig2.update_yaxes(title_text="좋아요", secondary_y=False)
            fig2.update_yaxes(title_text="댓글", secondary_y=True)


            # st.plotly_chart(fig2, use_container_width=True)

            subplot_fig.update_layout(legend=dict(x=0, y=1.4, orientation="h"),
                            legend_title_text = '구분')
            
            subplot_fig.update_traces(marker_line_width=2, marker_size=8)    
            st.plotly_chart(subplot_fig, use_container_width=True)

            # st.dataframe(plot_df[plot_df['channel_name'] == selected_channels[0]])


            st.markdown("### 영상목록")
            select_col_1, select_col_2 = st.columns(2)
            with select_col_1:
                select_1 = st.selectbox('데이터 수를 선택해주세요.',([10,50,100, '전체']))
            
            with select_col_2:
                select_2 = st.selectbox('정렬 기준을 선택해주세요.', (['시청수', '좋아요수', '댓글수','업로드 시간(최신)']))
 
            
            select_1 = len(df) if select_1 =='전체' else select_1
            select_2 = '업로드 시간' if select_2 == '업로드 시간(최신)' else select_2
                        
            view_df = df[['title', 'views', 'likes', 'comments', 'channel', 'platform', 'upload_time']]
            view_df.columns = ['제목', '시청수', '좋아요수', '댓글수', '채널명', '플랫폼', '업로드 시간']
            

            view_df = view_df.reset_index(drop=True).set_index('채널명', drop=True).sort_values([select_2], ascending=False)            
            st.dataframe(view_df[:select_1], use_container_width=True)
            st.write("**<p style=\"font-size:26px; \"> 채널별 주요 HashTag 20개 </p>**", unsafe_allow_html=True)

            from plotly_wordcloud import plotly_wordcloud as pwc
            import matplotlib.pyplot as plt
             

            st.pyplot(pwc(df1,df2))
            # chart, words = pwc(df1, df2)
            # st.pyplot(chart)

            # with open('print.txt', 'w') as f:
            #     f.write(", ".join(words))
                

            if real_time : sleep_time = 10
            else : break
            time.sleep(sleep_time)

if selected == '부정어 블락처리':
    st.markdown("**<p align='center'> <font size = '8'> 부정어 블락처리 </font></p>**", unsafe_allow_html=True)
    st.subheader('')
    # 1. 채널선택
    st.markdown("<p align='left'> <font size = '5'> 1. 채널 선택하기 </font></p>", unsafe_allow_html=True)
    channel_option = st.selectbox('채널을 선택해주세요',('재밌는 거 올라온다', 'Example_Channel','술먹지상렬'))
    channel_id = channel_name_to_id(channel_option)#또간집 ID
    st.subheader('')

    # 2. 현재 DB에 있는 부정어 사전 보여주기
    st.markdown("<p align='left'> <font size = '5'> 2. 해당 채널의 부정어 DB </font></p>", unsafe_allow_html=True)
    st.write('⚠️ 부정어로 등록된 단어들이 포함된 댓글들은 화면에서 보여지지 않습니다. 검토 대기중으로 처리되어 담당자의 승인 후 화면에서 보여지게 됩니다.')
    now_list = get_block_wordlist(channel_option) # 해당 채널 DB에 있는 단어들 모으기
    
    if len(now_list)==0 :
        st.info('현재 해당 채널의 부정어는 0개 입니다.')
    else :
        join_now_list = ','.join(now_list)
        st.info(join_now_list)
    st.subheader('')



    # 3. 최신 댓글을 바탕으로 한 부정어 후보
    st.markdown("<p align='left'> <font size = '5'> 3. 부정어 후보 단어들  </font></p>", unsafe_allow_html=True)
    st.write('최신 댓글들을 바탕으로한 부정어 단어 후보입니다. 단어를 선택하면 해당 단어가 들어가 있는 부정댓글들을 일부 확인 할 수 있습니다. ')

    with st.spinner("댓글 수집 중입니다. 잠시만 기다려주세요. ") :
        # 부정어 사전 계산 코드
        unpopular_df, popular_df = negdict_get_comment(channel_id) # 해당 비디오 댓글 수집
        popular_id = popular_df['video_id'][0]
        unpopular_id = unpopular_df['video_id'][0]
    # st.write(popular_id)
    # st.write(unpopular_id)
    
        #댓글 전처리
        popular_df = preprocessing(popular_df)
        unpopular_df = preprocessing(unpopular_df)
    
    with st.spinner('댓글 언어 판별 중입니다. 잠시만 기다려주세요.'):
        #댓글 언어 판별
        popular_df = identify_lang(popular_df)
        unpopular_df = identify_lang(unpopular_df)

    with st.spinner('댓글 감성 분석 중입니다. 잠시만 기다려주세요. '):
        #감정분석 진행
        model, device, tokenizer = load_model()
        popular_df.loc[popular_df['lang'] == 'ko', 'sentiment'] = popular_df[popular_df['lang'] == 'ko']['demoji_text'].apply(analyze_korean_sentiment,args= (model,device, tokenizer))
        unpopular_df.loc[unpopular_df['lang'] == 'ko', 'sentiment'] = unpopular_df[unpopular_df['lang'] == 'ko']['demoji_text'].apply(analyze_korean_sentiment,args= (model,device, tokenizer)) 
    
    with st.spinner('부정어 단어 후보들을 추출하는 중입니다. 잠시만 기다려주세요. '):
        #mecab 사용
        popular_mecab_df, popular_mecab_nouns = mecab_pos(popular_df)
        unpopular_mecab_df, unpopular_mecab_nouns = mecab_pos(unpopular_df)
        mecab_neg_list = mecab_diff_set(popular_mecab_nouns, unpopular_mecab_nouns) 
        #okt 사용
        popular_okt_df, popular_okt_nouns = okt_pos(popular_mecab_df) #시간 좀 걸림
        unpopular_okt_df, unpopular_okt_nouns = okt_pos(unpopular_mecab_df) 
        okt_neg_list = okt_diff_set(popular_okt_nouns, unpopular_okt_nouns) 
        # mecab, okt 교집합
        meokt_with_counts = mecab_okt_intersection(mecab_neg_list, okt_neg_list)
    final_list = []
    for tup in meokt_with_counts:
        final_list.append(tup[0])
    pre_word = st.selectbox('부정어 단어 후보들',final_list)

   
    #댓글예시 보여주는 코드
    comment_list = get_negdict_comment(meokt_with_counts, popular_mecab_df)
    if final_list==[]:
        st.write('부정어 단어 후보가 없습니다. ')
    else : 
        if pre_word in comment_list:
            comments = comment_list[pre_word]
            st.write(' ')
            my_expander_3 = st.expander(label=(f'"{pre_word}" 단어가 포함된 부정적 댓글 예시'))
            with my_expander_3:
                for comment in comments:
                    st.write("- "+ comment)
        else:
            st.write("선택된 단어에 대한 댓글이 없습니다.")




    st.subheader('')
    # 4. DB에 부정어 등록, 제거
    st.markdown("<p align='left'> <font size = '5'> 4. 부정어 단어 등록 & 삭제  </font></p>", unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1]) # 이분할
    c11,c12 = c1.columns([4,1])
    c11.markdown("<p align='left'> <font size = '4'> &emsp;➕ &emsp;  부정어 단어 등록  </font></p>", unsafe_allow_html=True)
    register_btn= c12.button('등록')
    add_word = c1.text_input('부정어로 등록할 단어를 입력한 후 등록 버튼을 눌러주세요.')
    if add_word != "" and register_btn:
        result = register_block_word(add_word, channel_option)
        if result: # 위과정 잘 실행되면
                c1.write(f'"{add_word}" 단어가 {channel_option} 채널의 부정어로 등록이 완료 되었습니다.')
    
    c21,c22 = c2.columns([4,1])
    c21.markdown("<p align='left'> <font size = '4'> &emsp;➖ &emsp; 부정어 단어 삭제  </font></p>", unsafe_allow_html=True)
    delete_btn= c22.button('삭제')
    out_word = c2.selectbox('부정어에서 삭제할 단어를 선택한 후 삭제 버튼을 눌러주세요. ',now_list)
    if out_word != "" and delete_btn:
        result = delete_block_word(out_word, channel_option)
        if result: # 위과정 잘 실행되면
                c2.write(f'"{out_word}" 단어를 {channel_option} 채널의 부정어에서 삭제했습니다.')
    st.subheader('')



