# -*- coding: utf-8 -*-

from flask import current_app, redirect, render_template, request, session, url_for, abort

from pubg.pubg_blueprint import pubg
from pubg.pubg_logger import Log
from pubg.database import dao
from pubg.model.player import Player, SoloStats, DuoStats, SquadStats
from pubg.controller.general import Pagination
from pubg.API.helper import getPlayerId


@pubg.route('/about')
def show_about():
    """Show about page."""
    
    return render_template('about.html')

@pubg.route('/leaderboard')
def show_leaderboard():
    """Show leaderboard page."""
    
    return render_template('placeholder.html')

@pubg.route('/statistics')
def show_statistics():
    """Show statistics page."""
    
    return render_template('placeholder.html')