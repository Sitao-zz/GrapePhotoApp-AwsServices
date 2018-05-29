var formatter = require('resultFormatter.js');
var uuid = require('uuid');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'Post';

exports.handler = (event, context, callback) => {
    var params = {
        TableName: table,
        Item: {
            "PostId": uuid.v1(),
            "LikeCount": 0,
            "Note": event.note,
            "Timestamp": new Date().toISOString(),
            "ImgUrl": event.imgurl,
            "ThumbUrl": event.thumburl,
            "UserId": event.userid
        }
    };

    docClient.put(params, function(err, data) {
        if (err) {
            callback(null, formatter.getResultError("Unable to insert item. " + err));
        } else {
            var obj = {
                Item: params.Item
            };
            callback(null, formatter.getResultMultiple(obj['Item']));
        }
    });
};
