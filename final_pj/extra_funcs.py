# video table에서 영상길이 형식에 맞춰 넣기 위한 함수
def running_time_func(x):
    if 'H' in x:
        if 'M' in x:
            if 'S' in x : #running_time_func('PT1H6M10S')
                x= x.replace("PT","").replace("S","").replace("H",":").replace("M",":")
                x_list = x.split(":")
                for idx, ele in enumerate(x_list):
                    if divmod(int(ele),10)[0]== 0:
                        x_list[idx]= '0'+str(x_list[idx])
                result = ':'.join(x_list)    
                
            else :  #running_time_func('PT1H6M')
                x= x.replace("PT","").replace("H",":").replace("M","")
                x_list = x.split(":")
                for idx, ele in enumerate(x_list):
                    print(idx, ele)
                    if divmod(int(ele),10)[0]== 0:
                        x_list[idx]= '0'+str(x_list[idx])
                result = ':'.join(x_list)+":00"
        else : 
            if 'S' in x : # running_time_func('PT1H35S')  1:0:35
                x= x.replace("PT","").replace("S","").replace("H",":0:")
                x_list = x.split(":")
                for idx, ele in enumerate(x_list):
                    if divmod(int(ele),10)[0]== 0:
                        x_list[idx]= '0'+str(x_list[idx])
                result = ':'.join(x_list)
                
            else : # running_time_func("PT1H")
                result = x= x.replace("PT","").replace("H",":00:00")
                if divmod(int(x.split(":")[0]),10)==0:
                    result = "0"+x
    else :
        if 'M' in x: 
            if 'S' in x : #running_time_func('PT11M55S')
                x= x.replace("PT","").replace("S","").replace("M",":")
                x_list = x.split(":")
                for idx, ele in enumerate(x_list):
                    if divmod(int(ele),10)[0]== 0:
                        x_list[idx]= '0'+str(x_list[idx])
                result = ':'.join(x_list)
            else : #running_time_func('PT3M') 3:00
                x= x.replace("M",":00").replace("PT","")
                result = "00:"+x
                if divmod(int(x.split(":")[0]),10)[0]==0:
                    result = "00:0"+x
                
        else : #running_time_func("PT31S") 
            result = "00:00:"+x.replace("PT","").replace("S","")
            if divmod(int(x),10)[0]==0:
                result = "00:00:0"+x
    return result 

# csvs 안에 있는 파일들 삭제하는 코드
def DeleteAllFiles(filepath = '/home/ubuntu/final_pj/csvs'):
    import os
    if os.path.exists(filepath):
        for file in os.scandir(filepath):
            os.remove(file.path)
        return 'Remove ALL Files'
    else :
        return 'Directory Not Found'
    
def clean_viewcount(x):
        x= x.replace(' 回視聴','')
        if '.' in x:
            if '万' in x:
                x= x.replace(".","").replace("万","")+"000" 
        else : 
            if '万' in x :
                x= x.replace("万","")+"0000"
        return x

def toNumber(text): # K를 1000으로 바꾸는 함수
    import re
    import locale
    try :
        number = re.search('^[0-9.]+', text).group(0)
        unit = re.search('[A-Z]+', text).group(0)
        number = locale.atof(number)
        if unit == 'K':
            unit = 1000 
        elif unit == 'M':
            unit = 1000000 # 백만
        elif unit == 'B':
            unit = 1000000000 # 10억
        result = int(number * unit)
    except :
        result = int(text)
    return result

def rel_to_abs(rel_date): # 날짜 변환하는 함수
    import datetime
    from datetime import timedelta
    from dateutil.relativedelta import relativedelta

    now = datetime.datetime.now()  # 2023-05-18 17:01:41.200788 
    abs_date = 0
    # .strftime('%Y-%m-%d %H:%M:%S ') 
    if 'd ago' in rel_date :
        much = int(rel_date.split("d ago")[0])
        abs_date = (now - timedelta(days=much)).strftime('%Y-%m-%d')
    elif 'h ago' in rel_date :
        much  = int(rel_date.split("h ago")[0])
        abs_date = (now - timedelta(hours=much)).strftime('%Y-%m-%d %H:%M:%S')
    elif 'w ago' in rel_date :
        much = int(rel_date.split("w ago")[0])
        abs_date = (now - relativedelta(weeks=much)).strftime('%Y-%m-%d %H:%M:%S')  
    elif len(rel_date.split("-")) == 2:
        date_str = rel_date
        date_1 = date_str.split("-")[0]
        date_2 = date_str.split("-")[1]
        date_str_1 = f'2023/{date_1}/{date_2} 00:00'
        abs_date = datetime.datetime.strptime(date_str_1, '%Y/%m/%d %H:%M')
    elif len(rel_date.split("-")) == 3:
        date_str = rel_date
        date_1 = date_str.split("-")[0]
        date_2 = date_str.split("-")[1]
        date_3 = date_str.split("-")[2]
        date_str_1 = f'{date_1}/{date_2}/{date_3} 00:00'
        abs_date = datetime.datetime.strptime(date_str_1, '%Y/%m/%d %H:%M')
    return abs_date


def id_to_name(df):
    return {row['id'] : row['title'] for idx, row in df.iterrows()}

