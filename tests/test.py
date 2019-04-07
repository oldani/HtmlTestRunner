# import HtmlTestRunner
# import unittest


# class TestStringMethods(unittest.TestCase):
#     """ Example test for HtmlRunner. """

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)

#     def test_error(self):
#         """ This test should be marked as error one. """
#         raise ValueError

#     def test_fail(self):
#         """ This test should fail. """
#         self.assertEqual(1, 2)

#     @unittest.skip("This is a skipped test.")
#     def test_skip(self):
#         """ This test should be skipped. """
#         pass

#     def test_subs_fail(self):
#         test_string = "test1"
#         for i, char in enumerate(test_string):
#             with self.subTest(i=i):
#                 self.assertEqual(char, "1")

#         with self.subTest(test_string=test_string):
#             # subtests that error will appear as a failure presently
#             raise AttributeError


# class MoreTests(unittest.TestCase):
#     def test_1(self):
#         print("This is different to test2.MoreTests.test_1")
#         self.assertEqual(100, -100)


# if __name__ == '__main__':
#     unittest.main(
#         testRunner=HtmlTestRunner.HTMLTestRunner(
#             open_in_browser=True,
#             combine_reports=True,
#             template_args={}
#         )
#     )
