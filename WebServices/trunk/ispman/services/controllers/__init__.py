"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""

import base64
from cgi import parse_qs

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

ROLES = (ROLE_DOMAIN, ROLE_CLIENT, ROLE_RESELLER, ROLE_ADMIN) = range(4)

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
        role = authheader.get('role')
        _authenticate(username=username, password=password, login_type=role)
        SimpleWSGISoapApp.onMethodExec(self,environ,body,py_params,soap_params)

class XMLRPCController(PylonsXMLRPCController):
    def __call__(self, environ, start_response):
        authorization = environ.get('HTTP_AUTHORIZATION', None)
        if not authorization:
            abort(401)
        uname, passwd = base64.decodestring(authorization.split()[1]).split(':')
        query = parse_qs(environ.get('QUERY_STRING', ''))
        login_type = query.get('login_type', 0)
        if isinstance(login_type, list):
            login_type = login_type[0]
        _authenticate(uname, passwd, login_type)
        return PylonsXMLRPCController.__call__(self, environ, start_response)

# 5 mins cache as default
@beaker_cache(expire=int(config.get('soap.session.timeout',300)), type="memory")
def _authenticate(username=None, password=None, login_type=None):
    if not (username or password or login_type):
        abort(401) # Unauthorized

    if not isinstance(login_type, int):
        login_type = int(login_type)

    if login_type == ROLE_DOMAIN:
        binddn = 'ispmanDomain=%s,%s' % (username, g.ldap_config['base_dn'])
    elif login_type in (ROLE_CLIENT, ROLE_RESELLER):
        if login_type == ROLE_CLIENT:
            base   = "ou=ispman,%s" % g.ldap_config['base_dn']
            scope  = "sub"
            filter = "&(objectClass=ispmanClient)(uid=%s)" % username
        elif login_type == ROLE_RESELLER:
            base   = "ou=ispman,%s" % g.ldap_config['base_dn']
            scope  = "one"
            filter = "&(objectClass=ispmanReseller)(uid=%s)" % username
        # search for binddn
        msg =  g.ldap.search(base   = base,
                             scope  = scope,
                             filter = filter,
                             attrs  = [])
        entry = msg.entry(0)
        if not entry:
            _log.debug('Entry not found for base: %s, scope: %s, filter: %s',
                       base, scope, filter)
            abort(403, "Failed to login")
        binddn = entry.dn()
    elif login_type == ROLE_ADMIN:
        # admin !?
        binddn = "uid=%s,ou=admins,%s" % (username, g.ldap_config['base_dn'])
    else:
        abort(405) # Method Not Allowed

    # Authenticate
    result =  g.ldap.bind(binddn, password=password)
    if result.code():
        _log.debug('Failed to login')
        print result.error()
        g.ldap.unbind()
        abort(401) # Re-Authenticate!?

    session['login_type'] = login_type
    session['username'] = username
    session['password'] = password
    session['binddn'] = binddn
    session.save()

    # We reached this far? Sucess!!! We're authenticated...
    _log.debug('login OK for user %s', username)

# Include the '_' function in the public names
__all__ = [__name for __name in locals().keys() if not __name.startswith('_') \
           or __name == '_']
