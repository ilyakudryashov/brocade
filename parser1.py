import glob
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


def parsing_config_objects(file):
    """
    Парсит файл по пути переданному в file. Создает два csv файла - с алиасами и зонами.
    :param file:    Необходимо передать полный путь к файлу
    :return:        Ничего не возвращает. Создает файлы
    """
    alias = parsing(file, "alias.")
    zone = parsing(file, "zone.")
    cfg = parsing(file, "cfg.", no_value=True)
    csv_writer(alias, cfg + "_alias.csv")
    csv_writer(zone, cfg + "_zone.csv")


def find_all_files_by_template_in_subdirs(pattern, folder=os.getcwd()):
    """
    Ищет все файлы по шаблону (pattern) в указанной папке (folder) и во всех вложенных.
    Если folder не указн то ищется в текущем каталоге
    """
    result = []
    for root, dirs, files in os.walk(folder):
        for filename in fnmatch.filter(files, pattern):
            fullname = os.path.join(root, filename)
            result.append(fullname)
    return result


if __name__ == '__main__':
    for file in find_all_files_by_template_in_subdirs('*SSHOW_SYS.txt'):
        parsing_config_objects(file)

