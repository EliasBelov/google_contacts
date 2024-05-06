import zipfile

from pandas import pandas as pd

from lib.src.ImportPhones import ImportPhones
from lib.src.convertDate import checkDate_tenDelta, convertDatePD_PY


class AdaptationIN:
    def __init__(self):
        self.fileDir = r'//192.168.5.70/change/Табель/Логистика/Журнал температуры/Табель/АДАПТАЦИЯ!!!.xlsb.xlsb'

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
            firstDay = df.iloc[i]['Дата визита']
            try:

                if checkDate_tenDelta(firstDay) and pd.isna(df.iloc[i]['Дата оформления']):


                    # Обработка ФИО
                    driverName = df.iloc[i]['ФИО Стажера']
                    dateIssue = convertDatePD_PY(df.iloc[i]['Дата оформления'])
                    r_driverName = " ".join(driverName.split()).replace("ё", "е")

                    if not dateIssue:
                        # Обработка телефона
                        driverPhone = df.iloc[i]['Телефон Стажера']
                        redactPhone = ImportPhones.get_list(str(driverPhone))

                        # Наполнение словаря
                        r_dict[r_driverName] = redactPhone

            except ValueError:
                continue

        return r_dict

# # Создание экземпляра класса Adaptation
# adaptation = Adaptation()

# # Вызов метода filterData()
# Adaptation.filterData(adaptation)
