import ezsheets
from datetime import datetime, timedelta
import os
from src.settings import inf, formating_error_message, timer

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
        list_of_download_files.append(f"{1}.{current_year + 1}")
        list_of_download_files.append(f"{2}.{current_year + 1}")

    else:
        list_of_download_files.append(f"{current_week_number}.{current_year}")
        list_of_download_files.append(f"{current_week_number + 1}.{current_year}")

    return list_of_download_files

@timer
def save_google_sheet(directory="excel_files"):
    """save googlsheet file like a Excel in directory

    Args:
        directory (str, optional): The directory where the file is save. Defaults to 'excel_files'.
    """
    for week_number_year in generate_name_of_file_google():
        try:
            if not os.path.exists(directory):
                os.makedirs(directory)
            all_spreadsheets = ezsheets.listSpreadsheets() # get all available files
            filtered_spreadsheets = {name: spreadsheet_id for spreadsheet_id, name in all_spreadsheets.items()\
                                      if name.endswith(week_number_year)} # filtred ended week_number_year from generate_name_of_file_google
            if len(filtered_spreadsheets) == 1:
                spreadsheet_id = next(iter(filtered_spreadsheets.values()))
                spreadsheet = ezsheets.Spreadsheet(spreadsheet_id)
                file_path = os.path.join(directory, f"Tydz {week_number_year}.xlsx")
                spreadsheet.downloadAsExcel(file_path)
            elif len(filtered_spreadsheets) == 0:
                inf(f"There isn't file has name ended {week_number_year}")
                raise Exception
            else:
                inf(f"More then one file has name ended {week_number_year}\nsheets: {filtered_spreadsheets}")
                raise Exception

        except Exception as err:

            inf(formating_error_message(err, "save_google_sheet"))
            
            continue