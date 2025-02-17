import re

def converter(list_for_convert):
    def convert_to_string(data):
        if not data:
            return ""
        try:
            data = str(data)
            data = data.strip()
            data = re.sub(r"\s+", " ", data)
            data = re.sub(r"\s*\bNone\b", "", data)
            return data
        except (TypeError, ValueError):
            return ""
        
    def convert_to_true_false(data):
        if not data:
            return False
        if data == '501':
            return False
        return True
    
        


    metres, times, firm, name, uwagi, przebieg, tel, wenz, pomp, sort = list_for_convert

    times = times.strftime("%H:%M")
    if tel:
        if isinstance(tel, float):
            tel = str(int(tel)).strip()
        elif isinstance(tel, str):
            tel = tel.strip()
    else:
        tel = ""

    przebieg = convert_to_string(przebieg)
    firm = convert_to_string(firm)
    name = convert_to_string(name)
    tel = convert_to_string(tel)
    uwagi = convert_to_string(uwagi)
    metres = convert_to_string(metres)
    pomp = convert_to_string(convert_to_true_false(pomp))
            
    return [metres, times, firm, name, uwagi, przebieg, tel, wenz, pomp, sort]



def compare_lists_by_tuples(del_lista, add_lista):
    matching_indices = []
    
    for index1, tuple1 in enumerate(del_lista):
        for index2, tuple2 in enumerate(add_lista):
            if tuple1[:3] == tuple2[:3] and tuple1[6] == tuple2[6]:
                matching_indices.append((index1, index2))
                
    del_lista, add_lista = make_list_with_teg(del_lista, add_lista, matching_indices)
    return del_lista, add_lista

def make_list_with_teg(del_lista, add_lista, matching_indices):
    del_lista_with_teg = del_lista
    add_lista_without_change = add_lista
    del_elem_from_add_lista = [tup[1] for tup in matching_indices]
    

    for matching in matching_indices:
        item_del = del_lista[matching[0]]
        item_add = add_lista[matching[1]]

        for index, (elem1, elem2) in enumerate(zip(item_del[:7], item_add[:7])):
            if elem1 != elem2:
                change_elem = (f'<span style="color: rgb(238, 36, 36); font-weight: bold; text-decoration: line-through;">{elem1}</span>'
                               f' <span style="color: rgb(0, 139, 7); font-weight: bold;">{elem2}</span>')
                del_lista_with_teg[matching[0]][index] =  change_elem
        del_lista_with_teg[matching[0]][8] = 0

    
    del_elem_from_add_lista.sort(reverse=True)
    for index in del_elem_from_add_lista:
        if 0 <= index < len(add_lista_without_change):
            del add_lista_without_change[index]
    

    return del_lista_with_teg, add_lista_without_change


def get_list_from_three_norm_del_add(lista_norm, lista_del, lista_add):
    """It creates a comprehensive list from elements that existed, were removed,
     or are new, adding an index at the end of each element: 0 for
      existing, 1 for removed, and 2 for new

    Args:
        lista_norm (list): The list has not changed since the last time
        lista_del (list): The list with removed items
        lista_add (list): The list with new items, sort items by time> metrs> firm

    Returns:
        list: list of cartege with three sort - add del norm
    """

    # Add the index of the list to which the element belongs at the end of the element
    # 0-normal 1-del  2 - add (SORT)
    lista_norm = [tup + (0,) for tup in lista_norm]
    lista_del = [tup + (1,) for tup in lista_del]
    lista_add = [tup + (2,) for tup in lista_add]

    lista_norm = list(map(converter, lista_norm))
    lista_del = list(map(converter, lista_del))
    lista_add = list(map(converter, lista_add))
    
    lista_del, lista_add = compare_lists_by_tuples(lista_del, lista_add)

    # If we do not find it in the list of new ones, then we add from the list of those that were already there.
    replacement_dict = {tuple(tup[:8]): tup for tup in lista_add}
    lista_norm_add = [replacement_dict.get(tuple(tup[:8]), tup) for tup in lista_norm]

    # добавляем всё что lista_del и всё что lista_norm_add кроме того что есть в  lista_del
    lista_norm_del_add = lista_del.copy() 
        
    for sublist2 in lista_norm_add:
        if not any(l1[:3] == sublist2[:3] for l1 in lista_del):  
            lista_norm_del_add.append(sublist2)




    # sorted by time, meters, name of firm
    lista_norm_del_add = sorted(lista_norm_del_add, key=lambda event: (event[1], event[2], event[3]))

    return  lista_norm_del_add

