import unittest
import network_devices_api as nda

class TestAPI(unittest.TestCase):
    def test_is_key_valid(self):
        self.assertEqual(nda.is_key_valid("xxx"),True)
        self.assertEqual(nda.is_key_valid(""),False)

    def test_is_data_valid(self):
        self.assertEqual(nda.is_data_valid({}),False)
        self.assertEqual(nda.is_data_valid(None),False)
        data = {'model':'ios-xr', 'version':''}
        self.assertEqual(nda.is_data_valid(data),True)

    def test_extract_key_and__data(self):
        data = {'fqdn':'xxx','model':'ios-xr', 'version':''}
        self.assertEqual(nda.extract_key(data),'xxx')
        self.assertEqual(nda.extract_key_and_data(data),('xxx',{'model':'ios-xr', 'version':''}))
        data = {'fqdn':'xxx','model':'ios-xr'}
        self.assertEqual(nda.extract_key_and_data(data),('xxx',{'model':'ios-xr', 'version':''}))
        pass

    def test_is_input_valid(self):
        data = {'fqxwxdn':'xxx'}
        self.assertEqual(nda.is_input_valid(data),False)
        self.assertEqual(nda.is_input_valid(data,'xxx'),False)
    
        data = {'fqdn':'xxx','model':'ios-xr', 'version':''}
        self.assertEqual(nda.is_input_valid(data),True)
        self.assertEqual(nda.is_input_valid(data,'xxx'),True)
        pass


if __name__ == '__main__':
    unittest.main()