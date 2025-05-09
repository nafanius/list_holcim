from src.get_lista import combination_of_some_days_list, find_day_request
from src.download_excel import save_google_sheet
from statistic.static_forms import rozklad_curs, forecast_driver
from src.reboot_system import check_internet

from jinja2 import Template
from html_driver.get_html import html_template
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError
import os
import argparse
from src.settings import Settings, inf, cr, formating_error_message


def get_dict():
    """creation and return of a dictionary with all data for HTML"""
    

    #  We save the latest Excel files from Google Drive.
    save_google_sheet()

    def parsing_args(dictinary):
        """ addes to the  dictionary warrnings, for whom the page is made/ and congratulations  

        Args:
            dictinary (dictionary): recives the dictionary an adds elements to it from variables when the programis launched

        Returns:
            dicnionary: dictionary with added elements
        """ 
        parser = argparse.ArgumentParser(
            description="Add tegs with congratulation? warrnings and other things"
        )
        parser.add_argument("--by_who", type=str, help="for whom it's maded")
        parser.add_argument("--cong", type=str, help="holiday greeting")
        parser.add_argument("--war", type=str, help="warrning")

        args = parser.parse_args()

        dictinary["brend"] = (
            args.by_who if args.by_who else 'Produced for "Holcim"'
        )
        dictinary["cong"] = args.cong if args.cong else ""
        dictinary["war"] = args.war if args.war else ""

        return dictinary

    dict_all_wenzels = {}
    for wenzel in Settings.wenzels:

        data = combination_of_some_days_list(wenzel)


        # adding statistics
        list_date_for_stat = [t[2] for t in find_day_request()]
        day_number = 1
        for date_for_stat in list_date_for_stat:
            rozklad_curs_data = rozklad_curs(wenzel=wenzel, date_of_request=date_for_stat)
            forecast_drive_data = forecast_driver(wenzel=wenzel, date_of_request=date_for_stat)
            
            
            data[f"count_{day_number}"] = rozklad_curs_data[1]
            data[f"clean_metrs_{day_number}"] = rozklad_curs_data[2]
            data[f"rozklad_curs_{day_number}"] = rozklad_curs_data[0]
            data[f"grap_intens_{day_number}"] = rozklad_curs_data[3]
            data[f"grap_intens_pie_{day_number}"] = rozklad_curs_data[4]

            data[f"forecast_driver_tab_{day_number}"] = forecast_drive_data[0]
            data[f"forecast_driver_brak_{day_number}"] = forecast_drive_data[1]
            data[f"grap_driver_{day_number}"] = forecast_drive_data[2]
            data[f"forcast_logist_{day_number}"] = forecast_drive_data[3]
            

            day_number += 1
        dict_all_wenzels[wenzel[0]] = data


    
    now = datetime.now()
    dict_all_wenzels["Zaktualizowano"] = f'Zaktualizowano na: {now.strftime("%d.%m.%Y %H:%M")}'

    parsing_args(dict_all_wenzels)

    return dict_all_wenzels


def save_html(data):
    """Fills the HTML template from the dictionary and saves the completed HTML to a file

    Args:
        data (dictionary): dictionary with data
    """
    template = Template(html_template)
    rendered_html = template.render(data = data)
    with open("./site/index.html", "w", encoding="utf-8") as f:
        f.write(rendered_html)


def upload_directory_to_s3(
    directory_path, bucket_name, s3_base_path="", region="eu-central-1"
):
    """Uploads the 'site' folder to an AWS S3 bucket

    Args:
        directory_path (str): The directory where the index and all nested folders and files are located
        bucket_name (str): bucket name
        s3_base_path (str, optional): The directory where we write files to the S3 bucket. Defaults to "".
        region (str, optional): region  Defaults to "eu-central-1".
    """    
    session = boto3.Session(region_name=region)
    s3_client = session.client("s3")

    # Walk through all the files and directories in the specified directory
    for root, _, files in os.walk(directory_path):
        for file in files:
            # Construct the full local file path
            local_path = os.path.join(root, file)

            # Construct the S3 path by joining base path with the relative path
            # to get the subdirectories structure
            relative_path = os.path.relpath(local_path, directory_path)
            s3_path = os.path.join(s3_base_path, relative_path).replace("\\", "/")

            # Upload the file
            try:
                s3_client.upload_file(
                    local_path,
                    bucket_name,
                    s3_path,
                    ExtraArgs={"ContentType": "text/html"},
                )
                s3_client.put_object_acl(
                    ACL="public-read", Bucket=bucket_name, Key=s3_path
                )
                inf(f"File {s3_path} uploaded to {bucket_name}/{s3_path}")

            except FileNotFoundError as err:
                cr(formating_error_message(err, f"upload_directory_to_s3 file {s3_path} was not found"))
                
            except NoCredentialsError as err:
                cr(formating_error_message(err, "upload_directory_to_s3 Credentials not available"))
               


if __name__ == "__main__":
    # pprint(get_dict())
    check_internet()
    save_html(get_dict())
    upload_directory_to_s3("./site", "list-holcim")
    # dict_zaw = get_dict()
