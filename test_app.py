import json
import unittest
from app import app


class TestTranslateSql(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_translate_sql(self):
        # Define the JSON data to send in the POST request
        data = {
            "sql": "SELECT * FROM my_table",
            "from": "mysql",
            "to": "postgres",
        }

        # Send a POST request to the /translate endpoint with the JSON data
        response = self.app.post(
            "/translate",
            data=json.dumps(data),
            content_type="application/json",
        )

        # Check that the response status code is 200 OK
        self.assertEqual(response.status_code, 200)

        # Check that the response JSON contains the expected 'sql' key
        response_data = json.loads(response.data)
        self.assertIn("sql", response_data)

        # Check that the response JSON contains the expected SQL translation
        self.assertEqual(response_data["sql"], "SELECT * FROM my_table")

    def test_translate_sql_with_stub_input_dialect(self):
        # Define the JSON data to send in the POST request
        data = {
            "sql": "SELECT * FROM my_table",
            "from": "stub",
            "to": "postgres"
        }

        # Send a POST request to the /translate endpoint with the JSON data
        response = self.app.post('/translate', data=json.dumps(data), content_type='application/json')

        # Check that the response status code is 400 Bad Request
        self.assertEqual(response.status_code, 400)

        # Check that the response JSON contains the expected error message
        response_data = json.loads(response.data)
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], 'Unsupported input dialect: stub')

if __name__ == "__main__":
    unittest.main()
