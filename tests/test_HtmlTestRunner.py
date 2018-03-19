#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_HtmlTestRunner
----------------------------------

Tests for `HtmlTestRunner` module.
"""


import glob
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

    def setUp(self):
        self.stream = StringIO()
        self.output = "reports/test_dir"
        self.html_runner = HTMLTestRunner(stream=self.stream, output="test_dir")

    def tearDown(self):
        shutil.rmtree(self.output)
        os.rmdir("reports")
        self.stream.close()

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

    def test_04_html_report(self):
        """ """
        suite = unittest.TestSuite()
        suite.addTest(self.DummyTestCase("test_01_pass"))
        suite.addTest(self.DummyTestCase("test_02_fail"))
        suite.addTest(self.DummyTestCase("test_03_error"))
        suite.addTest(self.DummyTestCase("test_04_skip"))

        self.html_runner.run(suite)

        file = glob.glob("{}/*html".format(self.output))
        with open(file[0], "r") as f:
            report = f.read()

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
            assert "DummyTestCase" in report
            assert "Test Suite" in report


if __name__ == "__main__":
    unittest.main()
