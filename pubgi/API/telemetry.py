# -*- coding: utf-8 -*-
"""
    pubgi.API.telemetry
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for processing telemetry data. 
      
    :copyright: (c) 2018 by rico0821.
    
"""
import json
import numpy as np


class TeleProcessor:
    """
    Telemetry data processing class.
    Each instance uses data for one match. 
    
    """
    
    def __init__(self, telemetry_data):
        """
        Create instance with telemetry data. 
        
        ARGS: telemetry_data 
        
        """
        
        self.telemetry = telemetry_data
            
    def getPlayerXY(self, player=None):
        """
        Get player(s) location coordinates.
        
        ARGS: (player) 
        
        """
        
        loc_data = [data for data in self.telemetry if data['_T']=='LogPlayerPosition']
        
        if player:
            loc_data = sorted([data for data in loc_data if data['character']['name']==player], key=lambda x: x['elapsedTime'])
        
        loc = [{'x' : data['character']['location']['x'], 
                 'y' : data['character']['location']['y'], 
                 'time' : data['elapsedTime']} for data in loc_data if data['elapsedTime'] != 0]
        
        return loc
    
    def getFlightFit(self):
        """Get flight line fit data."""
        
        loc = self.getPlayerXY()
        
        early_loc = [data for data in loc if data['time'] < 5]
        
        x = np.array([data['x'] for data in early_loc])
        y = np.array([data['y'] for data in early_loc])

        A = np.vstack([x, np.ones(len(x))]).T
        m, c = np.linalg.lstsq(A, y, rcond=None)[0]
        
        return m, c
        
    def getKillsXY(self, killer=None, victim=None):
        """
        Get kill location coordinates.
        
        ARGS: (killer), (victim) 
        
        """
        
        kills_data = [data for data in self.telemetry if data['_T']=='LogPlayerKill']
        
        if killer:
            kills_data = [data for data in kill_data if data['killer']['name']==player] 
        
        if victim:
            kills_data = next(data for data in kill_data if data['victim']['name']==player)
            
        kills = [{'x' : data['victim']['location']['x'], 
                  'y' : data['victim']['location']['y']} for data in kills_data]
        
        return kills
    
    def getItemFindsXY(self, player=None):
        """
        Get item pickup coordinates. 
        
        ARGS: (player) 
        
        """
        
        items_data = [data for data in self.telemetry if data['_T']=='LogItemPickup']
        
        if player:
            items_data = [data for data in items_data if data['character']['name']==player]
            
        item_finds = [{'x' : data['character']['location']['x'],
                           'y' : data['character']['location']['y']} for data in items_data]
        
        return item_finds
    
    def getMagneticXY(self):
        """Get magnetic centre coordinates and radii."""
        
        gamestate_data = [data for data in self.telemetry if data['_T']=='LogGameStatePeriodic']
        magnetic_raw = [{'x' : data['gameState']['safetyZonePosition']['x'], 
                               'y' : data['gameState']['safetyZonePosition']['y'], 
                               'r' : data['gameState']['safetyZoneRadius']} for data in gamestate_data]
        magnetic = [dict(t) for t in set([tuple(data.items()) for data in magnetic_raw if magnetic_raw.count(data) > 1])]
        
        return magnetic
