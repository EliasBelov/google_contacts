import pandas as pd
from datetime import datetime, timedelta

# Получение базовой даты 1 января 1900 года
base_date = pd.Timestamp('1900-01-01')

def checkDate_tenDelta(days_since_base: float, current_date: datetime = None) -> bool:
    """
        print(checkDate_tenDelta(45085.0, datetime(2023, 6, 11)))
    """

    # преобразование количества дней в datetime
    date = base_date + pd.DateOffset(days=int(days_since_base) - 2)

    # если текущая дата не указана, -> сегодняшнюю дату
    if current_date is None:
        current_date = datetime.now()

    # вычисление даты, которая сравнивается (текущая дата - 10 дней)
    timedelta_date = current_date - timedelta(days=10)

    # возваращение True, если дата больше timedelta_date, иначе False
    return timedelta_date < date



def convertDatePD_PY(days_since_base: float):
    """
        print(checkDate_tenDelta(45085.0, datetime(2023, 6, 11)))
    """    
    try:
        # преобразование количества дней в datetime
        date = base_date + pd.DateOffset(days=int(days_since_base) - 2)
        return date

    except ValueError:
        return False

