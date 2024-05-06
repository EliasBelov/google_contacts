# Синхронизация контактов
from lib.API_Contacts.add_contact import regular_add_contact
from lib.API_Contacts.delete_contact import delete_contact
from lib.API_Contacts.list_contacts import list_contacts
from lib.API_Contacts.update_contact import regular_update_contact
from lib.DataFrame.Central.RegularCentral import RegularCentral
from lib.DataFrame.IN.RegularIN import RegularIN
from lib.src.comparePhones import find_missing_phones
from lib.src.count_groups import count_groups, count_drivers
from lib.src.get_unmatched_keys import get_unmatched_keys, get_unmatched_keys_add
from lib.src.importGoogleDrivers import transformation_contacts


def main_regular(google_contacts_dict, groupName):
    # Используется для блокировки добавления на втором этапе
    count_add = False

    cars_regular_sheet = RegularIN.filterData(RegularIN())

    # Очистка DF от устаревших записей
    RegularCentral().remove_nonexistent(cars_regular_sheet)

    # Синхронизация с WorkSheetCentral
    RegularCentral().write(cars_regular_sheet, groupName)

    # Обработка Unsync
    driversUnsync = RegularCentral().get_unsynced()

    allDriversDF = RegularCentral().get_all_contacts()

    for i in driversUnsync:

        driverName = i[1]
        phones_list = i[2]

        # print(driverName, phones_list)

        # Если контакт не найден в Google Contacts
        if driverName not in google_contacts_dict:
            regular_add_contact(i)
            count_add = True
            continue

        # Если у существующего сотрудника найдены новые номера
        phones_for_add = find_missing_phones(driversUnsync, google_contacts_dict, driverName)
        if len(phones_for_add) > 0:
            # modify
            print((i[4], i[0], driverName, phones_list, i[3]))
            regular_update_contact((i[4], i[0], driverName, phones_list, i[3]))
            continue

        # Если у существующего сотрудника не найдены новые номера
        regular_update_contact((i[4], i[0], driverName, phones_list, i[3]))
        continue

    # Добавление сотрудников внутри группы (есть в DF, но отсутствуют в Google contacts)
    for i in get_unmatched_keys_add(cars_regular_sheet, google_contacts_dict, groupName):

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
                    regular_add_contact(driverName)

    # Удаление сотрудника внутри группы (есть в контактах, но нет внутри DF)
    for i in get_unmatched_keys(cars_regular_sheet, google_contacts_dict, groupName):
        delete_contact(i)
