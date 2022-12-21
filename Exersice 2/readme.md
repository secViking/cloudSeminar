Exercise 2

Links:
Site Link: https://nxoai43bln5zgfgc72jkvtta64.apigateway.il-jerusalem-1.oci.customer-oci.com/

getUserInput function Link: https://aqnio4nprc6ge6kqabg4ogo2vy.apigateway.il-jerusalem-1.oci.customer-oci.com/


In this exercise I created 2 new functions:

	newSite - same as exercise one with the new functionality of submitting user input

	getUserInput - getting the user input and inserting it into a txt file in the bucket.

The new site submits the user input by calling the getUserInput function endpoint.

I have created two new gateways, one for each new function, and configured the CORS to allow all origins and methods in order to allow access to the getUserInput function between the two different gateways.

Note: I have created two different gateways because I got an error(“Deployment corresponding to specified pathPrefix already exists”) when I tried to create a new deployment in the same gateway while using a different pathPrefix.


