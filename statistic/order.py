"""Order class for managing and processing orders.
This class provides methods to handle order data, including
calculating start and finish times, checking for specific conditions,
and converting data types. It also maintains a count of the total
number of orders created.
"""
from pprint import pprint
from data_drive.data_sql import get_newest_list_beton_or_lista
import re
import datetime
from src.settings import Settings


class Order:

    count_ordres = 0

    def __init__(
        self, date_order, metres, times, firm, name, uwagi, przebieg, tel, wenz, pompa_dzwig
    ):

        self.date_order = date_order
        self.metres = self.convert_to_float(metres)
        self.times = times
        self.firm = self.convert_to_string(firm)
        self.name = self.convert_to_string(name)
        self.uwagi = self.convert_to_string(uwagi)
        self.przebieg = self.convert_to_string(przebieg)
        self.tel = self.convert_to_string(self.tel_to_string(tel))
        self.wenz = wenz
        self.list_of_loads = []
        self.pompa_dzwig = self.check_pompa_dzwig(pompa_dzwig, self.metres)

        self.list_of_courses = self.get_list_courses()
        self.start_time = self.get_start_time()
        self.finish_time = self.get_finish_time_and_form_list_times_of_loads()
        self.it_is_zaprawa = self.check_zaprawa()
        self.it_is_concret = self.check_concret()
        self.reszta = self.get_reszta()

        Order.count_ordres += 1

    def tel_to_string(self, data):
        """converts the phone number to a string and removes any unwanted characters.

        Args:
            data (any): the phone number from cell tel to be converted
        Returns:
            str: the converted phone number 
        """        
        if data:
            if isinstance(data, float):
                return str(int(data)).strip()
            elif isinstance(data, int):
                return str(data).strip()
            elif isinstance(data, str):
                return data.strip()
            else:
                return ""
        else:
            return ""

    def convert_to_float(self, data):
        """converts the data to a float.
        If the data is None, it returns 0. If the data is a string, it tries to convert it to a float.
        If the data is a float or int, it returns the data as a float.
        If the data is a string that cannot be converted to a float, it returns 0.

        Args:
            data (any): raw data to be converted

        Returns:
            int or float: the converted data
        """        
        if data:
            if isinstance(data, float):
                return data
            elif isinstance(data, int):
                return float(data)
            else:
                return 0.0
        else:
            return 0.0

    def convert_to_string(self, data):
        """converts the data to a string.
        If the data is None, it returns an empty string.
        If the data is a string, it strips any unwanted characters.

        Args:
            data (any): dta from cell to be converted

        Returns:
            str: the converted data
        """        
        if not data:
            return ""
        try:
            data = str(data)
            data = re.sub(r"\s+", " ", data)
            data = data.strip()
            return data
        except (TypeError, ValueError):
            return ""

    def get_list_courses(self):
        """forms a list of courses based on the number of metres.
        The list is formed by dividing the number of metres by 8.

        Returns:
            list: list of courses
        """        

        if self.metres == 0:
            return [0,]

        # The number of courses equivalent to 8
        base_value = int(self.metres // 8)

        # A remainder of less than 8 meters
        remainder = self.metres % 8

        # Initializing a list with values equal to 8 meters
        result = [
            8.0,
        ] * base_value

        # if remainder less then 2 metrs
        if remainder != 0 and base_value > 0 and remainder < 2:
            # The last element is adjusted to be 1 less, and added this 1 metr to remainder
            result[-1] -= 1
            remainder += 1

            result = result + [
                remainder,
            ]

        elif remainder != 0 and base_value > 0 and remainder >= 2:
            # if remainder greater or equal 2 metrs, just added like a last element of list 
            result = result + [
                remainder,
            ]

        elif remainder != 0 and base_value == 0:
            result = [
                remainder,
            ]

        return result

    def get_start_time(self):
        """calculates the start time of the order.
        The start time is calculated by subtracting 30 minutes from the order time.

        Returns:
            datetime: the start time of the order
        """        
        date_order = datetime.datetime.strptime(
            self.date_order, "%d.%m.%Y").date()
        data_time_order = datetime.datetime.combine(date_order, self.times)

        return data_time_order - datetime.timedelta(minutes=30)

    def get_finish_time_and_form_list_times_of_loads(self):
        """calculates the finish time of the order.
        The finish time is calculated by adding the shipping duration to the start time.
        The shipping duration is calculated based on the number of courses and the type of pump or crane.

        Returns:
            datetime: the finish time of the order
        """        
        shipping_duration = 0
        self.list_of_loads += [self.start_time,]
        for cours in self.list_of_courses[:-1]:
            if self.pompa_dzwig:  # if it's pompa
                shipping_duration += cours * Settings.unloading_time_for_pomp
                self.list_of_loads += [self.list_of_loads[-1] + datetime.timedelta(
                    minutes=cours * Settings.unloading_time_for_pomp),]
            else:
                shipping_duration += cours * Settings.unloading_time_for_crane  # if it's crane
                self.list_of_loads += [self.list_of_loads[-1] + datetime.timedelta(
                    minutes=cours * Settings.unloading_time_for_crane),]

        return self.start_time + datetime.timedelta(minutes=shipping_duration)

    def check_pompa_dzwig(self, pompa_dzwig, metres):
        """ checks if the order is for a pump or crane.
        If the order is for a pump, it returns True.
        If the order is for a crane, it returns False.

        Args:
            pompa_dgwig (str): string keep infomation from excel about using pomp or 
            "" - if no use pomp
            metres (float): the number of metres in the order

        Returns:
            bool: True if the order is for a pump, False if it's for a crane
        """        
        if pompa_dzwig:  # if it's pompa
            data = str(pompa_dzwig)
            data = data.strip()
            if data == '501':
                return False
            return True
        elif not pompa_dzwig and metres > 50:
            return True
        
        return False

    def check_zaprawa(self):
        """checks if the order is for zaprawa.
        If the order is for zaprawa, it returns True.

        Returns:
            bool: True if the order is for zaprawa, False otherwise
        """        
        if (
            self.list_of_courses[0] < Settings.amount_of_zaprawa
            and self.times < Settings.time_of_end_upload_zaprawa
            and not re.search(Settings.names_dry_concret, self.name)
        ):
            return True
        return False

    def check_concret(self):
        """checks if the order is for concret.
        If the order is for concret, it returns True, not dry concret

        Returns:
            bool: True if the order is for concret, False otherwise
        """        

        if re.search(Settings.names_dry_concret, self.name):
            return False
        return True

    def get_reszta(self):
        reszta = []
        metres = self.metres

        for cours in self.list_of_courses:
            reszta.append(metres - cours)
            metres -= cours

        return reszta

    @classmethod
    def how_many(cls):
        """Prints the current population."""
        print("We have {:d} orders.".format(cls.count_ordres))


if __name__ == "__main__":

    # pprint(get_newest_list_beton_or_lista("beton", "03.02.2025")[5])

    # bud = Order(*get_newest_list_beton_or_lista("beton", "03.02.2025")[5])
    # bud1 = Order(*get_newest_list_beton_or_lista("beton", "03.02.2025")[9])
    # bud2 = Order(*get_newest_list_beton_or_lista("beton", "03.02.2025")[3])
    orders = {}
    count = 1
    date_order = "07.02.2025"
    for item in get_newest_list_beton_or_lista("beton", date_order, 'zawod'):
        orders[f"{count}bud"] = Order(date_order, *item)
        count += 1

    pprint(orders)

    df_bud = []
    for key_bud in orders.keys():
        bud = orders[key_bud]
        pprint(
            (
                bud.name,
                bud.metres,
                bud.times,
                bud.start_time,
                bud.finish_time,
                bud.list_of_loads,
                bud.it_is_zaprawa,
                bud.it_is_concret,
                bud.list_of_courses,
                bud.date_order,
                bud.count_ordres,
            )
        )
        df_bud.append({
            "name": bud.name,
            "metr": bud.metres,
            "time": bud.times,
            "start_time": bud.start_time,
            "finish_time": bud.finish_time,
            "list_of_loads": bud.list_of_loads,
            "it_is_zaprawa": bud.it_is_zaprawa,
            "it_is_concret": bud.it_is_concret,
            "list_of_courses": bud.list_of_courses,
            "date_order": bud.date_order,
            "date_order": bud.date_order,
        })
