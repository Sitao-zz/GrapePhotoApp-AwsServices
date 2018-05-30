from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import json
import boto3
import decimal
import time
import calendar
from resultFormatter import getResultSingle, getResultMultiple, getResultError

dynamodb_resource = resource('dynamodb')

def lambda_handler(event, context):
    data = get_items("User_Likes_Rank_Analysis")
    users=data['Items']
    users.sort(key=convert, reverse=False)
    if len(users) >= event['limit']:
        users=users[:event['limit']]
    response=getResultMultiple(users)
    return response

def get_items(table_name):
    table = dynamodb_resource.Table(table_name)
    data = table.scan()
    return data

def convert(user):
    return user['Rank']
