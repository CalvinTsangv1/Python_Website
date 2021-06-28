import boto3, botocore
from flask import Flask 
import os
from werkzeug.utils import secure_filename
from config import S3_KEY, S3_SECRET, S3_BUCKET

s3 = boto3.client(
   "s3",
   aws_access_key_id=S3_KEY,
   aws_secret_access_key=S3_SECRET
)