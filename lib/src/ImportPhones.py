from re import split, sub, search


class ImportPhones:
    """
        input: "89607618651 варвара +7(960)279-58-04   +79632651314"
        output: ["79607618651", "79602795804"]

    """

    @staticmethod
    def get_list(string):
        def f(x):
            s = search(r'[7|8]\d{10}|[^0]\d{9}', sub(r'[^\d]', '', x))
            return s and s[0] or ''

        try:
            listNumbers = [f(i) for i in split(r'[^\d\s\+\(\)-]+', str(string))]

        except TypeError:
            return 'Телефон не найден'

        # Очистка списка от пустых значений
        listNumbers = list(filter(None, listNumbers))

        corrected_listNumbers = []

        for i in listNumbers:

            firstSymb = i[0] == '4' or i[0] == '9'
            correctLen10 = len(i) == 10

            # Если первый символ 9 или 4 и длина на 1 меньше
            if firstSymb and correctLen10:
                correctNumber = f'7{i}'
                corrected_listNumbers.append(correctNumber)

            # Если первый символ 8 и длина норм
            correctLen11 = len(i) == 11

            if i[0] == '8' and correctLen11:
                fSymb = i[1:]
                cSymb = f'7{fSymb}'
                corrected_listNumbers.append(cSymb)

            if i[0] == '7' and correctLen11:
                fSymb = i[:]
                corrected_listNumbers.append(fSymb)

        # Если нет корректных номеров телефонов
        if not corrected_listNumbers:
            return 'Телефон не найден'

        return corrected_listNumbers

# tt = '8 929 932-35-23, +7 916 038-86-52, '
# print(ImportPhones.get_list(tt))