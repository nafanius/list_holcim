import time
import json
from sqlalchemy import (
    create_engine,
    Column,
    Integer,
    String,
    Float,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings import Settings

# Создание базового класса
Base = declarative_base()


# Определение структуры таблицы через класс


class Beton(Base):
    __tablename__ = "beton"

    event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_beton = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<User(user_id={self.event_time}, name ={self.list_beton})>"


class Lista(Base):
    __tablename__ = "lista"

    event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_send = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<User(user_id={self.event_time}, name ={self.list_send})>"


# Создание базы данных SQLite в файле
engine = create_engine(Settings.data_base)

# Создание всех таблиц, которые еще не существуют
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)


def record_beton(data):
    session = Session()
    get_list_beton_serialize = [(item[0], item[1].isoformat(), *item[2:]) for item in data["lista_beton"]]
    serialized_list_beton = json.dumps(get_list_beton_serialize)
    try:
        beton = Beton(
            event_time=time.time(),
            date_text=data["date_of_day_text"],
            list_beton=serialized_list_beton,
            day=data["day"],
            status=0,
        )

        session.add(beton)
        session.commit()
    except IntegrityError as e:
        print("Ошибка целостности данных: возможно, дубликат ключа")
        session.rollback()  # Отмена всех изменений в текущей транзакции

    except Exception as e:
        print("Ошибка при добавлении данных:", e)
        session.rollback()
    finally:
        session.close()


def record_lista(data):
    session = Session()

    get_list_serialize = [(item[0].isoformat(), item[1]) for item in data["lista"]]
    serialized_list = json.dumps(get_list_serialize)
    try:
        lista = Lista(
            event_time=time.time(),
            date_text=data["date_of_day_text"],
            list_send=serialized_list,
            day=data["day"],
            status=0,
        )

        session.add(lista)
        session.commit()
    except IntegrityError as e:
        print("Ошибка целостности данных: возможно, дубликат ключа")
        session.rollback()  # Отмена всех изменений в текущей транзакции

    except Exception as e:
        print("Ошибка при добавлении данных:", e)
        session.rollback()
    finally:
        session.close()


# TODO удалить это ниже этой отметки


# def record_to_dict(record):
#     return {
#         column.name: getattr(record, column.name) for column in record.__table__.columns
#     }


# def get_user_by_id(user_id):
#     session = Session()
#     try:
#         user = session.query(User).get(user_id)
#         return user
#     finally:
#         session.close()


# def get_request_by_inpol(inpol):
#     session = Session()
#     try:
#         request = session.query(Request).get(inpol)
#         return request

#     finally:
#         session.close()


# def det_request_list_by_inpol(inpol_req):
#     session = Session()
#     result = None
#     try:
#         record = session.query(Request).filter(Request.inpol == inpol_req).one_or_none()
#         if record:
#             result = record_to_dict(record)
#         return result

#     finally:
#         session.close()


# def get_requests(user_id):
#     session = Session()
#     try:
#         records = session.query(Request).filter(Request.user_id == user_id).all()
#         result = [record_to_dict(record) for record in records]
#         return result

#     finally:
#         session.close()


# def record_request(data):
#     session = Session()
#     try:
#         request = Request(
#             inpol=data["inpol"],
#             mos=data["mos"],
#             name=data["name"],
#             lname=data["lname"],
#             obywatelstwo=data["obywatelstwo"],
#             phone=data["phone"],
#             urodzenia=data["urodzenia"],
#             paszport=data["paszport"],
#             email=data["email"],
#             pobyt=data["pobyt"],
#             pelnomocnik=data["pelnomocnik"],
#             wiza=data["wiza"],
#             user_id=data["user_id"],
#             request_time=data["request_time"],
#             request_state=data["request_state"],
#         )

#         session.add(request)
#         session.commit()
#     except IntegrityError as e:
#         print("Ошибка целостности данных: возможно, дубликат ключа")
#         session.rollback()  # Отмена всех изменений в текущей транзакции

#     except Exception as e:
#         print("Ошибка при добавлении данных:", e)
#         session.rollback()
#     finally:
#         session.close()


# def update_request(data):
#     session = Session()

#     try:
#         record = (
#             session.query(Request).filter(Request.inpol == data["inpol"]).one_or_none()
#         )
#         if record:
#             record.mos = data["mos"]
#             record.name = data["name"]
#             record.lname = data["lname"]
#             record.obywatelstwo = data["obywatelstwo"]
#             record.phone = data["phone"]
#             record.urodzenia = data["urodzenia"]
#             record.paszport = data["paszport"]
#             record.email = data["email"]
#             record.pobyt = data["pobyt"]
#             record.pelnomocnik = data["pelnomocnik"]
#             record.wiza = data["wiza"]
#             record.user_id = data["user_id"]
#             record.request_time = data["request_time"]
#             record.request_state = data["request_state"]

#             session.commit()
#         else:
#             print(f"Запись не найдена.{data["inpol"]}")

#     except IntegrityError as e:
#         print("Ошибка целостности данных: возможно, дубликат ключа")
#         session.rollback()  # Отмена всех изменений в текущей транзакции

#     except Exception as e:
#         print("Ошибка при добавлении данных:", e)
#         session.rollback()
#     finally:
#         session.close()


# def update_user(data):
#     session = Session()

#     try:
#         record = (
#             session.query(User).filter(User.user_id == data["user_id"]).one_or_none()
#         )
#         if record:
#             record.status = data["status"]
#             record.registration_time = data["registration_time"]
#             record.name = data["name"]
#             record.id_chat = data["id_chat"]
#             record.user_state = data["user_state"]
#             record.agreement = data["agreement"]
#             record.language = data["language"]

#             session.commit()
#         else:
#             print(f"Запись не найдена.{data["user_id"]}")

#     except IntegrityError as e:
#         print("Ошибка целостности данных: возможно, дубликат ключа")
#         session.rollback()  # Отмена всех изменений в текущей транзакции

#     except Exception as e:
#         print("Ошибка при добавлении данных:", e)
#         session.rollback()
#     finally:
#         session.close()


# if __name__ == "__main__":
#     # Пример добавления данных (если необходимо)
#     session = Session()
#     users_data = {
#         "user_id": "154",
#         "status": True,
#         "registration_time": time.time(),
#         "name": "sdgsh",
#         "id_chat": "1125552",
#         "user_state": 0,
#         "agreement": 0,
#         "language": "RU",
#     }

#     user = User(
#         user_id=users_data["user_id"],
#         status=users_data["status"],
#         registration_time=users_data["registration_time"],
#         name=users_data["name"],
#         id_chat=users_data["id_chat"],
#         user_state=users_data["user_state"],
#         agreement=users_data["agreement"],
#         language=users_data["language"],
#     )
#     record_user(user)

#     # Получаем пользователя с определённым user_id
#     user_id_to_find = "1544"
#     found_user = get_user_by_id(user_id_to_find)

#     if found_user == None:
#         print("Пользователь найден:")
#     else:
#         print("Пользователь с user_id", user_id_to_find, "не найден.")
