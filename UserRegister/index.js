var formatter = require('resultFormatter.js');

var AWS = require("aws-sdk");
var docClient = new AWS.DynamoDB.DocumentClient();
var table = 'User';

exports.handler = (event, context, callback) => {
    getItem(event, insertItem, callback);
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
            callback(null, formatter.getReultError("Unable to register user. " + err));
        } else {
            if(typeof data.Item != 'undefined') {
                callback(null, formatter.getReultError("UserId already exists."));
            } else {
                nextcall(event, callback);
            }
        }
    });
}

function insertItem(event, callback) {
    let params = {
        TableName: table,
        Item: {
            "UserId": event.userid,
            "Password": event.pwd,
            "Email": event.email
        }
    };
    docClient.put(params, function(err, data) {
        if (err) {
            callback(null, formatter.getReultError("Unable to insert item. " + err));
        } else {
            callback(null, formatter.getResultSingle(null));
        }
    });
}
