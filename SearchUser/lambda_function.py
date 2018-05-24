from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr

dynamodb_resource = resource('dynamodb')

def lambda_handler(event, context):
    try:
        response = scan_table("User","UserName",event['username'])
    except Exception, e:
        print(e)
        raise e
    return response

def scan_table(table_name, filter_key=None, filter_value=None):
    table = dynamodb_resource.Table(table_name)
    if filter_key and filter_value:
        filtering_exp = Attr(filter_key).eq(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()
    return response
