import itertools
import operator
import boto3
import uuid
import json
from flask import Flask, request, jsonify

# Service resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomerAd')
# Init flask app
app = Flask(__name__)

@app.route('/ad', methods=['POST'])
def target():
  body = request.form
  name = body['name']
  template = body['template']
  acqusition_rate = body['acqusition_rate']

  response = table.put_item(
    TableName = "CustomerAd",
    Item = {
      "uuid": str(uuid.uuid4()),
      "customers_reached": {"N": 0},
      "customer_clicks": {"N": 0},
      "name": {"S": name},
      "customers_installed":{"N": 0},
      "template": {"S": template},
      "acqusition_rate": {"N": acqusition_rate},
      "descriptors": {"SS": [
        'string'
      ]}
    }
  )

  return jsonify(response), response['ResponseMetadata']['HTTPStatusCode']
 
if __name__ == '__main__':
    app.run(debug=True)