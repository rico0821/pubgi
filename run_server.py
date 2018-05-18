# -*- coding: utf-8 -*-
"""
    run_server
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for running Flask server locally. 
    
    :copyright: (c) 2018 by rico0821.
    
"""
from pubgi import create_app


app = create_app()

print('STARTING SERVER...')
app.run(host='0.0.0.0', port=3000, debug=True)