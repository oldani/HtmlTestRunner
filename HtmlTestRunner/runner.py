import sys
import time
from datetime import datetime

from unittest import TextTestRunner
from .result import _HtmlTestResult

UTF8 = "UTF-8"


class HTMLTestRunner(TextTestRunner):
    """" A test runner class that output the results. """

    def __init__(self, output, verbosity=2, stream=sys.stderr,
                 descriptions=True, failfast=False, buffer=False,
                 report_title=None, template=None, resultclass=None):
        self.verbosity = verbosity
        self.output = output
        self.encoding = UTF8

        TextTestRunner.__init__(self, stream, descriptions, verbosity,
                                failfast=failfast, buffer=buffer)

        self.outsuffix = time.strftime("%Y-%m-%d_%H-%M-%S")
        self.elapsed_times = True
        if resultclass is None:
            self.resultclass = _HtmlTestResult
        else:
            self.resultclass = resultclass

        self.report_title = report_title or "Test Result"
        self.template = template

    def _make_result(self):
        """ Create a TestResult object which will be used to store
        information about the executed tests. """
        return self.resultclass(self.stream, self.descriptions, self.verbosity,
                                self.elapsed_times)

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
                infos.append("expected failures={}".format(expectedFails))
            if unexpectedSuccesses:
                infos.append("unexpected successes={}".format(unexpectedSuccesses))

            if infos:
                self.stream.writeln(" ({})".format(", ".join(infos)))
            else:
                self.stream.writeln("\n")

            self.stream.writeln()
            self.stream.writeln('Generating HTML reports... ')
            result.generate_reports(self)
        finally:
            pass
        return result
