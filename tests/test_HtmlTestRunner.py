#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_HtmlTestRunner
----------------------------------

Tests for `HtmlTestRunner` module.
"""


import glob
import tempfile
import os
import shutil
from six import StringIO
import unittest

from HtmlTestRunner import HTMLTestRunner


class TestHtmlTestTunner(unittest.TestCase):

    class DummyTestCase(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_01_pass(self):
            """ This test should pass. """
            pass

        def test_02_fail(self):
            """ This test should fail. """
            assert 1 == 0

        def test_03_error(self):
            """ This test should rise an error. """
            raise ValueError("Error raised")

        @unittest.skip("skipping this test")
        def test_04_skip(self):
            """ This test should be skipped. """
            pass

    class DummyTestCase2(unittest.TestCase):

        def setUp(self):
            pass

        def tearDown(self):
            pass

        def test_01_pass(self):
            pass

        def test_02_fail(self):
            assert 1 == 0

        def test_03(self):
            pass

    def setUp(self):
        self.stream = StringIO()
        self.output = "reports/test_dir"
        self.html_runner = HTMLTestRunner(stream=self.stream, output="test_dir")

    def tearDown(self):
        try:
            shutil.rmtree(self.output)
            os.rmdir("reports")
            self.stream.close()
        except:
            pass

    def get_report(self):
        """ Read the report created. """
        file = glob.glob("{}/*html".format(self.output))
        with open(file[0], "r") as f:
            report = f.read()
        return report

    def test_01_report_dir(self):
        """ Test dirs are created. """
        self.html_runner.run(self.DummyTestCase("test_01_pass"))

        assert os.path.exists(self.output)

    def test_02_report_file(self):
        """ Test Html report is created. """
        self.html_runner.run(self.DummyTestCase("test_02_fail"))

        result = glob.glob("{}/*html".format(self.output))
        assert len(result) == 1

    def test_03_stream(self):
        """ Check stream output. """
        self.html_runner.run(self.DummyTestCase("test_01_pass"))

        result = self.stream.getvalue()

        assert "Running tests..." in result
        assert "This test should pass. ... OK" in result
        assert "Ran 1 test" in result
        assert "OK" in result
        assert "Generating HTML reports..." in result

    def test_04_stream(self):
        """ Check stream output. """
        suite = unittest.TestSuite()
        suite.addTest(self.DummyTestCase("test_01_pass"))
        suite.addTest(self.DummyTestCase("test_02_fail"))
        suite.addTest(self.DummyTestCase("test_03_error"))
        suite.addTest(self.DummyTestCase("test_04_skip"))

        self.html_runner.run(suite)

        result = self.stream.getvalue()

        assert "Running tests..." in result
        assert "This test should pass. ... OK" in result
        assert "This test should fail. ... FAIL" in result
        assert "This test should rise an error. ... ERROR" in result
        assert "This test should be skipped. ... SKIP" in result
        assert 'raise ValueError("Error raised")' in result
        assert "assert 1 == 0" in result
        assert "Ran 4 test" in result
        assert "FAILED" in result
        assert "(Failures=1, Errors=1, Skipped=1)" in result

    def test_05_html_report(self):
        """ Check out html report content. """
        suite = unittest.TestSuite()
        suite.addTest(self.DummyTestCase("test_01_pass"))
        suite.addTest(self.DummyTestCase("test_02_fail"))
        suite.addTest(self.DummyTestCase("test_03_error"))
        suite.addTest(self.DummyTestCase("test_04_skip"))

        self.html_runner.run(suite)

        report = self.get_report()

        # Check status
        assert "Pass: 1, Fail: 1, Error: 1, Skip: 1" in report
        assert "This test should pass." in report
        # Check fail and reason for
        assert "This test should fail." in report
        assert "AssertionError" in report
        # Check error, error type and message
        assert "This test should rise an error." in report
        assert "ValueError" in report
        assert "Error raised" in report
        # Check skip and message due.
        assert "This test should be skipped." in report
        assert "skipping this test" in report
        # Others
        assert "Total Test Runned: 4" in report
        # assert "DummyTestCase" in report
        assert "Test Suite" in report

    def test_06_test_docs(self):
        """ Check test func name is used when there's no test description. """
        suite = unittest.TestSuite()
        suite.addTest(self.DummyTestCase2("test_01_pass"))
        suite.addTest(self.DummyTestCase2("test_02_fail"))

        self.html_runner.run(suite)

        report = self.get_report()

        assert "test_01_pass" in report
        assert "test_02_fail" in report
        assert "AssertionError" in report

    def test_07_report_title(self):
        """ Check for custom report title. """
        title = "Test Report name"
        html_runner = HTMLTestRunner(stream=self.stream, output="test_dir",
                                     report_title=title)
        html_runner.run(self.DummyTestCase("test_01_pass"))

        report = self.get_report()

        assert title in report

    def test_08_report_title(self):
        """ Check for report title. """
        html_runner = HTMLTestRunner(stream=self.stream, output="test_dir",
                                     combine_suite=False)
        html_runner.run(self.DummyTestCase("test_01_pass"))

        report = self.get_report()

        assert "Test Result" in report

    def test_09_test_name(self):
        """ Check for test func name wich not follow conventions. """
        self.html_runner.run(self.DummyTestCase2("test_03"))
        # ... add more examples

        report = self.get_report()

        assert "test_03" in report

    def test_10_outsuffix(self):
        """ Check for outsuffix on report file name. """
        outsuffix = "my_outsuffix"

        self.html_runner.outsuffix = outsuffix
        self.html_runner.run(self.DummyTestCase("test_01_pass"))

        file = glob.glob("{}/*html".format(self.output))[0]

        assert outsuffix in file

    def test_11_custom_template(self):
        """ Test passing a custom templete for report. """
        template = """
            <html>
              <body>
                <div> {{title}} Custom</div>
                <div> {{title}} </div>
                <div> {{headers.status}} </div>
                <div> {{testcase_name}} </div>
                <div> {{testcase_name}} </div>
                <div> {{total_tests}} </div>
              </body>
            </html>
        """
        _, path = tempfile.mkstemp(text=True)
        with open(path, "w") as file:
            file.write(template)
        self.html_runner.template = path

        suite = unittest.TestSuite()
        suite.addTest(self.DummyTestCase("test_01_pass"))
        suite.addTest(self.DummyTestCase("test_02_fail"))
        suite.addTest(self.DummyTestCase("test_03_error"))
        suite.addTest(self.DummyTestCase("test_04_skip"))

        self.html_runner.run(suite)
        os.remove(path)

        report = self.get_report()

        assert "Test Suite Custom" in report

    def test_12_suite_report(self):
        """ Check a separate report is generated per test case. """
        dummy1 = unittest.TestLoader().loadTestsFromTestCase(self.DummyTestCase)
        dummy2 = unittest.TestLoader().loadTestsFromTestCase(self.DummyTestCase2)
        suite = unittest.TestSuite([dummy1, dummy2])

        self.html_runner.combine_suite = False

        self.html_runner.run(suite)

        result = glob.glob("{}/*html".format(self.output))
        assert len(result) == 2


if __name__ == "__main__":
    unittest.main()
