import logging

from ispman.services.controllers import *

log = logging.getLogger(__name__)

class XmlrpcController(XMLRPCController):

#    def index(self):
#        # Return a rendered template
#        #   return render('/some/template.mako')
#        # or, Return a response
#        return 'Hello World'


    def getUsers(self, domain=None, attrs_list=[]):
        if 'ispmanUserId' not in attrs_list:
            attrs_list.append('ispmanUserId')
        result = be.getUsers(domain, attrs_list)
        return result.values()
#    getUsers.signature =


#XmlrpcController = XMLRPCService()
