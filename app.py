import itertools
import operator
import uuid
import json
import pymongo
import boto3
from bson.objectid import ObjectId
from flask import Flask, request, jsonify
from flask.ext.pymongo import PyMongo
from bson import Binary, Code
from bson.json_util import dumps

# Service resource
s3 = boto3.resource('s3')
# Init flask app
app = Flask(__name__)
# Db client
client = pymongo.MongoClient("localhost", 27017)
db = client.customerad
client = MongoClient(uri)

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
  # for item in db.collection.find_one(sort=[("customer_clicks", -1)]):
  #   customer_clicks = item['customer_clicks']
  #   descriptors = item['descriptors']
  #   acqusition_rate = item['acqusition_rate']
  #   customers_installed = item['customers_installed']
  #   customers_reached = item['customers_reached']
  #   template = item['template']
  #   name = item['name']
  # item = db.collection.find_one(sort=[("customer_clicks", -1)])
  # return jsonify({'id': str(item['_id']), 'template': item['Item']['template']}), 201
  for item in db.collection.find().sort("customer_clicks", pymongo.ASCENDING):
    print str(item)
    print '\n'

  return "", 201

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


@app.route('/categories', methods=['GET'])
def home_page():
    uri = "mongodb://GitHubCrawlerUser:g22LrJvULU5B@mobiledata.bigdatacorp.com.br:21766/MobileAppsData?authMechanism=MONGODB-CR"
    packages = request.args.get("packages");
    packages = packages.split(",")

    #Create google play link for each package
    for i in range(0, len(packages)):
        packages[i] = 'https://play.google.com/store/apps/details?id=' + packages[i]

    if len(packages) > 0:
        # Grab categories for each google play link
        apps = client.MobileAppsData.PlayStore_2016_04.find({ "Url": { "$in": packages } }, {"Category": 1})[0:]

        return dumps(apps);
    else:
        return []

if __name__ == '__main__':
    app.run(debug=True)