from get_lista import combination_of_some_days_list
from jinja2 import Template
from get_html import html_template
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError
import os




def get_dict():
    data = combination_of_some_days_list()

    now = datetime.now()
    data["Zaktualizowano"] = f'Zaktualizowano na: {now.strftime("%d.%m.%Y %H:%M")}'

    return data

def save_html(data):
    template = Template(html_template)
    rendered_html = template.render(data)
    with open('./site/index.html', 'w', encoding='utf-8') as f:
        f.write(rendered_html)

def upload_file_to_s3(file_path, bucket, file_name, region="eu-central-1"):
    # Создаем сессию boto3 и клиент S3
    session = boto3.Session(
        region_name=region
    )
    s3_client = session.client('s3')

    try:
        # Загружаем файл в S3
        s3_client.upload_file(file_path, bucket, file_name, ExtraArgs={'ContentType': 'text/html'})
        s3_client.put_object_acl(ACL='public-read', Bucket=bucket, Key=file_name)

        print(f"File {file_name} uploaded to {bucket}/{file_name}")
    except FileNotFoundError:
        print(f"The file {file_name} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")



def upload_directory_to_s3(directory_path, bucket_name, index_file, s3_base_path='', region="eu-central-1"):
    session = boto3.Session(
        region_name=region
    )
    s3_client = session.client('s3')
    
    # Walk through all the files and directories in the specified directory
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            # Construct the full local file path
            local_path = os.path.join(root, file)
            
            # Construct the S3 path by joining base path with the relative path
            # to get the subdirectories structure
            relative_path = os.path.relpath(local_path, directory_path)
            s3_path = os.path.join(s3_base_path, relative_path).replace("\\", "/")
            
            # Upload the file
            try:
                s3_client.upload_file(local_path, bucket_name, s3_path, ExtraArgs={'ContentType': 'text/html'})
                print(f"File {s3_path} uploaded to {bucket_name}/{s3_path}")
            except FileNotFoundError:
                print(f"The file {s3_path} was not found.")
            except NoCredentialsError:
                print("Credentials not available.")
    try:
        # Загружаем файл в S3
        s3_client.put_object_acl(ACL='public-read', Bucket=bucket_name, Key=index_file)

    except FileNotFoundError:
        print(f"The file {index_file} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")


if __name__ == '__main__':
    # print(get_dict())
    save_html(get_dict())
    # upload_file_to_s3('./site/index.html', 'list-holcim', "index.html")
    upload_directory_to_s3('./site', 'list-holcim', "index.html")