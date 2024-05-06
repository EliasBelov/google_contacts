from lib.API_Contacts.add_contact import WorkSheetCentral, worksheet_add_contact
from lib.API_Contacts.delete_contact import delete_contact
from lib.API_Contacts.list_contacts import list_contacts
from lib.API_Contacts.update_contact import worksheet_update_contact, request_google_add_work_phone
from lib.DataFrame.Central.WorkSheetCentral import WorkSheetCentral
from lib.DataFrame.IN.WorkSheetIN import WorkSheetIN
from lib.src.comparePhones import find_missing_phones
from lib.src.count_groups import count_groups, count_drivers
from lib.src.decorators import timer_decorator
from lib.src.getGPH import get_employee_phone, check_gph_phones
from lib.src.get_unmatched_keys import get_unmatched_keys, get_unmatched_keys_add
from lib.src.importGoogleDrivers import transformation_contacts


# Обработка телефонов из графика
def main_worksheet(google_contacts_dict, groupName):

    # Используется для блокировки добавления на втором этапе
    count_add = False

    # Получение сотрудников из рабочей таблицы
    drivers_work_sheet = WorkSheetIN.filterData(WorkSheetIN())

    # Синхронизация с WorkSheetCentral
    WorkSheetCentral().write(drivers_work_sheet, groupName)

    # Очистка DF от устаревших записей
    WorkSheetCentral().remove_nonexistent(drivers_work_sheet)

    # Обработка Unsync
    driversUnsync = WorkSheetCentral().get_unsynced()
    allDriversDF = WorkSheetCentral().get_all_contacts()

    for ind, i in enumerate(driversUnsync):


        driverName = i[1]
        phones_list = i[2]

        # print(driverName, phones_list)

        # Если контакт не найден в Google Contacts
        if driverName not in google_contacts_dict:
            worksheet_add_contact(i)
            count_add = True
            continue

        # Если у существующего сотрудника найдены новые номера
        phones_for_add = find_missing_phones(driversUnsync, google_contacts_dict, driverName)
        if len(phones_for_add) > 0:
            # modify
            worksheet_update_contact((i[4], i[0], driverName, phones_list, i[3]))
            continue

        # Если у существующего сотрудника не найдены новые номера
        # Предполагается, что ошибка TypeError: 'float' object is not iterable возникает из-за того, что сотрудник есть в адаптации.
        # Будет происходить continue до тех пор пока он оттуда не исчезнет.
        try:
            worksheet_update_contact((i[4], i[0], driverName, phones_list, i[3]))
        except TypeError:
            continue

        continue


    # Добавление сотрудников внутри группы (есть в DF, но отсутствуют в Google contacts)
    for i in get_unmatched_keys_add(drivers_work_sheet, google_contacts_dict, groupName):

        for driverName in allDriversDF:

            # Проверка списка контактов (необходима при первом запуске, когда контакты пустые)
            if count_groups(google_contacts_dict, groupName) == 0:
                break

            # Если водитель найден внутри google contacts
            if count_drivers(google_contacts_dict, driverName, groupName) > 0:
                break

            # Если контакт найден в отсутствующих
            if i == driverName[1]:
                if not count_add:
                    worksheet_add_contact(driverName)

    # Удаление сотрудника внутри группы (есть в контактах, но нет внутри DF)
    for i in get_unmatched_keys(drivers_work_sheet, google_contacts_dict, groupName):
        delete_contact(i)





