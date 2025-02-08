from pprint import pprint
from data_sql import get_newest_list_beton_or_lista
import re
import datetime
from settings import Settings


class Order:

    count_ordres = 0

    def __init__(
        self, date_order, metres, times, firm, name, uwagi, przebieg, tel, wenz
    ):

        self.date_order = date_order
        self.metres = metres
        self.times = times
        self.firm = self.convert_to_string(firm)
        self.name = self.convert_to_string(name)
        self.uwagi = self.convert_to_string(uwagi)
        self.przebieg = self.convert_to_string(przebieg)
        self.tel = self.convert_to_string(self.tel_to_string(tel))
        self.wenz = wenz
        self.list_of_loads = []

        self.pompa_dzwig = self.check_pompa_dzwig()
        self.list_of_courses = self.get_list_courses()
        self.start_time = self.get_start_time()
        self.finish_time = self.get_finish_time_and_form_list_of_loads()
        self.it_is_zaprawa = self.check_zaprawa()
        self.it_is_concret = self.check_concret()
        self.reszta = self = self.get_reszta()

        Order.count_ordres += 1

    def tel_to_string(self, data):
        if data:
            if isinstance(data, float):
                return str(int(data)).strip()
            elif isinstance(data, str):
                return data.strip()
        else:
            return ""

    def convert_to_string(self, data):
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
        # Определение значения каждого элемента при равном делении
        base_value = int(self.metres // 8)

        # Подсчет остатка
        remainder = self.metres % 8

        # Инициализация list с основным значением
        result = [
            8.0,
        ] * base_value

        # Если остаток меньше 1
        if remainder != 0 and base_value > 0 and remainder < 2:
            # последний элемент корректируется на 1 меньше
            result[-1] -= 1
            remainder += 1

            result = result + [
                remainder,
            ]

        elif remainder != 0 and base_value > 0 and remainder >= 2:
            result = result + [
                remainder,
            ]

        elif remainder != 0 and base_value == 0:
            result = [
                remainder,
            ]

        return result

    def get_start_time(self):
        date_order = datetime.datetime.strptime(
            self.date_order, "%d.%m.%Y").date()
        data_time_order = datetime.datetime.combine(date_order, self.times)

        return data_time_order - datetime.timedelta(minutes=30)


    def get_finish_time_and_form_list_of_loads(self):
        shipping_duration = 0
        self.list_of_loads += [self.start_time,]
        for cours in self.list_of_courses[:-1]:
            if self.pompa_dzwig:  # if it's pompa
                shipping_duration += cours * Settings.unloading_time_for_pomp
                self.list_of_loads += [self.list_of_loads[-1] + datetime.timedelta(minutes=cours * Settings.unloading_time_for_pomp),]
            else:
                shipping_duration += cours * Settings.unloading_time_for_crane  # if it's crane
                self.list_of_loads += [self.list_of_loads[-1] + datetime.timedelta(minutes=cours * Settings.unloading_time_for_crane),]

        return self.start_time + datetime.timedelta(minutes=shipping_duration)

    # todo возможно передеть все переменные вычесленные в json и обработать потом в DATAFRAME
    # def convert_to_dict_for_df(self):
    #     return {}
    def check_pompa_dzwig(self):
        if self.metres > 18 and self.times < datetime.time(13 , 0):  # if it's pompa
            return True
        return False


    def check_zaprawa(self):
        if (
            self.list_of_courses[0] < Settings.amount_of_zaprawa
            and self.times < Settings.time_of_end_upload_zaprawa
            and not re.search(Settings.names_dry_concret, self.name)
        ):
            return True
        return False

    def check_concret(self):

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
    for item in get_newest_list_beton_or_lista("beton", date_order):
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
            "name":bud.name,
            "metr":bud.metres,
            "time":bud.times,
            "start_time":bud.start_time,
            "finish_time":bud.finish_time,
            "list_of_loads":bud.list_of_loads,
            "it_is_zaprawa":bud.it_is_zaprawa,
            "it_is_concret":bud.it_is_concret,
            "list_of_courses":bud.list_of_courses,
            "date_order":bud.date_order,
            "date_order":bud.date_order,
        })
