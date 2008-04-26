import logging

from ispman.soap.controllers import *
from ispman.soap.serializers import Account
from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array, Boolean

log = logging.getLogger(__name__)

class DomainService(SimpleWSGISoapApp):

#    def index(self):
#        # Return a rendered template
#        #   return render('/some/template.mako')
#        # or, Return a response
#        return 'Hello World'


    @soapmethod(String, String, Array(String), _returns=Array(Account))
    @tokencheck # called after in order to have globals registered on thread
    def getUsers(self, authtoken=None, domain=None, attrs_list=[]):
        result = pc.get_domain_users(domain, attrs_list)
        return result

    @soapmethod(String, String, String, _returns=Boolean)
    @tokencheck # called after in order to have globals registered on thread
    def hasAddress(self, authtoken, domain, address):
        return pc.address_exists_on_domain(domain, address)

    @soapmethod(String, String, String, _returns=Account)
    @tokencheck # called after in order to have globals registered on thread
    def userInfo(self, authtoken, domain, ispmanUserId):
        return pc.get_user_info(ispmanUserId, domain)
        return pc.address_exists_on_domain(domain, address)

DomainController = DomainService() # Make it a normal Pylons controller
