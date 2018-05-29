# DashboardService: calculate the posts included in each tag

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
    projection_exp2='ImgUrl'
    data2 = get_items("Post",projection_exp2)
    items2=data2['Items']

    result = {}
    for item in items1:
        # create tag for classification
        if not result.has_key(item["Tag"]):
            result[item["Tag"]]={}
            result[item["Tag"]]["Tag"]=item["Tag"]
            result[item["Tag"]]["Rank"]=0
            result[item["Tag"]]["Posts"]=0

        # Update the total post count
        for x in items2:
            if x["ImgUrl"].find(item["ImageName"]) >= 0:
                if result[item["Tag"]].has_key("Posts"):
                    result[item["Tag"]]["Posts"]+=1
                else:
                    result[item["Tag"]]["Posts"]=1

    # caculate the rank of each tags
    index = 1
    for key, value in sorted(result.iteritems(), key=lambda (k,v): (-v["Posts"],k)):
        value["Rank"]=index
        index+=1

    # save the ranked records to database
    selected=[]
    for record in result.values():
        if record["Rank"]<11:
            put_item("Tag_Posts_Rank_Analysis", record)
            selected.append(record)
    return result

def get_items(table_name, projExpr):
    table = dynamodb_resource.Table(table_name)
    data = table.scan(ProjectionExpression=projExpr)
    return data

def put_item(table_name, item):
    table = dynamodb_resource.Table(table_name)
    table.put_item(Item=item)
    return
