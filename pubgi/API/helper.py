# -*- coding: utf-8 -*-
"""
    pubgi.API.helper
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for PUBG API wrapper.
      
    :copyright: (c) 2018 by rico0821.
    
"""
import json, requests, time

from datetime import datetime

from pubg_python import Shard
from pubgi.pubgi_logger import Log


def _make_url(region, query_type, query_filter=None, query=None):
    """
    Make API request URL.
    
    ARGS: region, query_type, (query_filter), (query)
    
    """
    
    url = 'https://api.playbattlegrounds.com/shards/' + region + '/' + query_type
    
    if query_filter:
        url = url + '?filter[' + query_filter + ']=' + query

    elif query:
        url = url + '/' + query

    return url

def _getRequest(region, query_type, query_filter, query, api_key):
    """
    Use URL to send request to API.
    
    ARGS: region, query_type, query_filter, query, api_key
    
    """
    
    url = _make_url(region, query_type, query_filter, query)
   
    headers = {
      "Authorization" : api_key,
      "Accept" : "application/vnd.api+json"
    }

    try:
        Log.info('Sent API request to %s' % url)
        start_time = time.time()
        result = requests.get(url, headers=headers)
        Log.info('Received API request %r: took %f sec' % (result, time.time()-start_time))
        if result:
            result = result.json()
        
    except Exception as e:
        raise e
    
    return result
    
def _getPlayerData(region, player, api_key):
    """
    Get player data from API.
    
    ARGS: region, player, api_key
    
    """
    
    query_type = 'players'
    query_filter = 'playerNames'
    
    result = _getRequest(region, query_type, query_filter, player, api_key)
    
    return result

def _processPlayerId(data):
    """
    Find player ID from player data.
    
    ARGS: data
    
    """
    
    if 'data' in data:
        try:
            player_id = data['data'][0]['id']
            
        except Exception as e:
            raise e
    else:
        return False
    
    return player_id

def _processMatchIds(data):
    """
    Find match IDs from player data.
    
    ARGS: data
    
    """
    try: 
        matches = data['data'][0]['relationships']['matches']['data']
        for match in reversed(matches):
            yield match['id']
        else:
            return False

    except Exception as e:
        raise e
    
def _getMatch(region, match_id, api_key):
    """
    Get match data from API.
    
    ARGS: region, match_id, api_key
    
    """
    
    query_type = 'matches'
    query_filter = None
    
    result = _getRequest(region, query_type, query_filter, match_id, api_key)
    
    return result

def _processParticipantData(match_data, player_id):
    """
    Find player's stats from match data.
    
    ARGS: match_data, player_id
    
    """
    
    try:
        participant_data = next(data['attributes']['stats'] \
                            for data in match_data['included'] \
                            if data['type']=='participant' and \
                            data['attributes']['stats']['playerId'] == player_id)
        
    except Exception as e:
        raise e
        
    return participant_data

def _processMatchData(match_data):
    """
    Find match info from match data.
    
    ARGS: match_data
    
    """
    
    try:
        match_info = match_data['data']['attributes']
        
    except Exception as e:
        raise e
    
    return match_info

def _processRosterData(match_data, player_id):
    """
    Find roster data from match data.
    
    ARGS: match_data, player_id
    
    """
    
    try:
        participant_id = next(data['id'] for data in match_data['included'] \
                             if data['type']=='participant' and \
                             data['attributes']['stats']['playerId']==player_id)
        
        for data in match_data['included']:
            if data['type'] == 'roster':    
                for participant in data['relationships']['participants']['data']:
                    if participant['id'] == participant_id:
                        return data['id']

    except Exception as e:
        raise e

def _processTelemetryURL(match_data):
    """
    Find telemetry URL from match data.
    
    ARGS: match_data
    
    """
    
    try: 
        url = next(data['attributes']['URL'] for data in match_data['included'] \
                      if data['type']=='asset')
        
    except Exception as e:
        raise e
        
    return url
        
def getPlayerId(region, player, api_key):
    """
    Get a player's game id.
    
    ARGS: region, player, api_key
    
    """
    
    player_data = _getPlayerData(region, player, api_key)
    player_id = _processPlayerId(player_data)
    
    return player_id

def getPlayerStats(region, player, api_key, last_match_id):
    """
    Get a tuple containing player id, match id, match stats.
    
    ARGS: region, player, api_key, last_match_id
    
    """
    
    player_id = getPlayerId(region, player, api_key)
    player_data = _getPlayerData(region, player, api_key)
    match_ids = list(_processMatchIds(player_data))
    
    try:
        if last_match_id:
            upto = match_ids.index(last_match_id) + 1
        else: 
            upto = 0
            Log.info('No recent matches were recorded for player %r [region: %r]' % (player, region))
            
        for match_id in match_ids[upto:]:
            match_data = _getMatch(region, match_id, api_key)
            match_info = _processMatchData(match_data)
            match_stats = _processParticipantData(match_data, player_id)
            roster_data = _processRosterData(match_data, player_id)
            telemetry_url = _processTelemetryURL(match_data)
            yield (match_id, match_stats, match_info, roster_data, telemetry_url)
            
    except Exception as e:
        raise e
        Log.error('Error finding matches found for player %r [region: %r]' % (player, region))
        return False
    
def getTelemetry(url):
    """
    Get telemetry data using asset URL.
    
    ARGS: url
    
    """
    
    headers = {
      "Accept" : "application/vnd.api+json"
    }
    result = None
    try:
        Log.info('Sent API request to %s' % url)
        start_time = time.time()
        result = requests.get(url, headers=headers)
        Log.info('Received API request %r: took %f sec' % (result, time.time()-start_time))
        if result:
            result = result.json()
        
    except Exception as e:
        raise e
    
    return result

def filterTelemetry(telemetry, filters):
    try:
        filter_telemetry = [data for data in telemetry
                for filter in filters if data['_T'] == filter]
        Log.info("Filtered Telemetry Data : " + filter_telemetry.__repr__())

    except Exception as e:
        raise e

    return filter_telemetry

shardDict = {
    'pc-kakao' : Shard.PC_KAKAO,
    'pc-krjp' : Shard.PC_KRJP,
    'pc-eu' : Shard.PC_EU,
    'pc-na' : Shard.PC_NA,
    'pc-as' : Shard.PC_AS,
    'pc-oc' : Shard.PC_OC,
    'pc-sea' : Shard.PC_SEA,
    'pc-sa' : Shard.PC_SA,
    'pc-ru' : Shard.PC_RU,
    'pc-jp' : Shard.PC_JP
}