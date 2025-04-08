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

if os.environ.get('BIOS_DB_FILE'):
    bios_dbfile=os.environ['BIOS_DB_FILE']
else:
    bios_dbfile='bios-db.json'

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

try:
    with open(bios_dbfile, 'r') as f:
        bios_db = json.load(f)
except:
    bios_db = {}

app = Flask(__name__)

@app.route('/bios', methods=['POST'])
def add_bios():
    if not request.json or len(request.json.keys()) > 1:
        return jsonify({"error": "Bad Request"}), 400

    data = request.json
    product_name = None
    for item in list(data.keys()):
        logging.info("Adding device %s", item)
        bios_db[item] = data[item]
        product_name = item
    with open(bios_dbfile, 'w') as f:
        logging.info("Saving database")
        # Move the file pointer to the beginning
        f.seek(0)
        json.dump(bios_db, f, indent=4)
        f.truncate()
    return jsonify(bios_db[product_name]), 201

@app.route('/bios', methods=['GET'])
def get_bioses():
    logging.info("get_bioses")
    return jsonify(bios_db), 200

@app.route('/bios/<string:product_name>', methods=['GET'])
def get_bios(product_name):
    logging.info("get_dbios")
    logging.info("Querying for product_name: %s", product_name)

    if not list(bios_db.keys()).count(product_name):
        logging.info("BIOS %s not found", product_name)
        return jsonify({'error': 'BIOS not found'}), 404

    return jsonify(bios_db[product_name]), 200

@app.route('/devices', methods=['POST'])
def add_device():
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
