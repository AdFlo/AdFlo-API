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
customerad = client.customerad
profilemodel = client.profile

@app.route('/ad', methods=['POST'])
def ad():
  body = request.form
  name = body['name']
  acqusition_rate = body['acqusition_rate']
  template = body['template']
  descriptors = body['descriptors']

  response = customerad.collection.insert_one({
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

  return json.dumps({'success':True, 'id': str(response.inserted_id)}), 201, {'ContentType':'application/json'} 

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

  for item in customerad.collection.find().sort("customer_clicks", pymongo.ASCENDING):
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
  userid = body['userid']
  _id = id

  customerad_res = customerad.collection.update({
    '_id': ObjectId(_id)
  }, {
    '$inc': {
      'Item.customer_clicks': 1
    }
  })

  aa = profilemodel.collection.find({
    '_id': ObjectId(userid)
  })

  try:
    items = aa[0]['ads_served']
    for k in items:
      if k['uuid'] == _id:
        dyn = profilemodel.collection.update({ "ads_served": { "$elemMatch": {"uuid": _id }}}, {"$inc": {
          "ads_served.$.times_clicked": 1
        }})
        break
  except:
    profile_res = profilemodel.collection.update({
      '_id': ObjectId(userid)
    }, {
      "$addToSet": {
        "ads_served": {
          "uuid": _id,
          "times_clicked": 1,
          "excluded": False
        }
      }
    })

  return jsonify({"success": True}), 200

@app.route('/profile', methods=['POST'])
def profile():
  body = request.form

  response = profilemodel.collection.insert_one({
    "TableName": "profile",
    "Item": {
      "ads_served": []
    }
  })

  return json.dumps({'id': str(response.inserted_id)}), 201, {'ContentType':'application/json'} 

@app.route('/categories', methods=['GET'])
def getCategories():
    packages = request.aargs.get("packages");
    packages = packages.split(",")

    #Create google play link for each package
    for i in range(0, len(packages)):
        packages[i] = 'https://play.google.com/store/apps/details?id=' + packages[i]

    if len(packages) > 0:
        # Grab categories for each google play link
        apps = crawlerClient.MobileAppsData.PlayStore_2016_04.find({ "Url": { "$in": packages } }, {"Category": 1})[0:]

        return dumps(apps);
    else:
        return []

if __name__ == '__main__':
    app.run(debug=True)

      #       "uuid": str(uuid.uuid4()),
      #   "template": template,
      #   "times_clicked": 0,
      #   "exlcluded": False
      # ]