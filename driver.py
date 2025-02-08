class Driver:
    
    count_driver = 0
    
    def __init__(self, time_in_list, person):
        '''Initializes the data.'''
        self.time_in_list = time_in_list
        self.person = person
        
        Driver.count_driver += 1


    def convert_to_dict_for_df(self):
       
       return {}


    @classmethod
    def how_many(cls):
        '''Prints the current population.'''
        print('We have {:d} drivers.'.format(cls.count_driver))