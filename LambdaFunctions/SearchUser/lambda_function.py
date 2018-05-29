from boto3 import resource
from boto3.dynamodb.conditions import Key, Attr
from resultFormatter import getResultSingle, getResultMultiple, getResultError

dynamodb_resource = resource('dynamodb')

def lambda_handler(event, context):
    try:
        if(len(event['value'])) <= 1:
            response = getResultError("Search value must be more than 3 characters")
            return response

        if(event['key'] == 'Password'):
            response = getResultMultiple([])
            return response

        data = scan_table("User",event['key'],event['value'])
        result = extractInfo(data['Items'])
        response = getResultMultiple(result)
    except Exception, e:
        response = getResultError(str(e))
    return response

def scan_table(table_name, filter_key=None, filter_value=None):
    table = dynamodb_resource.Table(table_name)
    if filter_key and filter_value:
        filtering_exp = Attr(filter_key).contains(filter_value)
        response = table.scan(FilterExpression=filtering_exp)
    else:
        response = table.scan()
    return response

def extractInfo(users):
    list = []
    for user in users:
        item = {
            "UserId": user['UserId'],
            "UserName": user['UserName'],
            "Email": user['Email']
        }
        list.append(item)
    return list
