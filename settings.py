"""настройки и управление ботом"""
import json
import os


class Settings:
    user_data_file = "user_data.json"
    data_base = 'sqlite:///web_lista.db'
  
    def __init__(self):
        pass

    # Функция для записи словаря в файл
    @staticmethod
    def save_dict_to_file(dictionary, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(dictionary, f, ensure_ascii=False, indent=4)

    # Функция для загрузки словаря из файла
    @staticmethod
    def load_dict_from_file(filename):
        if os.path.isfile(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=4)
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)


