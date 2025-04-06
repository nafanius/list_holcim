""" module to check internet connection and reboot the system if not connected
"""
import os
from src.settings import inf

def check_internet(host="8.8.8.8", timeout=3):
    """checks if the internet is available by pinging a host.

    Args:
        host (str, optional): host to check Defaults to "8.8.8.8".
        timeout (int, optional): timeout in seconds Defaults to 3.

    Returns:
        booling: False if internet is available, True otherwise.
    """
    inf("Checking internet connection...")   
    param = "-c"  # Количество запросов
    command = ["ping", param, "1", "-W", str(timeout), host]
    return os.system(" ".join(command)) == 0

def reboot_device():
    """Reboots the Raspberry Pi device. for example 
    """    
    os.system("sudo reboot")

def start_checking_internet():
    """
    Checks the availability of an internet connection and reboots the device if the connection is unavailable.

    This function uses the `check_internet` function to determine if the internet is accessible.
    If the internet is not available, it logs a message indicating that the Raspberry Pi will be rebooted
    and calls the `reboot_device` function to perform the reboot. If the internet is available, it logs
    a message indicating that no action is needed.

    Dependencies:
        - check_internet(): A function that returns a boolean indicating internet availability.
        - inf(message: str): A function to log informational messages.
        - reboot_device(): A function to reboot the device.

    Returns:
        None
    """
    if not check_internet():
        inf("Reboot Raspberry Pi...")
        reboot_device()
    else:
        inf("Internet is available. No need to reboot.")


if __name__ == "__main__":
    start_checking_internet()

