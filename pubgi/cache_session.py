# -*- coding: utf-8 -*-
"""
    pubgi.cache_session
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    Module for custom cache session. 
    
    :copyright: (c) 2018 by rico0821.
    
"""
from datetime import timedelta
from uuid import uuid4

from werkzeug.contrib.cache import NullCache, SimpleCache
from werkzeug.datastructures import CallbackDict
from flask.sessions import SessionInterface, SessionMixin


class CacheSession(CallbackDict, SessionMixin):
    
    def __init__(self, initial=None, sid=None, new=False):
        
        def on_update(self):
            self.modified = True
        
        CallbackDict.__init__(self, initial, on_update)
        self.sid= sid
        self.new = new
        self. modified = False

        
class CacheSessionInterface(SessionInterface):
    
    session_class = CacheSession
    
    def __init__(self, cache=None, prefix='cache_session:'):
        
        if cache is None:
            cache = NullCache()
        self.cache = cache
        self.prefix = prefix
    
    def generate_sid(self):
        return str(uuid4())
      
    def get_cache_exp_time(self, app, session):
        if session.permanent:
            return app.permanent_session_lifetime
        return timedelta(days=1)
    
    def open_session(self, app, request):
        
        sid = request.cookies.get(app.session_cookie_name)
        
        if not sid:
            sid = self.generate_sid()
            return self.session_class(sid=sid, new=True)
        
        val = self.cache.get(self.prefix + sid)
        if val is not None:
            return self.session_class(val, sid=sid)
        return self.session_class(sid=sid, new=True)
    
    def save_session(self, app, session, response):
        
        domain = self.get_cookie_domain(app)
        if not session:
            self.cache.delete(self.prefix + session.sid)
            if session.modified:
                response.delete_cookie(app.session_cookie_name, 
                                       domain=domain)
            return
        
        cache_exp = self.get_cache_exp_time(app, session)
        
        val = dict(session)
        self.cache.set(self.prefix + session.sid, val,
                       int(cache_exp.total_seconds()))
        
        response.set_cookie(app.session_cookie_name, 
                            session.sid,
                            httponly=True, domain=domain)

        
class SimpleCacheSessionInterface(CacheSessionInterface):
    
    def __init__(self):
        CacheSessionInterface.__init__(self,
                                       cache=SimpleCache(),
                                       prefix='simple_cache_session:')