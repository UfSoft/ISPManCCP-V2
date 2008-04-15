import logging

from sha import sha
from datetime import datetime

from ispman.soap.controllers import *
from ispman.soap.serializers import Account
from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array

log = logging.getLogger(__name__)

ROLE_USER = 0
ROLE_RESELLER = 1
ROLE_ADMIN = 2

ROLES = (ROLE_CLIENT, ROLE_RESELLER, ROLE_ADMIN) = range(3)

class AuthenticateService(SimpleWSGISoapApp):

#    def index(self):
#        # Return a rendered template
#        #   return render('/some/template.mako')
#        # or, Return a response
#        return 'Hello World'

    @soapmethod(Integer, String, String, _returns=String)
    def login(self, login_type, uid, password):
        # prepare binddn
        if login_type in (ROLE_CLIENT, ROLE_RESELLER):
            if login_type == ROLE_CLIENT:
                base   = "ou=ispman,%s" % g.ldap_config['base_dn']
                scope  = "sub"
                filter = "&(objectClass=ispmanClient)(uid=%s)" % uid
            elif login_type == ROLE_RESELLER:
                base   = "ou=ispman,%s" % g.ldap_config['base_dn']
                scope  = "one"
                filter = "&(objectClass=ispmanReseller)(uid=%s)" % uid
            # search for binddn
            msg =  g.ldap.search(base   = base,
                                         scope  = scope,
                                         filter = filter,
                                         attrs  = [])
            entry = msg.entry(0)
            if not entry:
                log.debug('Entry not found for base: %s, scope: %s, filter: %s',
                          base, scope, filter)
                abort(403, "Failed to login")
            binddn = entry.dn()
        elif login_type == ROLE_ADMIN:
            # admin !?
            binddn = "uid=%s,ou=admins,%s" % (uid, g.ldap_config['base_dn'])
        else:
            abort(405) # Method Not Allowed

        # Authenticate
        result =  g.ldap.bind(binddn, password=password)
        if result.code():
            log.debug('Failed to login')
            print result.error()
            g.ldap.unbind()
            abort(401) # Re-Authenticate!?

        # We reached this far? Sucess!!! We're authenticated...
        log.debug('login OK for user %s', uid)

        # Generate AuthToken and save details in session
        session = g.session.new(uid, login_type)

        authtoken = session.token
        return authtoken

# Make it a normal Pylons controller
AuthenticateController = AuthenticateService()
