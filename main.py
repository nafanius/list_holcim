from get_lista import combination_of_some_days_list
from jinja2 import Template
from get_html import html_template
from datetime import datetime

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




if __name__ == '__main__':
    print(get_dict())
    save_html(get_dict())