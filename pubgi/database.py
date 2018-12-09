# -*- coding: utf-8 -*-
"""
    pubgi.database
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for pubgi app database.
    -- Create SQLAlchemy database engine.
    -- Create PyMongo database engine. 
    
    :copyright: (c) 2018 by rico0821.
    
"""
from flask_pymongo import PyMongo
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


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
        from pubgi.model import player
        from pubgi.model import match
        from pubgi.model import average
        from pubgi.model import Base
        Base.metadata.create_all(bind=DBManager.__engine)

dao = None

mongo = PyMongo() 