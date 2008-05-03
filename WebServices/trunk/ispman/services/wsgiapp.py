"""The ISPManSOAP WSGI application"""
import os
import sys
import logging

from paste.cascade import Cascade
from paste.registry import RegistryManager
from paste.urlparser import StaticURLParser
from paste.deploy.converters import asbool
from pylons import config
from pylons.error import error_template
from pylons.middleware import error_mapper, ErrorDocuments, ErrorHandler, \
    StaticJavascripts
from pylons.wsgiapp import PylonsApp

import ispman.services.helpers
from ispman.services.routing import make_map

log = logging.getLogger(__name__)

class Sniff(object):
    def __init__(self, app):
        self.application = app
    def __call__(self, environ, start_response):
        print 444, environ
        return self.application(environ, start_response)
#        return []

def load_environment(global_conf, app_conf):
    """Configure the Pylons environment via the ``pylons.config``
    object
    """
    # Pylons paths
    root = os.path.dirname(os.path.abspath(__file__))
    paths = dict(root=root,
                 controllers=os.path.join(root, 'controllers'),
                 static_files=os.path.join(root, 'public'),
                 templates=[os.path.join(root, 'templates')])

    # Initialize config with the basic options
    config.init_app(global_conf, app_conf, package='ispman.services',
                    template_engine='mako', paths=paths)

    config['routes.map'] = make_map()
    config['pylons.g'] = Globals()
    config['pylons.h'] = ispman.services.helpers

    # Customize templating options via this variable
    tmpl_options = config['buffet.template_options']

    # CONFIGURATION OPTIONS HERE (note: all config options will override
    # any Pylons config options)


def make_app(global_conf, full_stack=True, **app_conf):
    """Create a Pylons WSGI application and return it

    ``global_conf``
        The inherited configuration for this application. Normally from
        the [DEFAULT] section of the Paste ini file.

    ``full_stack``
        Whether or not this application provides a full WSGI stack (by
        default, meaning it handles its own exceptions and errors).
        Disable full_stack when this application is "managed" by another
        WSGI middleware.

    ``app_conf``
        The application's local configuration. Normally specified in the
        [app:<name>] section of the Paste ini file (where <name>
        defaults to main).
    """
    # Configure the Pylons environment
    load_environment(global_conf, app_conf)

    # The Pylons WSGI app
    app = PylonsApp()

    # CUSTOM MIDDLEWARE HERE (filtered by error handling middlewares)

    app = Sniff(app)

    if asbool(full_stack):
        # Handle Python exceptions
        app = ErrorHandler(app, global_conf, error_template=error_template,
                           **config['pylons.errorware'])

        # Display error documents for 401, 403, 404 status codes (and
        # 500 when debug is disabled)
        app = ErrorDocuments(app, global_conf, mapper=error_mapper, **app_conf)

    # Establish the Registry for this application
    app = RegistryManager(app)

    # Static files
    javascripts_app = StaticJavascripts()
    static_app = StaticURLParser(config['pylons.paths']['static_files'])
    app = Cascade([static_app, javascripts_app, app])
    return app


class Globals(object):
    """Globals acts as a container for objects available throughout the
    life of the application
    """

    def __init__(self):
        """One instance of Globals is created during application
        initialization and is available during requests via the 'g'
        variable.
        """


        try:
            import perl
        except ImportError:
            print "You need the pyperl module installed."
            print "You can get it from the ISPManSOAP source"
            sys.exit(1)
        self.perl = perl

        log.debug('Perl Is Now Setup')

        ispman_installdir = os.path.abspath(config['app_conf']['ispman_base_dir'])

        # Get Perl's @INC reference
        inc = perl.get_ref("@INC")
        # Add ISPMan lib directory to perl's @INC
        ispman_libs = os.path.join(ispman_installdir, 'lib')
        inc.append(ispman_libs)
        # Setup an ISPMan instance
        perl.require('ISPMan')
        perl.require('CGI')

        try:
            ispman_perl = perl.eval(
                '$ENV{"HTTP_USER_AGENT"} = "PYTHON-CCP"; ' +
                '$ispman = ISPMan->new() or die "$@"'
            )
        except Exception, e:
            print e



        self.ldap_config = dict(
            host    = ispman_perl.getConf('ldapHost'),
            version = ispman_perl.getConf('ldapVersion'),
            base_dn = ispman_perl.getConf('ldapBaseDN')
        )


        perl.require('Net::LDAP')
        log.debug('After require LDAP')
        eval_string = 'Net::LDAP->new( "%s",version => %s ) or die "$@";'
        log.debug('Eval String: %s',eval_string % (self.ldap_config['host'],
                                                   self.ldap_config['version']))
        try:
            ldap = perl.eval(eval_string % (self.ldap_config['host'],
                                            self.ldap_config['version']))
            self.ldap = ldap
        except perl.PerlError, error:
            print "Failed to connect to LDAP Server: %s" % error
            sys.exit(1)

        log.debug('After LDAP setup')

        self.ldap_config['allowed_user_attributes'] = (
            'dn', 'dialupAccess', 'radiusProfileDn', 'uid', 'uidNumber',
            'gidNumber', 'homeDirectory', 'loginShell', 'ispmanStatus',
            'ispmanCreateTimestamp', 'ispmanUserId', 'ispmanDomain',
            'DestinationAddress', 'DestinationPort', 'mailQuota', 'mailHost',
            'fileHost', 'cn', 'mailRoutingAddress', 'FTPStatus',
            'FTPQuotaMBytes', 'mailAlias', 'sn', 'mailLocalAddress',
            'userPassword', 'mailForwardingAddress', 'givenName')

        self.ldap_config['updatable_attributes'] = (
            'ispmanStatus', 'mailQuota', 'mailAlias', 'sn', 'userPassword',
            'givenName', 'updateUser', 'uid', 'mailForwardingAddress',
            'ispmanDomain', 'FTPQuotaMBytes', 'FTPStatus', 'mailHost',
            'fileHost', 'dialupAccess', 'radiusProfileDN')

        self.ispman = ispman_perl

        log.debug('ISPMan(perl) Is Now Setup')

