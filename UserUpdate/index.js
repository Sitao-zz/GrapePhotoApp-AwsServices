var formatter = require('resultFormatter.js');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'User';

exports.handler = (event, context, callback) => {
    getItem(event, updateItem, callback);
};

function getItem(event, nextcall, callback) {
    let params = {
        TableName:table,
        ProjectionExpression:"UserId",
        KeyConditionExpression: "UserId = :userid",
        ExpressionAttributeValues: {
            ":userid":event.userid
        }
    };
    docClient.query(params, function(err, data) {
        if (err) {
            callback(null, formatter.getResultError("Unable to update User. " + err));
        } else {
            if(data.Count == 0) {
                callback(null, formatter.getResultError("User does not exist."));
            } else {
                nextcall(event, callback);
            }
        }
    });
}

function updateItem(event, callback) {
    let expr = "";
    if (typeof event.pwd != 'undefined') {
        if(expr == "")  { expr += "set "; }
        else { expr += ", "; }
        expr += "Password=:p";
    }
    if (typeof event.email != 'undefined') {
        if(expr == "")  { expr += "set "; }
        else { expr += ", "; }
        expr += "Email=:e";
    }
    if (typeof event.username != 'undefined') {
        if(expr == "")  { expr += "set "; }
        else { expr += ", "; }
        expr += "UserName=:n";
    }
    let params = {
      TableName:table,
      Key:{
          "UserId": event.userid
      },
      UpdateExpression: expr,
      ExpressionAttributeValues:{
          ":p":event.pwd,
          ":e":event.email,
          ":n":event.username
      },
      ReturnValues:"UPDATED_NEW"
    };
    docClient.update(params, function(err, data) {
        if (err) {
            callback(null, formatter.getResultError("Unable to update item. " + err));
        } else {
            callback(null, formatter.getResultSingle(null));
        }
    });
}
