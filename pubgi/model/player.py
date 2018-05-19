# -*- coding: utf-8 -*-
"""
    pubgi.model.player
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for SQLAlchemy player models. 
    -- Create Player, PlayerStats, 
       SoloStats, DuoStats, SquadStats models.
      
    :copyright: (c) 2018 by rico0821.
    
"""
from datetime import datetime, timedelta

from sqlalchemy import Column, DateTime, Integer, Float, ForeignKey, String
from sqlalchemy.orm import relationship

from pubgi.model import Base


class Player(Base):
    
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    pubgID = Column(String(50), nullable=False)
    region = Column(String(30), nullable=False)
    updateTime = Column(DateTime, default=datetime.utcnow() - timedelta(minutes=1))
    
    eventGames = Column(Integer, default=0)
    
    records = relationship('Record',
                            cascade='delete',
                            backref='player')
    solo = relationship('SoloStats', 
                              cascade='delete',
                              backref='player')
    duo = relationship('DuoStats', 
                              cascade='delete',
                              backref='player')
    squad = relationship('SquadStats', 
                              cascade='delete',
                              backref='player')
    
    def __init__(self, name, pubgID, region):
        
        self.name = name
        self.pubgID = pubgID
        self.region = region
        
    def __repr__(self):
        return '<Player %r %r>' % (self.name, self.region)

    
class PlayerStats(Base):
    
    __tablename__ = 'player_stats'
    
    id = Column(Integer, primary_key=True)
    playerID = Column(Integer, ForeignKey(Player.id))
    
    gameType = Column(String(32), nullable=False)
    season = Column(Integer, nullable=False)
    
    game = Column(Integer, default=0)
    rating = Column(Float, default=0)
    place = Column(Float, default=0)
    top10 = Column(Float, default=0)
    win = Column(Float, default=0)
    winPoints = Column(Float, default=0)
    killPoints = Column(Float, default=0)
    lastwinPoints = Column(Float, default=0)
    lastkillPoints = Column(Float, default=0)
    
    damage = Column(Float, default=0)
    dBNOs = Column(Integer, default=0)
    kills = Column(Integer, default=0)
    headshotKills = Column(Integer, default=0)
    roadKills = Column(Integer, default=0)
    teamKills = Column(Integer, default=0)
    vehicleDestroys = Column(Integer, default=0)
    
    death = Column(Integer, default=0)
    timeSurvived = Column(Float, default=0)
    
    walkDistance = Column(Float, default=0)
    rideDistance = Column(Float, default=0)
    
    boosts = Column(Integer, default=0)
    heals = Column(Integer, default=0)
    weapons = Column(Integer, default=0)
    
    revives = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    
    __mapper_args__ = {'polymorphic_on': gameType}
    
    def __init__(self, gameType, season):
        
        self.gameType = gameType
        self.season = season
        
    def aggregate(self, stats):
        
        self.game += 1
        self.lastwinPoints = stats['winPoints']
        self.lastkillPoints = stats['killPoints']
        self.winPoints = self.lastwinPoints + stats['winPointsDelta']
        self.killPoints = self.lastkillPoints + stats['killPointsDelta']
        self.rating = self.winPoints + 0.2 * self.killPoints
        self.place += stats['winPlace']
        self.damage += stats['damageDealt']
        self.kills += stats['kills']
        self.headshotKills += stats['headshotKills']
        self.assists += stats['assists']
        self.roadKills += stats['roadKills']
        self.vehicleDestroys += stats['vehicleDestroys']
        self.dBNOs += stats['DBNOs']
        self.timeSurvived += stats['timeSurvived']
        self.walkDistance += stats['walkDistance'] 
        self.rideDistance += stats['rideDistance']
        self.boosts += stats['boosts']
        self.heals += stats['heals']
        self.weapons += stats['weaponsAcquired']
        self.revives += stats['revives']
        self.teamKills += stats['teamKills']
        
        if not stats['deathType'] == 'alive':
            self.death += 1
        if stats['winPlace'] == 1:
            self.win += 1
        elif stats['winPlace'] <= 10:
            self.top10 += 1
        


class SoloStats(PlayerStats):
    
    __mapper_args__ = {'polymorphic_identity': 'solo'}
    
    def __init__(self, season):
        super().__init__('solo', season)
        
    def __repr__(self):
        return '<Player solo stats %r %r>' % (self.id, self.playerID)
    
    
class DuoStats(PlayerStats):
    
    __mapper_args__ = {'polymorphic_identity': 'duo'}
    
    def __init__(self, season):
        super().__init__('duo', season)
        
    def __repr__(self):
        return '<Player duo stats %r %r>' % (self.id, self.playerID)
    
    
class SquadStats(PlayerStats):
    
    __mapper_args__ = {'polymorphic_identity': 'squad'}
    
    def __init__(self, season):
        super().__init__('squad', season)
        
    def __repr__(self):
        return '<Player squad stats %r %r>' % (self.id, self.playerID)