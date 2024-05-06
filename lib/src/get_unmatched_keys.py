def get_unmatched_keys(drivers_adaptation, google_contacts_dict, groupName):
    """
        in:
            drivers_adaptation = {'Зайцев Александр Геннадьевич': ['798..011..9'], 'Телегин Вадим Евгеньевич': ['791..454975', '79..7002105'], 'Закарая Лука Элгуджаевич': ['791..288936', '792..811111']}
            google_contacts_dict = {'Морозов Руслан': [{'emp_id': 'ef9b30b0..b41ea'}, {'resourceName': 'people/c1079090445692912106'}, {'position': '!Стажер'}, {'driverName': 'Морозов Руслан'}, {'phoneNumbers': ['791..030348']}, {'group': 'Adaptation'}], 'Глебов Михаил Александрович': [{'emp_id': '34ddf7dd8e7cee36'}, {'resourceName': 'people/c3..9473390..5692854'}, {'position': '!Стажер'}, {'driverName': 'Глебов Михаил Александрович'}, {'phoneNumbers': ['79....32..9']}, {'group': 'Adaptation'}], 'Маннабов Рустэм Махмудович': [{'emp_id': '4f493efc0e8562c6'}, {'resourceName': 'people/c57..16..54592488..4'}, {'position': '!Стажер'}, {'driverName': 'Маннабов Рустэм Махмудович'}, {'phoneNumbers': ['790..310336']}, {'group': 'Adaptation'}]}


    """
    unmatched_keys = []
    for key in google_contacts_dict:
        if google_contacts_dict[key][-1]['group'] == groupName:
            if key not in drivers_adaptation:
                unmatched_keys.append(google_contacts_dict[key][1]['resourceName'])
    return unmatched_keys


def get_unmatched_keys_add(drivers_adaptation, google_contacts_dict, groupName):
    """
        in:
            drivers_adaptation = {'Зайцев Александр Геннадьевич': ['798..011..9'], 'Телегин Вадим Евгеньевич': ['791..454975', '79..7002105'], 'Закарая Лука Элгуджаевич': ['791..288936', '792..811111']}
            google_contacts_dict = {'Морозов Руслан': [{'emp_id': 'ef9b30b0..b41ea'}, {'resourceName': 'people/c1079090445692912106'}, {'position': '!Стажер'}, {'driverName': 'Морозов Руслан'}, {'phoneNumbers': ['791..030348']}, {'group': 'Adaptation'}], 'Глебов Михаил Александрович': [{'emp_id': '34ddf7dd8e7cee36'}, {'resourceName': 'people/c3..9473390..5692854'}, {'position': '!Стажер'}, {'driverName': 'Глебов Михаил Александрович'}, {'phoneNumbers': ['79....32..9']}, {'group': 'Adaptation'}], 'Маннабов Рустэм Махмудович': [{'emp_id': '4f493efc0e8562c6'}, {'resourceName': 'people/c57..16..54592488..4'}, {'position': '!Стажер'}, {'driverName': 'Маннабов Рустэм Махмудович'}, {'phoneNumbers': ['790..310336']}, {'group': 'Adaptation'}]}


    """
    unmatched_keys = []
    for key in drivers_adaptation:
        if key not in google_contacts_dict or google_contacts_dict[key][-1]['group'] != groupName:
            unmatched_keys.append(key)
    return unmatched_keys


# # Архивное удаление, возможно потребуется для контактов созданных вручную
# def get_unmatched_keys(drivers_adaptation, google_contacts_dict):
#     """
#         in:
#             drivers_adaptation = {'Зайцев Александр Геннадьевич': ['798..011..9'], 'Телегин Вадим Евгеньевич': ['791..454975', '79..7002105'], 'Закарая Лука Элгуджаевич': ['791..288936', '792..811111']}
#             google_contacts_dict = {'Морозов Руслан': [{'emp_id': 'ef9b30b0..b41ea'}, {'resourceName': 'people/c1079090445692912106'}, {'position': '!Стажер'}, {'driverName': 'Морозов Руслан'}, {'phoneNumbers': ['791..030348']}, {'group': 'Adaptation'}], 'Глебов Михаил Александрович': [{'emp_id': '34ddf7dd8e7cee36'}, {'resourceName': 'people/c3..9473390..5692854'}, {'position': '!Стажер'}, {'driverName': 'Глебов Михаил Александрович'}, {'phoneNumbers': ['79....32..9']}, {'group': 'Adaptation'}], 'Маннабов Рустэм Махмудович': [{'emp_id': '4f493efc0e8562c6'}, {'resourceName': 'people/c57..16..54592488..4'}, {'position': '!Стажер'}, {'driverName': 'Маннабов Рустэм Махмудович'}, {'phoneNumbers': ['790..310336']}, {'group': 'Adaptation'}]}
#
#
#     """
#     unmatched_keys = set(google_contacts_dict) - set(drivers_adaptation)
#     result = []
#     for key in unmatched_keys:
#         result.append(google_contacts_dict[key][1]['resourceName'])
#     return result
#
