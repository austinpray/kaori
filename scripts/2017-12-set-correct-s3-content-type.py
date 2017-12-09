from kizuna_web.extentions import aws_client
import config
from kizuna_web.utils import image_path_to_content_type

res = aws_client.list_objects_v2(Bucket=config.S3_BUCKET)

for image in res['Contents']:
    key = image['Key']
    content_type = image_path_to_content_type(key) # get correct content type for image
    storage_class = 'REDUCED_REDUNDANCY'  # go ahead and set images as reduced redundancy for cheaper storage
    aws_client.copy_object(Bucket=config.S3_BUCKET,
                           CopySource="{}/{}".format(config.S3_BUCKET, key),
                           Key=key,
                           ACL='public-read',
                           MetadataDirective='REPLACE',
                           ContentType=content_type,
                           StorageClass=storage_class)
