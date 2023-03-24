#pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
#refer: https://medium.com/@victor.perez.berruezo/execute-google-apps-script-functions-or-sheets-macros-programmatically-using-python-apps-script-ec8343e29fcd
#refer: https://developers.google.com/apps-script/api/quickstart/python
#refer: https://developers.google.com/apps-script/api/how-tos/execute#python

import google.auth
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.errors import HttpError
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import Helper.JsonReader as json
import os.path

class AppsScriptAPI(object):
    def __init__(self):
        #Connect google service account
        self.__service = self.__get_scripts_service()
        
    def __del__(self):
        self.__service = None

    def Execute(self):
        config_Google_Apps_Script = json.getnodedata('Google_Apps_Script')
        API_ID = config_Google_Apps_Script['DeploymentID']
        requests = config_Google_Apps_Script['Request']

        for request in requests:
            try:
                response = self.__service.scripts().run(body=request, scriptId=API_ID).execute()
            except HttpError as error:
                # The API encountered a problem.
                print(error.content)

    def __get_scripts_service(self):
        creds = None
        service = None

        secret_key_path = json.getnodedata('Google_Service_Account_Credentials_OAuth')
        SCOPES = json.getnodedata('Google_Service_Account_Credentials_OAuth_Scopes')

        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                secret_key_path, SCOPES)
                creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        if creds and creds.valid:
            service = build('script', 'v1', credentials=creds)

        return service


#creds, _ = google.auth.default()
#service = build('script', 'v1', credentials=creds)  