import sys
import time
from datetime import datetime

from unittest import TextTestRunner
from .result import HtmlTestResult

UTF8 = "UTF-8"


class HTMLTestRunner(TextTestRunner):
    """" A test runner class that output the results. """

    time_format = "%Y-%m-%d_%H-%M-%S"

    def __init__(self, output="./reports/", verbosity=2, stream=sys.stderr,
                 descriptions=True, failfast=False, buffer=False,
                 report_title=None, report_name=None, template=None, resultclass=None,
                 add_timestamp=True, open_in_browser=False,
                 combine_reports=False, template_args=None):
        self.verbosity = verbosity
        self.output = output
        self.encoding = UTF8

        TextTestRunner.__init__(self, stream, descriptions, verbosity,
                                failfast=failfast, buffer=buffer)

        if add_timestamp:
            self.timestamp = time.strftime(self.time_format)
        else:
            self.timestamp = ""

        if resultclass is None:
            self.resultclass = HtmlTestResult
        else:
            self.resultclass = resultclass

        if template_args is not None and not isinstance(template_args, dict):
            raise ValueError("template_args must be a dict-like.")
        self.template_args = template_args or {}

        self.report_title = report_title or "Unittest Results"
        self.report_name = report_name
        self.template = template

        self.open_in_browser = open_in_browser
        self.combine_reports = combine_reports

        self.start_time = 0
        self.time_taken = 0

    def _make_result(self):
        """ Create a TestResult object which will be used to store
        information about the executed tests. """
        return self.resultclass(self.stream, self.descriptions, self.verbosity)

    def run(self, test):
        """ Runs the given testcase or testsuite. """
        try:

            result = self._make_result()
            result.failfast = self.failfast
            if hasattr(test, 'properties'):
                # junit testsuite properties
                result.properties = test.properties

            self.stream.writeln()
            self.stream.writeln("Running tests... ")
            self.stream.writeln(result.separator2)

            self.start_time = datetime.now()
            test(result)
            stop_time = datetime.now()
            self.time_taken = stop_time - self.start_time

            result.printErrors()
            self.stream.writeln(result.separator2)
            run = result.testsRun
            self.stream.writeln("Ran {} test{} in {}".format(run,
                                run != 1 and "s" or "", str(self.time_taken)[:7]))
            self.stream.writeln()

            expectedFails = len(result.expectedFailures)
            unexpectedSuccesses = len(result.unexpectedSuccesses)
            skipped = len(result.skipped)

            infos = []
            if not result.wasSuccessful():
                self.stream.writeln("FAILED")
                failed, errors = map(len, (result.failures, result.errors))
                if failed:
                    infos.append("Failures={0}".format(failed))
                if errors:
                    infos.append("Errors={0}".format(errors))
            else:
                self.stream.writeln("OK")

            if skipped:
                infos.append("Skipped={}".format(skipped))
            if expectedFails:
                infos.append("Expected Failures={}".format(expectedFails))
            if unexpectedSuccesses:
                infos.append("Unexpected Successes={}".format(unexpectedSuccesses))

            if infos:
                self.stream.writeln(" ({})".format(", ".join(infos)))
            else:
                self.stream.writeln("\n")

            self.stream.writeln()
            self.stream.writeln('Generating HTML reports... ')
            result.generate_reports(self)
            if self.open_in_browser:
                import webbrowser
                for report in result.report_files:
                    webbrowser.open_new_tab('file://' + report)
        finally:
            pass
        return result
