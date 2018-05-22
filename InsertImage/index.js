var formatter = require('resultFormatter.js');
var uuid = require('uuid');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'Photo';

exports.handler = (event, context, callback) => {
    var params = {
        TableName: table,
        Item: {
            "PhotoId": uuid.v4(),
            "LikeCount": 0,
            "Note": event.note,
            "Timestamp": new Date().toISOString(),
            "ImgUrl": event.url,
            "UserId": event.userid
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
