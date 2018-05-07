# -*- coding: utf-8 -*-

import os
from datetime import datetime


basedir = os.path.abspath(os.path.dirname(__file__))

class pubgConfig:
    
    # SQLAlchemy
    DB_URL= 'sqlite:///'
    DB_FILE_PATH= 'resource/database/pubg'
    TMP_FOLDER = 'resource/tmp/'
    
    # MongoDB
    MONGO_DBNAME = 'teledb'
    #MONGO_URI = 'mongodb://pubgg:rhemdfovj2018@ds247619.mlab.com:47619/teledb'
    MONGO_HOST = 'ds247619.mlab.com'
    MONGO_PORT = 47619
    MONGO_USERNAME = 'pubgg'
    MONGO_PASSWORD = 'rhemdfovj2018'
    
    # Session
    PERMANENT_SESSION_LIFETIME = 60 * 60
    SESSION_COOKIE_NAME= 'pubg_session'
    
    # Log
    LOG_LEVEL= 'debug'
    LOG_FILE_PATH= 'resource/log/pubg.log'
    DB_LOG_FLAG = 'False'
    
    # Paging
    PER_PAGE = 10
    
    # PUBG API
    UPDATE_WAIT_TIME = 60
    API_KEY = {
        'pc-kakao' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxOWEyNjE3MC0xOWU2LTAxMzYtYzUzYS0yZmZkMzhmZDU3ZmYiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTIyODEyNDgwLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InN0YXRlciIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.OT3XhJ7NY0TKvl7ObhaFhdumc0Fy_P_dhEH2N65MmRE',
        'pc-krjp' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxZjM3MTY0MC0xZTM1LTAxMzYtYTBhZC0wYjE5MWE5ZjM2ZmIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTIzMjg2MjI0LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InRlc3QyLTM5MmFmMDlmLWMzMWYtNDVhYy1hN2MzLTQyY2FkMzRmMTIyZiIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.ezy8Siq9MzZQ8ziuAzgQUCoTSx9BDGVrjK1FA_srGJw',
        'pc-eu' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIzMjY2M2IzMC0xZTM1LTAxMzYtYWM1NS0wZWQ2OWNlODVhZDEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTIzMjg2MjU3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InRlc3Q1Iiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.Gh5L0p58vfAc2VdmdP1jJhXgyY5zc8OL9lhKlLgTIEg',
        'pc-na' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyYTc4NmI1MC0xZTM1LTAxMzYtYTE2Yi0xYjkxNWQzZTYwZTIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTIzMjg2MjQzLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InRlc3Q0Iiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.PrE3c_7l1Kl6EXQHCh4djscItcV-k_I7Ae1BSJKICz4',
        'pc-as' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyNTgwMzM5MC0xZTM1LTAxMzYtYTE2OS0xYjkxNWQzZTYwZTIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTIzMjg2MjM1LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InRlc3QzLTExODljNGJkLTVkZTQtNDVjZS1hNGZmLTE3YTM3Y2Y5NjczOSIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.1L260ySikMlz8SGv27HVlt8cUwrN-1fLwDdSwS6trFA',
        'pc-oc' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIyMWUxOGVlMC0xZWQxLTAxMzYtY2NiNi0xMTdiNmJhYmQ1ODIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTIzMzUzMjMwLCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InBjLW9jIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.bIFJxg38zOFe6EK83fQRL_9AnA7U07t_4E3N7FkPhI4',
        'pc-sea' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiJmYzFmMDAwMC0xZWQwLTAxMzYtYTliMy0wMTkzZDc2NDgxOTEiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTIzMzUzMTY3LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InBjLXNlYSIsInNjb3BlIjoiY29tbXVuaXR5IiwibGltaXQiOjEwfQ.TArntkOsT_f-BK6OpVVDC_jLmQ2epvu4D3JJCkocKlo',
        'pc-sa' : 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJqdGkiOiIxOGZmNGIwMC0xZWQxLTAxMzYtY2NiNC0xMTdiNmJhYmQ1ODIiLCJpc3MiOiJnYW1lbG9ja2VyIiwiaWF0IjoxNTIzMzUzMjE1LCJwdWIiOiJibHVlaG9sZSIsInRpdGxlIjoicHViZyIsImFwcCI6InBjLXNhIiwic2NvcGUiOiJjb21tdW5pdHkiLCJsaW1pdCI6MTB9.GcPWT6EIrIXXSzytxHz_aALy5PrZ8cvKxzkndcD_siM'
    } 
    REGIONS = ['pc-krjp', 'pc-kakao', 'pc-sea', 'pc-sa', 'pc-as', 'pc-na', 'pc-eu', 'pc-oc']
    
    # Season
    CURRENT_SEASON = 5
    SEASON_UPDATE = datetime.strptime('2018-05-02 02:00:00', '%Y-%m-%d %H:%M:%S')
    
