from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
import json
import boto3
import decimal
import uuid
from resultFormatter import getResultSingle, getResultMultiple, getResultError

dynamodb_resource = resource('dynamodb')

def lambda_handler(event, context):
    try:
        if event['follow'] == 1:
            addedItem={'Id':uuid.uuid4().hex,'Follower':event['follower'],'Followee':event['followee']}
            result = add_item("Follow",addedItem)
        else:
            result = delete_item_by_attrs("Follow","Follower",event['follower'],"Followee",event['followee'])

        response=getResultSingle(None)
    except Exception, e:
        print(e)
        raise e
    return response

def add_item(table_name, col_dict):
    table = dynamodb_resource.Table(table_name)
    result = table.put_item(Item=col_dict)
    return True

def delete_item(table_name, pk_name, pk_value):
    table = dynamodb_resource.Table(table_name)
    result = table.delete_item(Key={pk_name: pk_value})
    return True

def delete_item_by_attrs(table_name, attr1, value1, attr2, value2):
    # retrieve the item to get the id
    table = dynamodb_resource.Table(table_name)
    filtering_exp1 = Attr(attr1).eq(value1)
    filtering_exp2 = Attr(attr2).eq(value2)
    data = table.scan(FilterExpression=filtering_exp1 & filtering_exp2)
    if data['Count'] <= 0:
        return False

    pk_value=data['Items'][0]['Id']
    pk_name='Id'

    # delete the item using id
    result = delete_item(table_name,pk_name,pk_value)
    return True
