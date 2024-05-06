from pathlib import Path
import patoolib
import os
from datetime import datetime, timedelta
import math
import argparse
import sys
import json


FileList = []                               # Общий список файлов
FormatList = []                             # Список с некопируемыми форматами
count_one_arch_file = 100                   # Количество файлов внутри одного архива
formats = (".py", ".ipynb",                 # Форматы для архивации
            ".html", ".txt",
            ".json", ".xlsx",
            ".bat", ".ps1",
            ".xlsb", ".zp",
            ".docx", )

cwd = os.getcwd()                           # Получение текущей директории
folderName = os.path.basename(cwd)          # Получение имени папки

# Список слов для остановка копирования
stopWords = [f'{folderName}/venv', f'{folderName}/backup',
            f'venv', f'backup',
            f'Lib', f'Backup']


# Проверка вхождения в список стоп слов внутри адреса
def find_stop_words(s_word):
    for i in stopWords:
        if str(s_word.find(i)) != '-1':
            return True
    return False


# Получение именованных аргументов при вызове функции
def createParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument ('-c', '--comment', default=False)

    return parser


# Получение текущей даты времени
def get_datetime():
    now = int(datetime.timestamp(datetime.now()))
    date_ = datetime.utcfromtimestamp(now).strftime('%Y-%m-%d %H:%M:%S')
    d_day = int(date_[8:10])
    d_month = int(date_[5:7])
    d_year = int(date_[0:4])
    t_hour = int(date_[11:13])
    t_minute = int(date_[14:16])
    t_second = int(date_[17:19])
    objectDate = str(datetime(d_year, d_month, d_day,
                                t_hour, t_minute, t_second) + timedelta(hours = 3)).replace(":", "-")
    return objectDate


# Проверка существования папки Backup
def generate_backup_folder():
    var = os.path.exists(f'{cwd}/backup')
    if not var:
        os.mkdir(f'{cwd}/backup')
    return var


# Создание папки datetime
def generate_datetime_folder():
    name_date_folder = get_datetime()
    var = os.path.exists(f'{cwd}/backup/{name_date_folder}')
    if not var:
        os.mkdir(f'{cwd}/backup/{name_date_folder}')
    return name_date_folder


# Генерация списка файлов
def checkDir(dvdv):
    r_Bool = dvdv.endswith(formats)
    return r_Bool


# Фильтрация файлов в папках
for top, dirs, files in os.walk(cwd):
    for nm in files:
        if find_stop_words(top):
            continue

        # Проверка искомого расширения
        if checkDir(nm):
            FileList.append(os.path.join(top, nm).replace(cwd + os.sep, ''))

        # Добавление в исключенные расширения
        if not checkDir(nm):
            # Проверка вхождения

            ra = Path(os.path.join(top, nm)).suffix
            if not ra in FormatList:
                FormatList.append(ra)

def multi_copy(cur_count_len_arch, comment_wr):
    text_log = []
    count_exit = False
    r_list_archive = []
    count_string = 0
    created_archives = []  # Список созданных архивов

    generate_backup_folder()
    dateVar = generate_datetime_folder()

    # Создание архивов с частями файлов
    for i in range(cur_count_len_arch):
        for ii in range(count_one_arch_file):
            try:
                r_list_archive.append(FileList[count_string])
                var_log = f'part {i + 1} - {FileList[count_string]}'
                text_log.append(var_log)
                count_string += 1
            except IndexError:
                archive_name = f'{folderName}-backup-{dateVar}_part_{i + 1}.zip'.replace(':', '-')
                archive_path = f'{cwd}/backup/{dateVar}/{archive_name}'
                patoolib.create_archive(archive_path, tuple(r_list_archive))
                created_archives.append(archive_path)
                count_exit = True
                break

        if not count_exit:
            archive_name = f'{folderName}-backup-{dateVar}_part_{i + 1}.zip'.replace(':', '-')
            archive_path = f'{cwd}/backup/{dateVar}/{archive_name}'
            patoolib.create_archive(archive_path, tuple(r_list_archive))
            created_archives.append(archive_path)
            r_list_archive = []

    # Запись лога
    output_txt_path = f'{cwd}/backup/{dateVar}/output.txt'
    MyFile = open(output_txt_path, 'w')
    MyFile.write(f"Len archive: {len(FileList)}")
    MyFile.write('\n')
    MyFile.write(f"Allowed formats: {formats}")
    MyFile.write('\n')
    if len(FormatList) > 0:
        MyFile.write(f"This formats is not copied: {FormatList}")
        MyFile.write('\n')
    MyFile.write('\n')
    for element in text_log:
        MyFile.write(element)
        MyFile.write('\n')
    MyFile.close()

    # Запись комментария
    comment_txt_path = f'{cwd}/backup/comment.txt'
    MyFile = open(comment_txt_path, 'a')
    comment = f'{dateVar} - {comment_wr}'
    MyFile.write(comment)
    MyFile.write('\n')
    MyFile.close()

    # Если создано больше одного архива, упаковываем их в один и удаляем старые
    if len(created_archives) > 1:
        created_archives.extend([output_txt_path, comment_txt_path])  # Добавляем output.txt и comment.txt
        common_archive_name = f'{folderName}-backup-{dateVar}_common.zip'.replace(':', '-')
        common_archive_path = f'{cwd}/backup/{dateVar}/{common_archive_name}'
        patoolib.create_archive(common_archive_path, tuple(created_archives))

        # Удаляем старые архивы, output.txt и comment.txt
        for archive_path in created_archives:

            # Пропуск удаления комментариев
            if "comment.txt" in archive_path:
                continue

            os.remove(archive_path)


if __name__ == '__main__':

    # Обработка комментария
    parser = createParser()
    commentSpace = parser.parse_args(sys.argv[1:])

    # Получение количества итераций
    cur_count_len_arch = len(FileList) // count_one_arch_file
    if (cur_count_len_arch * count_one_arch_file) < len(FileList):
        cur_count_len_arch += 1

    # Определение количества файлов за итерацию
    iteration_step_arch = len(FileList) // cur_count_len_arch

    # Вызов функции копирования
    comment = str(commentSpace.comment)#.replace('-', ' ').replace('_', ' ')
    multi_copy(cur_count_len_arch, comment)

print("Allowed formats:", formats)
print()
if len(FormatList) > 0:
    print("This formats is not copied:", FormatList)
print('Len archive:', len(FileList))