# -*- coding: utf-8 -*-
"""
    pubgi.controller.profile
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for profile controller functions.
    -- Show index page. 
    -- Show profile page.
    -- Show match history page. 
    -- Show detailed stats page. 
      
    :copyright: (c) 2018 by rico0821.
    
"""
from flask import abort, current_app, redirect, render_template, request, url_for
from pubg_python import PUBG, Shard

from pubgi.database import dao
from pubgi.pubgi_blueprint import pubgi
from pubgi.pubgi_logger import Log
from pubgi.API.helper import getPlayerId, shardDict
from pubgi.controller.general import Pagination
from pubgi.model.player import Player, SoloStats, DuoStats, SquadStats


@pubgi.route('/')
def index():
    """Show index page."""
    
    return render_template('index.html')

@pubgi.route('/profile/<player_name>')
def show_profile(player_name):
    """
    Show player profile page.
    
    ARGS: player_name, region
    
    1. Check whether player name and region are correctly given. 
        i) If not so: abort.
    2. Check if player with given name and region exists in DB.
        i) If not so:
            (a) Find PUBG player ID using API. If not found, render page for not found.
            (b) Create new player with stats for each game mode, append them accordingly and commit.
            (c) Render profile page for player created.
        ii) If so: render profile page for player found.
    3. Check whether stats exist for current season. 
        i) If not so:
            (a) Create new stats for each game mode, for current season.
            (b) Add all, append and then commit.
            
    """
    
    api_key = current_app.config['API_KEY']
    season = current_app.config['CURRENT_SEASON']
    region = request.args.get('region', '')
    
    if not (player_name or region):
        abort(404)
        
    player = dao.query(Player).filter_by(name=player_name).\
                               filter_by(region=region).first()
   
    if not player:
        
        api = PUBG(api_key, shardDict(region))
        pubg_player = api.players.filter(player_names=[player_name])
        #pubg_id = getPlayerId(region, player_name, api_key[region])
        
        if not pubg_id:
            return render_template('search.html', results=None, query=player_name)
        try:
            player = Player(player_name, pubg_id, region)
            soloStats = SoloStats(season)
            duoStats = DuoStats(season)
            squadStats = SquadStats(season)
            dao.add_all([player, soloStats, duoStats, squadStats])
            
            player.solo.append(soloStats)
            player.duo.append(duoStats)
            player.squad.append(squadStats)

            dao.commit()
            
            Log.info('New player %r added.' % player)
        
        except Exception as e:
            dao.rollback()
            Log.error(str(e))
            raise e
        
        else:
            return render_template('profile_overview.html', player=player)
        
    stats_exist = any(x.season == season for x in player.solo)
            
    if not stats_exist:
        try:
            soloStats = SoloStats(season)
            duoStats = DuoStats(season)
            squadStats = SquadStats(season)
            dao.add_all([soloStats, duoStats, squadStats])

            player.solo.append(soloStats)
            player.duo.append(duoStats)
            player.squad.append(squadStats)

            dao.commit()
            Log.info('New season stats for player %r added.' % player)
            
        except Exception as e:
            dao.rollback()
            Log.error(str(e))
            raise e        
    
    return render_template('profile_overview.html', player=player)

@pubgi.route('/profile/<player_name>/match_history/', defaults={'page': 1})
@pubgi.route('/profile/<player_name>/match_history/page/<int:page>')
def show_match_history(player_name, page=1):
    """
    Show player match history page.
    
    ARGS: player_name, region
    
    1. Check whether player name and region are correctly given.
        i) If not so: abort.
    2. Check whether player with given name and region exists. 
        i) If not so: redirect to profile page for player with given name and region.
    3. Set up for pagination:
        i) Get count of player's records.
        ii) Create Pagination instance
        iii) Create offset using page number.
        iv) Reverse and slice record for viewing.
    4. Render profile matches page passing in edited records list.
    
    """

    api_key = current_app.config['API_KEY']
    per_page = current_app.config['PER_PAGE']
    region = request.args.get('region', '')
    
    if not (player_name or region):
        abort(404)
        
    player = dao.query(Player).filter_by(name=player_name).\
                               filter_by(region=region).first()
    if not player:
        return redirect(url_for('.show_profile', player_name=player_name, region=region))
    
    match_count = len(player.records)
    pagination = Pagination(page, per_page, match_count)
    
    if page != 1:
        offset = per_page * (page - 1)
    else:
        offset = 0
    
    start = offset
    end = offset + per_page
    reversed_record = list(reversed(player.records))
    match_pages = reversed_record[start:end]
    
    return render_template('profile_matches.html', 
                           player=player, 
                           matches=match_pages,
                           pagination=pagination)

@pubgi.route('/profile/<player_name>/statistics')
def show_stats(player_name):
    """
    Show player statistics page.
    
    ARGS: player_name, region
    
    1. Check whether player name and region are correctly given. 
        i) If not so: abort.
    
    """
    
    region = request.args.get('region', '')
    
    if not (player_name or region):
        abort(404)
        
    player = dao.query(Player).filter_by(name=player_name).\
                               filter_by(region=region).first()
        
    if not player:
        return redirect(url_for('.show_profile', player_name=player_name, region=region))
    
    return render_template('profile_statistics.html', player=player)