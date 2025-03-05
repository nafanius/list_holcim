"""настройки и управление web lista"""
import datetime


class Settings:

    time_of_compare = 4
    data_base = 'sqlite:////home/user/.database_lista/web_lista.db'


    amount_of_zaprawa = 3.5
    names_dry_concret = r'\b(OW|Ow|ow|oW)\b'
    time_of_end_upload_zaprawa = datetime.time(8, 15)
    travel_to_the_construction = 30
    unloading_time_for_pomp = 3 # 1 metr
    unloading_time_for_crane = 8 # 1 metr 
    wenzels = (
        ("zawod",("zawodzie 2 ", "zawodzie 1 "), 26),
        ("odola",("if will be 2 wenz", "odolany 519"), 17),
        ("zeran",("if will be 2 wenz", "żerań 502"), 15),
        ("gora",("if will be 2 wenz", "góra kalwaria 502"), 6),
    )
  
    def __init__(self):
        pass
