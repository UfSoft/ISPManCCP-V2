# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: serializers.py 177 2008-05-03 14:32:06Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/branches/0.2.x/WebServices/trunk/ispman/services/serializers.py $
# $LastChangedDate: 2008-05-03 15:32:06 +0100 (Sat, 03 May 2008) $
#             $Rev: 177 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

#from pylons import g
from pylons import config
#from ispman.services.wsgiapp import Globals
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
