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
    posts = getPostsByUserId(event['userid'], event['limit'])
    posts = updatePostLikesAttr(posts, event['userid'])
    response=getResultMultiple(posts)
    return response

def convert(post):
    return post['Timestamp']

def getPostsByUserId(userid, limit):
    filtering_exp = Attr('UserId').eq(userid)
    data = get_items("Post",filtering_exp)
    posts = data['Items']
    if len(posts) >= limit:
        posts=posts[:limit]
        posts.sort(key=convert, reverse=True)
    return posts

def updatePostLikesAttr(posts, userid):
    for post in posts:
        filtering_exp = Attr('UserId').eq(userid)
        filtering_exp &= Attr('PostId').eq(post['PostId'])
        data = get_items('UserLike',filtering_exp)
        if data['Count']>0:
            post['Liked']=1
        else:
            post['Liked']=0
    return posts

def get_items(table_name, filterExpr):
    table = dynamodb_resource.Table(table_name)
    data = table.scan(FilterExpression=filterExpr)
    return data
