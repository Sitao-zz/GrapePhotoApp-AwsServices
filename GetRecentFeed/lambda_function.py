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
    if data['Count'] > 0:
        posts = []
        for item in data['Items']:
            filtering_exp = Attr('UserId').eq(item['Followee'])
            data_post = get_items("Post",filtering_exp)
            if data_post['Count'] > 0:
                posts.extend(data_post['Items'])
                if len(posts) >= event['limit']:
                    posts=posts[:event['limit']]
                    posts.sort(key=convert, reverse=True)
                    break
        response=getResultMultiple(posts)
    else:
        response=getResultSingle(None)

    return response

def convert(post):
    return calendar.timegm(time.strptime(post['Timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ'))

def get_items(table_name, expr):
    table = dynamodb_resource.Table(table_name)
    data = table.scan(FilterExpression=expr)
    return data
