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
        if event['like'] == 1:
            addedItem={'Id':uuid.uuid4().hex,'PostId':event['postid'],'UserId':event['userid']}
            result = add_item("UserLike",addedItem)
            if result == True:
                increase1_table_item("Post","PostId",event['postid'])
        else:
            result = delete_item_by_attrs("UserLike","PostId",event['postid'],"UserId",event['userid'])
            if result == True:
                decrease1_table_item("Post","PostId",event['postid'])

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

def increase1_table_item(table_name, pk_name, pk_value):
    table = dynamodb_resource.Table(table_name)

    # retrieve the item to get the sort key
    filtering_exp = Attr(pk_name).eq(pk_value)
    data=table.scan(FilterExpression=filtering_exp)
    sk_value=data['Items'][0]['Timestamp']
    sk_name='Timestamp'

    # update the item using partition key and sort key
    result = table.update_item(
        Key={pk_name: pk_value,sk_name: sk_value},
        UpdateExpression="set LikeCount = LikeCount + :val",
        ExpressionAttributeValues={':val': decimal.Decimal(1)},
        ReturnValues="UPDATED_NEW"
        )
    return result

def decrease1_table_item(table_name, pk_name, pk_value):
    table = dynamodb_resource.Table(table_name)

    # retrieve the item to get the sort key
    filtering_exp = Attr(pk_name).eq(pk_value)
    data=table.scan(FilterExpression=filtering_exp)
    sk_value=data['Items'][0]['Timestamp']
    sk_name='Timestamp'

    # update the item using partition key and sort key
    result = table.update_item(
        Key={pk_name: pk_value,sk_name: sk_value},
        UpdateExpression="set LikeCount = LikeCount - :val",
        ExpressionAttributeValues={':val': decimal.Decimal(1)},
        ReturnValues="UPDATED_NEW"
        )
    return result
