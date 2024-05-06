from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os.path
import pickle
from google.auth.transport.requests import Request

# Функция для получения учетных данных
from lib.DataFrame.Central.AdaptationCentral import AdaptationCentral
from lib.DataFrame.Central.OfficeCentral import OfficeCentral
from lib.DataFrame.Central.RegularCentral import RegularCentral
from lib.DataFrame.Central.WorkSheetCentral import WorkSheetCentral
from lib.src.importGoogleDrivers import transformation_contacts_update
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


# Функция для обновления контакта
def request_google_add_contacts(contact_resource_name, position, name, phone_numbers, group):
    r_dict = {}
    creds = get_credentials()
    service = build('people', 'v1', credentials=creds)

    # Получаем текущий контакт
    current_contact = service.people().get(resourceName=contact_resource_name, personFields='metadata').execute()
    etag = current_contact.get('etag')

    person = {
        'etag': etag,  # Используем полученное значение etag
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

    # Обновление контакта
    updated_contact = service.people().updateContact(
        resourceName=contact_resource_name,
        updatePersonFields='names,emailAddresses,phoneNumbers',
        body=person).execute()

    return updated_contact


def request_google_add_work_phone(contact_resource_name, work_phone=''):
    creds = get_credentials()
    service = build('people', 'v1', credentials=creds)

    # Получение контакта
    current_contact = service.people().get(resourceName=contact_resource_name, personFields='phoneNumbers').execute(num_retries=5)

    # Извлечение списка телефонов
    current_phone_numbers = current_contact.get('phoneNumbers', [])
    etag = current_contact.get('etag')

    # Проверка существующего рабочего номера
    for phone in current_phone_numbers:
        if phone.get('type') == 'work':
            current_phone_numbers.remove(phone)
            break

    # Добавление рабочего номера (если еще нет)
    if work_phone:
        work_phone = f"+{work_phone}"
        current_phone_numbers.append({
            'value': work_phone,
            'type': 'work'
        })

    person = {
        'etag': etag,
        'phoneNumbers': current_phone_numbers,
    }

    # Отправка обновлений
    updated_contact = service.people().updateContact(
        resourceName=contact_resource_name,
        updatePersonFields='phoneNumbers',
        body=person).execute()

    return updated_contact


def adaptation_update_contact(dataTuple):
    # Получение информации о добавленном контакте
    response = transformation_contacts_update(
        request_google_add_contacts(dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3], dataTuple[4]))
    # Обновление информции в файле DF адаптации
    AdaptationCentral().update_sync(response)


def worksheet_update_contact(dataTuple):
    # Получение информации о добавленном контакте
    response = transformation_contacts_update(
        request_google_add_contacts(dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3], dataTuple[4]))
    # Обновление информции в файле DF адаптации
    WorkSheetCentral().update_sync(response)


def regular_update_contact(dataTuple):
    # Получение информации о добавленном контакте
    response = transformation_contacts_update(
        request_google_add_contacts(dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3], dataTuple[4]))
    # Обновление информции в файле DF адаптации
    RegularCentral().update_sync(response)


def office_update_contact(dataTuple):
    # Получение информации о добавленном контакте
    response = transformation_contacts_update(
        request_google_add_contacts(dataTuple[0], dataTuple[1], dataTuple[2], dataTuple[3], dataTuple[4]))
    # Обновление информции в файле DF адаптации
    OfficeCentral().update_sync(response)
