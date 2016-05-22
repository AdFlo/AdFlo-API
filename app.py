import itertools
import operator
import uuid
import json
import pymongo
import boto3
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from bson import Binary, Code
from bson.json_util import dumps
import random
import ast

# Service resource
s3 = boto3.resource('s3')
# Init flask app
app = Flask(__name__)
# Db client
client = pymongo.MongoClient("localhost", 27017)
db = client.customerad

@app.route('/ad', methods=['POST'])
def ad():
  body = request.form
  name = body['name']
  acqusition_rate = body['acqusition_rate']
  template = body['template']
  descriptors = body['descriptors']

  response = db.collection.insert_one({
    "TableName": "customerad",
    "Item": {
      "uuid": str(uuid.uuid4()),
      "customers_reached": 0,
      "customer_clicks": 0,
      "name": name,
      "customers_installed": 0,
      "template": template,
      "acqusition_rate": acqusition_rate,
      "descriptors": descriptors
    }
  })

  return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 

@app.route('/target', methods=['GET'])
def target():
  descriptors = request.args.get("descriptors");
  descriptors = descriptors.split(",")

  description = {}
  percentages = {}

  category = ""
  template = ""

  total_len = len(descriptors)
  max = 0.0

  for category in descriptors:
    if category in description:
      description[category] = description[category] + 1
    else:
      description[category] = 1

  for category in descriptors:
    percentages[category] = description[category] / float(total_len)
    if percentages[category] > max:
      max = percentages[category]

  sorted_percentages = sorted(percentages, key=percentages.get, reverse=True)

  for percent in sorted_percentages:
    if float(random.uniform(0.0, 1.0)) > percentages[percent]:
      category = percent
      break

  for item in db.collection.find().sort("customer_clicks", pymongo.ASCENDING):
    curr_item = item['Item']
    curr_descriptor = ast.literal_eval(curr_item['descriptors'])

    for descriptor in curr_descriptor:
      if descriptor == category:
        return jsonify({'id': str(item['_id']), 'template': curr_item['template']}), 200

  return jsonify({ 'message': 'No ads to display'}), 200

@app.route('/ad', defaults={'id': None})
@app.route('/ad/<id>/click', methods=['POST'])
def click(id):
  body = request.form
  _id = id

  response = db.collection.update({
    '_id': ObjectId(_id)
  }, {
    '$inc': {
      'Item.customer_clicks': 1
    }
  })

  return jsonify(response), 200

if __name__ == '__main__':
    app.run(debug=True)