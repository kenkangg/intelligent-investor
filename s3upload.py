import boto3


def uploadToS3(filename):
    """ Uploads given csv file to AWS S3 database """
    # Create an S3 client
    s3 = boto3.client('s3')

    bucket_name = 'cryptoexchangedata'

    # Uploads the given file using a managed uploader, which will split up large
    # files automatically and upload parts in parallel.
    s3.upload_file(filename, bucket_name, filename)
