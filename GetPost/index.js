var formatter = require('resultFormatter.js');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'Post';

exports.handler = (event, context, callback) => {
    var params = {
        TableName: table,
        Key:{
            "PostId": event.postid
        }
    };

    docClient.get(params, function(err, data) {
        if (err) {
            callback(null, formatter.getResultError("Unable to read item. " + err));
        } else {
            callback(null, formatter.getResultSingle(data));
            //callback(null, JSON.stringify(data, null, 2));
        }
    });
};
