import sqlite3
import os
import csv
import fnmatch


def parsing(file_path, prefix, no_value=False):
    """
    Функция создания списка из строк с префиксами передаваемых в prefix
    """
    result = []
    with open(file_path, "rt", encoding="utf-8") as f:  # Открываем файл
        for line in f:
            line = line.strip()                       # Удаляем пробелы в начале и в конце
            if not line:
                continue
            if line.startswith(prefix):
                s = line.find(':')                    # Ищем первое вхождение ':'  в строке
                attribute = line[len(prefix):s]       # Отрезаем префикс строки, ':' и все что дальше. Присваеваем в att
                value = line[s+1:]                    # Присваеваем в value все что после ':'
                if no_value:
                    result = attribute                # Возращаем att как результат функции, если есть no_value
                else:
                    d = attribute+';'+value           # Склеиваем в новую строку с разделителм ';'
                    a = d.split(';')                  # Режем строку на список по разделителю ';'
                    result.append(a)                  # Вставляем полученый список как элемент результирующего списка
            else:
                continue
    return result


def csv_writer(data, file_name):
    """
    Запись в CSV файл
    """
    with open(os.getcwd()+'/'+file_name, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


def find_all_files_by_template_in_subdirs(pattern, folder=os.getcwd()):
    """
    Ищет все файлы по шаблону (pattern) в указанной папке (folder) и во всех вложенных.
    Если folder не указн то ищется в текущем каталоге
    """
    result = []
    for dirs, subdirs, files in os.walk(folder):
        for filename in fnmatch.filter(files, pattern):
            fullname = os.path.join(dirs, filename)
            result.append(fullname)
    return result


def parsing_sshow_sys(value, in_csv=False):
    """
    Парсим все найденные по маске *SSHOW_SYS.txt файлы (поиск alias и zone) и складываем в csv, если in_csv=True
    Если in_csv=False возращаем результат поиска
    :return:    возращает найденное
    """
    result = None
    find = value+'.'
    for file in find_all_files_by_template_in_subdirs('*SSHOW_SYS.txt'):
        parsing_result = parsing(file, find)
        cfg = parsing(file, "cfg.", no_value=True)
        if in_csv:
            csv_writer(parsing_result, cfg + "_" + value + ".csv")
            result = None
        else:
            result = parsing_result
    return result


def upload_cfg_object_to_db(file, object_name):
    """
    Создает в базе данных таблицу с именем переденным в object_name. В таблицу заносятся данные полученные после
    парсинга файла переданного в file.
    :param file:
    :param object_name:
    :return:
    """
    cursor.execute('CREATE TABLE '+object_name+' ('+object_name+'_id INTEGER PRIMARY KEY AUTOINCREMENT,'+object_name+'_name TEXT,'+object_name+'_members TEXT);')
    find = object_name + '.'
    object = parsing(file, find)
    for i in range(len(object)):
        name = None
        members = ' '
        for j in range(len(object[i])):
            if j == 0:
                name = object[i][j]
            elif j == len(object[i])-1:
                members = members + object[i][j]
            else:
                members = members + object[i][j] + ';'
        cursor.execute('INSERT INTO '+object_name+' ('+object_name+'_name,'+object_name+'_members) VALUES (?,?);', (name, members))


cfg_set = set()
for file in find_all_files_by_template_in_subdirs('*SSHOW_SYS.txt'):
    cfg = parsing(file, "cfg.", no_value=True)
    if cfg in cfg_set:
        pass
    else:
        cfg_set.add(cfg)
        connection = sqlite3.connect(cfg+'.sqlite')
        cursor = connection.cursor()
        upload_cfg_object_to_db(file, 'alias')
        upload_cfg_object_to_db(file, 'zone')
        upload_cfg_object_to_db(file, 'cfg')
        connection.commit()
        connection.close()

"""cursor.executescript('''
    CREATE TABLE alias (
    alias_id INTEGER PRIMARY KEY AUTOINCREMENT,
    alias_name TEXT,
    alias_members TEXT
    );
    CREATE TABLE zone (
    zone_id INTEGER PRIMARY KEY AUTOINCREMENT,
    zone_name TEXT,
    zone_members TEXT
    );
    ''')
upload_alias_to_db()
upload_zones_to_db()"""


