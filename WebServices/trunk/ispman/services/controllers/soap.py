import logging

from ispman.services.controllers import *
from ispman.services.serializers import Account
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array, Boolean, Fault

log = logging.getLogger(__name__)

class SOAPService(SoapController):

#    def index(self):
#        # Return a rendered template
#        #   return render('/some/template.mako')
#        # or, Return a response
#        return 'Hello World'


    @soapmethod(String, Array(String), _returns=Array(Account))
    def getUsers(self, domain=None, attrs_list=[]):
        if 'ispmanUserId' not in attrs_list:
            attrs_list.append('ispmanUserId')
        result = be.getUsers(domain, attrs_list)
        if result:
            results = []
            for user in result.itervalues():
                results.append(be.helpers.to_account(user))
        return results

    @soapmethod(String, _returns=Boolean)
    def userExists(self, uid):
        return be.userExists(uid)

    @soapmethod(String, _returns=Account)
    def getUserInfo(self, uid):
        return be.helpers.to_account(be.getUserInfo(uid))

    @soapmethod(String, _returns=Integer)
    def userCount(self, domain):
        return be.get_domain_user_count(domain)

    @soapmethod(String, _returns=Integer)
    def vhostCount(self, domain):
        return be.get_domain_vhost_count(domain)

    @soapmethod(String, String, _returns=Boolean)
    def changePassword(self, domain, password):
        return be.change_domain_password(domain, password)

SoapController = SOAPService() # Make it a normal Pylons controller
