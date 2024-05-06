from pandas import pandas as pd
import os


# Проверка существования DF Central
class AdaptationCentral:
    """
        check - Проверка существования \ пересоздания DF (метод класса)

        is_driver_exists - Проверка занесения водителя (метод класса)

        write - занесение водителя
        IN: {'Зайцев Александр Геннадьевич': ['79858011139'], 'Телегин Вадим Евгеньевич': ['79168454975', '79777002105'], 'Закарая Лука Элгуджаевич': ['79166288936']}

        update_sync - обновляет файл адаптации после синхнронизации с Google
        IN: transformation_contacts_one - {'Second employee': [{'emp_id': 'b7c345d8aeeac62'}, {'resourceName': 'people/c827594007896829026'}, {'position': '!Стажер'}, {'driverName': 'Second employee'}, {'phoneNumbers': ['79991234567', '79997654321']}]}

        get_unsynced - возвращает информацию из DF адаптация Unsync
        OUT: [('!Стажер', 'Зайцев Александр Геннадьевич', ['79858011139'], 'Adaptation')]


    """

    def __init__(self):
        # Директория экспорта
        self._PROJECTDIR = os.getcwd()
        self._EXPORTDIR = os.path.join(self._PROJECTDIR, 'txt')

        # Имя файла
        self._BASEDIR = os.path.basename(__file__)
        self.FILENAME = f"{os.path.splitext(os.path.basename(__file__))[0]}.xlsx"
        self.FILEDIR = os.path.join(self._EXPORTDIR, self.FILENAME)

    def check(self):
        if not os.path.exists(self.FILEDIR):
            headers = ['driverName', 'Position', 'Group', 'ID', 'Sync_Status',
                       'Enable_Status', 'Job_Phone', 'Phone_1',
                       'Phone_2', 'Phone_3', 'Phone_4', 'Phone_5']

            df = pd.DataFrame(columns=headers)

            with pd.ExcelWriter(self.FILEDIR) as writer:
                df.to_excel(writer, index=False, header=True)
                return df

        df = pd.read_excel(self.FILEDIR)
        return df

    def is_driver_exists(self, driverName):
        df = self.check()
        return driverName in df['driverName'].values

    def write(self, driverDict, groupName):
        # Создание DataFrame с заданными заголовками
        df = self.check()

        for driver, phones in driverDict.items():
            # Создание словаря для новой строки со всеми полями телефона пустыми
            new_row_dict = {
                'driverName': driver,  
                'ID': '',
                'Position': '!Стажер',
                'Group': groupName,
                'resourceName': '',
                'Sync_Status': 'Unsync',
                'Enable_Status': 'Enable',
                'Job_Phone': '',
                'Phone_1': '',
                'Phone_2': '',
                'Phone_3': '',
                'Phone_4': '',
                'Phone_5': '',
            }

            # Присваивание номера телефонов доступным полям
            for i in range(len(phones)):
                new_row_dict[f'Phone_{i + 1}'] = phones[i]

            # Проверка занесения водителя
            if self.is_driver_exists(driver):
                driver_df = df[df['driverName'] == driver]

                for i in range(1, 6): 
                    existing_phone = driver_df[f'Phone_{i}'].values[0]

                    if i <= len(phones):  # Если есть новый номер для этого поля
                        if pd.isnull(existing_phone) or str(phones[i - 1]) not in str(existing_phone):
                            # Обновление номера телефона и установка Sync_Status в Unsync
                            df.loc[df['driverName'] == driver, f'Phone_{i}'] = phones[i - 1]
                            df.loc[df['driverName'] == driver, 'Sync_Status'] = 'Unsync'
                    else:  # Если нет нового номера для этого поля, удаление старого
                        if not pd.isnull(existing_phone):
                            df.loc[df['driverName'] == driver, f'Phone_{i}'] = pd.NA
                            df.loc[df['driverName'] == driver, 'Sync_Status'] = 'Unsync'
            else:
                # Добавление новой строки в DataFrame
                df = pd.concat([df, pd.DataFrame([new_row_dict])], ignore_index=True)

        # Сохранение DataFrame в Excel файл
        df.to_excel(self.FILEDIR, index=False, header=True)

    def update_sync(self, driverDict):

        df = self.check()  # DataFrame

        for driver, data in driverDict.items():
            data_dict = {k: v for d in data for k, v in d.items()}  # Преобразование списка словарей в один словарь

            # Создаем словарь для обновления данных в DataFrame
            update_dict = {
                'ID': data_dict.get('emp_id', ''),  # emp_id, если он есть, иначе отравка пустой строки
                'resourceName': data_dict.get('resourceName', ''),
                # resourceName, если он есть, иначе оставка пустой строки
                'Sync_Status': 'Sync',  # -> Sync_Status в 'Sync'
            }

            # Если водитель уже существует в DataFrame, обновление его данных
            if self.is_driver_exists(driver):
                for key, value in update_dict.items():
                    df.loc[df['driverName'] == driver, key] = value
            else:
                print(f"Водитель {driver} не найден в DataFrame. Проверьте данные.")

        # Сохранение обновленного DataFrame в Excel файл
        df.to_excel(self.FILEDIR, index=False, header=True)

    def get_unsynced(self):
        df = self.check()  # DataFrame

        # unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        # unsynced_rows = df[:]

        # Создание списка для хранения результатов
        result = []

        for _, row in unsynced_rows.iterrows():
            # Получение позиции, имя и номера телефонов из строки
            position = row['Position']
            name = row['driverName']
            phone_numbers = [str(int(row[f'Phone_{i}'])) for i in range(1, 6) if pd.notna(row[f'Phone_{i}'])]
            group = row['Group']
            resourceName = row['resourceName']

            # Добавление кортежа с данными в список результатов
            result.append((position, name, phone_numbers, group, resourceName))

        return result

    def get_all_contacts(self):
        df = self.check()  # DataFrame

        # unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        # unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        unsynced_rows = df[:]

        # Создание списка для хранения результатов
        result = []

        for _, row in unsynced_rows.iterrows():
            # Получение позиции, имени и номера телефонов из строки
            position = row['Position']
            name = row['driverName']
            phone_numbers = [str(int(row[f'Phone_{i}'])) for i in range(1, 6) if pd.notna(row[f'Phone_{i}'])]
            group = row['Group']
            resourceName = row['resourceName']

            # Добавление кортежа с данными в список результатов
            result.append((position, name, phone_numbers, group, resourceName))

        return result

    def get_gph(self):
        df = self.check()  # DataFrame

        # unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        # unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        unsynced_rows = df[:]

        # Создание списка для хранения результатов
        result = []

        for _, row in unsynced_rows.iterrows():
            # Получение позиции, имени и номера телефонов из строки
            Job_Phone = row['Job_Phone']
            name = row['driverName']
            resourceName = row['resourceName']

            # Кортеж с данными в список результатов
            result.append((Job_Phone, name, resourceName))

        # Список результатов
        return result

    def remove_nonexistent(self, driverDict):
        df = self.check()  # DataFrame
        df_names = df['driverName'].tolist()  # Получение списка всех имен водителей в DataFrame
        dict_names = list(driverDict.keys())  # Получение списка имен водителей в предоставленном словаре

        # Проверка имени водителя в DataFrame
        for name in df_names:
            # Если имя водителя не найдено в предоставленном словаре, удаление строки с этим именем
            if name not in dict_names:
                df = df[df.driverName != name]

        # Сохранение обновленный DataFrame в Excel файл
        df.to_excel(self.FILEDIR, index=False, header=True)



