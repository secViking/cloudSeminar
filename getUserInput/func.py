import io
import json
import logging
import oci

from fdk import response


def handler(ctx, data: io.BytesIO = None):
    if None == ctx.RequestURL():
        return "Function loaded properly but not invoked via an HTTP request."
    signer = oci.auth.signers.get_resource_principals_signer()
    logging.getLogger().info("URI: " + ctx.RequestURL() )
    config = {
        # update with your tenancy's OCID
        "tenancy": "ocid1.tenancy.oc1..aaaaaaaat3g6mubuxwcl26ef5tve3gpoz3bnrueskq7ma2fyjlk3jiiinxea",
        # replace with the region you are using
        "region": "il-jerusalem-1"
    }
    
    try:
        object_storage = oci.object_storage.ObjectStorageClient(config, signer=signer)
        namespace = object_storage.get_namespace().data
        # update with your bucket name
        bucket_name = "nivWebappBucket"
        file_name = "data.txt"

        body = json.loads(data.getvalue())
        input_value = body.get("input")
                #object_storage.append_object(namespace, bucket_name, file_name, input_value)
        get_object_response = object_storage.get_object(namespace, bucket_name, file_name)
        contents = get_object_response.data.content.decode()

        # Append the new data to the contents
        contents += '\n'+input_value

        # Write the updated contents back to the file in Oracle Cloud
        object_storage.put_object(namespace, bucket_name, file_name, contents)

    except (Exception, ValueError) as ex:
        logging.getLogger().info('error parsing json payload: ' + str(ex))

    logging.getLogger().info("Inside Python Hello World function")
    return response.Response(
        ctx, response_data=json.dumps(
            {"message": "Succesfuuly added data to file"}),
        headers={"Content-Type": "application/json"}
    )
