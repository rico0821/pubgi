# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from flask import request, url_for


def url_for_other_page(page, player_name, region):
    
    args = request.view_args.copy()
    args['page'] = page
    args['player_name'] = player_name
    args['region'] = region
    
    return url_for(request.endpoint, **args)

def translate_mode(mode):
    """Translate game mode into Korean."""
    
    dic = {
        'solo' : '솔로',
        'duo' : '듀오',
        'squad' : '스쿼드',
        'tequilatpp' : '데킬라',
        'warmodetpp' : '워모드'
    }
        
    return dic[mode]

def translate_map(name):
    """Translate map name into Korean."""
    
    if name =='':
        return 'N/A'
    dic = {
        'Erangel_Main' : '에란겔',
        'Desert_Main' : '미라마',
        'N/A' : 'N/A'
    }
    
    return dic[name]

def translate_timestamp(timestamp):
    """Create a datetime object for PUBG timestamp."""
    
    date_object = datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%SZ')
    
    return date_object

def format_datetime(timestamp, timezone):
    """Format a timestamp for display."""
    if timezone == 'KR':
        timestamp = timestamp + timedelta(hours=9)
        value = timestamp.strftime('%Y-%m-%d %H:%M')
    return value

def timesince(dt, default=None):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    """
    if not default:
        default = "방금 전"
    now = datetime.utcnow()
    diff = now - dt
    
    periods = (
        (diff.days / 365, "년"),
        (diff.days / 30, "개월"),
        (diff.days / 7, "주"),
        (diff.days, "일"),
        (diff.seconds / 3600, "시간"),
        (diff.seconds / 60, "분"),
        (diff.seconds, "초")
    )

    for period, singular in periods:
        
        if int(period):
            return "%d%s 전" % (period, singular)

    return default

def recently_updated(timestamp):
    """
    Check whether the player has updated recently.
    """

    now = datetime.utcnow()
    diff = now - timestamp
    
    result = True
    
    if diff.seconds > 60:
        result = False

    return result

def format_number(value):
    """Format number to have commas for thousands."""
    
    return '{:,}'.format(value)

def grade(stats):
    """Turn stats into grade. (Needs improvement)"""
    
    battle_stats = stats.kill + stats.dbno
    survive_stats = stats.timeSurvived
    try:
        mobility_stats = stats.rideDistance / stats.walkDistance
    except:
        mobility_stats = 0
    support_stats = stats.assist + stats.revive
    supply_stats = stats.boost + stats.heal + stats.weapon
    
    if hasattr(stats, 'game'):
        battle_stats = battle_stats / max(1,(stats.game))
        survive_stats = survive_stats / max(1,(stats.game))
        support_stats = support_stats / max(1,(stats.game))
        supply_stats = supply_stats / max(1,(stats.game))
            
    
    if battle_stats > 15:
        battle = 'S'
    elif battle_stats > 10:
        battle = 'A'
    elif battle_stats > 7:
        battle = 'B'
    elif battle_stats > 5:
        battle = 'C'
    elif battle_stats > 3:
        battle = 'D'
    elif battle_stats > 1:
        battle = 'E'
    else:
        battle = 'F'
        
    if survive_stats > 30*60:
        survive = 'S'
    elif survive_stats > 25*60:
        survive = 'A'
    elif survive_stats > 20*60:
        survive = 'B'
    elif survive_stats > 15*60:
        survive = 'C'
    elif survive_stats > 10*60:
        survive = 'D'
    elif survive_stats > 5*60:
        survive = 'E'
    else:
        survive = 'F'
        
    if mobility_stats > 4:
        mobility = 'S'
    elif mobility_stats > 3:
        mobility = 'A'
    elif mobility_stats > 2:
        mobility = 'B'
    elif mobility_stats > 1:
        mobility = 'C'
    elif mobility_stats > 0.5:
        mobility = 'D'
    elif mobility_stats > 0.25:
        mobility = 'E'
    else:
        mobility = 'F'
        
    if support_stats > 9:
        support = 'S'
    elif support_stats > 7:
        support = 'A'
    elif support_stats > 5:
        support = 'B'
    elif support_stats > 3:
        support = 'C'
    elif support_stats > 1:
        support = 'D'
    else:
        support = 'F'
        
    if supply_stats > 20:
        supply = 'S'
    elif supply_stats > 15:
        supply = 'A'
    elif supply_stats > 10:
        supply = 'B'
    elif supply_stats > 5:
        supply = 'C'
    elif supply_stats > 3:
        supply = 'D'
    elif supply_stats > 1:
        supply = 'E'
    else:
        supply = 'F'
        
    grades = {
        'battle' : battle,
        'survive' : survive,
        'mobility' : mobility,
        'support' : support,
        'supply' : supply,
        'battle_stats' : battle_stats,
        'survive_stats' : survive_stats,
        'mobility_stats' : mobility_stats,
        'support_stats' : support_stats,
        'supply_stats' : supply_stats
    }
    
    return grades