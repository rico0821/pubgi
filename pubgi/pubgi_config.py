# -*- coding: utf-8 -*-
"""
    pubgi.pubgi_config
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Configuration for pubgi app. 
    
    :copyright: (c) 2018 by rico0821.
    
"""
import os
from datetime import datetime


basedir = os.path.abspath(os.path.dirname(__file__))

class pubgiConfig:
    """Configuration object."""
    
    # SQLAlchemy
    DB_URL= 'sqlite:///'
    DB_FILE_PATH= 'resource/database/pubgi'
    TMP_FOLDER = 'resource/tmp/'
    
    # MongoDB
    MONGO_DBNAME = 'teledb'
    MONGO_HOST = ''
    MONGO_PORT = 
    MONGO_USERNAME = ''
    MONGO_PASSWORD = ''
    
    # Session
    PERMANENT_SESSION_LIFETIME = 60 * 60
    SESSION_COOKIE_NAME= 'pubgi_session'
    
    # Log
    LOG_LEVEL= 'debug'
    LOG_FILE_PATH= 'resource/log/pubgi.log'
    DB_LOG_FLAG = 'False'
    
    # Paging
    PER_PAGE = 10
    
    # PUBG API
    UPDATE_WAIT_TIME = 60
    API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxOWEyNjE3MC0xOWU2LTAxMzYtYzUzYS0yZmZkMzhmZDU3ZmYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTIyODEyNDgwLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InN0YXRlciIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.OT3XhJ7NY0TKvl7ObhaFhdumc0Fy_P_dhEH2N65MmRE'
    REGIONS = ['pc-krjp', 'pc-jp', 'pc-kakao', 'pc-sea', 'pc-sa', 'pc-as', 'pc-na', 'pc-eu', 'pc-oc', 'pc-ru']
    MODES = ['solo', 'duo', 'squad']
    MAP_NAMES = ['erangel', 'miramar', 'sanhok']
    
    # Season
    CURRENT_SEASON = 5
    SEASON_UPDATE = datetime.strptime('2018-05-02 02:00:00', '%Y-%m-%d %H:%M:%S')
