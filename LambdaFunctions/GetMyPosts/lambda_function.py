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
    filtering_exp = Attr('UserId').eq(event['userid'])
    projection_exp='PostId, #ts, ImgUrl, LikeCount, Note, ThumbUrl, Width, Height'
    attrname_exp = { '#ts': 'Timestamp' }
    data = get_items("Post",filtering_exp,projection_exp,attrname_exp)
    posts = data['Items']
    if len(posts) >= event['limit']:
        posts=posts[:event['limit']]
        posts.sort(key=convert, reverse=True)

    response=getResultMultiple(posts)
    return response

def convert(post):
    return post['Timestamp']

def get_items(table_name, filterExpr, projExpr, attrname_exp):
    table = dynamodb_resource.Table(table_name)
    data = table.scan(FilterExpression=filterExpr,ProjectionExpression=projExpr,ExpressionAttributeNames=attrname_exp)
    return data
