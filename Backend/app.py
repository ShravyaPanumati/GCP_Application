import os
import base64

from flask import Flask, request, jsonify
import flask_cors
import pyodbc
from google.cloud import storage

app = Flask(__name__)
flask_cors.CORS(app)  # Enable CORS for all routes

# Google Cloud configuration
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')  # Get from environment variable

# Set the environment variable for Google Application Credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/app/service-account-file.json'  # Ensure this is mounted in your container

# Database connection function
def connect_db():
    server = '34.42.71.28'  # Replace with your instance public IP
    database = 'myappdb'  # Replace with your database name
    username = os.getenv('DB_USERNAME')  # Get username from environment variable
    password = os.getenv('DB_PASSWORD')  # Get password from environment variable
    driver = '{ODBC Driver 17 for SQL Server}'  # ODBC driver

    connection = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}')
    return connection

# Ensure these values are fetched as environment variables
@app.before_first_request
def load_config():
    # Load GCS_BUCKET_NAME from secret
    if not GCS_BUCKET_NAME:
        raise ValueError("GCS_BUCKET_NAME is not set")

# Function to create the table if it doesn't exist
def create_values_table():
    conn = connect_db()
    cursor = conn.cursor()

    # Create table query
    create_table_query = '''
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='values_table' and xtype='U')
    CREATE TABLE values_table (
        id INT PRIMARY KEY IDENTITY(1,1),
        value1 NVARCHAR(50) NOT NULL,
        value2 NVARCHAR(50) NOT NULL
    );
    '''
    cursor.execute(create_table_query)
    conn.commit()
    cursor.close()
    conn.close()

# Route to insert values into the database
@app.route('/insert', methods=['POST'])
def insert_values():
    data = request.json
    value1 = data.get('value1')
    value2 = data.get('value2')

    # Validate the input
    if not value1 or not value2:
        return jsonify({'error': 'Invalid data'}), 400

    conn = connect_db()
    cursor = conn.cursor()

    # Insert values into the database
    insert_values_query = 'INSERT INTO values_table (value1, value2) VALUES (?, ?)'
    cursor.execute(insert_values_query, (value1, value2))
    conn.commit()

    cursor.close()
    conn.close()

    return jsonify({'message': 'Values inserted successfully'}), 200

# Route to fetch values from the database
@app.route('/fetch', methods=['GET'])
def fetch_values():
    conn = connect_db()
    cursor = conn.cursor()

    # Fetch all values from the database
    cursor.execute('SELECT * FROM values_table')
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    values_list = [{'id': row[0], 'value1': row[1], 'value2': row[2]} for row in rows]

    cursor.close()
    conn.close()

    return jsonify(values_list), 200

# Route to upload a file to Google Cloud Storage
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    # Upload the file to GCS
    storage_client = storage.Client()
    bucket = storage_client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(file.filename)

    blob.upload_from_file(file)

    return jsonify({'message': f'File {file.filename} uploaded successfully to {GCS_BUCKET_NAME}.'}), 200

# Main block
if __name__ == '__main__':
    # Ensure the values_table exists
    create_values_table()
    app.run(host='0.0.0.0', port=5000, debug=True)
