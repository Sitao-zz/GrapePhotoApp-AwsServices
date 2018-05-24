var formatter = require('resultFormatter.js');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'Post';

var scan_callback = null;
var scan_event = null;

exports.handler = (event, context, callback) => {
    var params = {
        TableName: table,
        Key:{
            "PostId": event.postid
        }
    };

    var params = {
        TableName: table,
        ProjectionExpression: "PostId, #ts, ImgUrl, LikeCount, Note, UserId",
        FilterExpression: "PostId = :postid",
        ExpressionAttributeNames: {
            "#ts": "Timestamp",
        },
        ExpressionAttributeValues: {
             ":postid": event.postid
        },
        ScanIndexForward: false
    };

    scan_callback = callback;
    scan_event = event;
    docClient.scan(params, onScan);
};

function onScan(err, data) {
    if (err) {
        scan_callback(null, formatter.getResultError("Unable to read item. " + err));
    } else {
        data.Items.forEach(function(post) {
           scan_callback(null, formatter.getResultSingle(post));
           return;
        });

        scan_callback(null, formatter.getResultError("Post is not found."));
    }
}
