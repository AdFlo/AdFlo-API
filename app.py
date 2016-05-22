import itertools
import operator
import boto3
from flask import Flask
from flask.ext.restful import Api, Resource

# Service resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CustomerAd')
# Init flask app
app = Flask(__name__)
api = Api(app)


if __name__ == '__main__':
    app.run(debug=True)