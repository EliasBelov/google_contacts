# Синхронизация контактов
from lib.API_Contacts.add_contact import adaptation_add_contact
from lib.API_Contacts.delete_contact import delete_contact
from lib.API_Contacts.list_contacts import list_contacts
from lib.API_Contacts.update_contact import adaptation_update_contact
from lib.DataFrame.Central.AdaptationCentral import AdaptationCentral
from lib.DataFrame.IN.AdaptationIN import AdaptationIN
from lib.src.comparePhones import find_missing_phones
from lib.src.count_groups import count_groups, count_drivers
from lib.src.decorators import timer_decorator
from lib.src.get_unmatched_keys import get_unmatched_keys, get_unmatched_keys_add
from lib.src.importGoogleDrivers import transformation_contacts


def main_adaptation(google_contacts_dict, groupName):
    # Используется для блокировки добавления на втором этапе
    count_add = False

    drivers_adaptation = AdaptationIN.filterData(AdaptationIN())

    # Синхронизация с AdaptationCentral
    AdaptationCentral().write(drivers_adaptation, groupName)

    # Очистка DF от устаревших записей
    AdaptationCentral().remove_nonexistent(drivers_adaptation)

    # Обработка Unsync
    driversUnsync = AdaptationCentral().get_unsynced()

    allDriversDF = AdaptationCentral().get_all_contacts()

    for i in driversUnsync:
        driverName = i[1]
        phones_list = i[2]

        # print(driverName, phones_list)

        # Если контакт не найден в Google Contacts
        if driverName not in google_contacts_dict:
            adaptation_add_contact(i)
            count_add = True
            continue

        # Если у существующего сотрудника найдены новые номера
        phones_for_add = find_missing_phones(driversUnsync, google_contacts_dict, driverName)
        if len(phones_for_add) > 0:
            # modify
            adaptation_update_contact((i[4], i[0], driverName, phones_list, i[3]))
            continue

        # Если у существующего сотрудника не найдены новые номера
        try:
            adaptation_update_contact((i[4], i[0], driverName, phones_list, i[3]))
        except TypeError:
            continue

        continue

    # Добавление сотрудников внутри группы (есть в DF, но отсутствуют в Google contacts)
    for i in get_unmatched_keys_add(drivers_adaptation, google_contacts_dict, groupName):

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
                    adaptation_add_contact(driverName)

    # Удаление сотрудника внутри группы (есть в контактах, но нет внутри DF)
    for i in get_unmatched_keys(drivers_adaptation, google_contacts_dict, groupName):
        delete_contact(i)
