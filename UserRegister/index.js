var formatter = require('resultFormatter.js');
var uuid = require('uuid');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'User';

exports.handler = (event, context, callback) => {
    var params = {
        TableName: table,
        Item: {
            "UserId": event.uid,
            "Password": event.pwd,
            "Email": event.email
        }
    };

    docClient.put(params, function(err, data) {
        if (err) {
            callback(null, formatter.getReultError("Unable to insert item. " + err));
        } else {
            var obj = {
                Item: params.Item
            };
            callback(null, formatter.getResultSingle(obj));
        }
    });
};
