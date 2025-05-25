import threading
import time
from data_drive import data_sql
from src.settings import Settings
from collections import Counter 

db_lock = threading.Lock()

def get_old_list_beton(date_of_lista_text, wenzel, hours = Settings.time_of_compare):
    """Get the oldest list of concrete from the database

    Args:
        date_of_lista_text (str): date of day request - '12.03.2024'
        wenzel (str): name of the wenzel
        hours (int, optional): time in hours to check for old records. Defaults to Settings.time_of_compare.
        If the time is not set, it will be taken from the settings.
        It is used to delete old records from the database.

    Returns:
        list: list of old records beton
   """    

    threshold = time.time() - hours * 3600

    with db_lock:
        data_sql.delete_records_below_threshold(threshold, "beton", wenzel[0])

        return data_sql.get_oldest_list_beton_or_lista("beton", date_of_lista_text, wenzel[0])
   
    return []

def check_del_add_lista(date_of_lista_text, currant_list_beton, wenzel):
    """It checks for any removed or new entries in the new dictionary
     compared to the old one and returns two dictionaries: one for
      removed entries and one for new entries

    Args:
        date_of_lista (str): date of day request - '12.03.2024'
        currant_list_beton (list): new list of shipment

    Returns:
        tuple: two lists - one for removed entries and one for new entries del_lista and add_lista
    """    
    del_lista = []
    add_lista = []
    old_stan_lista_beton = get_old_list_beton(date_of_lista_text, wenzel=wenzel)

    old_counter = Counter(old_stan_lista_beton)                                                                        
    currant_counter = Counter(currant_list_beton)

        # Ищем элементы, которые нужно удалить (из old_list, но отсутствуют или меньше раз в currant_list
    for item in old_counter:                                                                               
        if old_counter[item] > currant_counter[item]:                                                      
            del_lista.extend([item] * (old_counter[item] - currant_counter[item]))                         
                                                                                                        
    # Ищем элементы, которые нужно добавить (из currant_list, но отсутствуют или меньше раз в old_list)    
    for item in currant_counter:                                                                           
        if currant_counter[item] > old_counter[item]:                                                      
            add_lista.extend([item] * (currant_counter[item] - old_counter[item]))  

    # для контроля отображения
    # del_lista = del_lista + currant_list_beton[2:3]
    # add_lista = add_lista + currant_list_beton[0:2]

    return del_lista, add_lista

if __name__ == "__main__":
    pass