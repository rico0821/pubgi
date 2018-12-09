# -*- coding: utf-8 -*-
"""
    pubgi.model.average
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for SQLAlchemy average models. 
    -- Create WinnerAverage model.
      
    :copyright: (c) 2018 by rico0821.
    
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, Float, String

from pubgi.model import Base


class WinnerAverage(Base):
    
    __tablename__ = 'winner_average'

    id = Column(Integer, primary_key=True)

    updateTime = Column(DateTime, default=datetime.utcnow())
    
    region = Column(String(20), nullable=False)
    mode = Column(String(20), nullable=False)
    mapName = Column(String(20), nullable=False)

    kills = Column(Integer, default=0)
    damage = Column(Float, default=0)
    walkDistance = Column(Float, default=0)
    rideDistance = Column(Float, default=0)
    boosts = Column(Integer, default=0)
    heals = Column(Integer, default=0)

    def __init__(self, region, mode, mapName):
        
        self.region = region
        self.mode = mode
        self.mapName = mapName
        
    def __repr__(self):
        return '<Winner Average Stats %r>' % (self.id)

    def update(self, data):

    	self.kills = data['kills']
    	self.damage = data['damage']
    	self.walkDistance = data['walkDistance']
    	self.rideDistance = data['rideDistance']
    	self.boosts = data['boosts']
    	self.heals = data['heals']

