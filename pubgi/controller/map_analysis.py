# -*- coding: utf-8 -*-
"""
    pubgi.controller.map_analysis
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for map analysis controller functions.
    -- Show map page.
    -- Return map telemetry data. 
      
    :copyright: (c) 2018 by rico0821.
    
"""
from flask import jsonify, render_template, request

from pubgi.database import mongo
from pubgi.pubgi_blueprint import pubgi
from pubgi.pubgi_logger import Log
from pubgi.API.telemetry import TeleProcessor


@pubgi.route('/map')
def show_map():
    """Show map page."""
    
    return render_template('map.html')

@pubgi.route('/map/kills', methods=['POST'])
def get_map_data():
    """
    Return map telemetry data for the given map. 
    
    ARGS: map_name, data_type
    
    """
    
    map_name = request.json['map_name']
    data_type = request.json['data_type']
    
    if map_name == 'erangel':
        map_name = 'Erangel_Main'
    elif map_name == 'miramar':
        map_name = 'Desert_Main'
        
    mongo_data = mongo.db.matches.find_one({'map' : map_name})
    data = mongo_data['data']
    
    tele = TeleProcessor(data)
    
    if data_type == 'kills':
        xy_data = tele.getKillsXY()
    elif data_type =='items':
        xy_data = tele.getItemFindsXY()
    
    return jsonify(xy_data=xy_data)