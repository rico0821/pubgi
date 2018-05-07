# -*- coding: utf-8 -*-

from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from pubg.model import Base


class Player(Base):
    
    __tablename__ = 'players'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    pubg_id = Column(String(50), nullable=False)
    region = Column(String(30), nullable=False)
    update_time = Column(DateTime, default=datetime.utcnow()-timedelta(minutes=1))
    
    event_games = Column(Integer, default=0)
    
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
    
    def __init__(self, name, pubg_id, region):
        
        self.name = name
        self.pubg_id = pubg_id
        self.region = region
        
    def __repr__(self):
        return '<Player %r %r>' % (self.name, self.region)

    
class PlayerStats(Base):
    
    __tablename__ = 'player_stats'
    
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey(Player.id))
    
    game_type = Column(String(32), nullable=False)
    season = Column(Integer, nullable=False)
    
    game = Column(Integer, default=0)
    rating = Column(Float, default=0)
    place = Column(Float, default=0)
    top10 = Column(Float, default=0)
    win = Column(Float, default=0)
    winPoint = Column(Float, default=0)
    killPoint = Column(Float, default=0)
    lastwinPoint = Column(Float, default=0)
    lastkillPoints = Column(Float, default=0)
    
    damage = Column(Float, default=0)
    dbno = Column(Integer, default=0)
    kill = Column(Integer, default=0)
    headshot = Column(Integer, default=0)
    roadKill = Column(Integer, default=0)
    teamKill = Column(Integer, default=0)
    vehicleDestroyed = Column(Integer, default=0)
    
    death = Column(Integer, default=0)
    timeSurvived = Column(Float, default=0)
    
    walkDistance = Column(Float, default=0)
    rideDistance = Column(Float, default=0)
    
    boost = Column(Integer, default=0)
    heal = Column(Integer, default=0)
    weapon = Column(Integer, default=0)
    
    revive = Column(Integer, default=0)
    assist = Column(Integer, default=0)
    
    __mapper_args__ = {'polymorphic_on': game_type}
    
    def __init__(self, game_type, season):
        
        self.game_type = game_type
        self.season = season
        
    def aggregate(self, stats):
        
        self.game += 1
        self.lastwinPoint = stats['winPoints']
        self.lastkillPoint = stats['killPoints']
        self.winPoint = self.lastwinPoint + stats['winPointsDelta']
        self.killPoint = self.lastkillPoint + stats['killPointsDelta']
        self.lastwinPoint = stats['winPoints']
        self.lastkillPoint = stats['killPoints']
        self.rating = self.winPoint + 0.2 * self.killPoint
        self.place += stats['winPlace']
        self.damage += stats['damageDealt']
        self.kill += stats['kills']
        self.headshot += stats['headshotKills']
        self.assist += stats['assists']
        self.roadKill += stats['roadKills']
        self.vehicleDestroyed += stats['vehicleDestroys']
        self.dbno += stats['DBNOs']
        self.timeSurvived += stats['timeSurvived']
        self.walkDistance += stats['walkDistance'] 
        self.rideDistance += stats['rideDistance']
        self.boost += stats['boosts']
        self.heal += stats['heals'] 
        self.weapon += stats['weaponsAcquired']
        self.revive += stats['revives']    
        self.teamKill += stats['teamKills']
        
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
        return '<Player solo stats %r %r>' % (self.id, self.player_id)
    
    
class DuoStats(PlayerStats):
    
    __mapper_args__ = {'polymorphic_identity': 'duo'}
    
    def __init__(self, season):
        super().__init__('duo', season)
        
    def __repr__(self):
        return '<Player duo stats %r %r>' % (self.id, self.player_id)
    
    
class SquadStats(PlayerStats):
    
    __mapper_args__ = {'polymorphic_identity': 'squad'}
    
    def __init__(self, season):
        super().__init__('squad', season)
        
    def __repr__(self):
        return '<Player squad stats %r %r>' % (self.id, self.player_id)