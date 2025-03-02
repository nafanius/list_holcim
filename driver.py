from pprint import pprint
from data_sql import get_newest_list_beton_or_lista
import re
import datetime
from settings import Settings



class Driver:
    
    count_driver = 0
    
    def __init__(self, work_day, time_in_list, person):
        '''Initializes the data.'''
        self.date_order = work_day
        self.time_in_list = time_in_list
        self.person = person
        
        Driver.count_driver += 1


    def convert_to_dict_for_df(self):
       
       return {}


    @classmethod
    def how_many(cls):
        '''Prints the current population.'''
        print('We have {:d} drivers.'.format(cls.count_driver))



if __name__ == "__main__":

    drivers = {}
    count = 1
    work_day = "03.03.2025"

    for item in get_newest_list_beton_or_lista("lista", work_day, 'zawod'):
        drivers[f"{count}bud"] = Driver(work_day, *item)
        count += 1

    pprint(drivers)

    df_driver = []
    for key_driver in drivers.keys():
        driver = drivers[key_driver]
        pprint(
            (
                driver.time_in_list,
                driver.person,
            )
        )
        df_driver.append({
            "time_start": driver.time_in_list,
            "person": driver.person,
        })
