import basic_lambda_testutils as main_utils
import unittest
unittest.TestLoader.sortTestMethodsUsing = None
lambda_func_name = 'basic_lambda'

class Test(unittest.TestCase):
    def test_a_setup_class(self):
        print('\r\nCreating the lambda function...')
        main_utils.create_lambda(lambda_func_name)
    def test_b_invoke_function_and_response(self):
        print('\r\nInvoking the lambda function...')
        payload = main_utils.invoke_function(lambda_func_name)
        self.assertEqual(payload['message'], 'Hello User!')
    def test_c_teardown_class(self):
        print('\r\nDeleting the lambda function...')
        main_utils.delete_lambda(lambda_func_name)