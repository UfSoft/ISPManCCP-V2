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
    def getUserCount(self, domain):
        return be.getUserCount(domain)

    @soapmethod(String, _returns=Integer)
    def getVhostsCount(self, domain):
        return be.getVhostsCount(domain)

    @soapmethod(String, String, _returns=Boolean)
    def changeDomainPassword(self, domain, password):
        return be.changeDomainPassword(domain, password)

SoapController = SOAPService() # Make it a normal Pylons controller
