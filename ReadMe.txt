// Lambda services deployed to AWS service
Lambda

************************
***** Post Service *****
************************

#AddPost#
input: image
- create thumbnail
- store image in S3
- save URL to DB

#GetPost#
input: postid, userid
- get the full image
x- get the image tag
- get the like counts
x- get whether he/she has liked the post

#GetRecentPosts#
input: limit
- retrieve the all recent images (thumbnail) urls within the limit count

#LikePost#
- add record of like
- retrieve the like counts

#Image analyser#
- analyse the image and create tag save to DB

************************
***** User Service *****
************************

#Register user#
- save user particular (userId, email, password, phoneId)

#Login user#
- authentication
- call #Image Retieval#

#Search users#
input: user id, phone, number, email or something
- search the users according to criteria
- return the user list

#Follow users#
- update DB

********************************
***** Notification Service *****
********************************

#Notification#
input: image, uploader
- retrieve the subscribers of the user and send notification
