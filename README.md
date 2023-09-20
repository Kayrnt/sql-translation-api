# SQL Translation API

This is a Flask API that translates SQL queries from one dialect to another using the `sqlglot` library.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Kayrnt/sql-translation-api.git
   ```

2. Install the dependencies using Poetry:

   ```bash
   cd sql-translation-api
   poetry install
   ```

3. Start the Flask development server:

   ```bash
   poetry shell
   flask run
   ```

   The API will be available at `http://localhost:5000/translate`.

## Usage

To translate a SQL query, send a POST request to the `/translate` endpoint with a JSON body that contains the following keys:

- `sql`: The SQL query to translate
- `from`: The dialect of the input SQL query (e.g., `mysql`, `postgres`, `sqlite`)
- `to`: The dialect to translate the SQL query to (e.g., `mysql`, `postgres`, `sqlite`)

The API will return a JSON response with the translated SQL query.

Here's an example using the `curl` command:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"sql": "SELECT * FROM my_table", "from": "mysql", "to": "postgresql"}' http://localhost:5000/translate
```

This will return a JSON response with the translated SQL query.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
