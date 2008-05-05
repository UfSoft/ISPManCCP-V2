"""ISPMan UserMan WebServices"""

from ispman.services.backend.base import *

def cantAddUsersToReplicaDomain(params):
    raise WontImplementError

def createUser(params):
    raise WontImplementError

def newUser(params):
    raise WontImplementError

def addUser(params):
    raise NotImplemented

AddUser = addUser

def getDNForMailAddress(mail):
    raise NotImplemented

def getUserInfo(uid):
    """Retrieve the user information

        **uid**: The user id in the form of `user@domain.tld` or
        `user_domain_tld`
    """
    return to_unicode(g.ispman.getUserInfo(uid))

def editUser(params):
    raise NotImplemented

def killUser(dn):
    raise NotImplemented

def deleteUser(params):
    raise NotImplemented

def updateUser(params):
    raise WontImplementError # because it will redirect to editUser

def containsInvalidMailAliases(user, masterDomain, aliases):
    raise NotImplemented

def update_user(params):
    raise NotImplemented

def set_user_attributes(domain, uid, data):
    raise NotImplemented

def changePassword(uid, domain, passwd, method):
    raise NotImplemented

def addMailAliasForUser(uid, domain, values):
    raise NotImplemented

def replaceMailAliasForUser(uid, domain, values):
    raise NotImplemented

def getMailAliasesForUser(uid, domain):
    raise NotImplemented

def addMailForwardForUser(uid, domain, values):
    raise NotImplemented

def replaceMailForwardForUser(uid, domain, values):
    raise NotImplemented

def getMailForwardsForUser(uid, domain):
    raise NotImplemented

def getUsersCount():
    raise NotImplemented

def getUserCount(domain):
    raise NotImplemented

def getUsersBranchDN(domain):
    raise NotImplemented

def getUserDN(domain, uid):
    raise NotImplemented

def getUsers(domain, attrs=[]):
    userlist = to_unicode(g.ispman.getUsers(domain, attrs))
    if not userlist:
        return []
    return userlist

def fixDuplicateUsers(userhash):
    raise NotImplemented

def searchUsers():
    raise WontImplementError

def userExists(uid):
    return g.ispman.userExists(uid)

def suspend_user(domain, uid):
    raise NotImplemented

def unsuspend_user(domain, uid):
    raise NotImplemented

def replaceUserAttributeValues(uid, domain, attribute, values):
    raise NotImplemented

def getUserAttributeValues(uid, domain, attribute):
    raise NotImplemented

def addUserAttributeValues(uid, domain, attribute, values):
    raise NotImplemented

def create_uid(userID, domain):
    raise NotImplemented

def addUserFileServerProcess(domain, uid, process, params):
    raise NotImplemented
