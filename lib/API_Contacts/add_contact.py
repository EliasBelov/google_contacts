import os.path
import pickle
from datetime import time

from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from lib.DataFrame.Central.AdaptationCentral import AdaptationCentral
from lib.DataFrame.Central.OfficeCentral import OfficeCentral
from lib.DataFrame.Central.RegularCentral import RegularCentral
from lib.DataFrame.Central.WorkSheetCentral import WorkSheetCentral
from lib.src.importGoogleDrivers import transformation_contacts_add
from lib.src.processed_numbers import process_numbers


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


def request_google_add_contacts(position, name, phone_numbers, group):
    r_dict = {}

    if len(str(name)) > 0 and len(str(phone_numbers)) > 0:

        creds = get_credentials()
        service = build('people', 'v1', credentials=creds)

        person = {
            'names': [
                {
                    'familyName': name,
                    'givenName': position,
                }
            ],
            'emailAddresses': [
                {
                    'value': ''
                }
            ],
            'phoneNumbers': [
                {
                    'value': f"+{phone}"
                } for phone in process_numbers(phone_numbers)
            ],
            'userDefined': [
                {
                    'key': 'group',
                    'value': group
                }
            ]
        }

        contact = service.people().createContact(
            body=person,
            personFields='names,emailAddresses,phoneNumbers').execute()

        return contact


def adaptation_add_contact(dataTuple):
    # Получение информации о добавленном контакте
    response = transformation_contacts_add(
        request_google_add_contacts(dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3]))
    # Обновление информции в файле DF адаптации
    AdaptationCentral().update_sync(response)


def worksheet_add_contact(dataTuple):
    # Получение информации о добавленном контакте
    response = transformation_contacts_add(
        request_google_add_contacts(dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3]))
    # Обновление информции в файле DF адаптации
    WorkSheetCentral().update_sync(response)


def regular_add_contact(dataTuple):
    # Получение информации о добавленном контакте
    response = transformation_contacts_add(
        request_google_add_contacts(dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3]))
    # Обновление информции в файле DF адаптации
    RegularCentral().update_sync(response)


def office_add_contact(dataTuple):
    # Получение информации о добавленном контакте
    response = transformation_contacts_add(
        request_google_add_contacts(dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3]))
    # Обновление информции в файле DF адаптации
    OfficeCentral().update_sync(response)


"""
    {
      'Second employee': [{
        'emp_id': 'b7c345d8aeeac62'
      }, {
        'resourceName': 'people/c827594007896829026'
      }, {
        'position': '!Стажер'
      }, {
        'driverName': 'Second employee'
      }, {
        'phoneNumbers': ['79991234567', '79997654321']
      }]
    }
"""

# if __name__ == '__main__':
#     add_contact('Добавлен тест', 'ivan.ivanov@example.com', ['+79991234567', '+79997654321'], 'Group1')
