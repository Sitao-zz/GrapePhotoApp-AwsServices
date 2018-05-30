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
    data = get_items("User_Likes_Rank_Analysis",None,None)
    ranks=data['Items']
    ranks.sort(key=convert, reverse=False)
    if len(ranks) >= event['limit']:
        ranks=ranks[:event['limit']]
    users=getUsersByRanks(ranks)
    response=getResultMultiple(users)
    return response

def getUsersByRanks(ranks):
    users = []
    for rank in ranks:
        filtering_exp = Attr('UserId').eq(rank['UserId'])
        projection_exp='UserId, Email, UserName'
        data = get_items("User",filtering_exp,projection_exp)
        if data['Count'] > 0:
            users.extend(data['Items'])
    return users

def convert(user):
    return user['Rank']

def get_items(table_name, filterExpr, projExpr):
    table = dynamodb_resource.Table(table_name)
    if filterExpr==None and projExpr==None:
        data = table.scan()
    else:
        data = table.scan(FilterExpression=filterExpr,ProjectionExpression=projExpr)
    return data
