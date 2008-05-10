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
    getUsers.signature = [['array', 'string'],
                          ['array', 'string', 'array']]
    getUsers.__doc__ = be.getUsers.__doc__


    def userExists(self, uid):
        return be.userExists(uid)
    userExists.signature = [['boolean', 'string']]
    userExists.__doc__ = be.userExists.__doc__


    def getUserInfo(self, uid):
        return be.getUserInfo(uid)
    getUserInfo.signature = [['struct', 'string']]
    getUserInfo.__doc__ = be.getUserInfo.__doc__


    def getUserCount(self, domain):
        return be.getUserCount(domain)
    getUserCount.signature = [['integer', 'string']]
    getUserCount.__doc__ = be.getUserCount.__doc__

    def changeDomainPassword(self, domain, password):
        return be.changeDomainPassword(domain, password)
    changeDomainPassword.signature = [['boolean', 'string', 'string']]
    changeDomainPassword.__doc__ = be.changeDomainPassword.__doc__
