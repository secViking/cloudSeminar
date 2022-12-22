import io
import json
import logging
import oci
import hashlib

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
        file_object_name = ctx.RequestURL()
        if file_object_name.endswith("/"):
            logging.getLogger().info("Adding index.html to reques URL " + file_object_name)
            file_object_name += "indexNew2.html"

        # strip off the first character of the URI (i.e. the /)
        file_object_name = file_object_name[1:]

        obj = object_storage.get_object(namespace, bucket_name, file_object_name)


        if ctx.Method() == "GET":
            return response.Response(
                ctx, response_data=obj.data.content,
                headers={"Content-Type": obj.headers['Content-type']}
        )

        if ctx.Method() == "POST":
            
            objectList = object_storage.list_objects(namespace,bucket_name)
            objects = objectList.data.objects
            body = json.loads(data.getvalue())
            email = body["email"]
            name = body["name"]
            description = body["description"]
            delete = body["delete"]
            file_name_hash = hashlib.md5(email.encode())
            file_name = str(file_name_hash.hexdigest())
            file_name += '.txt'
            contents = email + "\n" + name + "\n" + description

            #check if file already created - means that email already registered            
            for x in objects:
                if x.name == file_name:
                    #delte file if it was requested by the user
                    if delete == True:
                        delete_object_res = object_storage.delete_object(namespace,bucket_name,file_name)
                        return response.Response(ctx, response_data="file found and deleted",headers={"Content-Type": obj.headers['Content-type']})
                    #update file content                    
                    else:
                        put_object_res = object_storage.put_object(namespace, bucket_name, file_name, contents)
                        return response.Response(ctx, response_data="file found and updated",headers={"Content-Type": obj.headers['Content-type']})
            #file doesn't exist creating new file
            put_object_res = object_storage.put_object(namespace, bucket_name, file_name, contents)
            return response.Response(ctx, response_data="file not found and created",headers={"Content-Type": obj.headers['Content-type']})
          
    except (Exception) as e:
        return response.Response(
            ctx, response_data="500 Server error",
            headers={"Content-Type": "text/plain"}
            )