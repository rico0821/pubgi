# -*- coding: utf-8 -*-

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_pymongo import PyMongo

class DBManager:
    """Common class for handling DB."""
    
    __engine = None
    __session = None

    @staticmethod
    def init(db_url, db_log_flag=True):
        DBManager.__engine = create_engine(db_url, echo=db_log_flag) 
        DBManager.__session = scoped_session(sessionmaker(autocommit=False, 
                                                                              autoflush=False, 
                                                                              bind=DBManager.__engine))
        global dao
        dao = DBManager.__session
    
    @staticmethod
    def init_db():
        from pubg.model import player
        from pubg.model import match
        from pubg.model import Base
        Base.metadata.create_all(bind=DBManager.__engine)

dao = None

mongo = PyMongo() 