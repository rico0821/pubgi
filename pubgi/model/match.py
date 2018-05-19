# -*- coding: utf-8 -*-
"""
    pubgi.model.match
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for SQLAlchemy match models. 
    -- Create Match, MatchInfo, 
       MatchStats, Record, Roster models.
      
    :copyright: (c) 2018 by rico0821.
    
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Float, String, ForeignKey
from sqlalchemy.orm import relationship

from pubgi.model import Base
from pubgi.model.player import Player


class Match(Base):
    
    __tablename__ = 'matches'
    
    id = Column(Integer, primary_key=True)
    pubgID = Column(String(50), nullable=False)
    
    retrievedAt = Column(DateTime, default=datetime.utcnow())
    
    info = relationship('MatchInfo', 
                            uselist=False, 
                            cascade='delete',
                            backref='match')
    rosters = relationship('Roster',
                             cascade='delete',
                             backref='match')
    
    def __init__(self, pubgID):
        
        self.pubgID = pubgID
        
    def __repr__(self):
        return '<Match %r>' % (self.pubgID)


class MatchInfo(Base):
    
    __tablename__ = 'match_info'
    
    id = Column(Integer, primary_key=True)
    matchID = Column(Integer, ForeignKey(Match.id), unique=True)
    
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
        return '<Match info %r %r>' % (self.id, self.matchID)
        
        
class Roster(Base):
    
    __tablename__ = 'rosters'
    
    id = Column(Integer, primary_key=True)
    matchID = Column(Integer, ForeignKey(Match.id))
    pubgRosterID = Column(String(50), nullable=False)
    
    participants = relationship('Record',
                               backref='roster')
    
    def __init__(self, pubgRosterID):
        
        self.pubgRosterID = pubgRosterID
    def __repr__(self):
        return '<Roster %r in match %r>' % (self.id, self.matchID)
    
    
class Record(Base):
    
    __tablename__ = 'records'
    
    id = Column(Integer, primary_key=True)
    
    playerID = Column(Integer, ForeignKey(Player.id))
    rosterID = Column(Integer, ForeignKey(Roster.id))
    pubgMatchID = Column(String(50), nullable=False)
    season = Column(Integer, nullable=False)
    
    stats = relationship('MatchStats', 
                              uselist=False, 
                              cascade='delete',
                              backref='record')
    
    def __init__(self, pubgMatchID, season):
        
        self.pubgMatchID = pubgMatchID
        self.season = season
        
    def __repr__(self):
        return '<Record of player %r in roster %r>' % (self.playerID, self.rosterID)

    
class MatchStats(Base):
    
    __tablename__ = 'match_stats'
    
    id = Column(Integer, primary_key=True)
    recordID = Column(Integer, ForeignKey(Record.id), unique=True)
    
    place = Column(Integer)
    winPointsDelta = Column(Float)
    killPointsDelta = Column(Float)
    damage = Column(Float)
    kills = Column(Integer)
    headshotKills = Column(Integer)
    assists = Column(Integer)
    roadKills = Column(Integer)
    vehicleDestroys= Column(Integer)
    dBNOs = Column(Integer)
    timeSurvived = Column(Float)
    walkDistance = Column(Float)
    rideDistance = Column(Float)
    boosts = Column(Integer)
    heals = Column(Integer)
    weapons = Column(Integer)
    revives = Column(Integer)
    deathType = Column(String(30))
    teamKills = Column(Integer)
    longestKill = Column(Float)
    
    def __init__(self, stats):
        # 스키마 포맷 통일 - 18.05.20 by JH
        self.place = stats['winPlace']
        self.winPointsDelta = stats['winPointsDelta']
        self.killPointsDelta = stats['killPointsDelta']
        self.damage = stats['damageDealt']
        self.kills = stats['kills']
        self.headshotKills = stats['headshotKills']
        self.assists = stats['assists']
        self.roadKills = stats['roadKills']
        self.vehicleDestroys = stats['vehicleDestroys']
        self.dBNOs = stats['DBNOs']
        self.timeSurvived = stats['timeSurvived']
        self.walkDistance = stats['walkDistance'] 
        self.rideDistance = stats['rideDistance']
        self.boosts = stats['boosts']
        self.heals = stats['heals']
        self.weapons = stats['weaponsAcquired']
        self.revives = stats['revives']
        self.deathType = stats['deathType']
        self.longestKill = stats['longestKill']
        self.teamKills = stats['teamKills']
        
    def __repr__(self):
        return '<Match stats %r %r>' % (self.id, self.recordID)
    
    