// Lambda services deployed to AWS service
Lambda
#Register user#
- save user particular (userId, email, password, phoneId)

#Login user#
- authentication
- call #Image Retieval#

#Image uploader#
input: image
- create thumbnail
- store image in S3
- save URL to DB

#Image analyser#
- analyse the image and create tag save to DB

#Notification#
input: image, uploader
- retrieve the subscribers of the user and send notification

#Recent Image#
input: user
- get list of followees
- retrieve the recent images thumbnails by the followees
- retrieve the like counts

#Image full access#
input: imageId
- get the full image
- get the image tag
- get the like counts

#Like photo#
- add record of like

#Search users#
input: user id, phone, number, email or something
- search the users according to criteria
- return the user list

#Follow users#
- update DB
