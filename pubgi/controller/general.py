# -*- coding: utf-8 -*-
"""
    pubgi.controller.general
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for general controller functions. 
    -- Close db session at request teardown.
    -- Pagination object. 
      
    :copyright: (c) 2018 by rico0821.
    
"""
from math import ceil

from flask import request

from pubgi.database import dao
from pubgi.pubgi_blueprint import pubgi
from pubgi.pubgi_logger import Log

 
@pubgi.teardown_request
def close_db_session(exception=None):
    """Close DB session at request teardown."""
    
    try:
        dao.remove()
    except Exception as e:
        Log.error(str(e))

#######################################################################        
class Pagination:
    
    def __init__(self, page, per_page, total_count):
        self.page = page
        self.per_page = per_page
        self.total_count = total_count

    @property
    def pages(self):
        return int(ceil(self.total_count / float(self.per_page)))

    @property
    def has_prev(self):
        return self.page > 1

    @property
    def has_next(self):
        return self.page < self.pages

    def iter_pages(self, left_edge=2, left_current=2,
                   right_current=5, right_edge=2):
        last = 0
        for num in range(1, self.pages + 1):
            if num <= left_edge or \
               (num > self.page - left_current - 1 and \
                num < self.page + right_current) or \
                num > self.pages - right_edge:
                if last + 1 != num:
                    yield None
                yield num
                last = num