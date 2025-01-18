import threading
import time
import data_sql

db_lock = threading.Lock()

def get_old_list_beton(date, hours = 4):

    threshold = time.time() - hours * 3600

    with db_lock:
        data_sql.delete_records_below_threshold(threshold, "beton")

        return data_sql.get_oldest_list_beton_or_lista("beton", date)
   
    return []

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
    old_stan_lista_beton = get_old_list_beton(date = date_of_lista)
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


if __name__ == "__main__":
    pass