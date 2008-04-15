import logging

from sha import sha
from datetime import datetime, timedelta

from pylons import config
from paste.registry import StackedObjectProxy

log = logging.getLogger(__name__)

class Session(object):
    def __init__(self, uid, login_type):
        self.stamp = datetime.utcnow()
        self.type = login_type
        self.uid = uid
        token = sha(config['soap.session.secret'])
        token.update(self.stamp.isoformat())
        token.update(uid)
        self.token = token.hexdigest()
        self.session_time = timedelta(minutes=int(config['soap.session.expire']))

    def update(self):
        self.stamp = datetime.utcnow()

    def valid(self):
        return datetime.utcnow() + self.session_time < self.stamp


class SoapSession(object):
    active_sessions = {}

    def __init__(self):
        log.debug("SOAP session storage initialized")
        self.expire_time = timedelta(minutes=int(config['soap.session.expire']))

    def new(self, uid, login_type):
        log.debug("Creating new session for uid: %s", uid)
        session = Session(uid, login_type)
        log.debug(session.__dict__)
        self.active_sessions[session.token] = session
        self.cleanup()
        return session

    def get(self, authtoken):
        self.cleanup()
        log.debug("Grabbing new session for authtoken: %s", authtoken)
        print self.active_sessions
        if authtoken in self.active_sessions:
            self.active_sessions[authtoken].update()
            log.debug(self.active_sessions[authtoken].__dict__)
            return self.active_sessions[authtoken]
        return None

    def cleanup(self):
        invalid_sessions = 0
        valid_stamp = datetime.utcnow() - self.expire_time
        for session in self.active_sessions.values():
            if session.stamp < valid_stamp:
                invalid_sessions += 1
                del(self.active_sessions[session.token])
        log.debug("Cleaned up %d sessions", invalid_sessions)
        log.debug(self.active_sessions)

session = StackedObjectProxy(name='session')

__all__ = ['session']
