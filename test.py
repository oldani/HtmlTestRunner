import unittest
from runner import HTMLTestRunner

class TestRunner(HTMLTestRunner):

	_output = 'report/test'
	_ver = 2
	_buffer = True

	def __init__(self):
		super(TestRunner, self).__init__(output=self._output, verbosity=self._ver, buffer=self._buffer,
										  descriptions=False)


class TestUno(unittest.TestCase):
	""" HEYHEY """

	def setUp(self):
		n = 0
		result = 6

	def test_01_suma(self):
		""" HOLAAA """
		n_m = n + 3
		self.assertTrue(n_m == 3)
		a = n_m + 3
		self.assertTrue(a == self.result)
		print 'hola'

	def test_02_mul(self):
		""" HEYYY """
		b = (n + 1) * 3
		c = b * 2
		self.assertEqual(c, self.result)

	def tearDown(self):
		print 1
		pass

if __name__ == '__main__':
	unittest.main(testRunner=TestRunner())
