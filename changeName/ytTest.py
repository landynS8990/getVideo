import argparse
import os
import pickle
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = 'client_secret.json'

SCOPES = ['https://www.googleapis.com/auth/youtube']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'
vidId = 'REPLACE_YOUR_VIDEO_ID'

def get_authenticated_service():
  flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
  credentials = None

  if os.path.exists('token.pickle'):
      with open('token.pickle', 'rb') as token:
          creds = pickle.load(token)
  if not creds or not creds.valid:
      if creds and creds.expired and creds.refresh_token:
          creds.refresh(Request())
      else:
          flow = InstalledAppFlow.from_client_secrets_file(
              'credentials.json', SCOPES)
          creds = flow.run_local_server(port=0)
      with open('token.pickle', 'wb') as token:
          pickle.dump(creds, token)

  print(credentials)
  return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def update_video(youtube, title):

  videos_list_response = youtube.videos().list(
    id=vidId,
    part='snippet'
  ).execute()

  if not videos_list_response['items']:
    print('Video "%s" was not found.' % vidId)
    sys.exit(1)

  videos_list_snippet = videos_list_response['items'][0]['snippet']

  videos_list_snippet['title'] = title

  print(videos_list_snippet);

  videos_update_response = youtube.videos().update(
    part='snippet',
    body=dict(
      snippet=videos_list_snippet,
      id=vidId
    )).execute()

  print('The updated video metadata is:\n' +
        'Title: ' + videos_update_response['snippet']['title'] + '\n')



if __name__ == '__main__':

  youtube = get_authenticated_service()
  strin = 'OpenCV Colour Tracking Demo'
  update_video(youtube, strin)
