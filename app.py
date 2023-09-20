from flask import Flask, request, jsonify
import sqlglot

app = Flask(__name__)

supported_dialects = [
    "bigquery",
    "clickhouse",
    "databricks",
    "doris",
    "drill",
    "duckdb",
    "hive",
    "mysql",
    "oracle",
    "postgres",
    "presto",
    "redshift",
    "snowflake",
    "spark",
    "spark2",
    "sqlite",
    "starrocks",
    "tableau",
    "teradata",
    "trino",
    "tsql"
]


@app.route("/translate", methods=["POST"])
def translate_sql():
    try:
        # Get the JSON data from the POST request
        data = request.get_json()

        # Ensure that the required keys 'sql', 'from', and 'to' are present in the JSON
        if "sql" in data and "from" in data and "to" in data:
            sql_query = data["sql"]
            from_dialect = data["from"]
            to_dialect = data["to"]

            # Ensure that the input and output dialects are supported
            if from_dialect not in supported_dialects:
                return jsonify(
                    {"error": "Unsupported input dialect: {}".format(from_dialect)}
                ), 400

            translation = sqlglot.transpile(
                sql_query, read=from_dialect, write=to_dialect
            )[0]

            response_data = {"sql": translation}

            return jsonify(response_data), 200
        else:
            return jsonify({"error": "Invalid JSON format"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/")
def home():
    return "home"
