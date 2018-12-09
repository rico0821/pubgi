# -*- coding: utf-8 -*-

from pubgi import create_app


app = create_app()

if __name__ == '__main__':
    
    print('STARTING SERVER...')
    app.run(host='0.0.0.0', port=3000, debug=True)