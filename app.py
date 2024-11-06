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

@app.route('/devices', methods=['POST'])
def add_device():
    print(request.json)
    if not request.json or len(request.json.keys()) > 1:
        return jsonify({"error": "Bad Request"}), 400

    data = request.json
    serial = None
    for item in list(data.keys()):
        logging.info("Adding device %s", item)
        db[item] = data[item]
        serial = item
    with open(dbfile, 'w') as f:
        logging.info("Saving database")
        # Move the file pointer to the beginning
        f.seek(0)
        json.dump(db, f, indent=4)
        f.truncate()
    return jsonify(db[serial]), 201

@app.route('/devices', methods=['GET'])
def get_devices():
    logging.info("get_devices")
    return jsonify(db), 200

@app.route('/devices/<string:serial>', methods=['GET'])
def get_device(serial):
    logging.info("get_device")
    logging.info("Querying for serial: %s", serial)

    if not list(db.keys()).count(serial):
        logging.info("Serial %s not found", serial)
        return jsonify({'error': 'Serial not found'}), 404

    return jsonify(db[serial]), 200

@app.route('/autoinstall', methods=['POST'])
def add_autoinstall():
    print(request.json)
    if not request.json or len(request.json.keys()) > 1:
        return jsonify({"error": "Bad Request"}), 400
    data = request.json
    serial = None
    for item in list(data.keys()):
        logging.info("Adding device %s", item)
        autoinstall_db[item] = data[item]
        serial = item
    with open(autoinstall_dbfile, 'w') as f:
        logging.info("Saving database")
        # Move the file pointer to the beginning
        f.seek(0)
        json.dump(autoinstall_db, f, indent=4)
        f.truncate()
    return yaml.dump(data[serial]), 201

@app.route('/autoinstall/<string:serial>', methods=['GET'])
def autoinstall(serial):
    logging.info("AUTOINSTALL")
    logging.info("Generating autoinstall.yaml for serial: %s", serial)

    if not list(autoinstall_db.keys()).count(serial):
        logging.info("Serial %s not found", serial)
        return jsonify({'error': 'Serial not found'})

    return yaml.dump(autoinstall_db[serial]), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
