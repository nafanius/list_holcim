"""Settings for the application.
This module contains the configuration settings for the application,
including database connection details, time intervals, and other parameters.
It is designed to be easily modifiable to suit different environments
and requirements.
"""

import datetime
from pprint import pformat
import logging
import traceback
import time

class Settings:

    time_of_compare = 4 # time of compare in hours betwen the last and current state of the database
    data_base = 'sqlite:////home/user/.database_lista/web_lista.db' # path to the database

    min_interval = 7 # minimum interval for the departure
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


# region logging
class PrettyFormatter(logging.Formatter):
       def format(self, record):
           # Если message относится к структуре данных, отформатируйте ее
           if isinstance(record.msg, (dict, list, tuple)):
               record.msg = pformat(record.msg)
           return super().format(record)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
handler.setFormatter(PrettyFormatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)

lg = logger.debug
cr = logger.critical
inf = logger.info
exp = logger.exception
logging.disable(logging.DEBUG)
# logging.disable(logging.INFO)
# logging.disable(logging.CRITICAL)
# logging.disable(logging.EXCEPTION)
# endregion

def formating_error_message(error, name):
    """Format the error message for logging

    Args:
        error (Exception): error message

    Returns:
        str: formatted error message
    """
    err_type = type(error).__name__
    tb_str = traceback.format_exc()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_frame = traceback.extract_tb(error.__traceback__)[-1]
    function_name = current_frame.name

    explan_mistake = f"""
        Mistake mame: {name}
        Time: {timestamp}
        Type of error: {err_type} type of
        Message: {error}
        Function name: {function_name}
        Traceback:
        {tb_str}
        """

    return explan_mistake

def timer(func):
    """
    A decorator that measures and logs the execution time of the wrapped function.

    Args:
        func (callable): The function to be wrapped and timed.

    Returns:
        callable: The wrapped function with execution time logging.

    Logs:
            Logs the execution time of the function in seconds using the `inf` logger
    """
    def wrapper(*args, **kwargs):
        """
        A decorator function that measures the execution time of the wrapped function.

        Args:
            *args: Positional arguments to be passed to the wrapped function.
            **kwargs: Keyword arguments to be passed to the wrapped function.

        Returns:
            The result of the wrapped function.

        Logs:
            Logs the execution time of the wrapped function in seconds.
        """
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        lg(f"Function {func.__name__} executed for {end_time - start_time} seconds") 
        return result
    return wrapper
