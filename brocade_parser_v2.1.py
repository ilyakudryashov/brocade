import os
import gzip
import fnmatch


class _SupportSaveFile:
    """
    Работа с файлами из supportsave
    """
    file_type = None
    file_full_path = None
    file_path = None
    file_name = None
    file_content = None
    target_path = None
    cfg_name = None

    def __init__(self, path):
        self.file_full_path = path
        self.target_path = os.getcwd()
        (self.file_path, self.file_name) = os.path.split(path)
        if 'SSHOW_SYS' in path:
            self.file_type = 'sys'
            self.cfg_name = self.parsing(self.file_full_path, "cfg.", no_value=True)
        elif 'SSHOW_FABRIC' in path:
            self.file_type = 'fabric'
        else:
            self.file_type = 'unknown'
        if '.gz' in path:
            self.file_content = gzip.open(path,'rt').read()
        else:
            self.file_content = open(path, "rt", encoding="utf-8")

    def parsing_by_prefix(self, prefix, no_value=False):
        """
        Функция создания списка из строк с префиксами передаваемых в prefix
        """
        result = []
        #with open(file_path, "rt", encoding="utf-8") as f:  # Открываем файл
        for line in self.file_content:
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
        if self.file_type = 'sys':
            for obj in ('alias', 'zone'):
                parsing_result = self.parsing_by_prefix(obj+'.')
                self.csv_writer(parsing_result, self.cfg_name + "_"+obj+".csv")
        else:
            print ('не SYS файл')

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
