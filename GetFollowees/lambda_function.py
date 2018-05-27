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
    filtering_exp = Attr('Follower').eq(event['userid'])
    data = get_items("Follow",filtering_exp)
    response=getResultMultiple(data['Items'])
    return response

def get_items(table_name, expr):
    table = dynamodb_resource.Table(table_name)
    data = table.scan(FilterExpression=expr)
    return data
