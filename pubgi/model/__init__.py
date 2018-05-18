# -*- coding: utf-8 -*-
"""
    pubgi.model
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for initialising pubgi model package.
    -- Create declarative base for SQLAlchemy.
    
    :copyright: (c) 2018 by rico0821.
    
"""
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()

__all__ = ['player', 'match']