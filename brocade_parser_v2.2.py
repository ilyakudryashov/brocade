import os
import gzip
import fnmatch
import csv
import sqlite3
from pyparsing import *


class _SupportSaveFile:
    """
    Работа с файлами из supportsave
    """
    file_type = None
    file_full_path = None
    file_path = None
    file_name = None
    target_path = None
    cfg_name = None

    def __init__(self, path, target_path=os.getcwd()):
        self.file_full_path = path
        self.target_path = target_path
        (self.file_path, self.file_name) = os.path.split(path)
        if 'SSHOW_SYS' in path:
            self.file_type = 'sys'
            self.cfg_name = self.parsing_cfg_object_by_prefix("cfg.", no_value=True)
        elif 'SSHOW_FABRIC' in path:
            self.file_type = 'fabric'
        elif 'SSHOW_SERVICE' in path:
            self.file_type = 'service'
        else:
            self.file_type = 'unknown'

    def parsing_cfg_object_by_prefix(self, prefix, no_value=False):
        """
        Функция создания списка из строк с префиксами передаваемых в prefix
        """
        result = []
        if 'SSHOW_SYS.txt.gz' in self.file_name:
            gz = gzip.open(self.file_full_path, 'rt')
            fl = list(gz)
        elif 'SSHOW_SYS.txt' in self.file_name:
            fl = open(self.file_full_path, "rt", encoding="utf-8")
        else:
            print("Wrong file, not a SSHOW_SYS")
            return
        for line in fl:
            line = line.strip()  # Удаляем пробелы в начале и в конце
            if not line:
                continue
            if line.startswith(prefix):
                s = line.find(':')  # Ищем первое вхождение ':'  в строке
                attribute = line[len(prefix):s]  # Отрезаем префикс строки, ':' и все что дальше. Присваеваем в att
                value = line[s + 1:]  # Присваеваем в value все что после ':'
                if no_value:
                    result = attribute  # Возращаем att как результат функции, если есть no_value
                else:
                    d = attribute + ';' + value  # Склеиваем в новую строку с разделителм ';'
                    a = d.split(';')  # Режем строку на список по разделителю ';'
                    result.append(a)  # Вставляем полученый список как элемент результирующего списка
            else:
                continue
        return result

    def csv_writer(self, data, file_name):
        """
        Запись в CSV файл
        """
        with open(self.target_path + '/' + file_name, "w", newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=',')
            for line in data:
                writer.writerow(line)

    def upload_cfg_object_to_csv(self):
        if 'sys' in self.file_type:
            for obj in ('alias.', 'zone.', 'cfg.'):
                parsing_result = self.parsing_cfg_object_by_prefix(obj)
                self.csv_writer(parsing_result, self.cfg_name + "_"+obj[:-1]+".csv")
        else:
            print('не SSHOW_SYS файл')

    def insert_cfg_object_to_table(self, object_name, cursor):
        """
        Создает в базе данных таблицу с именем переденным в object_name (подходит только для alias и zone).
        В таблицу заносятся данные полученные после парсинга файла переданного в file.
        :param file:
        :param object_name:
        :return:
        """
        cursor.execute(
            'CREATE TABLE ' + object_name + ' (' + object_name + '_id INTEGER PRIMARY KEY AUTOINCREMENT,' + object_name + '_name TEXT);')
        find = object_name + '.'
        object = self.parsing_cfg_object_by_prefix(find)
        for i in range(len(object)):
            name = str()
            members = str()
            members_column = str()
            for j in range(len(object[i])):
                if j == 0:
                    name = object[i][j]
                elif j == len(object[i]) - 1:
                    members_column = members_column + object_name + '_member' + str(j)
                    members = members + '"' + str(object[i][j]) + '"'
                    try:
                        cursor.execute(
                            'ALTER TABLE ' + object_name + ' ADD COLUMN ' + object_name + '_member' + str(j) + ' TEXT;')
                    except:
                        pass
                else:
                    members_column = members_column + object_name + '_member' + str(j) + ', '
                    members = members + '"' + str(object[i][j]) + '", '
                    try:
                        cursor.execute(
                            'ALTER TABLE ' + object_name + ' ADD COLUMN ' + object_name + '_member' + str(j) + ' TEXT;')
                    except:
                        pass
            cursor.execute(
                'INSERT INTO ' + object_name + ' (' + object_name + '_name, ' + members_column + ') VALUES ("' + name + '", ' + members + ');')

    def upload_cfg_object_to_db(self):
        """

        :return:
        """
        connection = sqlite3.connect(self.target_path+'\\'+self.cfg_name+'.sqlite')
        cursor = connection.cursor()
        self.insert_cfg_object_to_table('alias', cursor)
        self.insert_cfg_object_to_table('zone', cursor)
        #self.insert_cfg_object_to_table('cfg', cursor)
        connection.commit()
        connection.close()

    def parsing_ns_object(self):
        result = []
        if 'SSHOW_SERVICE.txt.gz' in self.file_name:
            gz = gzip.open(self.file_full_path, 'rt')
            fl = list(gz)
        elif 'SSHOW_SERVICE.txt' in self.file_name:
            fl = open(self.file_full_path, "rt", encoding="utf-8")
        else:
            print("Wrong file, not a SSHOW_SERVICE")
            return
        wwn = Word(alphanums + ':')
        FabricPortName = 'Fabric Port Name: ' + wwn
        PermanentPortName = "Permanent Port Name: " + wwn
        datafile = OneOrMore(Group(PermanentPortName^FabricPortName))
        for line in fl:
            line = line.strip()
            try:
                s=datafile.parseString(line)
                list(s)
                print(s)
            except:
                pass


    def upload_ns_object_to_csv(self):
        pass

    def upload_ns_object_to_db(self):
        pass




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


if __name__ == '__main__':
    #work_path = r"C:\Users\ia.kudryashov\Desktop\python_test"
    work_path = os.getcwd()
    cfg_set = set()
    for file in find_all_files_by_template_in_subdirs('*SSHOW_SYS.txt*', work_path):
        SupportSaveFile = _SupportSaveFile(file, work_path)
        cfg = SupportSaveFile.parsing_cfg_object_by_prefix('cfg.', no_value=True)
        if cfg in cfg_set:
            pass
        else:
            cfg_set.add(cfg)

            SupportSaveFile.upload_cfg_object_to_csv()
            SupportSaveFile.upload_cfg_object_to_db()
    #file = r"C:\Users\ia.kudryashov\Desktop\python_test\SSHOW_FABRIC.txt"
    #service = _SupportSaveFile(file, work_path)
    #service.parsing_ns_object()


