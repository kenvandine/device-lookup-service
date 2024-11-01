from flask import Flask, jsonify, request
import json
import logging

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

try:
    with open('db.json', 'r') as f:
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
    with open('db.json', 'w') as f:
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
