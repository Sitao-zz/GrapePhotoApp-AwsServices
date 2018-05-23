var formatter = require('resultFormatter.js');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'User';

exports.handler = (event, context, callback) => {
    let params = {
        TableName:table,
        ProjectionExpression:"UserId, UserName, Email, Password",
        KeyConditionExpression: "UserId = :userid",
        ExpressionAttributeValues: {
            ":userid":event.userid
        }
    };
    docClient.query(params, function(err, data) {
        if (err) {
            callback(null, formatter.getResultError("Unable to read item. " + err));
        } else {
            if(data.Count > 0) {
                if (data.Items[0].Password == event.pwd) {
                    let result = {
                        "UserId": data.Items[0].UserId,
                        "UserName": data.Items[0].UserName,
                        "Email": data.Items[0].Email
                    }
                    callback(null, formatter.getResultSingle(result));
                } else {
                    callback(null, formatter.getResultError("Password is not correct."));
                }
            } else {
                callback(null, formatter.getResultError("User does not exist."));
            }
        }
    });
};
