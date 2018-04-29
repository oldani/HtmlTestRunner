from __future__ import print_function
import os
import sys
import time
import traceback
from unittest import TestResult, TextTestResult
from unittest.result import failfast

from jinja2 import Template


DEFAULT_TEMPLATE = os.path.join(os.path.dirname(__file__), "template",
                                "report_template.html")


def load_template(template):
    """ Try to read a file from a given path, if file
        does not exist, load default one. """
    file = None
    try:
        if template:
            with open(template, "r") as f:
                file = f.read()
    except Exception as err:
        print("Error: Your Template wasn't loaded", err,
              "Loading Default Template", sep="\n")
    finally:
        if not file:
            with open(DEFAULT_TEMPLATE, "r") as f:
                file = f.read()
        return file


def render_html(template, **kwargs):
    template_file = load_template(template)
    if template_file:
        template = Template(template_file)
        return template.render(**kwargs)


def testcase_name(test_method):
    testcase = type(test_method)

    module = testcase.__module__ + "."
    if module == "__main__.":
        module = ""
    result = module + testcase.__name__
    return result


class _TestInfo(object):
    """" Keeps information about the execution of a test method. """

    (SUCCESS, FAILURE, ERROR, SKIP) = range(4)

    def __init__(self, test_result, test_method, outcome=SUCCESS,
                 err=None, subTest=None):
        self.test_result = test_result
        self.outcome = outcome
        self.elapsed_time = 0
        self.err = err
        self.stdout = test_result._stdout_data
        self.stderr = test_result._stderr_data

        self.test_description = self.test_result.getDescription(test_method)
        self.test_exception_info = (
            '' if outcome in (self.SUCCESS, self.SKIP)
            else self.test_result._exc_info_to_string(
                self.err, test_method))

        self.test_name = testcase_name(test_method)
        self.test_id = test_method.id()
        if subTest:
            self.test_id = subTest.id()

    def id(self):
        return self.test_id

    def test_finished(self):
        self.elapsed_time = \
            self.test_result.stop_time - self.test_result.start_time

    def get_description(self):
        return self.test_description

    def get_error_info(self):
        return self.test_exception_info


