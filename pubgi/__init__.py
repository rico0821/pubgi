# -*- coding: utf-8 -*-
"""
    pubgi
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for initialising pubgi package. 
    -- Create a Flask application for pubgi.
    -- Initilaise config, blueprint, session, DB.
    
    :copyright: (c) 2018 by rico0821.
    
"""

import os
from datetime import datetime

from flask import Flask, render_template, url_for


def print_settings(config):
    """
    Print settings on console.
    
    ARGS: config
    
    """
    
    print('-----------------------------------------------')
    print('SETTINGS')
    print('-----------------------------------------------')
    for key, value in config:
        print('%s=%s' % (key, value))
    print('-----------------------------------------------')

def not_found(error):
    """
    Common response handler for 404 error. 
    
    ARGS: error 
    
    """
    
    return render_template('404.html'), 404

def server_error(error):
    """
    Common response handler for 500 error. 
    
    ARGS: error 
    
    """
    
    err_msg = str(error)
    return render_template('500.html', err_msg=err_msg), 500

########################################################
def create_app(config_filepath='resource/config.cfg'):
    """
    Create Flask application for pubgi. 
    
    ARGS: config_filepath 
    
    """
    
    app = Flask(__name__)
        
    # CONFIG
    from pubgi.pubgi_config import pubgiConfig
    app.config.from_object(pubgiConfig)
    app.config.from_pyfile(config_filepath, silent=True)
    print_settings(app.config.items())
    
    # Initialise Log
    from pubgi.pubgi_logger import Log
    log_filepath = os.path.join(app.root_path,
                                app.config['LOG_FILE_PATH'])
    Log.init(log_filepath=log_filepath)
    
    # Load SQLAlchemy DB, Migrate
    from flask_migrate import Migrate
    from pubgi.database import DBManager, dao
    db_filepath = os.path.join(app.root_path, 
                               app.config['DB_FILE_PATH'])
    db_url = app.config['DB_URL'] + db_filepath
    DBManager.init(db_url, eval(app.config['DB_LOG_FLAG']))    
    DBManager.init_db()
    migrate = Migrate(app, dao)
    
    # Load MongoDB
    from pubgi.database import mongo
    mongo.init_app(app)
    
    # Load view functions
    from pubgi.controller import general
    from pubgi.controller import map_analysis
    from pubgi.controller import profile
    from pubgi.controller import search
    from pubgi.controller import statistics
    from pubgi.controller import update
    
    # Register blueprint
    from pubgi.pubgi_blueprint import pubgi 
    app.register_blueprint(pubgi)
    
    # Register SessionInterface
    from pubgi.cache_session import SimpleCacheSessionInterface
    app.session_interface = SimpleCacheSessionInterface()
    
    # Common error handlers
    app.register_error_handler(404, not_found)
    app.register_error_handler(500, server_error)
    
    # Jinja methods and filters
    import pubgi.pubgi_jinja as pj
    app.jinja_env.globals['url_for_other_page'] = pj.url_for_other_page
    app.jinja_env.filters['translate_mode'] = pj.translate_mode
    app.jinja_env.filters['translate_map'] = pj.translate_map
    app.jinja_env.filters['datetimeformat'] = pj.format_datetime
    app.jinja_env.filters['timesince'] = pj.timesince
    app.jinja_env.filters['numberformat'] = pj.format_number
    app.jinja_env.filters['recently_updated'] = pj.recently_updated
    app.jinja_env.filters['grade'] = pj.grade
    
    return app