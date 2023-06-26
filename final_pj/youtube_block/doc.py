import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import sys
sys.path.append('/home/ubuntu/final_pj') # 같은 선상에 있는 파일이 아니기 때문에
from db_connect import get_comments_with_word
from db_connect import get_block_wordlist

# crontab 돌리기 성공~
# mix.py와 동일코드 https://pbj0812.tistory.com/266

def set_moderation_status(youtube,status, arg_id):
  youtube.comments().setModerationStatus(
    id=arg_id,
    # status = heldForReview : 검토로 상태 바꾸기, published : 공개로 상태 바꾸기, rejected
    moderationStatus=status,
    banAuthor = False # 댓글 작성자 차단여부
  ).execute()

  print ("%s moderated succesfully" % (arg_id)) 

def get_authenticated_service():
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    API_SERVICE_NAME = "youtube"
    API_VERSION = "v3"
    #client_secrets_file = "client_secrets.json"
    CLIENT_SECRETS_FILE = "/home/ubuntu/final_pj/youtube_block/client_secrets.json"
    SCOPES= ["https://www.googleapis.com/auth/youtube.force-ssl"]
    
    credentials = None
    if os.path.exists('/home/ubuntu/final_pj/youtube_block/token.pickle'):
        with open('/home/ubuntu/final_pj/youtube_block/token.pickle', 'rb') as token:
            credentials = pickle.load(token)
            print('여기1')
    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
            print('여기2')
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_console()
            print('여기3')

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)


def main():
    youtube = get_authenticated_service()
    word_list =  get_block_wordlist('Example_Channel')
    for word in word_list :
        id_list = get_comments_with_word('Example_Channel', word)
        for idname in id_list :
        #idname = 'Ugw2zzrWKInW27BT6ep4AaABAg' # 이런 고양이
            set_moderation_status(youtube, 'heldForReview',idname)
            print(f'{idname} set_moderation_status 완료')
        print(f'{word} 포함 댓글 처리 완료')


if __name__ == "__main__":
    main()