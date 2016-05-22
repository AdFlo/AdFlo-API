from flask import Flask, request
from flask.ext.pymongo import PyMongo
from pymongo import MongoClient
from bson import Binary, Code
from bson.json_util import dumps

app = Flask(__name__)
mongo = PyMongo(app)

uri = "mongodb://GitHubCrawlerUser:g22LrJvULU5B@mobiledata.bigdatacorp.com.br:21766/MobileAppsData?authMechanism=MONGODB-CR"
client = MongoClient(uri)

@app.route('/categories', methods=['GET'])
def home_page():
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
    app.debug = True
    app.run()
