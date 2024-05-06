def find_missing_phones(df_adaptation_list, google_dict, fio):
    """
        Функция сравнивает телефоны внутри списка с телефонами внутри словаря.
        По умолчанию, функция предназначается для поиска новых телефонов внутри DF для выявления новых телефонов

        example in data:
            df_adaptation_list = [('!Стажер', 'Зайцев Александр Геннадьевич', ['798..011139'], 'Adaptation'), ('!Стажер', 'Телегин Вадим Евгеньевич', ['791..454975', '797..002105'], 'Adaptation'), ('!Стажер', 'Закарая Лука Элгуджаевич', ['791..288936', '792..811111'], 'Adaptation')]
            google_dict = {'Зайцев Александр Геннадьевич': [{'emp_id': '6e41118a8ad60d45'}, {'resourceName': 'people/c7944650504390708549'}, {'position': '!Стажер'}, {'driverName': 'Зайцев Александр Геннадьевич'}, {'phoneNumbers': ['798..011139']}], 'Телегин Вадим Евгеньевич': [{'emp_id': '1cb720c38eeb9216'}, {'resourceName': 'people/c2069158578088546838'}, {'position': '!Стажер'}, {'driverName': 'Телегин Вадим Евгеньевич'}, {'phoneNumbers': ['791..454975', '797..002105']}], 'Закарая Лука Элгуджаевич': [{'emp_id': '515ea68f09700d6d'}, {'resourceName': 'people/c5863306898151837037'}, {'position': '!Стажер'}, {'driverName': 'Закарая Лука Элгуджаевич'}, {'phoneNumbers': ['791..288936']}]}
            fio = 'Зайцев Александр Геннадьевич'
"""

    missing_phones = []

    # Iterate over the df_adaptation_list
    for i in df_adaptation_list:
        # Check if the name is the same as the fio parameter
        if i[1] == fio:
            # Check if this fio is in the google_dict
            if i[1] in google_dict:
                employee_data = google_dict[i[1]]
                employee_phones = [phone['phoneNumbers'] for phone in employee_data if 'phoneNumbers' in phone]
                employee_phones = [phone for sublist in employee_phones for phone in
                                   sublist]  # Flatten nested lists

                # Check each phone in df_adaptation_list
                for phone in i[2]:
                    # If this phone isn't in the google_dict, add it to the missing_phones
                    if phone not in employee_phones:
                        missing_phones.append(phone)

    return missing_phones