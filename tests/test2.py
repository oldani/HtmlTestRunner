# import unittest

# from HtmlTestRunner import HTMLTestRunner

# from test import TestStringMethods
# from test import MoreTests as MoreTests_


# class My_Tests(unittest.TestCase):

#     def test_one(self):
#         self.assertTrue(True)

#     def test_two(self):
#         # demonstrate that stdout is captured in passing tests
#         print("HOLA CARACOLA")
#         self.assertTrue(True)

#     def test_three(self):
#         self.assertTrue(True)

#     def test_1(self):
#         # demonstrate that stdout is captured in failing tests
#         print("HELLO")
#         self.assertTrue(False)

#     def test_2(self):
#         self.assertTrue(False)

#     def test_3(self):
#         self.assertTrue(False)

#     def test_z_subs_pass(self):
#         for i in range(2):
#             with self.subTest(i=i):
#                 print("i = {}".format(i))  # this won't appear for now
#                 self.assertEqual(i, i)


# class MoreTests(unittest.TestCase):
#     def test_1(self):
#         print("This is different to test.MoreTests.test_1")
#         self.assertAlmostEqual(1, 1.1, delta=0.05)


# if __name__ == '__main__':
#     tests = unittest.TestLoader().loadTestsFromTestCase(My_Tests)
#     other_tests = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
#     more_tests = unittest.TestLoader().loadTestsFromTestCase(MoreTests)
#     more_tests_ = unittest.TestLoader().loadTestsFromTestCase(MoreTests_)
#     suite = unittest.TestSuite([tests, other_tests, more_tests, more_tests_])
#     HTMLTestRunner(
#         report_title='TEST COMBINED',
#         report_name="MyReports",
#         add_timestamp=False,
#         open_in_browser=True,
#         combine_reports=True
#     ).run(suite)

#     tests = unittest.TestLoader().loadTestsFromTestCase(My_Tests)
#     other_tests = unittest.TestLoader().loadTestsFromTestCase(TestStringMethods)
#     more_tests = unittest.TestLoader().loadTestsFromTestCase(MoreTests)
#     more_tests_ = unittest.TestLoader().loadTestsFromTestCase(MoreTests_)
#     suite = unittest.TestSuite([tests, other_tests, more_tests, more_tests_])
#     HTMLTestRunner(
#         report_title='TEST SEPARATE',
#         report_name="MyReports",
#         open_in_browser=True,
#         combine_reports=False
#     ).run(suite)
