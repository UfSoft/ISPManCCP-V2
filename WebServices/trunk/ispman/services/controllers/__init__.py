"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""

import base64

from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
#from pylons.decorators import jsonify, validate,
from pylons.decorators.cache import beaker_cache
from pylons.i18n import _, ungettext, N_
from pylons.templating import render

import ispman.services.helpers as h
import ispman.services.backend as be

from soaplib.wsgi_soap import SimpleWSGISoapApp, request as soap_request
from pylons.controllers import XMLRPCController as PylonsXMLRPCController

import logging as _logging

_log = _logging.getLogger(__name__)

ROLES = (ROLE_CLIENT, ROLE_RESELLER, ROLE_ADMIN) = range(3)

class BaseController(WSGIController):

    def __call__(self, environ, start_response):
        """Invoke the Controller"""
        # WSGIController.__call__ dispatches to the Controller method
        # the request is routed to. This routing information is
        # available in environ['pylons.routes_dict']
        return WSGIController.__call__(self, environ, start_response)

class SoapController(SimpleWSGISoapApp):
    def __call__(self, environ, start_response):
        return SimpleWSGISoapApp.__call__(self, environ, start_response)

    def onMethodExec(self,environ,body,py_params,soap_params):
        '''
        Called BEFORE the service implementing the functionality is called
        @param the wsgi environment
        @param the body element of the soap request
        @param the tuple of python params being passed to the method
        @param the soap elements for each params
        '''
        authheader = soap_request.header.find('Authentication')
        username = authheader.get('username')
        password = authheader.get('password')
        _authenticate(username=username, password=password)
        SimpleWSGISoapApp.onMethodExec(self,environ,body,py_params,soap_params)

class XMLRPCController(PylonsXMLRPCController):
    def __call__(self, environ, start_response):
        authorization = environ.get('HTTP_AUTHORIZATION', None)
        if not authorization:
            abort(401)
        uname, passwd = base64.decodestring(authorization.split()[1]).split(':')
        _authenticate(uname, passwd)
        return PylonsXMLRPCController.__call__(self, environ, start_response)

# 5 mins cache
@beaker_cache(expire=int(config.get('soap.session.timeout', 15)), type="memory")
def _authenticate(username=None, password=None):
    if not (username or password):
        abort(401) # Unauthorized

    valid_login = False

    # Try Admins first
    binddn = "uid=%s,ou=admins,%s" % (username, g.ldap_config['base_dn'])
    result =  g.ldap.bind(binddn, password=password)
    if result.code():
        # Now Resselers
        base   = "ou=ispman,%s" % g.ldap_config['base_dn']
        scope  = "one"
        filter = "&(objectClass=ispmanReseller)(uid=%s)" % username
        msg =  g.ldap.search(base   = base,
                             scope  = scope,
                             filter = filter,
                             attrs  = [])
        entry = msg.entry(0)
        if not entry:
            # Now clients
            base   = "ou=ispman,%s" % g.ldap_config['base_dn']
            scope  = "sub"
            filter = "&(objectClass=ispmanClient)(uid=%s)" % username
            entry = msg.entry(0)
            if not entry:
                abort(403, "Failed to login")
            else:
                binddn = entry.dn()
                result =  g.ldap.bind(binddn, password=password)
                if result.code():
                    abort(403, "Failed to login")
                else:
                    valid_login = True
                    session['login_type'] = ROLE_CLIENT
        else:
            binddn = entry.dn()
            result =  g.ldap.bind(binddn, password=password)
            if result.code():
                abort(403, "Failed to login")
            else:
                valid_login = True
                session['login_type'] = ROLE_RESELLER
    else:
        valid_login = True
        session['login_type'] = ROLE_ADMIN

    if not valid_login:
        _log.debug('Failed to login')
        print result.error()
        g.ldap.unbind()
        abort(401) # Re-Authenticate!?

    session.save()
    # We reached this far? Sucess!!! We're authenticated...
    _log.debug('login OK for user %s', username)

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
