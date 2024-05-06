import zipfile
from pandas import pandas as pd
from lib.src.ImportPhones import ImportPhones
from lib.src.convertDate import checkDate_tenDelta, convertDatePD_PY


class RegularIN:
    def __init__(self):
        self.fileDir = r'D:/Job/Выдача оборудования/Телефоны ШТАТ.xlsx'

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
            carType = df['Тип'][i]
            carName = df['Сотрудник'][i]
            carPhone = df['Телефон'][i]

            r_dict[carName] = {'carPhone': carPhone, 'carType': carType, 'carName': carName}

        return r_dict

# # Создание экземпляра класса Adaptation
# adaptation = Adaptation()

# # Вызов метода filterData()
# Adaptation.filterData(adaptation)
