var formatter = require('resultFormatter.js');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'Post';

exports.handler = (event, context, callback) => {
    getPost(event, getUserLike, callback);
};

function getPost(event, nextcall, callback) {
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

    docClient.scan(params, function (err, data) {
        if (err) {
            callback(null, formatter.getResultError("Unable to read item. " + err));
        } else {
            if(data.Count > 0){
                nextcall(event, data.Items[0], callback);
            } else {
                callback(null, formatter.getResultError("Post is not found."));
            }
        }
    });
}

function getUserLike(event, post, callback) {
    var params = {
        TableName: 'UserLike',
        ProjectionExpression: "Id",
        FilterExpression: "PostId = :postid and UserId = :userid",
        ExpressionAttributeValues: {
             ":postid": event.postid,
             ":userid": event.userid
        },
        ScanIndexForward: false
    };

    docClient.scan(params, function (err, data) {
        if (err) {
            callback(null, formatter.getResultError("Unable to read UserLike item. " + err));
        } else {
            let result = {
                "Post": post,
                "Liked": 0
            };
            if (data.Count > 0) {
                result.Liked = 1;
            }
            callback(null, formatter.getResultSingle(result));
        }
    });
}
