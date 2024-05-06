import pandas as pd

from lib.API_Contacts.update_contact import request_google_add_work_phone
from lib.DataFrame.Central.WorkSheetCentral import WorkSheetCentral


def get_employee_phone():
    filepath = "D:\\Job\\Выдача оборудования\\Оборудование ГПХ.xlsx"
    return [[
        ' '.join(row.Сотрудник.replace('ё', 'е').split()),
        '7' + str(row.Телефон) if str(row.Телефон).startswith('9') else str(row.Телефон)
    ] for _, row in pd.read_excel(filepath).iterrows()]


def check_gph_phones(google_contacts_dict):
    list_gph = get_employee_phone()
    list_df = WorkSheetCentral().get_gph()

    # Сначала создадим словарь из list_df
    dict_df = {name: (people_link, phone) for phone, name, people_link in list_df}

    # Циклический перебор значений из list_gph
    for gph_name, gph_phone in list_gph:
        gph_name = str(gph_name).replace('.0', '')
        gph_phone = str(gph_phone).replace('.0', '')

        # Извлечение номеров из словаря Google
        try:
            phone_google_list = google_contacts_dict.get(gph_name)[4].get('phoneNumbers')

            # Если ФИО есть в dict_df
            if gph_name in dict_df:
                df_people_link, df_phone = dict_df[gph_name]


                # Если телефоны не равны
                if str(gph_phone) != str(df_phone) or str(gph_phone) not in phone_google_list:
                    # Выводим на print значения из list_gph
                    WorkSheetCentral().add_phone(gph_name, gph_phone)
                    # Обновляем номер телефона в Google
                    request_google_add_work_phone(df_people_link, gph_phone)
        except TypeError:
            continue
