import ezsheets
from datetime import datetime, timedelta
import os
from src.settings import inf, formating_error_message

# dyspozytor.warszawa@holcim.com


def generate_name_of_file_google():
    """Forms the file names that need to be downloaded based on the current date, returning a list of file names

    Returns:
        list of str: list of file names
    """
    list_of_download_files = []

    now = datetime.now()
    current_week_number = now.isocalendar()[1]
    current_year = now.year

    if current_week_number == 1 and current_year == (now - timedelta(weeks=1)).year:
        list_of_download_files.append(f"Tydz {1}.{current_year + 1}")
        list_of_download_files.append(f"Tydz {2}.{current_year + 1}")

    else:
        list_of_download_files.append(f"Tydz {current_week_number}.{current_year}")
        list_of_download_files.append(f"Tydz {current_week_number + 1}.{current_year}")

    return list_of_download_files


def save_google_sheet(directory="excel_files"):
    """save googlsheet file like a Excel in directory

    Args:
        directory (str, optional): The directory where the file is save. Defaults to 'excel_files'.
    """
    for file in generate_name_of_file_google():
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            ss = ezsheets.Spreadsheet(file)
            ss_name = ss.title
            file_path = os.path.join(directory, f"{ss_name}.xlsx")
            ss.downloadAsExcel(file_path)
        except Exception as err:

            inf(formating_error_message(err, "save_google_sheet"))
            
            continue