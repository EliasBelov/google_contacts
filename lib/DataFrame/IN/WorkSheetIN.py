import zipfile

from pandas import pandas as pd
from pytz import timezone
from lib.src.ImportPhones import ImportPhones
from lib.src.convertDate import checkDate_tenDelta, convertDatePD_PY

from datetime import datetime

import pandas as pd
from datetime import datetime, timedelta


def correct_fio(driverName):
    return " ".join(driverName.split()).replace("ё", "е")


class DataProcessor:
    def __init__(self, dictionary):
        self.dictionary = dictionary

    def process_current_date(self):
        # Получаем текущую дату без времени

        moscow_tz = timezone('Europe/Moscow')
        current_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

        # Преобразуем текущую дату в строку в формате '%d.%m.%Y'
        current_date_str = current_date.strftime('%d.%m.%Y')

        if current_date in self.dictionary:
            result_dict = {
                'driver_type': self.dictionary.get('Кат'),
                'driver_name': correct_fio(str(self.dictionary.get('Вод'))),
                'phone': ImportPhones.get_list(self.dictionary.get('Телефон')),
                'job_value': self.dictionary.get(current_date),
                'current_date': current_date_str,
            }

            return result_dict
        else:
            raise TypeError(f"Не удалось найти ключ с датой {current_date}")


class PathProcessor:
    def __init__(self):
        self.path = r'//192.168.5.70/change/Табель/Логистика/Журнал температуры/Табель/ГРАФИК ВЫХОДОВ ИЮНЬ.xlsm.xlsm'
        self.months_ru = {
            1: 'ЯНВАРЬ',
            2: 'ФЕВРАЛЬ',
            3: 'МАРТ',
            4: 'АПРЕЛЬ',
            5: 'МАЙ',
            6: 'ИЮНЬ',
            7: 'ИЮЛЬ',
            8: 'АВГУСТ',
            9: 'СЕНТЯБРЬ',
            10: 'ОКТЯБРЬ',
            11: 'НОЯБРЬ',
            12: 'ДЕКАБРЬ'
        }

    def get_current_month_path(self):
        current_month = datetime.now().month
        current_month_ru = self.months_ru[current_month]
        new_path = self.path.replace("ИЮНЬ", current_month_ru)
        return new_path


class WorkSheetIN:
    def __init__(self):
        self.fileDir = PathProcessor().get_current_month_path()

    @classmethod
    def getFrame(cls):
        df = pd.read_excel(cls().fileDir)
        return df

    @staticmethod
    def filterData(adaptation_instance):
        goodType_list = ['Вод', 'Экс', 'ГПХ', 'Заб']
        r_dict = {}
        df = adaptation_instance.getFrame()

        for i in range(len(df)):
            new_columns = dict(zip(df.columns, df.iloc[i]))
            # Фильтрация по типу сотрудника
            filterString = DataProcessor(new_columns).process_current_date()

            try:
                if filterString.get('driver_type') in goodType_list and \
                        filterString.get('phone') != 'Телефон не найден':
                    # Наполнение словаря
                    r_dict[filterString.get('driver_name')] = [filterString]
            except KeyError:
                continue

        return r_dict

# ({'driver_type': 'ГПХ',
# 'driver_name': 'Телегин Вадим Евгеньевич',
# 'phone': ['791..454975'],
# 'job_value': '1?',
# 'current_date': '30.06.2023'},)
