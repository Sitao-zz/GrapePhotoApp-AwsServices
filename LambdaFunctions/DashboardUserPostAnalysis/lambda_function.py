# DashboardService: calculate the user posts statistics

from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import json
import boto3
import decimal
import uuid
from resultFormatter import getResultSingle, getResultMultiple, getResultError

dynamodb_resource = resource('dynamodb')

def lambda_handler(event, context):
    projection_exp='UserId, LikeCount'
    data = get_items("Post",projection_exp)
    items=data['Items']
    result = {}
    for item in items:
        # create user
        if not result.has_key(item["UserId"]):
            result[item["UserId"]]={}

        # Update the post count
        if not result[item["UserId"]].has_key("Posts"):
            result[item["UserId"]]["Posts"]=1
        else:
            result[item["UserId"]]["Posts"]+=1

        # Update the total like count
        if not result[item["UserId"]].has_key("Likes"):
            result[item["UserId"]]["Likes"]=item["LikeCount"]
        else:
            result[item["UserId"]]["Likes"]+=item["LikeCount"]
    return result

def get_items(table_name, projExpr):
    table = dynamodb_resource.Table(table_name)
    data = table.scan(ProjectionExpression=projExpr)
    return data
