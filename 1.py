import glob


in_sys_file = glob.glob('test_files/*SYS*')
print(in_sys_file[0])


def parsing(file_path, prefix):
    """Функция создания списка из строк с префиксами передаваемых в prefix"""
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
                d = attribute+';'+value               # Склеиваем в новую строку с разделителм ';'
                a = d.split(';')                      # Режем строку на список по разделителю ';'
                result.append(a)                      # Вставляем полученый список как элемент результирующего списка
            else:
                continue
    return result


if __name__ == '__main__':
    print(parsing(in_sys_file[0], "alias."))
    print(parsing(in_sys_file[0], "zone."))

