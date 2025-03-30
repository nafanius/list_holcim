"""настройки и управление web lista"""
import datetime


class Settings:

    time_of_compare = 4
    data_base = 'sqlite:////home/user/.database_lista/web_lista.db'

    min_interval = 10
    amount_of_zaprawa = 5
    names_dry_concret = r'\b(OW|Ow|ow|oW)\b'
    time_of_end_upload_zaprawa = datetime.time(8, 15)
    travel_to_the_construction = 30
    unloading_time_for_pomp = 2 # 1 metr
    unloading_time_for_crane = 6.2 # 1 metr 
    wenzels = (
        ("zawod",("zawodzie 2 ", "zawodzie 1 "), 24),
        ("odola",("if will be 2 wenz", "odolany 519"), 17),
        ("zeran",("if will be 2 wenz", "żerań 502"), 12),
        ("gora",("if will be 2 wenz", "góra kalwaria 502"), 6),
    )
  
    def __init__(self):
        pass
