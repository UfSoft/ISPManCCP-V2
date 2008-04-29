import logging

from ispman.soap.controllers import *
from ispman.soap.serializers import Account
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array, Boolean, Fault

log = logging.getLogger(__name__)

class DomainService(SoapController):

#    def index(self):
#        # Return a rendered template
#        #   return render('/some/template.mako')
#        # or, Return a response
#        return 'Hello World'


    @soapmethod(String, Array(String), _returns=Array(Account))
    def getUsers(self, domain=None, attrs_list=[]):
        result = pc.get_domain_users(domain, attrs_list)
        return result

    @soapmethod(String, String, _returns=Boolean)
    def hasAddress(self, domain, address):
        return pc.address_exists_on_domain(domain, address)

    @soapmethod(String, String, _returns=Account)
    def userInfo(self, domain, ispmanUserId):
        return pc.get_user_info(ispmanUserId, domain)

DomainController = DomainService() # Make it a normal Pylons controller
