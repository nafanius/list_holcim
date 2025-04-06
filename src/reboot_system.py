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
    param = "-c"  # Количество запросов
    command = ["ping", param, "1", "-W", str(timeout), host]
    return os.system(" ".join(command)) == 0

def reboot_device():
    """Reboots the Raspberry Pi device. for example 
    """    
    os.system("sudo reboot")

def main():
    if not check_internet():
        inf("Reboot Raspberry Pi...")
        reboot_device()
    else:
        inf("Internet is available. No need to reboot.")


if __name__ == "__main__":
    main()

