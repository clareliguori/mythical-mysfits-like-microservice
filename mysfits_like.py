from __future__ import print_function

import json
import os
import boto3
from flask import Flask, jsonify, json, Response
from flask_cors import CORS
from flask_swagger_ui import get_swaggerui_blueprint

APP = Flask(__name__, static_url_path='')
CORS(APP)

CLIENT = boto3.client('dynamodb')
TABLE = os.environ['DATABASE_TABLE_NAME']

SWAGGER_URL = '/docs'
API_URL = '/api.yaml'

SWAGGERUI = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'APP_name': "Mythical Mysfits 'Likes' Microservice"
    },
)

APP.register_blueprint(SWAGGERUI, url_prefix=SWAGGER_URL)

@APP.route("/")
def health_check_response():
    return jsonify({"message" : "Nothing here, used for health check."})

@APP.route("/mysfits/<mysfit_id>/like", methods=['POST'])
def like_mysfit(mysfit_id):
    response = increment_mysfit_likes(mysfit_id)
    flask_response = Response(response)
    flask_response.headers["Content-Type"] = "APPlication/json"
    return flask_response

def increment_mysfit_likes(mysfit_id):
    CLIENT.update_item(
        TableName=TABLE,
        Key={
            'MysfitId': {
                'S': mysfit_id
            }
        },
        UpdateExpression="SET Likes = Likes + :n",
        ExpressionAttributeValues={':n': {'N': '1'}}
    )

    response = CLIENT.get_item(
        TableName=TABLE,
        Key={
            'MysfitId': {
                'S': mysfit_id
            }
        }
    )

    item = response["Item"]

    mysfit = {}
    mysfit["id"] = item["MysfitId"]["S"]
    mysfit["name"] = item["Name"]["S"]
    mysfit["likes"] = item["Likes"]["N"]

    return json.dumps(mysfit)

# Run the service on the local server it has been deployed to,
# listening on port 80.
if __name__ == "__main__":
    APP.run(host="0.0.0.0", port=80)
