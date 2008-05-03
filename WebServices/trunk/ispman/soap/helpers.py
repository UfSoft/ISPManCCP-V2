"""Helper functions

Consists of functions to typically be used within templates, but also
available to Controllers. This module is available to both as 'h'.
"""
from webhelpers import *

import os
import sys
from pwd import getpwuid
from grp import getgrgid
from stat import ST_MODE


import logging

log = logging.getLogger(__name__)

def check_path_perms(path):
    """Function to check a path's permissions.
    Based on recipe found on:
        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/436211
    """
    path = os.path.abspath(path)

    if not os.access(path, os.F_OK):
        log.error("I'm bailing out! "
                  "%r does not exist. ", path)
        log.error("Please correct the above problems and run again...")
        sys.exit(1)

    path_perms = os.stat(path)
    running_uid = os.getuid()
    running_gid = os.getgid()
    running_uid_name = getpwuid(running_uid)[0]
    running_gid_name = getgrgid(running_gid)[0]
    R_MSK, W_MSK, X_MSK, Z_MSK =   4,   2,   1,   0
    R_STR, W_STR, X_STR, Z_STR = 'r', 'w', 'x', '-'

    def iff( test_, then_, else_ ): # then_, else_ always get evaled so pls be atoms
        if test_:
            return then_
        else:
            return else_

    def mode2str( mode ):
        r, w, x = mode & R_MSK, mode & W_MSK, mode & X_MSK
        return iff( r, R_STR, Z_STR ) + iff( w, W_STR, Z_STR ) + iff( x, X_STR, Z_STR )

    def fullmode2str( mode ):
        u, g, o = mode >> 6 & 0x7, mode >> 3 & 0x7, mode & 0x7
        return mode2str( u ) + mode2str( g ) + mode2str( o )

    if not os.access(path, os.F_OK) or not os.access(path, os.X_OK):
        log.error("I'm bailing out! "
                  "I don't have read access to %r. "
                  "I'm running as '%s(%i):%s(%i)' and directory is\n"
                  "owned by '%s(%i):%s(%i) with perms '%s'.",
                  path,
                  running_uid_name,
                  running_uid,
                  running_gid_name,
                  running_gid,
                  getpwuid(path_perms[4])[0],
                  path_perms[4],
                  getgrgid(path_perms[5])[0],
                  path_perms[5],
                  fullmode2str(path_perms[ST_MODE]))
        log.error("Please correct the above problems and run again...")
        sys.exit(1)
