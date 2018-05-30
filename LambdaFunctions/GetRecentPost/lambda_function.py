# PostService_GetRecentPost

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
    posts=getPosts(event['limit'])
    posts=updatePostLikesAttr(posts, event['userid'])
    response=getResultMultiple(posts)
    return response

def getPosts(limit):
    data = get_items("Post",None)
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

def convert(post):
    return post['Timestamp']

def get_items(table_name, expr):
    table = dynamodb_resource.Table(table_name)
    if expr==None:
        data = table.scan()
    else:
        data = table.scan(FilterExpression=expr)
    return data
