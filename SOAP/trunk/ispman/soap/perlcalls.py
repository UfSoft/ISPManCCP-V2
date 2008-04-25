# -*- coding: utf-8 -*-
# vim: sw=4 ts=4 fenc=utf-8
# =============================================================================
# $Id: perlcalls.py 168 2008-04-25 15:36:34Z s0undt3ch $
# =============================================================================
#             $URL: http://ispmanccp.ufsoft.org/svn/branches/0.2.x/SOAP/trunk/ispman/soap/perlcalls.py $
# $LastChangedDate: 2008-04-25 16:36:34 +0100 (Fri, 25 Apr 2008) $
#             $Rev: 168 $
#   $LastChangedBy: s0undt3ch $
# =============================================================================
# Copyright (C) 2008 UfSoft.org - Pedro Algarvio <ufs@ufsoft.org>
#
# Please view LICENSE for additional licensing information.
# =============================================================================

import logging
from pylons import g
from ispman.soap.serializers import Account

log = logging.getLogger(__name__)

def get_domain_users(domain, attrs_list):
    if attrs_list.count('ispmanUserId') < 1:
        attrs_list.append('ispmanUserId')
    log.debug('Passed in attrs_list: %s', attrs_list)
    userlist = to_unicode(g.ispman.getUsers(domain, attrs_list))
    if not userlist:
        return []
    result = []
    for uid, dict_ in userlist.iteritems():
        account = Account()
        account.uid = uid
        for k, v, in dict_.iteritems():
            try:
                if hasattr(account, k):
                    setattr(account, k, v)
            except Exception, err:
                print k, v, err
        result.append(account)
    return result

def address_exists_on_domain(domain, address):
    lookup_attrs = [
        "ispmanUserId", "mailAlias", "mailLocalAddress",#"mailForwardingAddress"
    ]
    users = get_domain_users(domain, lookup_attrs)
    for user in users:
        for attr in lookup_attrs:
            attrval = getattr(user, attr)
            if isinstance(attrval, list):
                for val in attrval:
                    if val == address:
                        return True
            elif attrval == address:
                return True
    return False

# ------------------------------------------------------------------------------
# Local helpers
# ------------------------------------------------------------------------------
def to_unicode(in_obj):
    """ Function to convert whatever we can to unicode."""
    if not in_obj: # or in_obj == '':
        pass
    elif isinstance(in_obj, unicode) or isinstance(in_obj, int):
        return in_obj
    elif isinstance(in_obj, str):
        return unicode(in_obj, 'UTF-8')
    elif isinstance(in_obj, list):
        return [to_unicode(x) for x in in_obj] # if x not in ('', u'', None)]
    elif isinstance(in_obj, dict):
        def conv_to_list(obj):
            if isinstance(obj, str) or isinstance(obj, unicode):
                return [to_unicode(obj)]
            else:
                return to_unicode(obj)
        out_dict = {}
        for key, val in in_obj.iteritems():
            if key == 'mailAlias':
                out_dict[key] = conv_to_list(val)
            elif key == 'mailForwardingAddress':
                out_dict[key] = conv_to_list(val)
            else:
                out_dict[key] = to_unicode(val)
        return out_dict
    else:
        try:
            return to_unicode(dict(in_obj))
        except: # Failed to convert to dict
            pass
        try:
            return to_unicode(list(in_obj))
        except: # Failed to convert to list
            pass
    return in_obj
