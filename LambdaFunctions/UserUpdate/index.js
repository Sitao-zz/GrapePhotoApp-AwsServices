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
    let attr = {};
    console.log(event.pwd);
    if (event.pwd) {
        if(expr == "")  { expr += "set "; }
        else { expr += ", "; }
        expr += "Password=:p";
        attr[":p"]=event.pwd;
    }
    if (event.email) {
        if(expr == "")  { expr += "set "; }
        else { expr += ", "; }
        expr += "Email=:e";
        attr[":e"]=event.email;
    }
    if (event.username) {
        if(expr == "")  { expr += "set "; }
        else { expr += ", "; }
        expr += "UserName=:n";
        attr[":n"]=event.username;
    }
    let params = {
      TableName:table,
      Key:{
          "UserId": event.userid
      },
      UpdateExpression: expr,
      ExpressionAttributeValues: attr,
      ReturnValues:"UPDATED_NEW"
    };
    docClient.update(params, function(err, data) {
        if (err) {
            callback(null, formatter.getResultError("Unable to update item. " + err));
        } else {
            callback(null, formatter.getResultMultiple([]));
        }
    });
}
