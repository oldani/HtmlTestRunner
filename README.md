# HtmlTestRunner

HtmlTest runner is a unittest test runner that save test results
in Html files, for human readable presentation of results.

This Package was inspired in `unittest-xml-reporting` and
`HtmlTestRunner by tungwaiyip`.

This project was created due to needs of getting human readables reports 
for test runned, i found one but was lack and with a lot of bad practice,
but i liked how `xml-reporting` works. So i create this one that 
incorporated code from both projects but up to date.

## Usage

````python
import HtmlTestRunner
import unittest

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

if __name__ == '__main__':
    unittest.main(testRunner=HtmlTestRunner.HTMLTestRunner(output='example_dir'))
````
As simple as import the class an initialize it, it only have one request parameter that is
output, this one is use to place the report in a sub direcotry in `reports` directory.
