def get_list_from_three_norm_del_add(lista_norm, lista_del, lista_add):
    """ add
    :param lista_norm: The list has not changed since the last time.
    :param list_del:  The list with removed items.
    :param lista_add: The list with new items
    :return: list of cartege with three sort - add del norm
    """

    # Add the index of the list to which the element belongs at the end of the element
    # 0-normal 1-del  2 - add
    lista_norm = [tup + (0,) for tup in lista_norm]
    lista_del = [tup + (1,) for tup in lista_del]
    lista_add = [tup + (2,) for tup in lista_add]

    # If we do not find it in the list of new ones, then we add from the list of those that were already there.
    replacement_dict = {tup[:8]: tup for tup in lista_add}
    lista_norm_add = [replacement_dict.get(tup[:8], tup) for tup in lista_norm]

    # add list of removed items
    lista_norm_del_add = lista_norm_add + lista_del

    # sorted by time, meters, name of firm
    lista_norm_del_add = sorted(lista_norm_del_add, key=lambda event: (event[1], event[2], event[3]))

    return  lista_norm_del_add

