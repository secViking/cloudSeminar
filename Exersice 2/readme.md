Exercise 2

Links:
Site Link: https://nxoai43bln5zgfgc72jkvtta64.apigateway.il-jerusalem-1.oci.customer-oci.com/

In this exercise I enhance the previous site to handle user data.
The application have one function the handle GET and POST requests.

GET - access to site by getting index.html file from object storage.
POST - can be use to perform 3 methos: update, create delete.

The application demonstarte a simple use case of users form/landing page submission.
The possible actions:

CREATE - When the user submits data - If it is the first time we see this email, a file in the bucket will be created with the email hash as a file name.

UPDATE - When the user submits data with already used email - the file content will be updated with the new one.

DELETE - IF a user wishes to delete his data - the file will be deleted from the bucket.






