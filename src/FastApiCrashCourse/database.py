from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os

Base = declarative_base()

class DBManager:
    def __init__(self):
        self.__db_engine =  create_engine(url=os.getenv("POSTGRES_BASE_URL"))
        self.__sql_alchemy_base = Base
        self.__sql_alchemy_base.metadata.create_all(bind=self.__db_engine)
        self.__db_session = sessionmaker(bind=self.__db_engine, autoflush=False, autocommit=False)
    def get_db_session(self):
        try:
            db_sessionx = self.__db_session()
            yield db_sessionx
        except Exception as e:
            raise e
        finally:
            db_sessionx.close()
