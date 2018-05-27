// Lambda services deployed to AWS service
Lambda

************************
***** Post Service *****
************************

/post/add
input: post
- save URL to DB

/post/full
input: postid, userid
- get the full image
- get the image tag
- get the like counts
- get whether he/she has liked the post

/post/recent
input: limit
- retrieve the all recent images (thumbnail) urls within the limit count

/post/feeds
input: userid
- retrieve the recent images (thumbnail) urls by the followees

/post/like
input: userid, postid, like
- add record of like
- retrieve the like counts

#Image analyser#
- analyse the image and create tag save to DB

************************
***** User Service *****
************************

/user/register
input: userid, username, pwd, email
- save user particular (userId, email, password, phoneId)

/user/login
input: userid, pwd
- authentication
- call #Image Retieval#

/user/update
input: userid, username, pwd, email
- update user record

/user/search
input: username, number, email or something
- search the users according to criteria
- return the user list

/user/follow
input: follower, followee, follow
- update DB

/user/followees
input: userid
- get list of followees

********************************
***** Notification Service *****
********************************

#Notification#
input: image, uploader
- retrieve the subscribers of the user and send notification
