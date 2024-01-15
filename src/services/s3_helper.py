import boto3,os
import json,logging 
from config.config import S3_EMBEDDINGS_PATH,S3_SAVE_INPUT_BUCKET,S3_BUCKET_NAME

s3_client = boto3.client('s3',region_name="ap-south-1")
s3_read_resource = boto3.resource('s3')




def convert_s3_url(file_name):
    url = s3_client.generate_presigned_url('get_object',
                                           Params = {'Bucket':S3_BUCKET_NAME,'Key':S3_SAVE_INPUT_BUCKET+file_name},
                                           ExpiresIn = 3600)
    
    return url
    

def put_presigned_url(file_name):
    url = s3_client.generate_presigned_url(ClientMethod = 'put_object',
    Params = {'Bucket':S3_BUCKET_NAME, 'Key':S3_SAVE_INPUT_BUCKET+file_name+".pdf"},
    ExpiresIn = 3600)
    
    return url


def upload_file_object(filename):
    response = s3_client.put_object(
        Bucket = S3_BUCKET_NAME,
        key = S3_SAVE_INPUT_BUCKET+filename,
        Body = filename,
    )

    return "Success"

def fetch_from_s3(filename,key):
    print("filename",filename, "\nkey",key)
    print("BNNBJHBJHBNJNBNMMNB",key+filename)
    response = s3_client.get_object(Bucket=S3_BUCKET_NAME, Key = key+filename)
    
    


    return response 





def local_to_s3(local_folder_path,):



    # Specify the local folder path to upload
    local_folder_path = local_folder_path  # Replace with the path to your local folder

    # Specify the S3 bucket name and folder (prefix) in S3
    bucket_name = S3_BUCKET_NAME
    s3_folder = S3_EMBEDDINGS_PATH  # If you want to upload the folder into a specific folder in the bucket

    # Walk through the local folder and upload files to S3
    for root, dirs, files in os.walk(local_folder_path):
        for file in files:
            local_file_path = os.path.join(root, file)
            s3_object_key = s3_folder + os.path.relpath(local_file_path, local_folder_path)
            
            # Upload the file to S3
            s3_client.upload_file(local_file_path, bucket_name, s3_object_key)

    print(f"Folder '{local_folder_path}' uploaded to s3://{bucket_name}/{s3_folder}")
