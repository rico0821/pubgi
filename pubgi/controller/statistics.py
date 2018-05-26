# -*- coding: utf-8 -*-
"""
    pubgi.controller.statistics
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for statistics controller functions. 
    -- Show about page.
    -- Show leaderboard page.
    -- Return leaderboard data for requested region and mode.
    -- Show statistics page.
      
    :copyright: (c) 2018 by rico0821.
    
"""
from flask import current_app, redirect, render_template, request, url_for
from sqlalchemy import desc

from pubgi.database import dao
from pubgi.pubgi_blueprint import pubgi
from pubgi.model.player import Player, SoloStats, DuoStats, SquadStats


@pubgi.route('/about')
def show_about():
    """Show about page."""
    
    return render_template('about.html')

@pubgi.route('/leaderboard')
def show_leaderboard():
    """
    Show leaderboard page for given region and mode.
    
    ARGS: region, mode
    
    """
    
    season = current_app.config['CURRENT_SEASON']
    region = request.args.get('region', '')
    mode = request.args.get('mode', '')
    
    if not region: 
        region = 'pc-krjp'
    if not mode:
        mode = 'solo'
        
    if mode == 'solo': 
        mod = SoloStats 
    elif mode == 'duo':
        mod = DuoStats
    elif mode == 'squad':
        mod = SquadStats
    else:
        return redirect(url_for('.show_leaderboard'))
    
    leaders = dao.query(mod).\
                         filter_by(season=season).\
                         filter_by(gameType=mode).\
                         join(mod.player).\
                         filter(Player.region==region).\
                         order_by(desc(mod.rating)).\
                         limit(100).all()
    
    return render_template('leaderboard.html', mode=mode,
                                                            region=region,
                                                            leaders=leaders)

@pubgi.route('/statistics')
def show_statistics():
    """Show statistics page."""
    
    return render_template('placeholder.html')