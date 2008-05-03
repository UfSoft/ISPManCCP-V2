from ispman.tests import *

class TestDomainController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='ispman/soap/domain'))
        # Test response...
