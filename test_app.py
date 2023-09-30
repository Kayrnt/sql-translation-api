import json
from textwrap import dedent
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
        self.assertEqual(response_data["sql"], "SELECT * FROM my_table;")

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

    def test_valid_translation(self):
        data = {
            "sql": "SELECT * FROM my_table",
            "from": "postgres",
            "to": "mysql",
            "pretty": True
        }
        response = self.app.post('/translate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('sql', json.loads(response.data))

    def test_missing_sql(self):
        data = {
            "from": "postgres",
            "to": "mysql",
            "pretty": True
        }
        response = self.app.post('/translate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

    def test_missing_from(self):
        data = {
            "sql": "SELECT * FROM my_table",
            "to": "mysql",
            "pretty": True
        }
        response = self.app.post('/translate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

    def test_missing_to(self):
        data = {
            "sql": "SELECT * FROM my_table",
            "from": "postgres",
            "pretty": True
        }
        response = self.app.post('/translate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

    def test_invalid_pretty(self):
        data = {
            "sql": "SELECT * FROM my_table",
            "from": "postgres",
            "to": "mysql",
            "pretty": "not_a_boolean"
        }
        response = self.app.post('/translate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

    def test_unsupported_from_dialect(self):
        data = {
            "sql": "SELECT * FROM my_table",
            "from": "invalid_dialect",
            "to": "mysql",
            "pretty": True
        }
        response = self.app.post('/translate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

    def test_unsupported_to_dialect(self):
        data = {
            "sql": "SELECT * FROM my_table",
            "from": "postgres",
            "to": "invalid_dialect",
            "pretty": True
        }
        response = self.app.post('/translate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', json.loads(response.data))

    def test_supported_dialect_and_pretty(self):
        data = {
            "sql": "SELECT * FROM my_table",
            "from": "postgres",
            "to": "mysql",
            "pretty": True
        }
        response = self.app.post('/translate', data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('sql', json.loads(response.data))
        # assert sql is pretty
        expected_sql = dedent("""\
                              SELECT
                                *
                              FROM my_table;""")
        self.assertEqual(expected_sql, json.loads(response.data)['sql'])


if __name__ == "__main__":
    unittest.main()
