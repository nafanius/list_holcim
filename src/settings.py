"""Settings for the application.
This module contains the configuration settings for the application,
including database connection details, time intervals, and other parameters.
It is designed to be easily modifiable to suit different environments
and requirements.
"""

import datetime


class Settings:

    time_of_compare = 4 # time of compare in hours betwen the last and current state of the database
    data_base = 'sqlite:////home/user/.database_lista/web_lista.db' # path to the database

    min_interval = 9 # minimum interval for the departure
    amount_of_zaprawa = 6 # amount of zaprawa m3
    names_dry_concret = r'\b(OW|Ow|ow|oW)\b' # regex for dry concret
    time_of_end_upload_zaprawa = datetime.time(8, 15) # time of end upload zaprawa
    travel_to_the_construction = 30 # time of travel to the construction and back
    unloading_time_for_pomp = 2 # time of unloading for pomp
    unloading_time_for_crane = 5.2 # 1 time of unloading for crane
    wenzels = (
        ("zawod",("zawodzie 2 ", "zawodzie 1 "), 24),
        ("odola",("if will be 2 wenz", "odolany 519"), 17),
        ("zeran",("if will be 2 wenz", "żerań 502"), 12),
        ("gora",("if will be 2 wenz", "góra kalwaria 502"), 6),
    )
  
    def __init__(self):
        pass
