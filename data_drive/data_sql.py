from pprint import pprint 
import time
from datetime import time as time_from_datatime
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

from src.settings import Settings
import logging


# region logging

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")
lg = logging.debug
cr = logging.critical
inf = logging.info
exp = logging.exception
# logging.disable(logging.DEBUG)
# logging.disable(logging.INFO)
# logging.disable(logging.CRITICAL)
# logging_end
# endregion

# Создание базового класса
Base = declarative_base()


# Определение структуры таблицы через класс


class Beton_zawod(Base):
    __tablename__ = "beton_zawod"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<BETHON(id_event_time={self.id_event_time}, DETE ={self.date_text})>"
    
class Beton_odola(Base):
    __tablename__ = "beton_odola"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<BETHON(id_event_time={self.id_event_time}, DETE ={self.date_text})>"
    
class Beton_zeran(Base):
    __tablename__ = "beton_zeran"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<BETHON(id_event_time={self.id_event_time}, DETE ={self.date_text})>"
    
class Beton_gora(Base):
    __tablename__ = "beton_gora"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<BETHON(id_event_time={self.id_event_time}, DETE ={self.date_text})>"


class Lista_zawod(Base):
    __tablename__ = "lista_zawod"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<LISTA(id_event_time={self.id_event_time}, DATE ={self.date_text})>"
    
class Lista_odola(Base):
    __tablename__ = "lista_odola"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<LISTA(id_event_time={self.id_event_time}, DATE ={self.date_text})>"
    
class Lista_zeran(Base):
    __tablename__ = "lista_zeran"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<LISTA(id_event_time={self.id_event_time}, DATE ={self.date_text})>"
    
class Lista_gora(Base):
    __tablename__ = "lista_gora"

    id_event_time = Column(Float, primary_key=True)
    date_text = Column(String)
    list_data = Column(String)
    day = Column(Integer)
    status = Column(Integer)

    def __repr__(self):
        return f"<LISTA(id_event_time={self.id_event_time}, DATE ={self.date_text})>"


# Создание базы данных SQLite в файле
engine = create_engine(Settings.data_base)

# Создание всех таблиц, которые еще не существуют
Base.metadata.create_all(engine)

# Создание сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)


def record_beton(data):
    session = Session()
    get_list_beton_serialize = [(item[0], item[1].isoformat(), *item[2:]) for item in data["lista_beton"]]
    serialized_list_beton = json.dumps(get_list_beton_serialize, default=str)
    try:
        if data["wenz"] == "zawod":
            beton = Beton_zawod(
                id_event_time=time.time(),
                date_text=data["date_of_day_text"],
                list_data=serialized_list_beton,
                day=data["day"],
                status=0,
            )
        elif data["wenz"] == "odola":
            beton = Beton_odola(
                id_event_time=time.time(),
                date_text=data["date_of_day_text"],
                list_data=serialized_list_beton,
                day=data["day"],
                status=0,
            )
        elif data["wenz"] == "zeran":
            beton = Beton_zeran(
                id_event_time=time.time(),
                date_text=data["date_of_day_text"],
                list_data=serialized_list_beton,
                day=data["day"],
                status=0,
            )
        elif data["wenz"] == "gora":
            beton = Beton_gora(
                id_event_time=time.time(),
                date_text=data["date_of_day_text"],
                list_data=serialized_list_beton,
                day=data["day"],
                status=0,
            )

        session.add(beton)
        session.commit()
    except IntegrityError as e:
        inf("Ошибка целостности данных: возможно, дубликат ключа")
        session.rollback()  # Отмена всех изменений в текущей транзакции

    except Exception as e:
        inf("Ошибка при добавлении данных:", e)
        session.rollback()
    finally:
        session.close()


def record_lista(data):
    session = Session()

    get_list_serialize = [(item[0].isoformat(), item[1]) for item in data["lista"]]
    serialized_list = json.dumps(get_list_serialize, default=str)
    try:
        if data["wenz"] == "zawod":
            lista = Lista_zawod(
                id_event_time=time.time(),
                date_text=data["date_of_day_text"],
                list_data=serialized_list,
                day=data["day"],
                status=0,
            )
        elif data["wenz"] == "odola":
            lista = Lista_odola(
                id_event_time=time.time(),
                date_text=data["date_of_day_text"],
                list_data=serialized_list,
                day=data["day"],
                status=0,
            )
        elif data["wenz"] == "zeran":
            lista = Lista_zeran(
                id_event_time=time.time(),
                date_text=data["date_of_day_text"],
                list_data=serialized_list,
                day=data["day"],
                status=0,
            )
        elif data["wenz"] == "gora":
            lista = Lista_gora(
                id_event_time=time.time(),
                date_text=data["date_of_day_text"],
                list_data=serialized_list,
                day=data["day"],
                status=0,
            )

        session.add(lista)
        session.commit()
    except IntegrityError as e:
        inf("Ошибка целостности данных: возможно, дубликат ключа")
        session.rollback()  # Отмена всех изменений в текущей транзакции

    except Exception as e:
        inf("Ошибка при добавлении данных:", e)
        session.rollback()
    finally:
        session.close()


