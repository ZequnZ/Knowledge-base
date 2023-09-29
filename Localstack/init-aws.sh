#!/usr/bin/env bash

set -euo pipefail

# Create s3 bucket
awslocal s3 mb s3://my-bucket --region us-west-2
# Copy files into bucket 
awslocal s3 cp /device_dir/mock_s3 s3://my-bucket/mock_s3/ --recursive
