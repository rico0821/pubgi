# -*- coding: utf-8 -*-
"""
    pubmap
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    pubgmap 모듈. 
    :copyright: (c) 2018 by rico0821.
    :license: 
    
"""

from flask import current_app, redirect, render_template, request, session, url_for, abort

from pubg.pubgmap import pubgmap
from pubg.pubg_logger import Log
from pubg.database import dao
from pubg.model.player import Player, PlayerStats
from pubg.model.match import Match, MatchInfo, MatchStats


@pubgmap.route('/')
def index():
    pass