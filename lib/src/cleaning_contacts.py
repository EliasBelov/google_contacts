from lib.API_Contacts.delete_contact import delete_contact
from lib.API_Contacts.list_contacts import list_contacts
from lib.src.importGoogleDrivers import transformation_contacts
from lib.src.telegram import send_telegram


def find_none_group_and_return_resource(input_dict):
    r_list = []
    for key, value_list in input_dict.items():
        for info_dict in value_list:
            if 'group' in info_dict and info_dict['group'] is None:
                for data in value_list:
                    if 'resourceName' in data:
                        r_list.append(data['resourceName'])
    return r_list


def clean_contacts(google_contacts_dict):

    checkListClean = find_none_group_and_return_resource(google_contacts_dict)

    if len(checkListClean) > 0:
        for i in checkListClean:
            delete_contact(i)
            txt_msg = f'Sync_contacts: Был удален добавленный вручную контакт\n{i}'
            send_telegram(txt_msg)


def find_duplicate(google_contacts_dict):
    # Создание словаря для отслеживания групп и связанных с ними ресурсов
    group_resources = {}

    for key, value_list in google_contacts_dict.items():
        for info_dict in value_list:
            if 'group' in info_dict and 'resourceName' in info_dict:
                if info_dict['group'] in group_resources:
                    group_resources[info_dict['group']].append(info_dict['resourceName'])
                else:
                    group_resources[info_dict['group']] = [info_dict['resourceName']]

    # Поиск групп, содержащих более одного уникального resourceName
    for group, resources in group_resources.items():
        if len(set(resources)) > 1:
            return {group: resources}

    return None


