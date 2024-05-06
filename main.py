import traceback
from lib.API_Contacts.list_contacts import list_contacts
from lib.src.cleaning_contacts import clean_contacts, find_duplicate
from lib.src.getGPH import check_gph_phones
from lib.src.importGoogleDrivers import transformation_contacts
from lib.src.main_adaptation import main_adaptation
from lib.src.main_office import main_office
from lib.src.main_regular import main_regular
from lib.src.main_worksheet import main_worksheet
from lib.src.telegram import send_telegram

try:
    google_contacts_dict = transformation_contacts(list_contacts())  # Получение контактов Google
    main_adaptation(google_contacts_dict, groupName='Adaptation')  # Контакты адаптация
    main_worksheet(google_contacts_dict, groupName='Worksheet')  # Контакты табель
    main_regular(google_contacts_dict, groupName='Regular')  # Контакты штатных авто
    main_office(google_contacts_dict, groupName='Office')  # Контакты офис и магазины
    check_gph_phones(google_contacts_dict)  # Синхронизация корпоративных телефонов ГПХ
    clean_contacts(google_contacts_dict)  # Очистка контактов от созданных вручную
    # send_telegram(str('дубликат в контаках', find_duplicate(google_contacts_dict)))   # Очистка от дубликатов


except:
    print(f'Ошибка выполнения:\n, {traceback.format_exc()}')
    t = f'Ошибка выполнения:\n, {traceback.format_exc()}'
    send_telegram(t)

