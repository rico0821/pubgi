# -*- coding: utf-8 -*-
"""
    pubgi.controller.update 
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for update controller functions.
    -- Update player records. 
      
    :copyright: (c) 2018 by rico0821.
    
"""
from datetime import datetime

from flask import abort, current_app, jsonify, redirect, render_template, url_for

from pubgi.database import dao, mongo
from pubgi.pubgi_blueprint import pubgi
from pubgi.pubgi_logger import Log
from pubgi.API.helper import getPlayerStats, getTelemetry, filterTelemetry
from pubgi.model.match import Match, MatchInfo, MatchStats, Record, Roster
from pubgi.model.player import Player, SoloStats, DuoStats, SquadStats


@pubgi.route('/profile/<player_id>/update')
def update(player_id):
    """
    Update player's matches.
    
    ARGS: player_id
    
    1. Check if player with given ID exists.
        i) If not so, abort.
    2. Check if the player has been recently updated.
        i) If so, redirect to profile page for player with given name and region.
    3. Check season.
        i) If new season, create new player stats for each game mode, append them and commit.
    4. Find the PUBG match ID of the latest record and use it to get data from API on matches since.
    5. For each match data:
        i) Check if record with PUBG match ID for player with given ID exists in DB. 
            (a) If so: nothing happens.
        ii) Check if match with PUBG match ID exists in DB.
            (a) If not so: create one and its match info and save telemetry data to mongoDB.
        iii) Check if roster with PUBG roster ID exists in DB. If not so, create one and append to match.
        iv) Check match season.
        v) Create record and match stats and append them accordingly.
        vi) Check game mode and aggregate player stats accordingly.
        vii) Set player's update time to now and finally commit.
    6. Return jsonified signal for success or failure
    
    """
    
    api_key = current_app.config['API_KEY']
    season = current_app.config['CURRENT_SEASON']
    season_update = current_app.config['SEASON_UPDATE']
        
    player = dao.query(Player).get(player_id)
    
    if not player:
        abort(404)
    
    diff = datetime.utcnow() - player.updateTime
    
    if diff.seconds < current_app.config['UPDATE_WAIT_TIME']:
        return redirect(url_for('.show_profile', player_name=player.name, region=player.region))
    
    stats_exist = any(x.season == season for x in player.solo)
            
    if not stats_exist:
        try:
            new_soloStats = SoloStats(season)
            new_duoStats = DuoStats(season)
            new_squadStats = SquadStats(season)
            dao.add_all([new_soloStats, new_duoStats, new_squadStats])

            player.solo.append(new_soloStats)
            player.duo.append(new_duoStats)
            player.squad.append(new_squadStats)

            dao.commit()
            Log.info('New season stats for player %r added.' % player)
        
        except Exception as e:
            dao.rollback()
            Log.error(str(e)+" in check1")
            raise e
            
    last_match_id = None
    
    if player.records:
        last_match_id = player.records[-1].pubgMatchID
    player_stats = getPlayerStats(player.region, player.name, api_key, last_match_id)
    # player_stats = (match_id, match_stats, match_info, roster_data, telemetry_url)
    for data in player_stats:
        
        pubg_match_id = data[0]

        record_exist = dao.query(Record).filter_by(playerID=player.id).\
                        filter_by(pubgMatchID=pubg_match_id).first()
        
        try:
            if not record_exist:
                    match_exist = dao.query(Match).filter_by(pubgID=pubg_match_id).first()

                    if not match_exist:
                        match_exist = Match(pubg_match_id)
                        match_info = MatchInfo(data[2])
                        dao.add_all([match_exist, match_info])

                        match_exist.info = match_info
                        
                        telemetry_data = getTelemetry(data[4])
                        tele_exist = mongo.db.matches.find_one({'matchID' : pubg_match_id})
                        """
                        if not tele_exist:
                            filter_tele = filterTelemetry(telemetry_data, ["LogItemPickup", "LogPlayerPosition", "LogGameStatePeriodic", "LogPlayerKill"])
                            mongo.db.matches.insert({'matchID' : pubg_match_id, 
                                                              'map' : match_info.mapName,
                                                              'data' : telemetry_data})
                            Log.info('Telemetry data added for match %r' % match_exist)
                        """
                    roster = dao.query(Roster).filter_by(pubgRosterID=data[3]).first()

                    if not roster:
                        roster = Roster(data[3])
                        dao.add(roster)

                        match_exist.rosters.append(roster)
                    
                    timestamp = match_exist.info.createdAt
                    createdAt = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
                    match_season = season
                    if createdAt < season_update:
                        match_season = season - 1
                    
                    record = Record(pubg_match_id, match_season)
                    match_stats = MatchStats(data[1])
                    dao.add_all([match_stats, record])

                    roster.participants.append(record)
                    record.stats = match_stats
                    player.records.append(record)

                    info = roster.match.info
                    if info.gameMode == 'solo':
                        next(stats for stats in player.solo if stats.season==match_season).aggregate(data[1])
                    elif info.gameMode == 'duo':
                        next(stats for stats in player.duo if stats.season==match_season).aggregate(data[1])
                    elif info.gameMode == 'squad':
                        next(stats for stats in player.squad if stats.season==match_season).aggregate(data[1])
                    else:
                        player.event_games += 1
                    
                    dao.commit()
                    Log.info('%r with %r added to %r' % (record, match_stats, player))
            
        except Exception as e:
            dao.rollback()
            Log.error(str(e))
            return jsonify(result=False)
    
    player.updateTime = datetime.utcnow()
    dao.commit()

    return jsonify(result=True)