import os
import sys

from pymongo import MongoClient
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging

app = Flask(__name__)
CORS(app)

mongo_address = os.environ['MONGO_DATABASE']
logging.getLogger().addHandler(logging.StreamHandler(sys.stdout))
logging.debug("mongo address is", mongo_address)
client = MongoClient(mongo_address)
db = client.local
collection = db.working

IN_CALL_KEY = 'inCall'


@app.route('/set-in-call',  methods=["POST"])
def in_call_set():
    in_call_to_set = str2bool(request.args.get(IN_CALL_KEY))

    result = collection.find_one()
    collection.delete_one(filter=result)

    result[IN_CALL_KEY] = in_call_to_set
    collection.insert_one(result)
    return jsonify(success=True)


@app.route('/inCall',  methods=["GET"])
def in_call_get():
    result = collection.find_one()
    return jsonify(inCall=result['inCall'])


def str2bool(v):
    return str(v).lower() in ("yes", "true", "t", "1")


if __name__ == '__main__':
    result = collection.find_one()
    if result is None:
        default_value = {"inCall": False}
        collection.insert_one(default_value)

    app.run(host="0.0.0.0", debug=False)
    app.logger.setLevel(logging.INFO)
