"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
    """Create, configure and return the routes Mapper"""
    map = Mapper(directory=config['pylons.paths']['controllers'],
                 always_scan=config['debug'])

    # CUSTOM ROUTES HERE
    map.connect('SOAP', 'SOAP/:action/:id', controller='soap')
    map.connect('RPC2', 'RPC2/:action/:id', controller='xmlrpc')
    map.connect(':(controller).wsdl')
    map.connect(':controller/:action/:id')
    return map
