# -*- coding: utf-8 -*-

from flask import Blueprint
from pubg.pubg_logger import Log


pubg = Blueprint('pubg', __name__, template_folder='../templates', static_folder='../static')

Log.info('static folder: %s' % pubg.static_folder)
Log.info('template folder: %s' % pubg.template_folder)