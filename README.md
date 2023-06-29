# 유튜브 채널 실시간 이슈 감지 및 분석 서비스

특정 기업과 연예인에 대한 이슈가 생기면 해당 대상이 운영하는 SNS 채널 댓글이 폭팔적으로 증가하는 현상이 발생하고 있다. 
'유튜브 채널 실시간 이슈 감지 및 분석 서비스'를 이용하면 실시간 모니터링을 통해 이상 현상을 즉시 감지하며, 긍정적인 이슈라면 마케팅 수단으로 활용하고, 부정적인 이슈라면 즉각적으로 대처할 수 있다. 

## Table Of Contents
[1. Overview](#overview)  
[2. Demo](#demo)  
[3. Main Features](#main-features)  
[4. Stack](#stack)  
[5. ERD](#erd)  
[6. Contributors](#contributors)  

## Overview 

![final_project process](https://github.com/kdt-service/Final_PJT_Team3/assets/123911402/0ff530e3-45a9-4cbe-bb47-b186da107ef2)

## Demo 
http://15.152.250.135:8501/ 

## Main Features 
- 채널 분석 (최근 업로드한 5개 영상)
    - 시간대별 조회수 평균 상승률
    - 각 영상별 시간대별 조회수 증가량
    - 각 영상별 댓글 분석
        - 국가별
        - 긍정/부정(감성분석)
        - 날짜별 감성 변화
- 경쟁 채널 비교 분석 (기준 채널 vs 비교 채널) 
    - 기준 채널의 통합 데이터(영상수, 조회수, 좋아요, 댓글, 구독자) 표시 및 비교 채널과 상대적 수치 표기
    - 가장 최근 영상끼리 조회수/좋아요/댓글 추이 비교 (조회수 - 구독자 대비 도달률)
        - 실시간 비교 가능(최근 5개 영상에 대해서 10초 간격 노출)
    - 기준, 비교 채널의 주요 해시태그 20개(빈도수 기준)
- 채널별 부정어 사전 구축 및 차단
    - 부정어 사전에 등록할 단어 목록 제공
    - 부정어 등록 및 삭제
    - 부정어 등록시 해당 단어가 포함된 댓글 차단

## Stack
1. 크롤링  
Youtube API, Selenium 사용 

2. 전처리  
Null값 제거, 중복 댓글 제거, 한글자 댓글 제거, html 태그 제거, @사용자 이름+댓글 내용으로 수집된 경우 @사용자 이름 제거, 댓글에 의미없이 반복되는 문자열 제거(soynlp)

3. 언어 분석  
댓글 내 이모지, 특수문자 제거하여 langid 라이브러리 통한 언어 판별하고, 알파벳, 한글 수 비교하여 한글이 더 많으면 한글로, 알파벳이 더 많으면 영어로 2차 분류  

4. 감성 분석   
- 한글 댓글 감성 분석  
    - 긍정·중립/부정으로 이진 분류된 댓글 데이터로 KcELECTRA 파인튜닝 
- 영어 댓글 감성 분석 
    - vaderSentiment(소셜 미디어 텍스트 감성분석을 위한 rule-based model) 사용 

5. 부정어 사전 구축  
전처리, 언어 판별, 감성 분석, 형태소 분석을 통한 부정어 추출

6. 대시보드 제작   
plotly을 이용한 데이터 시각화, streamlit를 통한 대시보드 제작


## ERD 
![FINAL_ERD](https://github.com/kdt-service/Final_PJT_Team3/assets/123911402/d86e629d-b0bd-4180-9c54-69f3d468d254)

## Contributors 
문다은 https://github.com/daeun-moon   
이석호 https://github.com/LSH0414   
정경원 https://github.com/mabeljeong 
