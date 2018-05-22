var formatter = require('resultFormatter.js');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'User';

exports.handler = (event, context, callback) => {
    var params = {
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

    docClient.get(params, function(err, data) {
        if (err) {
            callback(null, formatter.getReultError("Unable to update item. " + err));
        } else {
            if(typeof data.Item == 'undefined') {
                callback(null, formatter.getReultError("Item does not exist."));
            } else {
                updateItem(params, callback);
            }
        }
    });
};

function updateItem(params, callback) {
    docClient.update(params, function(err, data) {
        if (err) {
            callback(null, formatter.getReultError("Unable to update item. " + err));
        } else {
            callback(null, formatter.getResultSingle(""));
        }
    });
}
