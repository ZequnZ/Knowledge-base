import basic_lambda_testutils as testutils
from unittest import TestCase
import time

lambda_func_name = 'basic_lambda'

class Test(TestCase):

    @classmethod
    def setup_class(cls):
        print('\r\nSetting up the class')
        testutils.create_lambda(lambda_func_name)
        time.sleep(20)

    @classmethod
    def teardown_class(cls):
        print('\r\nTearing down the class')
        testutils.delete_lambda(lambda_func_name)

    def test_that_lambda_returns_correct_message(self):
        payload = testutils.invoke_function(lambda_func_name)
        self.assertEqual(payload['message'], 'Hello Mei Zhou!')