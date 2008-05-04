import logging

from ispman.services.controllers import *
from ispman.services.serializers import Account
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array, Boolean, Fault

log = logging.getLogger(__name__)

class SoapService(SoapController):

#    def index(self):
#        # Return a rendered template
#        #   return render('/some/template.mako')
#        # or, Return a response
#        return 'Hello World'


    @soapmethod(String, Array(String), _returns=Array(Account))
    def getUsers(self, domain=None, attrs_list=[]):
        result = pc.getUsers(domain, attrs_list)
        if result:
            results = []
            for user in result:
                results.append()
        return result

    @soapmethod(String, String, _returns=Boolean)
    def hasAddress(self, domain, address):
        return pc.address_exists_on_domain(domain, address)

    @soapmethod(String, String, _returns=Account)
    def userInfo(self, domain, ispmanUserId):
        return pc.get_user_info(ispmanUserId, domain)

    @soapmethod(String, _returns=Integer)
    def userCount(self, domain):
        return pc.get_domain_user_count(domain)

    @soapmethod(String, _returns=Integer)
    def vhostCount(self, domain):
        return pc.get_domain_vhost_count(domain)

    @soapmethod(String, String, _returns=Boolean)
    def changePassword(self, domain, password):
        return pc.change_domain_password(domain, password)

SoapController = SoapService() # Make it a normal Pylons controller
