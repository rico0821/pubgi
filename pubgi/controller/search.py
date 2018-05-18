# -*- coding: utf-8 -*-
"""
    pubgi.controller.search
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for search controller functions.
    -- Search for a player and shows results.
      
    :copyright: (c) 2018 by rico0821.
    
"""
from flask import current_app, redirect, render_template, request, url_for
from sqlalchemy import func

from pubgi.database import dao
from pubgi.pubgi_blueprint import pubgi
from pubgi.pubgi_logger import Log
from pubgi.API.helper import getPlayerId
from pubgi.model.player import Player, SoloStats, DuoStats, SquadStats


@pubgi.route('/search', methods=['POST'])
def search():
    """
    Search for a player.
    
    FORM: search_word
    
    1. For each region:
        i) Check whether PUBG player ID for player with given name and region exists:
            (a) If so: check whether the player exists in DB.
        ii) If player is not found in DB:
            (a) Create new player and stats, append accordingly.
            (b) Commit.
    2. Search DB for players with given name, ignoring case sensitivity. 
        i) If length = 1, return redirect to profile page for that player.
    3. Render template for search page, passing in results.
    
    """
    
    api_key = current_app.config['API_KEY']
    regions = current_app.config['REGIONS']
    season = current_app.config['CURRENT_SEASON']
    query = request.form['search_word']
    
    query_lower = query.lower()
    
    for region in regions:
        
        exist = False
        player_id = getPlayerId(region, query, api_key)
        
        if player_id:
            exist = dao.query(Player).filter_by(pubg_id=player_id).first()
        
        if player_id and not exist:
            try:
                new_player = Player(query, player_id, region)
                new_soloStats = SoloStats(season)
                new_duoStats = DuoStats(season)
                new_squadStats = SquadStats(season)
                dao.add_all([new_player, new_soloStats, new_duoStats, new_squadStats])
                
                new_player.solo.append(new_soloStats)
                new_player.duo.append(new_duoStats)
                new_player.squad.append(new_squadStats)

                dao.commit()

                Log.info('New player %r added.' % new_player)
            
            except Exception as e:
                dao.rollback()
                Log.error(str(e))
                raise e
                
    results = dao.query(Player).filter(func.lower(Player.name)==query_lower).all()
    
    if len(results) == 1:
        player = results[0]
        return redirect(url_for('.show_profile', 
                                player_name=player.name, region=player.region))
    
    return render_template('search.html', results=results, query=query)