import pickle
import time
import os
from datetime import datetime, timedelta

save_number = 1
global_dic = {}

def save_dict_to_pickle(dictionary, directory = "save_old_dict"):
    """Saves the dictionary to a file in pickle format

    Args:
        dictionary (dic): The dictionary to save
        directory (str, optional): the directory where we save.  Defaults to "save_old_dict".
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    # Генерация имени нового файла
    current_time = datetime.now()
    new_filename = f"{current_time.strftime('%Y%m%d_%H%M%S')}.pkl"
    filename = os.path.join(directory, new_filename)

    with open(filename, 'wb') as f:
        pickle.dump(dictionary, f)





def load_dict_from_pickle(hours = 4, directory = "save_old_dict"):
    """Loads a dictionary from the saved oldest file that is not older than the configured time

    Args:
        directory (str, optional): _description_. Defaults to "save_old_dict".
        hours (int):     Defaults to 4

    Returns:
        _type_: _description_
    """

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

    # Deleting files older than 4 hours 
    three_hours_ago = time.time() - hours * 3600
    for file, mtime in files:
        if mtime < three_hours_ago:
            os.remove(os.path.join(directory, file))
            print(f"Удалён файл: {file}")

    # Updating the list of files after deletion
    files = [
        (file, os.path.getmtime(os.path.join(directory, file)))
        for file in os.listdir(directory)
        if os.path.isfile(os.path.join(directory, file))
    ]

    # If there are files, find the oldest one
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
    """Generates an up-to-date list from the saved list by removing entries with
      a date earlier than the current date

    Returns:
        dict: Returns a dictionary with dates that are current as of now.
    """    

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
    """It creates a dictionary from 3 days in 3 iterations, each iteration
     being 1 day. The overall dictionary is saved in the global variable `global_dic`
     and save  summary this dictionary in pickle file

    Args:
        dict_of_day (dict): A single day's dictionary
    """    
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
    """It checks for any removed or new entries in the new dictionary
     compared to the old one and returns two dictionaries: one for
      removed entries and one for new entries

    Args:
        date_of_lista (str): date of day request - '12.03.2024'
        currant_list_beton (list): new list of shipment

    Returns:
        two lists: list of removed entries, list of new entries
    """    
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


