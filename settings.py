"""настройки и управление web lista"""
import datetime


class Settings:

    time_of_compare = 4
    data_base = 'sqlite:////home/user/.database_lista/web_lista.db'


    amount_of_zaprawa = 3.5
    names_dry_concret = r'\b(OW|Ow|ow|oW)\b'
    time_of_end_upload_zaprawa = datetime.time(7, 30)
    travel_to_the_construction = 30
    unloading_time_for_pomp = 3 # 1 metr
    unloading_time_for_crane = 8 # 1 metr   
  
    def __init__(self):
        pass
