"""ISPMan ApacheMan WebServices"""

from ispman.services.backend.base import *

def editVhost(params):
    raise NotImplemented

def getApacheVhosts(dn):
    raise NotImplemented

def updateVhost(params):
    raise NotImplemented

def suspendVhost(params):
    raise NotImplemented

def unsuspendVhost(params):
    raise NotImplemented

def suspend_vhost(domain, vhost):
    raise NotImplemented

def unsuspend_vhost(domain, vhost):
    raise NotImplemented

def update_vhost(params):
    raise NotImplemented

def createVhost(params):
    raise NotImplemented

def newVhost(params):
    raise NotImplemented

def addVhost(params):
    raise NotImplemented

def getVhostDN(domain, vhost):
    raise NotImplemented

def getVhostBranchDN(domain):
    raise NotImplemented

def delete_vhost(ispmanVhostName, ispmanDomain):
    raise NotImplemented

def deleteVhost(params):
    raise NotImplemented

def getVhostInfo(ispmanVhostName, domain):
    raise NotImplemented

def getVhostsCount(domain):
    """Returns the number of vhosts a domain has.

        **domain**: Fully Qualified Domain Name
    """
    return g.ispman.getVhostsCount(domain)

def addVhostProcess(domain, vhost, process, param):
    raise NotImplemented

def addVirtualHostDirectoriesProcess(domain, vhost, process, param):
    raise NotImplemented

def changeVhostPassword(domain, vhost, password):
    raise NotImplemented

def getVhostAttribute(domain, vhost, attribute):
    raise NotImplemented

def setVhostAttribute(domain, vhost, attribute, values):
    raise NotImplemented

