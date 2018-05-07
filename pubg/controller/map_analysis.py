# -*- coding: utf-8 -*-

from datetime import datetime

from flask import current_app, redirect, render_template, request, session, url_for, abort

from pubg.pubg_blueprint import pubg
from pubg.pubg_logger import Log
from pubg.database import dao
from pubg.model.player import Player, PlayerStats
from pubg.model.match import Match, MatchInfo, MatchStats


@pubg.route('/map')
def show_map():
    """Show map page."""
    
    return render_template('map.html')