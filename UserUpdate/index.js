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

    docClient.update(params, function(err, data) {
        if (err) {
            callback(null, formatter.getReultError("Unable to update item. " + err));
        } else {
            var obj = {
                Item: params.Item
            };
            callback(null, formatter.getResultSingle(obj));
        }
    });
};
