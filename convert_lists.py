def get_list_from_three_norm_del_add(lista_norm, lista_del, lista_add):
    lista_norm = [tup + (0,) for tup in lista_norm]
    lista_del = [tup + (1,) for tup in lista_del]
    lista_add = [tup + (2,) for tup in lista_add]

    replacement_dict = {tup[:8]: tup for tup in lista_add}
    lista_norm_add = [replacement_dict.get(tup[:8], tup) for tup in lista_norm]

    lista_norm_del_add = lista_norm_add + lista_del
    lista_norm_del_add = sorted(lista_norm_del_add, key=lambda event: event[1])

    return  lista_norm_del_add

