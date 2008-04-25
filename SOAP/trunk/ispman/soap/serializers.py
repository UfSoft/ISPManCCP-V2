# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: serializers.py 168 2008-04-25 15:36:34Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/branches/0.2.x/SOAP/trunk/ispman/soap/serializers.py $
# $LastChangedDate: 2008-04-25 16:36:34 +0100 (Fri, 25 Apr 2008) $
#             $Rev: 168 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

#from pylons import g
from pylons import config
from ispman.soap.wsgiapp import Globals
from soaplib.serializers.primitive import *
from soaplib.serializers.clazz import *


class Account(ClassSerializer):
    class types:
        dn = String
        dialupAccess = String
        radiusProfileDn = String
        uid = String
        uidNumber = String
        gidNumber = String
        homeDirectory = String
        loginShell = String
        ispmanStatus = String
        ispmanCreateTimestamp = String
        ispmanUserId = String
        ispmanDomain = String
        DestinationAddress = String
        DestinationPort = String
        mailQuota = String
        mailHost = String
        fileHost = String
        cn = String
        mailRoutingAddress = String
        FTPStatus = String
        FTPQuotaMBytes = String
        mailAlias = String
        sn = String
        mailLocalAddress = String
        userPassword = String
        mailForwardingAddress = String
        givenName = String

    def __repr__(self):
        return "<Account: ispmanUserID: %r>" % self.ispmanUserId
