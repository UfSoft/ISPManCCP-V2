# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: decorators.py 168 2008-04-25 15:36:34Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/branches/0.2.x/SOAP/trunk/ispman/soap/decorators.py $
# $LastChangedDate: 2008-04-25 16:36:34 +0100 (Fri, 25 Apr 2008) $
#             $Rev: 168 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

from pylons import g
from decorator import decorator
from pylons.controllers.util import abort

def tokencheck(func, *args, **kwargs):
    if not g.session.get(args[1]):
        abort(401) # Un-Authorized
    return func(*args, **kwargs)
tokencheck = decorator(tokencheck)

