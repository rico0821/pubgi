# -*- coding: utf-8 -*-
"""
    pub.gg
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pubg 패키지 초기화 모듈. 
    pubg에 대한 flask 어플리케이션을 생성함.
    config, blueprint, session, DB연결 등을 초기화함.
    :copyright: (c) 2018 by rico0821.
    :license: 
    
"""

import os
from datetime import datetime

from flask import Flask, render_template, request, url_for


def print_settings(config):
    print('-----------------------------------------------')
    print('SETTINGS')
    print('-----------------------------------------------')
    for key, value in config:
        print('%s=%s' % (key, value))
    print('-----------------------------------------------')

def not_found(error):
    return render_template('404.html'), 404

def server_error(error):
    err_msg = str(error)
    return render_template('500.html', err_msg=err_msg), 500

########################################################
def create_app(config_filepath='resource/config.cfg'):
    
    app = Flask(__name__)
        
    # CONFIG
    from pubg.pubg_config import pubgConfig
    app.config.from_object(pubgConfig)
    app.config.from_pyfile(config_filepath, silent=True)
    print_settings(app.config.items())
    
    # Initialise Log
    from pubg.pubg_logger import Log
    log_filepath = os.path.join(app.root_path,
                                app.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)
    
    # Load SQLAlchemy DB, Migrate
    from flask_migrate import Migrate
    from pubg.database import DBManager, dao
    db_filepath = os.path.join(app.root_path, 
                               app.config['DB_FILE_PATH'])
    db_url = app.config['DB_URL'] + db_filepath
    DBManager.init(db_url, eval(app.config['DB_LOG_FLAG']))    
    DBManager.init_db()
    migrate = Migrate(app, dao)
    
    # Load MongoDB
    from pubg.database import mongo
    mongo.init_app(app)
    
    # Load view functions
    from pubg.controller import general
    from pubg.controller import profile
    from pubg.controller import search
    from pubg.controller import update
    from pubg.controller import statistics
    from pubg.controller import map_analysis
    
    # Blueprint
    from pubg.pubg_blueprint import pubg 
    from pubg.pubgmap import pubgmap
    app.register_blueprint(pubg)
    app.register_blueprint(pubgmap)
        
    # SessionInterface
    from pubg.cache_session import SimpleCacheSessionInterface
    app.session_interface = SimpleCacheSessionInterface()
    
    # Common error handlers
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, server_error)
    
    # Jinja methods and filters
    import pubg.pubg_jinja as pj
    app.jinja_env.globals['url_for_other_page'] = pj.url_for_other_page
    app.jinja_env.filters['translate_mode'] = pj.translate_mode
    app.jinja_env.filters['translate_map'] = pj.translate_map
    app.jinja_env.filters['translate_timestamp'] = pj.translate_timestamp
    app.jinja_env.filters['datetimeformat'] = pj.format_datetime
    app.jinja_env.filters['timesince'] = pj.timesince
    app.jinja_env.filters['numberformat'] = pj.format_number
    app.jinja_env.filters['recently_updated'] = pj.recently_updated
    app.jinja_env.filters['grade'] = pj.grade
    
    return app