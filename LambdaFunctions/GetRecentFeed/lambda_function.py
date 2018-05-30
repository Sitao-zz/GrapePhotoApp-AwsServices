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
    data=getFolloweesDataByUserId(event['userid'])
    if data['Count'] > 0:
        posts=getPostsByFollowees(data['Items'], event['limit'])
        posts=updatePostLikesAttr(posts, event['userid'])
        response=getResultMultiple(posts)
    else:
        response=getResultMultiple([])

    return response

def getFolloweesDataByUserId(userid):
    filtering_exp = Attr('Follower').eq(userid)
    data = get_items("Follow",filtering_exp)
    return data

def getPostsByFollowees(followees, limit):
    posts = []
    for item in followees:
        filtering_exp = Attr('UserId').eq(item['Followee'])
        data = get_items("Post",filtering_exp)
        if data['Count'] > 0:
            posts.extend(data['Items'])
            posts.sort(key=convert, reverse=True)
            if len(posts) >= limit:
                posts=posts[:limit]
                break
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
    data = table.scan(FilterExpression=expr)
    return data
