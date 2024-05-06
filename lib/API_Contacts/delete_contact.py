from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
import pickle
from google.auth.transport.requests import Request

# Функция для получения учетных данных
def get_credentials():
    creds = None
    token_path = 'lib/API_Contacts/token.pickle'
    credentials_path = 'lib/API_Contacts/credentials.json'

    if os.path.exists(token_path):
        with open(token_path, 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_path,
                ['https://www.googleapis.com/auth/contacts',
                 'https://www.googleapis.com/auth/user.phonenumbers.read',
                 'https://www.googleapis.com/auth/userinfo.email',
                 'openid'])
        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


# Функция для удаления контакта
def delete_contact(contact_resource_name):
    creds = get_credentials()
    service = build('people', 'v1', credentials=creds)
    service.people().deleteContact(resourceName=contact_resource_name).execute(num_retries=5)

