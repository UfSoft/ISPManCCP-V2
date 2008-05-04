"""ISPMan UserMan.WebUser WebServices"""

from ispman.services.backend.base import *

def editWebUser(params_dict):
    raise WontImplementError

def updateWebUser(params_dict):
    raise WontImplementError

def deleteWebUser(params_dict):
    raise NotImplemented

def addWebUser(params_dict):
    raise WontImplementError

def getWebUsersBranchDN(domain):
    raise NotImplemented

def getWebUserDN(domain, user):
    raise NotImplemented

def getWebUsers(domain):
    raise NotImplemented

def getWebUserInfo(domain, user):
    raise NotImplemented

def add_webuser(domain, user, passwd):
    raise NotImplemented

def update_webuser(domain, user, passwd, olduser):
    raise NotImplemented

def delete_webuser(domain, user):
    raise NotImplemented


#__all__ = [ __name for __name in locals().keys() if not __name.startswith('_') ]
