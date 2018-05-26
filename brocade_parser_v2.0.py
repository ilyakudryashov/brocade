import os
import csv
import fnmatch
import tkinter


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


def csv_writer(data, file_name):
    """
    Запись в CSV файл
    """
    with open(os.getcwd()+'/'+file_name, "w", newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in data:
            writer.writerow(line)


def parsing_sshow_sys(value, in_csv=False):
    """
    Парсим все найденные по маске *SSHOW_SYS.txt файлы (поиск alias и zone) и складываем в csv, если in_csv=True
    Если in_csv=False возращаем результат поискаю
    :return:    возращает найденное
    """
    result = []
    find = value+'.'
    for file in find_all_files_by_template_in_subdirs('*SSHOW_SYS.txt'):
        parsing_result = parsing(file, find)
        cfg = parsing(file, "cfg.", no_value=True)
        if in_csv:
            csv_writer(parsing_result, cfg + "_" + value + ".csv")
            result = None
        else:
            result.append(parsing_result)
    return result


def load_sshow_sys(value):
    text_result.delete('1.0', 'end')
    text_result.insert('1.0', parsing_sshow_sys(value))


if __name__ == '__main__':
    root = tkinter.Tk()
    root.title('Brocade Parser v2.0')
    root.minsize(800, 450)

    frame_button = tkinter.Frame(root, bg='gray15', border=1, relief='raise')
    frame_text = tkinter.LabelFrame(root, bg='gray15', border=1, relief='flat', text='Результат:', fg='sienna1')

    frame_button.pack(side='top', fill='both')
    frame_text.pack(side='top', fill='both')

    # ---frame_button---
    button_alias_to_csv = tkinter.Button(frame_button, text="alias->CSV", bg='gray20', fg='sienna1', font='Arial 8',
                                         relief='raise', overrelief='sunken', activebackground='sienna1')
    button_zone_to_csv = tkinter.Button(frame_button, text="zone->CSV", bg='gray20', fg='sienna1', font='Arial 8',
                                        relief='raise', overrelief='sunken', activebackground='sienna1')
    button_load_alias_in_text = tkinter.Button(frame_button, text="показать все alias", bg='gray20', fg='sienna1',
                                               font='Arial 8', relief='raise', overrelief='sunken',
                                               activebackground='sienna1')

    button_alias_to_csv.pack(side='left')
    button_zone_to_csv.pack(side='left')
    button_load_alias_in_text.pack(side='left')
    # ------------------

    # ---frame_text-----
    text_result = tkinter.Text(frame_text, font='Arial 7', bg='gray20', fg='sienna1')
    scrollbar_text_result = tkinter.Scrollbar(frame_text, bg='gray20', activebackground='gray20')
    scrollbar_text_result['command'] = text_result.yview
    text_result['yscrollcommand'] = scrollbar_text_result.set

    text_result.pack(side='left', fill='both')
    scrollbar_text_result.pack(side='right', fill='y')
    # ------------------

    button_alias_to_csv.bind("<Button-1>", lambda event: parsing_sshow_sys('alias', in_csv=True))
    button_zone_to_csv.bind("<Button-1>", lambda event: parsing_sshow_sys('zone', in_csv=True))
    #button_load_alias_in_text("<Button-1>", load)
    load_sshow_sys('alias')

    root.mainloop()


