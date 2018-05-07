# -*- coding: utf-8 -*-

from pubg import create_app


app = create_app()

print('STARTING SERVER...')
app.run(host='0.0.0.0', port=3000, debug=True)