""" This module contains the Driver class.
It is used to create a driver object with the following attributes:
- date_order: the date of the order
- time_in_list: the time in the loading schedule
- person: the person who created the order
- count_driver: the number of drivers created       
"""

from pprint import pprint
from data_drive.data_sql import get_newest_list_beton_or_lista



class Driver:
    
    count_driver = 0
    
    def __init__(self, work_day, time_in_list, person):
        """Card of depart driver

        Args:
            work_day (str): date string format "dd.mm.yyyy"
            time_in_list (datetime.time): time from lista
            person (str): name of driver and car's number
        """        
        self.date_order: str = work_day
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
