import zipfile
from pandas import pandas as pd
from lib.src.ImportPhones import ImportPhones
from lib.src.convertDate import checkDate_tenDelta, convertDatePD_PY


class OfficeIN:
    def __init__(self):
        self.fileDir = r'\\192.168.5.70\change\Телефоны\Контакты_ОФИС.xlsx'

    @classmethod
    def getFrame(cls):
        df = pd.read_excel(cls().fileDir)
        return df

    @staticmethod
    def filterData(adaptation_instance):
        r_dict = {}
        df = adaptation_instance.getFrame()

        for i in range(len(df)):

            # Извлечение диапазона дат

            empType = df['Тип'][i]
            empName = df['Сотрудник'][i]
            empPhone = ImportPhones().get_list(df['Телефон'][i])
            # Проверка телефона
            if empPhone != 'Телефон не найден':
                r_dict[empName] = {'empPhone': empPhone, 'empType': empType, 'empName': empName}

        return r_dict

# # Создание экземпляра класса Adaptation
# adaptation = Adaptation()

# # Вызов метода filterData()
# Adaptation.filterData(adaptation)
