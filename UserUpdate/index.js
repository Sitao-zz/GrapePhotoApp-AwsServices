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
      Key:{
          "UserId": event.userid
      }
    };
    docClient.get(params, function(err, data) {
        if (err) {
            callback(null, formatter.getResultError("Unable to update User. " + err));
        } else {
            if(typeof data.Item == 'undefined') {
                callback(null, formatter.getResultError("User does not exist."));
            } else {
                nextcall(event, callback);
            }
        }
    });
}

function updateItem(event, callback) {
    let params = {
      TableName:table,
      Key:{
          "UserId": event.userid
      },
      UpdateExpression: "set Password = :p, Email=:e",
      ExpressionAttributeValues:{
          ":p":event.pwd,
          ":e":event.email
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
