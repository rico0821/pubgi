# -*- coding: utf-8 -*-

from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from pubg.model import Base
from pubg.model.player import Player


class Match(Base):
    
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    pubg_id = Column(String(50), nullable=False)
    
    retrievedAt = Column(DateTime, default=datetime.utcnow())
    
    info = relationship('MatchInfo', 
                            uselist=False, 
                            cascade='delete',
                            backref='match')
    rosters = relationship('Roster',
                             cascade='delete',
                             backref='match')
    
    def __init__(self, pubg_id):
        
        self.pubg_id = pubg_id
        
    def __repr__(self):
        return '<Match %r>' % (self.pubg_id)


class MatchInfo(Base):
    
    __tablename__ = 'match_info'
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey(Match.id), unique=True)
    
    createdAt = Column(String(50), nullable=False)
    gameMode = Column(String(30), nullable=False)
    mapName = Column(String(30), nullable=False)
    
    def __init__(self, info):
        
        self.createdAt = info['createdAt']
        self.gameMode = info['gameMode']
        try:
            self.mapName = info['mapName']
        except:
            self.mapName = 'N/A'
    
    def __repr__(self):
        return '<Match info %r %r>' % (self.id, self.match_id)
        
        
class Roster(Base):
    
    __tablename__ = 'rosters'
    
    id = Column(Integer, primary_key=True)
    match_id = Column(Integer, ForeignKey(Match.id))
    pubg_roster_id = Column(String(50), nullable=False)
    
    participants = relationship('Record',
                               backref='roster')
    
    def __init__(self, pubg_roster_id):
        
        self.pubg_roster_id = pubg_roster_id
    def __repr__(self):
        return '<Roster %r in match %r>' % (self.id, self.match_id)    
    
    
class Record(Base):
    
    __tablename__ = 'records'
    
    id = Column(Integer, primary_key=True)
    
    player_id = Column(Integer, ForeignKey(Player.id))
    roster_id = Column(Integer, ForeignKey(Roster.id))
    pubg_match_id = Column(String(50), nullable=False)
    season = Column(Integer, nullable=False)
    
    stats = relationship('MatchStats', 
                              uselist=False, 
                              cascade='delete',
                              backref='record')
    
    def __init__(self, pubg_match_id, season):
        
        self.pubg_match_id = pubg_match_id
        self.season = season
        
    def __repr__(self):
        return '<Record of player %r in roster %r>' % (self.player_id, self.roster_id)

    
class MatchStats(Base):
    
    __tablename__ = 'match_stats'
    
    id = Column(Integer, primary_key=True)
    record_id = Column(Integer, ForeignKey(Record.id), unique=True)
    
    place = Column(Integer)
    winPointDelta = Column(Float)
    killPointDelta = Column(Float)
    damage = Column(Float)
    kill = Column(Integer)
    headshot = Column(Integer)
    assist = Column(Integer)
    roadKill = Column(Integer)
    vehicleDestroyed= Column(Integer)
    dbno = Column(Integer)
    timeSurvived = Column(Float)
    walkDistance = Column(Float)
    rideDistance = Column(Float)
    boost = Column(Integer)
    heal = Column(Integer)
    weapon = Column(Integer)
    revive = Column(Integer)
    deathType = Column(String(30))
    teamKill = Column(Integer)
    longestKill = Column(Float)
    
    def __init__(self, stats):
        
        self.place = stats['winPlace']
        self.winPointDelta = stats['winPointsDelta']
        self.killPointDelta = stats['killPointsDelta']
        self.damage = stats['damageDealt']
        self.kill = stats['kills']
        self.headshot = stats['headshotKills']
        self.assist = stats['assists']
        self.roadKill = stats['roadKills']
        self.vehicleDestroyed = stats['vehicleDestroys']
        self.dbno = stats['DBNOs']
        self.timeSurvived = stats['timeSurvived']
        self.walkDistance = stats['walkDistance'] 
        self.rideDistance = stats['rideDistance']
        self.boost = stats['boosts']
        self.heal = stats['heals'] 
        self.weapon = stats['weaponsAcquired']
        self.revive = stats['revives']    
        self.deathType = stats['deathType']
        self.longestKill = stats['longestKill']
        self.teamKill = stats['teamKills']
        
    def __repr__(self):
        return '<Match stats %r %r>' % (self.id, self.record_id)
    
    