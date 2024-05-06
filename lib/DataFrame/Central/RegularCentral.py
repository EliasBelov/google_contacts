from pandas import pandas as pd
import os


# Проверка существования DF Central
class RegularCentral:
    """
        check - Проверка существования \ пересоздания DF (метод класса)

        is_driver_exists - Проверка занесения водителя (метод класса)

        write - занесение водителя
        IN: {'Зайцев Александр Геннадьевич': ['798..11139'], 'Телегин Вадим Евгеньевич': ['791..54975', '797..02105'], 'Закарая Лука Элгуджаевич': ['791..88936']}

        update_sync - обновляет файл адаптации после синхнронизации с Google
        IN: transformation_contacts_one - {'Second employee': [{'emp_id': 'b7c345d8aeeac62'}, {'resourceName': 'people/c827594007896829026'}, {'position': '!Стажер'}, {'driverName': 'Second employee'}, {'phoneNumbers': ['799..34567', '799..54321']}]}

        get_unsynced - возвращает информацию из DF адаптация Unsync
        OUT: [('!Стажер', 'Зайцев Александр Геннадьевич', ['798...11139'], 'Adaptation')]


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

        df = self.check()

        for i in car_dict.keys():
            car_data = car_dict.get(i)
            car_type = car_data.get('carType')
            car_name = car_data.get('carName')
            phone = [str(car_data.get('carPhone')).replace('.0',''), ]


            new_row_dict = {
                'driverName': car_name, 
                'ID': '',
                'Position': car_type,
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

            # Присваивание номера телефонов доступным полям
            for i in range(len(phone)):
                new_row_dict[f'Phone_{i + 1}'] = phone[i]

            # Проверка занесения водителя
            if self.is_driver_exists(car_name):
                driver_df = df[df['driverName'] == car_name]

                for i in range(1, 6): # Прохождение по телефонным полям
                    existing_phone = driver_df[f'Phone_{i}'].values[0]

                    if i <= len(phone):  # Если есть новый номер для этого поля
                        if pd.isnull(existing_phone) or str(phone[i - 1]) not in str(existing_phone):
                            # Обновление номера телефона и установка Sync_Status в Unsync
                            df.loc[df['driverName'] == car_name, f'Phone_{i}'] = phone[i - 1]
                            df.loc[df['driverName'] == car_name, 'Sync_Status'] = 'Unsync'
                    else:  # Если нет нового номера для этого поля -> удаление номера
                        if not pd.isnull(existing_phone):
                            df.loc[df['driverName'] == car_name, f'Phone_{i}'] = pd.NA
                            df.loc[df['driverName'] == car_name, 'Sync_Status'] = 'Unsync'
            else:

                df = pd.concat([df, pd.DataFrame([new_row_dict])], ignore_index=True)

        # Сохранение DataFrame в Excel файл
        df.to_excel(self.FILEDIR, index=False, header=True)

    def update_sync(self, driverDict):
        df = self.check()  
        for driver, data in driverDict.items():
            data_dict = {k: v for d in data for k, v in d.items()}

            # Создание словаря для обновления данных в DataFrame
            update_dict = {
                'ID': data_dict.get('emp_id', ''), 
                'resourceName': data_dict.get('resourceName', ''),

                'Sync_Status': 'Sync',  
            }

            # Если водитель уже существует в DataFrame, обновление данных
            if self.is_driver_exists(driver):
                for key, value in update_dict.items():
                    df.loc[df['driverName'] == driver, key] = value
            else:
                print(f"Водитель {driver} не найден в DataFrame. Проверьте данные.")

        # Сохранение обновленного DataFrame в Excel файл
        df.to_excel(self.FILEDIR, index=False, header=True)

    def get_unsynced(self):
        df = self.check() 

        # unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        # unsynced_rows = df[:]

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

            # Добавление кортеж с данными в список результатов
            result.append((position, name, phone_numbers, group, resourceName))

        # Возвращение списка результатов
        return result

    def get_gph(self):
        df = self.check()

        # unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        # unsynced_rows = df[df['Sync_Status'] == 'Unsync']
        unsynced_rows = df[:]

        # Создание списка для хранения результатов
        result = []

        for _, row in unsynced_rows.iterrows():
            # Получение позиции, имя и номера телефонов из строки
            Job_Phone = row['Job_Phone']
            name = row['driverName']
            resourceName = row['resourceName']

            # Добавление кортежа с данными в список результатов
            result.append((Job_Phone, name, resourceName))

        return result

    def remove_nonexistent(self, driverDict):
        df = self.check()  # DataFrame
        df_names = df['driverName'].tolist()
        dict_names = list(driverDict.keys())

        # Проверка каждого имени водителя в DataFrame
        for name in df_names:
            # Если имя водителя не найдено в предоставленном словаре -> удаление строки
            if name not in dict_names:
                df = df[df.driverName != name]

        # Сохранение обновленный DataFrame в Excel файл
        df.to_excel(self.FILEDIR, index=False, header=True)

    def add_phone(self, driver_name, phone):
        df = self.check()  # Загрузка текущий DataFrame

        # Проверка, есть ли водитель в базе данных
        if self.is_driver_exists(driver_name):
            df.loc[df['driverName'] == driver_name, 'Job_Phone'] = phone 
            # Сохранение DataFrame в Excel файл
            df.to_excel(self.FILEDIR, index=False, header=True)
        else:
            print(f"Водитель {driver_name} не найден в базе данных.")



