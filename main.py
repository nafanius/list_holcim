from get_lista import combination_of_some_days_list
from jinja2 import Template
from get_html import html_template
from datetime import datetime
import boto3
from botocore.exceptions import NoCredentialsError


def get_dict():
    data = combination_of_some_days_list()

    now = datetime.now()
    data["Zaktualizowano"] = f"Zaktualizowano na: {now.strftime("%d.%m.%Y %H:%M")}"

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



if __name__ == '__main__':
    print(get_dict())
    save_html(get_dict())
    upload_file_to_s3('./site/index.html', 'list-holcim', "index.html")