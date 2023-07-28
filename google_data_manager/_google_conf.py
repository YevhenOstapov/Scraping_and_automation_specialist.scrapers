import httplib2

from apiclient import discovery
from oauth2client.service_account import ServiceAccountCredentials

from conf import CREDENTIALS_FILE, SCOPES


credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, SCOPES)

# Authentication
httpAuth = credentials.authorize(httplib2.Http())

spreadsheets_service = discovery.build('sheets', 'v4', http=httpAuth)
drive_service = discovery.build('drive', 'v3', http=httpAuth)
