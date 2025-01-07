import pickle
import time
import os
from datetime import datetime, timedelta

save_number = 1
global_dic = {}

def save_dict_to_pickle(dictionary, directory = "save_old_dict"):
    """
    Сохраняет словарь в файл формата pickle.

    :param directory:
    :param dictionary: Словарь, который нужно сохранить.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Генерация имени нового файла
    current_time = datetime.now()
    new_filename = f"{current_time.strftime('%Y%m%d_%H%M%S')}.pkl"
    filename = os.path.join(directory, new_filename)

    with open(filename, 'wb') as f:
        pickle.dump(dictionary, f)





def load_dict_from_pickle(directory = "save_old_dict"):
    """
    Загружает список из файла формата pickle.

    :param filename: Имя файла, из которого нужно загрузить словарь.
    :return: Загруженный словарь.
    """
    files = [
        (file, os.path.getmtime(os.path.join(directory, file)))
        for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file))
    ]



    # Удаление файлов старше 3 часов
    three_hours_ago = time.time() - 4 * 3600
    for file, mtime in files:
        if mtime < three_hours_ago:
            os.remove(os.path.join(directory, file))
            print(f"Удалён файл: {file}")

    # Обновляем список файлов после удаления
    files = [
        (file, os.path.getmtime(os.path.join(directory, file)))
        for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file))
    ]

    # Если есть файлы, ищем самый старый
    if files:
        oldest_file = min(files, key=lambda f: f[1])[0]
        filename = os.path.join(directory, oldest_file)

    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception as err:
        print(err)
        return {}

def get_list_of_beton():
    '''формирует из сохраненого списка актуальный удаляет записи с датой меньше текущей'''

    try:
        dict_old_of_beton = load_dict_from_pickle()
        dict_new_of_beton = dict_old_of_beton.copy()
        now = datetime.now()
        for item in dict_old_of_beton.keys():
            if datetime.strptime(item, '%d.%m.%Y') < datetime(year=now.year, month=now.month, day=now.day):
                del dict_new_of_beton[item]

        return dict_new_of_beton
    except Exception as err:
        print(err)
        return {}

def combine_dict_from_get_list(dict_of_day):
    global save_number
    global global_dic
    current_dic = get_list_of_beton()
    print(f"SAVE NUMDER {save_number} ")

    if save_number == 1:
        global_dic = current_dic | dict_of_day
        save_number += 1
    elif save_number != 1 and save_number != 3 :
        global_dic = global_dic | dict_of_day
        save_number += 1
    else:
        global_dic = global_dic | dict_of_day
        save_dict_to_pickle(global_dic)

def check_del_add_lista(date_of_lista, currant_list_beton):
    del_lista = []
    add_lista = []
    current_dic = get_list_of_beton()
    old_stan_lista_beton = current_dic.get(date_of_lista, [])
    for i in old_stan_lista_beton:
        if i not in currant_list_beton:
            del_lista.append(i)
    for i in currant_list_beton:
        if i not in old_stan_lista_beton:
            add_lista.append(i)

    # для контроля отображения
    # del_lista = del_lista + currant_list_beton[2:3]
    # add_lista = add_lista + currant_list_beton[0:2]

    return del_lista, add_lista


