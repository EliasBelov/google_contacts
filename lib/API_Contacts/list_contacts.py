import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


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
            creds = flow.run_local_server(port=0)

        with open(token_path, 'wb') as token:
            pickle.dump(creds, token)

    return creds


def list_contacts():
    creds = get_credentials()
    service = build('people', 'v1', credentials=creds)

    results = service.people().connections().list(
        resourceName='people/me',
        pageSize=1000,
        personFields='names,emailAddresses,phoneNumbers,userDefined').execute(num_retries=5)

    connections = results.get('connections', [])

    return connections
    # print(connections)

    # for person in connections:
    #     names = person.get('names', [])
    #     if names:
    #         name = names[0].get('displayName')
    #         print(name)

    #     emails = person.get('emailAddresses', [])
    #     if emails:
    #         email = emails[0].get('value')
    #         print(email)

    #     phones = person.get('phoneNumbers', [])
    #     if phones:
    #         phone = phones[0].get('value')
    #         print(phone)

    # print('---')

# if __name__ == '__main__':
#     list_contacts()
