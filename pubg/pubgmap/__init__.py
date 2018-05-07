# -*- coding: utf-8 -*-
"""
    pubgmap
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pubgmap 패키지 초기화 모듈. 
    pubgmap에 대한 flask 블루프린트를 생성함.
    :copyright: (c) 2018 by rico0821.
    :license: 
    
"""

from flask import Blueprint


pubgmap = Blueprint('pubgmap', 'pubgmap', url_prefix='/pubg_map')