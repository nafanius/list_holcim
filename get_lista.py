import ezsheets

import openpyxl
from datetime import time
from datetime import datetime, timedelta
import os


def generate_name_of_file_google():
    """генерируем файлы для загрузки"""
    list_of_download_files = []

    now = datetime.now()
    current_week_number = now.isocalendar()[1]
    current_year = now.year
    list_of_download_files.append(f"Tydz {current_week_number}.{current_year}")
    list_of_download_files.append(f"Tydz {current_week_number + 1}.{current_year}")

    return list_of_download_files


def get_from_google_sheet():
    for file in generate_name_of_file_google():
        try:
            directory = 'excel_files'
            ss = ezsheets.Spreadsheet(file)
            ss_name = ss.title
            file_path = os.path.join(directory, f'{ss_name}.xlsx')
            ss.downloadAsExcel(file_path)
        except:
            print("ERRR")
            continue


def form_lista(excel_file, day):
    '''дастоём расписание из файла'''
    lista = []
    try:
        wb = openpyxl.load_workbook(excel_file)
    except:
        print("такого файла нет " + excel_file)
        return []
    sheet = wb[wb.sheetnames[day]]

    def fill_list(time_str, row, column):
        if isinstance(time_str, time):
            lista.append((time_str, (sheet.cell(row=row, column=column - 1).value).strip()))

    for row_in_file in range(1, sheet.max_row):
        c = sheet.cell(row=row_in_file, column=3).value
        if "zawodzie 2 " in str(c).lower() or "zawodzie 1 " in str(c).lower():
            for row_in_list_time in range(15):
                fill_list(sheet.cell(row=row_in_file + row_in_list_time, column=12).value,
                          row_in_file + row_in_list_time, 12)
                fill_list(sheet.cell(row=row_in_file + row_in_list_time, column=15).value,
                          row_in_file + row_in_list_time, 15)

    lista = sorted(lista, key=lambda event: event[0])

    return lista


def lista_in_bot(lista):
    """"фотрмируем list в текстовый формат для высолки в бот """

    if not lista:
        return ""
    lista_text = ""
    for time, person in lista:
        lista_text += f"{time.strftime('%H:%M')} {person}\n"

    return lista_text


def find_day_request():
    list_of_days = []

    now = datetime.now()
    # Извлекаем номер недели с помощью isocalendar
    current_week_number = now.isocalendar()[1]
    day_of_week = now.weekday()
    current_year = now.year
    if day_of_week in (0, 1, 2, 3):
        list_of_days.append((day_of_week, f"./excel_files/Tydz {current_week_number}.{current_year}.xlsx",
                             now.strftime('%d.%m.%Y')))
        list_of_days.append((day_of_week + 1, f"./excel_files/Tydz {current_week_number}.{current_year}.xlsx",
                             (now + timedelta(days=1)).strftime('%d.%m.%Y')))
        list_of_days.append((day_of_week + 2, f"./excel_files/Tydz {current_week_number}.{current_year}.xlsx",
                             (now + timedelta(days=2)).strftime('%d.%m.%Y')))
    elif day_of_week == 4:
        list_of_days.append((day_of_week, f"./excel_files/Tydz {current_week_number}.{current_year}.xlsx",
                             now.strftime('%d.%m.%Y')))
        list_of_days.append((day_of_week + 1, f"./excel_files/Tydz {current_week_number}.{current_year}.xlsx",
                             (now + timedelta(days=1)).strftime('%d.%m.%Y')))
        list_of_days.append((0, f"./excel_files/Tydz {current_week_number + 1}.{current_year}.xlsx",
                             (now + timedelta(days=3)).strftime('%d.%m.%Y')))
    elif day_of_week == 5:
        list_of_days.append((day_of_week, f"./excel_files/Tydz {current_week_number}.{current_year}.xlsx",
                             now.strftime('%d.%m.%Y')))
        list_of_days.append((0, f"./excel_files/Tydz {current_week_number + 1}.{current_year}.xlsx",
                             (now + timedelta(days=2)).strftime('%d.%m.%Y')))
        list_of_days.append((1, f"./excel_files/Tydz {current_week_number + 1}.{current_year}.xlsx",
                             (now + timedelta(days=2)).strftime('%d.%m.%Y')))

    elif day_of_week == 6:
        list_of_days.append((0, f"./excel_files/Tydz {current_week_number + 1}.{current_year}.xlsx",
                             (now + timedelta(days=2)).strftime('%d.%m.%Y')))
        list_of_days.append((1, f"./excel_files/Tydz {current_week_number + 1}.{current_year}.xlsx",
                             (now + timedelta(days=2)).strftime('%d.%m.%Y')))
        list_of_days.append((2, f"./excel_files/Tydz {current_week_number + 1}.{current_year}.xlsx",
                             (now + timedelta(days=2)).strftime('%d.%m.%Y')))

    return list_of_days

def combination_of_some_days_list():
    """формируем общий лист на несколько дней в зависимости от дня недели"""
    get_from_google_sheet()
    dict_list = {}
    number_day = 1
    for day, file, date in find_day_request():

        dict_list[number_day] = [f"***{date}***",  (lista_in_bot(form_lista(file, day))).split("\n")]
        number_day += 1


    return dict_list

if __name__ == '__main__':
    print(combination_of_some_days_list())
