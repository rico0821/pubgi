# -*- coding: utf-8 -*-
"""
    pubgi.pubgi_logger
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for pubgi app server logging. 
    
    :copyright: (c) 2018 by rico0821.
    
"""

import logging
from logging import getLogger, handlers, Formatter


class Log:
    """Log engine class."""
    
    __log_level_dict = {
        'debug' : logging.DEBUG,
        'info' : logging.INFO,
        'warn' : logging.WARN,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    __my_logger=None
    
    @staticmethod
    def init(logger_name='PUBGI', 
             log_level='debug', 
             log_filepath='pubgi/resource/pubgi.log'):
        Log.__web_logger = getLogger(logger_name)
        Log.__web_logger.setLevel(Log.__log_level_dict.get(log_level, 'warn'))
        
        formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
        
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        Log.__web_logger.addHandler(console_handler)
        
        file_handler = handlers.TimedRotatingFileHandler(log_filepath,
                                                         when='D',
                                                         interval=1)
        file_handler.setFormatter(formatter)
        
        Log.__web_logger.addHandler(file_handler)
        
    @staticmethod
    def debug(msg):
        Log.__web_logger.debug(msg)
    
    @staticmethod
    def info(msg):
        Log.__web_logger.info(msg)
        
    @staticmethod
    def warn(msg):
        Log.__web_logger.warn(msg)
        
    @staticmethod
    def error(msg):
        Log.__web_logger.error(msg)
        
    @staticmethod
    def critical(msg):
        Log.__web_logger.critical(msg)