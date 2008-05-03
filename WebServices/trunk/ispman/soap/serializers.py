# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: serializers.py 169 2008-04-26 12:04:02Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/branches/0.2.x/WebServices/trunk/ispman/soap/serializers.py $
# $LastChangedDate: 2008-04-26 13:04:02 +0100 (Sat, 26 Apr 2008) $
#             $Rev: 169 $
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
        uid = Array(String)
        uidNumber = Integer
        gidNumber = Integer
        homeDirectory = String
        loginShell = String
        ispmanStatus = String
        ispmanCreateTimestamp = Integer
        ispmanUserId = String
        ispmanDomain = String
        DestinationAddress = String
        DestinationPort = Integer
        mailQuota = Integer
        mailHost = String
        fileHost = String
        cn = String
        mailRoutingAddress = String
        FTPStatus = String
        FTPQuotaMBytes = Integer
        mailAlias = String
        sn = String
        mailLocalAddress = String
        userPassword = String
        mailForwardingAddress = String
        givenName = String

    def __repr__(self):
        return "<Account: ispmanUserID: %r>" % self.ispmanUserId
