#!/usr/bin/env python3

from flask import Flask, jsonify, request
import os
import json
import logging

if os.environ.get('LOG_FILE'):
    logfile=os.environ['LOG_FILE']
else:
    logfile='app.log'
if os.environ.get('DB_FILE'):
    dbfile=os.environ['DB_FILE']
else:
    dbfile='db.json'

# Configure logging
logging.basicConfig(filename=logfile, level=logging.INFO)

try:
    with open(dbfile, 'r') as f:
        db = json.load(f)
except:
    db = {}

app = Flask(__name__)

@app.route('/add', methods=['POST'])
def add():
    data = request.json
    for item in list(data.keys()):
        logging.info("Adding device %s", item)
        db[item] = data[item]
    with open(dbfile, 'w') as f:
        logging.info("Saving database")
        # Move the file pointer to the beginning
        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()
    return jsonify({'Success': 'Added'})

@app.route('/query', methods=['POST'])
def query():
    logging.info("QUERY")
    data = request.json
    serial = data['serial']
    logging.info("Querying for serial: %s", serial)

    if not list(db.keys()).count(serial):
        logging.info("Serial %s not found", serial)
        return jsonify({'error': 'Serial not found'})

    return jsonify(db[serial])

@app.route('/', methods=['GET'])
def index():
    logging.info("index")
    return jsonify(db)

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