def delete_records_below_threshold(threshold, base, wenz):
    """"Deletes all records from [base name] with id_event_time less than [threshold]

    Args:
        threshold (float): Time as a float from the beginning of the epoch
        base_name (str): base name
    """    

    if base == "beton" and wenz == "zawod":
        base_name = Beton_zawod
    elif base == "beton" and wenz == "odola":
        base_name = Beton_odola
    elif base == "beton" and wenz == "zeran":
        base_name = Beton_zeran
    elif base == "beton" and wenz == "gora":
        base_name = Beton_gora
    elif base == "lista" and wenz ==  "zawod":
        base_name = Lista_zawod
    elif base == "lista" and wenz ==  "odola":
        base_name = Lista_odola
    elif base == "lista" and wenz ==  "zeran":
        base_name = Lista_zeran
    elif base == "lista" and wenz ==  "gora":
        base_name = Lista_gora

    session = Session()

    try:
        # Отберите записи с большим или меньшим значением первичного ключа
        records_to_delete = session.query(base_name).filter(base_name.id_event_time < threshold).order_by(base_name.id_event_time).all()

        # Удалите выбранные записи
        for record in records_to_delete:
            session.delete(record)
        
        # Подтвердите изменения
        session.commit()
    except Exception as e:
        session.rollback()
        inf(f"An error occurred: {e}")
    finally:
        session.close()


def get_oldest_list_beton_or_lista(base, date_of_lista, wenz):
    
    if base == "beton" and wenz == "zawod":
        base_name = Beton_zawod
    elif base == "beton" and wenz == "odola":
        base_name = Beton_odola
    elif base == "beton" and wenz == "zeran":
        base_name = Beton_zeran
    elif base == "beton" and wenz == "gora":
        base_name = Beton_gora
    elif base == "lista" and wenz ==  "zawod":
        base_name = Lista_zawod
    elif base == "lista" and wenz ==  "odola":
        base_name = Lista_odola
    elif base == "lista" and wenz ==  "zeran":
        base_name = Lista_zeran
    elif base == "lista" and wenz ==  "gora":
        base_name = Lista_gora

    session = Session()

    try:
        result = session.query(base_name.list_data).filter(base_name.date_text == date_of_lista).order_by(base_name.id_event_time.asc()).first()
        
        if result:
            if base == "beton":
                deserialized_list = json.loads(result[0])
                result_list = [(item[0], time_from_datatime.fromisoformat(item[1]), *item[2:]) for item in deserialized_list]
                return result_list
            
            elif base == "lista":
                pass
           
        return []
    
    finally:
        session.close()

def get_newest_list_beton_or_lista(base, date_of_lista, wenz):
    
    if base == "beton" and wenz == "zawod":
        base_name = Beton_zawod
    elif base == "beton" and wenz == "odola":
        base_name = Beton_odola
    elif base == "beton" and wenz == "zeran":
        base_name = Beton_zeran
    elif base == "beton" and wenz == "gora":
        base_name = Beton_gora
    elif base == "lista" and wenz ==  "zawod":
        base_name = Lista_zawod
    elif base == "lista" and wenz ==  "odola":
        base_name = Lista_odola
    elif base == "lista" and wenz ==  "zeran":
        base_name = Lista_zeran
    elif base == "lista" and wenz ==  "gora":
        base_name = Lista_gora

    session = Session()

    try:
        result = session.query(base_name.list_data).filter(base_name.date_text == date_of_lista).order_by(base_name.id_event_time.desc()).first()
        inf("REZULT_____________________________________________________")
        if result:
            
            if base == "beton":
                deserialized_list = json.loads(result[0])
                result_list = [(item[0], time_from_datatime.fromisoformat(item[1]), *item[2:]) for item in deserialized_list]
                return result_list
            
            elif base == "lista":
                deserialized_list = json.loads(result[0])
                result_list = [(time_from_datatime.fromisoformat(item[0]), item[1]) for item in deserialized_list]
                return result_list
           
        return []
    
    finally:
        session.close()
    
    
if __name__ == '__main__':
    pprint(get_newest_list_beton_or_lista('beton', '03.02.2025', Settings.wenzels[0]))
