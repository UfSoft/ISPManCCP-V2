"""ISPMan DomainMan WebServices"""

from ispman.services.backend.base import *

def addDomainDNSProcess(domain, process, params):
    raise NotImplemented

def addDomainFileServerProcess(domain, process, params):
    raise NotImplemented

def addDomainSMTPProcess(domain, process, params):
    raise NotImplemented

def addDomain(params):
    raise NotImplemented

def checkDomainType(domain, type):
    """Check's for domain type.

      **domain**: Fully Qualified Domain Name

      **type**: Type of domain; one of `primary`, `slave`, `nodns`, `replica`.

    returns `True` if domain is of passed `type`, `False` otherwise.
    """
    raise NotImplemented

def deleteDomain(params):
    raise WontImplementError # Redirects to HTML on errors...

def delete_domain(domain):
    """Deletes a domain.

        **domain**: Fully Qualified Domain Name

    """
    raise NotImplemented


def domainExists(domain):
    """Checks the existance of a domain.

        **domain**: Fully Qualified Domain Name

    returns `True` if domain exists, `False` otherwise.
    """

def domainLockedBy(domain):
    """Checks who locked the domain.

        **domain**: Fully Qualified Domain Name

    returns who locked the domain, if anyone.
    """
    raise NotImplemented


def editDomain(params):
    raise WontImplementError # HTML user input


def genericModifyDomain(params, type):
    """Modify domain.

        **params**: dictionary with domain attributes.

        **type**: Type of domain; one of `primary`, `slave`, `nodns`, `replica`.

    """
    raise NotImplemented

def getDomainAsDCObject(domain):
    """Get the domain as an LDAP DC object.

        **domain**: Fully Qualified Domain Name

    """
    raise NotImplemented

def getDomainAttribute(domain, attr):
    """Returns the value(s) of the attribute for the domain.

        **domain**: Fully Qualified Domain Name

        **attr**: Domain attribute to retrieve

    >>> owner = getDomainAttribute("domain.tld", "ispmanDomainOwner")
    >>> print owner

    """
    raise NotImplemented

def getDomainDN(domain):
    """Returns the DN of the domain.

        **domain**: Fully Qualified Domain Name

    >>> dn = getDomainDN("domain.tld")
    >>> print dn

    If you want the DN of the domain, use this method.
    Do not recreate the domain's DN by concatinating
    `ispmanDomain=name` and `ldapBaseDN`.

    """
    raise NotImplemented

def getDomainGid(domain):
    """Returns the GID(gidnumber) of the domain.

        **domain**: Fully Qualified Domain Name

    """
    raise NotImplemented

def getDomainInfo(domain, forget=False):
    """Return the information about a domain.

        **domain**: Fully Qualified Domain Name or domain's DN

        **forget**: should results be cached of forgotten

    Getting domain info by passing a domain name:

    >>> getDomainInfo("developer.ch")

    Getting domain info by passing a domain's DN:

    >>> getDomainInfo("ispmanDomain=developer.ch, o=4unet");

    The first time this function is called, it searches the LDAP directory for
    all domains and caches the result. Every subsequent request gets a cached
    result.

    You can pass optionally a positive value to `forget` so that you don't get
    a cached result.

    Getting domain info by passing a domain name, requesting fresh result from
    LDAP:

    >>> getDomainInfo("developer.ch", 1)

    """
    raise NotImplemented

def getDomainType(domain):
    """Return the type information about a domain.

        **domain**: Fully Qualified Domain Name
    """
    raise NotImplemented

def getDomains(filter, attr):
    """
    returns concatenated result of:
      * getPrimaryDomains
      * getSlaveDomains
      * getReplicaDomains
      * getNoDnsDomains

    """
    # XXX: extend the above doc
    raise NotImplemented

def getDomainsCount(filter):
    raise NotImplemented

def domainHasService(domain, service):
    """Check if domain has a specific service.

        **domain**: Fully Qualified Domain Name

        **service**: service name to check for

    If you want to check that domain `test.com` has the service `mail`:

    >>> domainHasService("test.com", "mail")

    returns `True` or `False`

    """
    raise NotImplemented

def getDomainsWithService(service):
    """Get list of domains that have a specific service.

        **service**: service name to check for

    If you want to list all domains that have `domainservice=ftp`:

    >>> getDomainsWithService("ftp")
    ['domain1.com', 'domain2.com', 'domain2.com']

    """
    raise NotImplemented

def getNodnsDomains():
    raise NotImplemented

def getPrimaryDomains():
    raise NotImplemented

def getReplicaCountForDomain(domain):
    """Returns a count of replicas for domain.

        **domain**: Fully Qualified Domain Name

    """
    raise NotImplemented

def getReplicaDomains():
    raise NotImplemented

def getReplicasOfDomain(domain):
    """Returns a hashref of domains that are a replica of another
    domain which is passed as the parameter.

        **domain**: Fully Qualified Domain Name

    """
    raise NotImplemented

def getSlaveDomains():
    raise NotImplemented

def getTransportMap(domain):
    """Returns the transport map for the specified domain.
    (either 'smtp' or 'local')

        **domain**: Fully Qualified Domain Name


    """
    raise NotImplemented

def gotoEditDomain(params):
    raise WontImplementError

def isDomainEditable(domain):
    raise NotImplemented

def isDomainLocked(domain):
    raise NotImplemented

def lockDomain(domain, whom):
    raise NotImplemented

def makeDomainDN(string):
    raise NotImplemented

def makeDomainHash(domains):
    raise WontImplementError # Internal function

def modifyNoDNSDomain(params):
    """Called from ispman.cgi, calls ISPMan::DomainMan::NoDNSDomain::modifyDomain
    Modifies data for the nodns  Domain such as domain services, domain owner, etc
    """
    raise NotImplemented

def modifyPrimaryDomain(params):
    """Called from ispman.cgi, calls ISPMan::DomainMan::NoDNSDomain::modifyDomain
    Modifies data for the nodns  Domain such as domain services, domain owner, etc
    """
    raise NotImplemented


def modifyReplicaDomain(params):
    """Called from ispman.cgi, calls ISPMan::DomainMan::NoDNSDomain::modifyDomain
    Modifies data for the nodns  Domain such as domain services, domain owner, etc
    """
    raise NotImplemented

def modifySlaveDomain(params):
    """Called from ispman.cgi, calls ISPMan::DomainMan::NoDNSDomain::modifyDomain
    Modifies data for the nodns  Domain such as domain services, domain owner, etc
    """
    raise NotImplemented

def newDomain(params):
    raise WontImplementError # HTML

def prepareDNSBranch(string):
    raise NotImplemented

def selectDomainType(params):
    raise WontImplementError # HTML

def setDomainAttribute(domain, attribute, value):
    raise NotImplemented

def setMailTransport(domain, transport):
    raise NotImplemented

def summary():
    raise WontImplementError

def suspend_domain(domain):
    raise NotImplemented

def unlockDomain(domain):
    raise NotImplemented

def unsuspend_domain(domain):
    raise NotImplemented

def changeDomainPassword(domain, password):
    """Change the domain password.

        **domain**: FQDN
        **password**: The new password for the passed `domain`
    """
    return g.ispman.changeDomainPassword(domain, password)

def getDefaultFileHost(domain):
    raise NotImplemented

def getDefaultMailHost(domain):
    raise NotImplemented

def getDefaultWebHost(domain):
    raise NotImplemented


