# -*- coding: utf-8 -*-

from datetime import datetime

from flask import current_app, redirect, render_template, request, session, url_for, abort, jsonify

from pubg.database import dao, mongo
from pubg.pubg_blueprint import pubg
from pubg.pubg_logger import Log
from pubg.API.helper import getPlayerStats, getTelemetry
from pubg.model.match import Match, MatchInfo, MatchStats, Record, Roster
from pubg.model.player import Player, SoloStats, DuoStats, SquadStats


@pubg.route('/profile/<player_id>/update')
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
    
    diff = datetime.utcnow() - player.update_time
    
    if diff.seconds < current_app.config['UPDATE_WAIT_TIME']:
        return redirect(url_for('.show_profile', player_name=player.name, region=player.region))
    
    stats_exist = any(x.season == season for x in player.solo)
            
    if not stats_exist:
        try:
            new_soloStats = SoloStats(season)
            new_duoStats = DuoStats(season)
            new_squadStats = SquadStats(season)
            dao.add_all([new_soloStats, new_duoStats, new_squadStats])

            new_player.solo.append(new_soloStats)
            new_player.duo.append(new_duoStats)
            new_player.squad.append(new_squadStats)

            dao.commit()
            Log.info('New season stats for player %r added.' % player)
        
        except Exception as e:
            dao.rollback()
            Log.error(str(e))
            raise e
            
    last_match_id = None
    
    if player.records:
        last_match_id = player.records[-1].pubg_match_id
    player_stats = getPlayerStats(player.region, player.name, api_key[player.region], last_match_id)
    # player_stats = (match_id, match_stats, match_info, roster_data, telemetry_url)
    for data in player_stats:
        
        pubg_match_id = data[0]

        record_exist = dao.query(Record).filter_by(player_id=player.id).\
                        filter_by(pubg_match_id=pubg_match_id).first()
        
        try:
            if not record_exist:
                    match_exist = dao.query(Match).filter_by(pubg_id=pubg_match_id).first()

                    if not match_exist:
                        match_exist = Match(pubg_match_id)
                        match_info = MatchInfo(data[2])
                        dao.add_all([match_exist, match_info])

                        match_exist.info = match_info
                        
                        telemetry_data = getTelemetry(data[4])
                        tele_exist = mongo.db.matches.find_one({'match_id' : pubg_match_id})
                        if not tele_exist:
                            mongo.db.matches.insert({'match_id' : pubg_match_id, 'data' : telemetry_data})
                            Log.info('Telemetry data added for match %r' % match_exist)
                        Log.info('Match %r added' % match_exist)

                    roster = dao.query(Roster).filter_by(pubg_roster_id=data[3]).first()

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
              
            player.update_time = datetime.utcnow()
            dao.commit()
            
        except Exception as e:
            dao.rollback()
            Log.error(str(e))
            return jsonify(result=False)

    return jsonify(result=True)

        