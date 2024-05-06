from pandas import pandas as pd
import os


# Проверка существования DF Central
class OfficeCentral:
    """
        check - Проверка существования \ пересоздания DF (метод класса)

        is_driver_exists - Проверка занесения водителя (метод класса)

        write - занесение водителя
        IN: {'Зайцев Александр Геннадьевич': ['79..8011139'], 'Телегин Вадим Евгеньевич': ['791..454975', '79777..2105'], 'Закарая Лука Элгуджаевич': ['7916..88936']}

        update_sync - обновляет файл адаптации после синхнронизации с Google
        IN: transformation_contacts_one - {'Second employee': [{'emp_id': 'b7c345d8aeeac62'}, {'resourceName': 'people/c82759..07896829026'}, {'position': '!Стажер'}, {'driverName': 'Second employee'}, {'phoneNumbers': ['799..234567', '799..654321']}]}

        get_unsynced - возвращает информацию из DF адаптация Unsync
        OUT: [('!Стажер', 'Зайцев Александр Геннадьевич', ['798..011139'], 'Adaptation')]


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

    def write(self, car_dict, groupName):
        # DataFrame с заданными заголовками
        df = self.check()

        for i in car_dict.keys():
            emp_data = car_dict.get(i)
            emp_type = emp_data.get('empType')
            emp_name = emp_data.get('empName')
            phone = emp_data.get('empPhone')

            # Новый словарь для новой строки со всеми полями телефона пустыми
            new_row_dict = {
                'driverName': emp_name,
                'ID': '',
                'Position': emp_type,
                'Group': groupName,
                'resourceName': '',
                'Sync_Status': 'Unsync',
                'Enable_Status': '',
                'Job_Phone': '',
                'Phone_1': '',
                'Phone_2': '',
                'Phone_3': '',
                'Phone_4': '',
                'Phone_5': '',
            }

            # Присваиваивание номера телефонов доступным полям
            for i in range(len(phone)):
                new_row_dict[f'Phone_{i + 1}'] = phone[i]


            # Проверка занесения водителя
            if self.is_driver_exists(emp_name):
                driver_df = df[df['driverName'] == emp_name]

                for i in range(1, 6): 
                    existing_phone = driver_df[f'Phone_{i}'].values[0]

                    if i <= len(phone):  # Если есть новый номер для этого поля
                        if pd.isnull(existing_phone) or str(phone[i - 1]) not in str(existing_phone):
                            # Обновление номера телефона и установка Sync_Status в Unsync
                            df.loc[df['driverName'] == emp_name, f'Phone_{i}'] = phone[i - 1]
                            df.loc[df['driverName'] == emp_name, 'Sync_Status'] = 'Unsync'
                    else:  # Если нет нового номера для этого поля, удаление старого
                        if not pd.isnull(existing_phone):
                            df.loc[df['driverName'] == emp_name, f'Phone_{i}'] = pd.NA
                            df.loc[df['driverName'] == emp_name, 'Sync_Status'] = 'Unsync'
            else:
                # Добавление новой строки в DataFrame
                df = pd.concat([df, pd.DataFrame([new_row_dict])], ignore_index=True)

        # DataFrame в Excel файл
        df.to_excel(self.FILEDIR, index=False, header=True)

    def update_sync(self, driverDict):
        df = self.check()  # Загрузка DataFrame

        for driver, data in driverDict.items():
            data_dict = {k: v for d in data for k, v in d.items()}

            # Создание словаря для обновления данных в DataFrame
            update_dict = {
                'ID': data_dict.get('emp_id', ''), 
                'resourceName': data_dict.get('resourceName', ''),
                'Sync_Status': 'Sync',
            }

            # Если водитель уже существует в DataFrame
            if self.is_driver_exists(driver):
                for key, value in update_dict.items():
                    df.loc[df['driverName'] == driver, key] = value
            else:
                print(f"Водитель {driver} не найден в DataFrame. Проверьте данные.")

        # Сохранение DataFrame в Excel файл
        df.to_excel(self.FILEDIR, index=False, header=True)

    def get_unsynced(self):
        df = self.check()  DataFrame

        # unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        # unsynced_rows = df[:]

        # Список для хранения результатов
        result = []

        for _, row in unsynced_rows.iterrows():
            # Получение позиции, имени и номера телефонов из строки
            position = row['Position']
            name = row['driverName']
            phone_numbers = [str(int(row[f'Phone_{i}'])) for i in range(1, 6) if pd.notna(row[f'Phone_{i}'])]
            group = row['Group']
            resourceName = row['resourceName']

            # Добавление кортеж с данными в список результатов
            result.append((position, name, phone_numbers, group, resourceName))

        # Возвращение списка результатов
        return result

    def get_all_contacts(self):
        df = self.check()  # Загрузка DataFrame

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

            # Кортеж с данными в список результатов
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

            # Добавление кортежа с данными в список результатов
            result.append((Job_Phone, name, resourceName))

        # Возвращ список результатов
        return result

    def remove_nonexistent(self, driverDict):
        df = self.check()  # Загрузка DataFrame
        df_names = df['driverName'].tolist()  # Получение списка всех имен водителей в DataFrame
        dict_names = list(driverDict.keys())  # Получение списка имен водителей в предоставленном словаре

        # Проверка каждого имя водителя в DataFrame
        for name in df_names:
            # Если имя водителя не найдено в предоставленном словаре, удаление строки с этим именем
            if name not in dict_names:
                df = df[df.driverName != name]

        # Сохранение обновленного DataFrame в Excel файл
        df.to_excel(self.FILEDIR, index=False, header=True)

    def add_phone(self, driver_name, phone):
        df = self.check()  # Загрузка текущего DataFrame

        # Проверка, есть ли водитель в базе данных
        if self.is_driver_exists(driver_name):
            df.loc[df['driverName'] == driver_name, 'Job_Phone'] = phone 

            # Сохранение DataFrame в Excel файл
            df.to_excel(self.FILEDIR, index=False, header=True)
        else:
            print(f"Водитель {driver_name} не найден в базе данных.")



