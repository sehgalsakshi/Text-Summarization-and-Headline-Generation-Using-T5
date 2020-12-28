try:
    from run import app
    import unittest 
    from werkzeug import FileStorage
except Exception as e:
    print("Some modules are missing {} ".format(e))

class TestRestApi(unittest.TestCase):
    """
    This class runs some mandatory unit tests to check the performance of rest api.
    """
    # check valid status code (200) and json response
    def test_valid_upload(self):
        filename = 'sample.pdf'
        fileobj = open(filename, 'rb')
        file = FileStorage(stream=fileobj, filename="sample.pdf", content_type="application/pdf")
        data = {
            'file': file,
        }
        headers = {'content_type': 'multipart/form-data'}
        tester = app.test_client(self)
        response = tester.post('/proccess_pdf', data=data, headers=headers)
        assert response.status_code == 200
    
    # check valid status code (200) and json response
    def test_size_constraints_upload(self):
        filename = 'sample.pdf'
        fileobj = open(filename, 'rb')
        file = FileStorage(stream=fileobj, filename="sample.pdf", content_type="application/pdf")
        data = {
            'file': file,
        }
        headers = {'content_type': 'multipart/form-data'}
        tester = app.test_client(self)
        response = tester.post('/proccess_pdf', data=data, headers=headers)
        assert response.status_code == 400

if __name__ == "__main__":
    unittest.main()