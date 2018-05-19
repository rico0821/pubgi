# -*- coding: utf-8 -*-
"""
    pubgi.controller.statistics
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for statistics controller functions. 
    -- Show about page. 
    -- Show leaderboard page. 
    -- Show statistics page. 
      
    :copyright: (c) 2018 by rico0821.
    
"""
from flask import current_app, render_template, url_for

from pubgi.database import dao
from pubgi.pubgi_blueprint import pubgi
from pubgi.pubgi_logger import Log
from pubgi.API.helper import getPlayerId
from pubgi.controller.general import Pagination
from pubgi.model.player import Player, SoloStats, DuoStats, SquadStats


@pubgi.route('/about')
def show_about():
    """Show about page."""
    
    return render_template('about.html')

@pubgi.route('/leaderboard')
def show_leaderboard():
    """Show leaderboard page."""
    
    return render_template('leaderboard.html')

@pubgi.route('/statistics')
def show_statistics():
    """Show statistics page."""
    
    return render_template('placeholder.html')