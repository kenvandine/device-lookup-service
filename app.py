#!/usr/bin/env python3

from flask import Flask, jsonify, request
import os
import json
import yaml
import logging

if os.environ.get('LOG_FILE'):
    logfile=os.environ['LOG_FILE']
else:
    logfile='app.log'

if os.environ.get('DB_FILE'):
    dbfile=os.environ['DB_FILE']
else:
    dbfile='db.json'

if os.environ.get('AUTOINSTALL_DB_FILE'):
    autoinstall_dbfile=os.environ['AUTOINSTALL_DB_FILE']
else:
    autoinstall_dbfile='autoinstall-db.json'

# Configure logging
logging.basicConfig(filename=logfile, level=logging.INFO)

try:
    with open(dbfile, 'r') as f:
        db = json.load(f)
except:
    db = {}

try:
    with open(autoinstall_dbfile, 'r') as f:
        autoinstall_db = json.load(f)
except:
    autoinstall_db = {}

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

@app.route('/query', methods=['GET'])
def query():
    logging.info("QUERY")
    serial = request.args.get('serial')
    logging.info("Querying for serial: %s", serial)

    if not list(db.keys()).count(serial):
        logging.info("Serial %s not found", serial)
        return jsonify({'error': 'Serial not found'})

    return jsonify(db[serial])

@app.route('/', methods=['GET'])
def index():
    logging.info("index")
    return jsonify(db)

@app.route('/add-autoinstall', methods=['POST'])
def add_autoinstall():
    data = request.json
    for item in list(data.keys()):
        logging.info("Adding device %s", item)
        autoinstall_db[item] = data[item]
    with open(autoinstall_dbfile, 'w') as f:
        logging.info("Saving database")
        # Move the file pointer to the beginning
        f.seek(0)
        json.dump(autoinstall_db, f, indent=4)
        f.truncate()
    return jsonify({'Success': 'Added'})

@app.route('/autoinstall', methods=['GET'])
def autoinstall():
    logging.info("AUTOINSTALL")
    serial = request.args.get('serial')
    logging.info("Generating autoinstall.yaml for serial: %s", serial)

    if not list(autoinstall_db.keys()).count(serial):
        logging.info("Serial %s not found", serial)
        return jsonify({'error': 'Serial not found'})

    return yaml.dump(autoinstall_db[serial])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
