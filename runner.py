import sys
import time

from unittests import TextTestRunner
from result import _TestResult

UTF8 = "UTF-8"


class HTMLTestRunner(TextTestRunner):
    """" A test runner class that output the results. """

    def __init__(self, output, verbosity=1, stream=sys.stderr,
                 descriptions=True, failfast=False, buffer=False,
                 resultclass=None):
        self.verbosity = verbosity
        self.output = output
        self.encoding = UTF8

        TextTestRunner.__init__(self, stream, descriptions, verbosity,
                                failfast=failfast, buffer=buffer)

        self.outsuffix = time.strftime("%Y%m%d%H%M%S")
        self.elapsed_times = True
        if resultclass is None:
            self.resultclass = _TestResult
        else:
            self.resultclass = resultclass

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

            start_time = time.time()
            test(result)
            stop_time = time.time()
            time_taken = stop_time - start_time

            result.printErrors()
            self.stream.writeln(result.separator2)
            run = result.testRun
            self.stream.writeln("Ran {} test{} in {:.3f}s".format(run,
                                run != 1 and "s" or "", time_taken))
            self.stream.writeln()

            expectedFails = len(result.expectedFailures)
            unexpectedSuccesses = len(result.unexpectedSuccesses)
            skipped = len(result.skipped)

            infos = []
            if not result.wasSuccessful():
                self.stream.writeln("FAILED")
                failed, errors = map(len, (result.failures, result.errors))
                if failed:
                    infos.append("failures={0}".format(failed))
                if errors:
                    infos.append("errors={0}".format(errors))
            else:
                self.stream.writeln("OK")

            if skipped:
                infos.append("skipped={}".format(skipped))
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