class HtmlTestResult(TextTestResult):
    """ A test result class that express test results in Html. """

    start_time = None
    stop_time = None

    def __init__(self, stream, descriptions, verbosity):
        TextTestResult.__init__(self, stream, descriptions, verbosity)
        self.buffer = True
        self._stdout_data = None
        self._stderr_data = None
        self.successes = []
        self.callback = None
        self.infoclass = _TestInfo
        self.report_files = []

    def _prepare_callback(self, test_info, target_list, verbose_str,
                          short_str):
        """ Appends a 'info class' to the given target list and sets a
            callback method to be called by stopTest method."""
        target_list.append(test_info)

        def callback():
            """ Print test method outcome to the stream and elapsed time too."""
            test_info.test_finished()

            if self.showAll:
                self.stream.writeln(
                    "{} ({:3f})s".format(verbose_str, test_info.elapsed_time))
            elif self.dots:
                self.stream.write(short_str)
        self.callback = callback

    def getDescription(self, test):
        """ Return the test description if not have test name. """
        doc_first_line = test.shortDescription()
        if self.descriptions and doc_first_line:
            return doc_first_line
        else:
            return str(test)

    def startTest(self, test):
        """ Called before execute each method. """
        self.start_time = time.time()
        TestResult.startTest(self, test)

        if self.showAll:
            self.stream.write(" " + self.getDescription(test))
            self.stream.write(" ... ")

    def _save_output_data(self):
        try:
            self._stdout_data = sys.stdout.getvalue()
            self._stderr_data = sys.stderr.getvalue()
        except AttributeError:
            pass

    def stopTest(self, test):
        """ Called after excute each test method. """
        self._save_output_data()
        TextTestResult.stopTest(self, test)
        self.stop_time = time.time()

        if self.callback and callable(self.callback):
            self.callback()
            self.callback = None

    def addSuccess(self, test):
        """ Called when a test executes successfully. """
        self._save_output_data()
        self._prepare_callback(
            self.infoclass(self, test), self.successes, "OK", ".")

    @failfast
    def addFailure(self, test, err):
        """ Called when a test method fails. """
        self._save_output_data()
        testinfo = self.infoclass(
            self, test, self.infoclass.FAILURE, err)
        self.failures.append((testinfo,
                             self._exc_info_to_string(err, test)))
        self._prepare_callback(testinfo, [], "FAIL", "F")

    @failfast
    def addError(self, test, err):
        """" Called when a test method raises an error. """
        self._save_output_data()
        testinfo = self.infoclass(
            self, test, self.infoclass.ERROR, err)
        self.errors.append((
            testinfo,
            self._exc_info_to_string(err, test)
        ))
        self._prepare_callback(testinfo, [], 'ERROR', 'E')

    def addSubTest(self, testcase, test, err):
        """ Called when a subTest method raise an error. """
        if err is not None:
            self._save_output_data()
            testinfo = self.infoclass(
                self, testcase, self.infoclass.ERROR, err, subTest=test)
            self.errors.append((
                testinfo,
                self._exc_info_to_string(err, testcase)
            ))
            self._prepare_callback(testinfo, [], "ERROR", "E")

    def addSkip(self, test, reason):
        """" Called when a test method was skipped. """
        self._save_output_data()
        testinfo = self.infoclass(
            self, test, self.infoclass.SKIP, reason)
        self.skipped.append((testinfo, reason))
        self._prepare_callback(testinfo, [], "SKIP", "S")

    def printErrorList(self, flavour, errors):
        """
        Writes information about the FAIL or ERROR to the stream.
        """
        for test_info, dummy in errors:
            self.stream.writeln(self.separator1)
            self.stream.writeln(
                '{} [{:3f}s]: {}'.format(flavour, test_info.elapsed_time,
                                         test_info.get_description())
            )
            self.stream.writeln(self.separator2)
            self.stream.writeln('%s' % test_info.get_error_info())

    def _get_info_by_testcase(self):
        """ Organize test results  by TestCase module. """

        tests_by_testcase = {}

        for tests in (self.successes, self.failures, self.errors, self.skipped):
            for test_info in tests:
                if isinstance(test_info, tuple):
                    test_info = test_info[0]
                testcase_name = test_info.test_name
                if testcase_name not in tests_by_testcase:
                    tests_by_testcase[testcase_name] = []
                tests_by_testcase[testcase_name].append(test_info)

        return tests_by_testcase

    @staticmethod
    def _format_duration(elapsed_time):
        if elapsed_time > 1:
            duration = '{:2.2f} s'.format(elapsed_time)
        else:
            duration = '{:2.2f} ms'.format(elapsed_time * 1000)
        return duration

    def get_results_summary(self, tests, elapsed_time=None):
        # """ Setup the header info for the report. """

        failures = errors = skips = success = 0
        for test in tests:
            outcome = test.outcome
            if outcome == test.ERROR:
                errors += 1
            elif outcome == test.FAILURE:
                failures += 1
            elif outcome == test.SKIP:
                skips += 1
            elif outcome == test.SUCCESS:
                success += 1

        status = ['Total: {}'.format(len(tests))]
        if success:
            status.append('Pass: {}'.format(success))
        if failures:
            status.append('Fail: {}'.format(failures))
        if errors:
            status.append('Error: {}'.format(errors))
        if skips:
            status.append('Skip: {}'.format(skips))
        result_summary = ', '.join(status)

        if elapsed_time is not None:
            result_summary += ". Duration: {}".format(self._format_duration(elapsed_time))

        return result_summary

    def _get_header_info(self, tests, start_time, elapsed_time):
        result_summary = self.get_results_summary(tests)
        duration = self._format_duration(elapsed_time)

        header_info = {
            "start_time": start_time,
            "duration": duration,
            "status": result_summary
        }
        return header_info

    @staticmethod
    def _test_method_name(test_id):
        """ Return a test name of the test id. """
        return test_id.split('.')[-1]

    def _report_tests(self, all_results, testRunner):
        # """ Generate a html file for a given suite.  """
        start_time = testRunner.start_time
        elapsed_time = testRunner.time_taken.total_seconds()

        header_info = self._get_header_info(
            [item for sublist in all_results.values() for item in sublist],
            start_time, elapsed_time)

        summaries = {}
        # call get_report_attributes once for all tests and once for each set
        for test_case_class_name, test_case_tests in all_results.items():
            elapsed_time = 0
            for test in test_case_tests:
                elapsed_time += test.elapsed_time
            summaries[test_case_class_name] = self.get_results_summary(test_case_tests, elapsed_time)

        return header_info, summaries

    def generate_reports(self, testRunner):
        """ Generate report for all given runned test object. """
        status_tags = ('success', 'danger', 'warning', 'info')
        all_results = self._get_info_by_testcase()

        header_info, summaries = self._report_tests(all_results, testRunner)

        if not testRunner.combine_reports:
            for test_case_class_name, test_case_tests in all_results.items():
                html_file = render_html(testRunner.template, title=testRunner.report_title,
                                        header_info=header_info,
                                        all_results={test_case_class_name: test_case_tests},
                                        status_tags=status_tags,
                                        summaries=summaries,
                                        **testRunner.template_args)

                self.generate_file(testRunner, test_case_class_name, html_file)

        else:
            html_file = render_html(testRunner.template, title=testRunner.report_title,
                                    header_info=header_info,
                                    all_results=all_results,
                                    status_tags=status_tags,
                                    summaries=summaries,
                                    **testRunner.template_args)

            # TODO: allow user to provide a filename body?
            self.generate_file(testRunner, "_".join(all_results.keys()), html_file)

    def generate_file(self, testRunner, report_name, report):
        """ Generate the report file in the given path. """
        dir_to = os.path.join(testRunner.output, 'reports')
        if not os.path.exists(dir_to):
            os.makedirs(dir_to)

        if testRunner.timestamp:
            report_name += "_" + testRunner.timestamp
        report_name = "{}_{}.html".format("TestResults", report_name)

        path_file = os.path.abspath(os.path.join(dir_to, report_name))
        self.stream.writeln(os.path.relpath(path_file))
        self.report_files.append(path_file)
        with open(path_file, 'w') as report_file:
            report_file.write(report)

    def _exc_info_to_string(self, err, test):
        """ Converts a sys.exc_info()-style tuple of values into a string."""
        # if six.PY3:
        #     # It works fine in python 3
        #     try:
        #         return super(_HTMLTestResult, self)._exc_info_to_string(
        #             err, test)
        #     except AttributeError:
        #         # We keep going using the legacy python <= 2 way
        #         pass

        # This comes directly from python2 unittest
        exctype, value, tb = err
        # Skip test runner traceback levels
        while tb and self._is_relevant_tb_level(tb):
            tb = tb.tb_next

        if exctype is test.failureException:
            # Skip assert*() traceback levels
            length = self._count_relevant_tb_levels(tb)
            msg_lines = traceback.format_exception(exctype, value, tb, length)
        else:
            msg_lines = traceback.format_exception(exctype, value, tb)

        if self.buffer:
            # Only try to get sys.stderr as it might not be
            # StringIO yet, e.g. when test fails during __call__
            try:
                error = sys.stderr.getvalue()
            except AttributeError:
                error = None
            if error:
                if not error.endswith('\n'):
                    error += '\n'
                msg_lines.append(error)
        # This is the extra magic to make sure all lines are str
        encoding = getattr(sys.stdout, 'encoding', 'utf-8')
        lines = []
        for line in msg_lines:
            if not isinstance(line, str):
                # utf8 shouldn't be hard-coded, but not sure f
                line = line.encode(encoding)
            lines.append(line)

        return ''.join(lines)
