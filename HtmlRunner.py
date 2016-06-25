from HtmlReports import HTMLTestRunner

class HtmlRunner(HTMLTestRunner.HTMLTestRunner):
    """ HOLAAAA. """
    title = "Test Report: Site %s"
    _output = '%s'
    _verbosity = 2

    def __init__(self, site):
        super(HtmlRunner, self).__init__(output=self._output%site, verbosity = self._verbosity, title= self.title%site)
