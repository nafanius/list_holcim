import pickle
from datetime import datetime, timedelta



def save_dict_to_pickle(dictionary, filename):
    """
    Сохраняет словарь в файл формата pickle.

    :param dictionary: Словарь, который нужно сохранить.
    :param filename: Имя файла, в который будет сохранен словарь.
    """

    with open(filename, 'wb') as f:
        pickle.dump(dictionary, f)



def load_dict_from_pickle(filename):
    """
    Загружает список из файла формата pickle.

    :param filename: Имя файла, из которого нужно загрузить словарь.
    :return: Загруженный словарь.
    """
    try:
        with open(filename, 'rb') as f:
            return pickle.load(f)
    except Exception as err:
        print(err)
        return {}

def get_list_of_beton():
    '''формирует из сохраненого списка актуальный удаляет записи с датой меньше текущей'''
    try:
        dict_old_of_beton = load_dict_from_pickle("old_dic_of_beton.pkl")
        dict_new_of_beton = dict_old_of_beton.copy()
        now = datetime.now()
        for item in dict_old_of_beton.keys():
            if datetime.strptime(item, '%d.%m.%Y') < datetime(year=now.year, month=now.month, day=now.day):
                del dict_new_of_beton[item]

        print(dict_new_of_beton)
        return dict_new_of_beton
    except Exception as err:
        print(err)
        return {}

def combine_dict_from_get_list(dict_of_day):
    current_dic = get_list_of_beton()
    save_dict_to_pickle(current_dic | dict_of_day, "old_dic_of_beton.pkl")

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
    return del_lista, add_lista


