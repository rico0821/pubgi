# -*- coding: utf-8 -*-
"""
    pubgi.pubgi_blueprint
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for pubgi Flask blueprint.
    
    :copyright: (c) 2018 by rico0821.
    
"""
from flask import Blueprint

from pubgi.pubgi_logger import Log


pubgi = Blueprint('pubgi', __name__, template_folder='../templates', static_folder='../static')

Log.info('static folder: %s' % pubgi.static_folder)
Log.info('template folder: %s' % pubgi.template_folder)