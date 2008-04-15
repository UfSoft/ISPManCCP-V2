import logging

from ispman.soap.controllers import *
from ispman.soap.serializers import Account
from soaplib.wsgi_soap import SimpleWSGISoapApp
from soaplib.service import soapmethod
from soaplib.serializers.primitive import String, Integer, Array

log = logging.getLogger(__name__)

class DomainService(SimpleWSGISoapApp):

#    def index(self):
#        # Return a rendered template
#        #   return render('/some/template.mako')
#        # or, Return a response
#        return 'Hello World'

    @soapmethod(String, String, _returns=Array(Account))
    def getUsers(self, authtoken, domain, attrs_list=[]):
        if not g.session.get(authtoken):
            abort(401)
        import pprint
        if attrs_list.count('ispmanUserId') < 1:
            attrs_list.append('ispmanUserId')
        userlist = h.to_unicode(g.ispman.getUsers(domain, attrs_list))
        if not userlist:
            return []
        result = []
        for uid, dict_ in userlist.iteritems():
            for k, v, in dict_.iteritems():
                account = Account()
                account.uid = uid
                try:
                    if hasattr(account, k):
                        setattr(account, k, v)
                except Exception, err:
                    print k, v, err
                result.append(account)
        print result
        return result

DomainController = DomainService() # Make it a normal Pylons controller
