var formatter = require('resultFormatter.js');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'Post';

var scan_callback = null;
var scan_event = null;
var scan_data = null;
var scan_params = null;

exports.handler = (event, context, callback) => {
    getPosts(event, callback)
};

function getPosts(event, callback) {
    var params = {
        TableName: table,
        ProjectionExpression: "PostId, #ts, ImgUrl, LikeCount, Note, UserId",
        ExpressionAttributeNames: {
            "#ts": "Timestamp",
        },
        Limit: event.limit,
        ScanIndexForward: false
    };

    scan_params = params;
    scan_callback = callback;
    scan_event = event;
    scan_data = [];
    docClient.scan(params, onScan);
}

function onScan(err, data) {
    if (err) {
        scan_callback(null, formatter.getResultError("Unable to read item. " + err));
    } else {
        data.Items.forEach(function(post) {
            scan_data.push(post);
            if(scan_data.length >= scan_event.limit) {
                scan_callback(null, formatter.getResultMultiple(scan_data));
                return;
            }
        });

        // continue scanning if we have more posts, because
        // scan can retrieve a maximum of 1MB of data
        if (typeof data.LastEvaluatedKey != "undefined") {
            console.log("Scanning for more...");
            scan_params.ExclusiveStartKey = data.LastEvaluatedKey;
            docClient.scan(scan_params, onScan);
        } else {
            scan_callback(null, formatter.getResultMultiple(scan_data));
            return;
        }
    }
}
