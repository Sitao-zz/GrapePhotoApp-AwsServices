# DashboardService: calculate the likes gained in each tag

from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import json
import boto3
import decimal
import uuid

dynamodb_resource = resource('dynamodb')

def lambda_handler(event, context):
    #Read from ImageTag table
    projection_exp1='ImageName, Tag'
    data1 = get_items("ImageTag",projection_exp1)
    items1=data1['Items']
    #Read from Post table
    projection_exp2='ImgUrl, LikeCount'
    data2 = get_items("Post",projection_exp2)
    items2=data2['Items']

    result = {}
    for item in items1:
        # create tag for classification
        if not result.has_key(item["Tag"]):
            result[item["Tag"]]={}
            result[item["Tag"]]["Tag"]=item["Tag"]
            result[item["Tag"]]["Rank"]=0
        #concat timage
        imagename = 'https://s3.amazonaws.com/image-us-east-1-824831449792/'+item["ImageName"]
        likecount = 0
        for x in items2:
            if imagename == x["ImgUrl"]:
                likecount = x["LikeCount"]

        # Update the total like count
        if not result[item["Tag"]].has_key("Likes"):
            result[item["Tag"]]["Likes"]=likecount
        else:
            result[item["Tag"]]["Likes"]+=likecount

    # caculate the rank of each user
    index = 1
    for key, value in sorted(result.iteritems(), key=lambda (k,v): (-v["Likes"],k)):
        value["Rank"]=index
        index+=1

    # save the ranked records to database
    selected=[]
    for record in result.values():
        if record["Rank"]<11:
            put_item("Tag_Likes_Rank_Analysis", record)
            selected.append(record)
    return selected

def get_items(table_name, projExpr):
    table = dynamodb_resource.Table(table_name)
    data = table.scan(ProjectionExpression=projExpr)
    return data

def put_item(table_name, item):
    table = dynamodb_resource.Table(table_name)
    table.put_item(Item=item)
    return
