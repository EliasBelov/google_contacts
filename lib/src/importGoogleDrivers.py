import json

import google.auth.exceptions

from lib.src.map_keys_visual import map_keys_visual
from lib.src.telegram import send_telegram


def extract_phone_numbers(lst):
    return [item['canonicalForm'][1:] for item in lst if 'canonicalForm' in item]


def transformation_contacts(extract_goolge):

    try:

        global resourceName, emp_id, position, driverName, phoneNumbers
        r_dict = {}

        for i in range(len(extract_goolge)):

            try:
                emp_id = extract_goolge[i].get('names')[0].get('metadata').get('source').get('id')
                resourceName = extract_goolge[i].get('resourceName')
                position = extract_goolge[i].get('names')[0].get('givenName')
                driverName = extract_goolge[i].get('names')[0].get('familyName')
                phoneNumbers = extract_phone_numbers(extract_goolge[i].get('phoneNumbers'))

            except:
                send_telegram(f"Ошибка при импорте контактов. Скорее всего обнаружен пусток контакт. \n {resourceName}")

            user_defined = extract_goolge[i].get('userDefined', [{}])
            group_value = None
            if user_defined:
                group_value = user_defined[0].get('value')

            r_dict[driverName] = [{"emp_id": emp_id},
                                  {"resourceName": resourceName},
                                  {"position": position},
                                  {"driverName": driverName},
                                  {"phoneNumbers": phoneNumbers},
                                  {"group": group_value}]

        return r_dict

    except google.auth.exceptions.RefreshError:
        import subprocess
        zp_proj_dir = "C:\py\synс_cont\scripts/run_update_token.bat"
        subprocess.run([zp_proj_dir])




def transformation_contacts_add(extract_goolge):
    r_dict = {}

    emp_id = extract_goolge.get('names')[0].get('metadata').get('source').get('id')
    resourceName = extract_goolge.get('resourceName')
    position = extract_goolge.get('names')[0].get('givenName')
    driverName = extract_goolge.get('names')[0].get('familyName')
    phoneNumbers = extract_phone_numbers(extract_goolge.get('phoneNumbers'))

    r_dict[driverName] = [{"emp_id": emp_id},
                          {"resourceName": resourceName},
                          {"position": position},
                          {"driverName": driverName},
                          {"phoneNumbers": phoneNumbers},
                          ]

    return r_dict


def transformation_contacts_update(extract_goolge):
    r_dict = {}
    emp_id = extract_goolge.get('names')[0].get('metadata').get('source').get('id')
    resourceName = extract_goolge.get('resourceName')
    position = extract_goolge.get('names')[0].get('givenName')
    driverName = extract_goolge.get('names')[0].get('familyName')
    phoneNumbers = extract_phone_numbers(extract_goolge.get('phoneNumbers'))

    r_dict[driverName] = [{"emp_id": emp_id},
                          {"resourceName": resourceName},
                          {"position": position},
                          {"driverName": driverName},
                          {"phoneNumbers": phoneNumbers},
                          ]

    return r_dict
