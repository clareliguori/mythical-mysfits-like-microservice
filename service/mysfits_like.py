from __future__ import print_function

import boto3
import json
from flask import Flask, jsonify, json, Response, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

client = boto3.client('dynamodb')
table_name = os.environ['DATABASE_TABLE_NAME']

@app.route("/")
def health_check_response():
    return jsonify({"message" : "Nothing here, used for health check."})

@app.route("/mysfits/<mysfit_id>/like", methods=['POST'])
def like_mysfit(mysfit_id):
    response = increment_mysfit_likes(mysfit_id)
    flask_response = Response(response)
    flask_response.headers["Content-Type"] = "application/json"
    return flask_response

def increment_mysfit_likes(mysfit_id):
    client.update_item(
        TableName=table_name,
        Key={
            'MysfitId': {
                'S': mysfit_id
            }
        },
        UpdateExpression="SET Likes = Likes + :n",
        ExpressionAttributeValues={':n': {'N': '1'}}
    )

    response = client.get_item(
        TableName=table_name,
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
    app.run(host="0.0.0.0", port=80)
