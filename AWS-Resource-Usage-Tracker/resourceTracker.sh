#!/bin/bash

##########################
# Author: Pooja
# Date: 08/08/2025
# Version: v1
#
# Description:
# This script will generate a daily AWS resource usage report
# including EC2, S3, Lambda, and IAM information.
##########################

set -x  # Enables debug mode - prints commands before executing

# Define output file
OUTPUT_FILE="resourceTracker"

# Add timestamp
echo "########## AWS Resource Report - $(date) ##########" >> $OUTPUT_FILE

# Print list of S3 buckets
echo -e "\n List of S3 Buckets:" >> $OUTPUT_FILE
aws s3 ls >> $OUTPUT_FILE

# Print list of EC2 instances
echo -e "\n List of EC2 Instances:" >> $OUTPUT_FILE
aws ec2 describe-instances | jq '.Reservations[].Instances[] | {InstanceId, InstanceType, State: .State.Name, LaunchTime}' >> $OUTPUT_FILE

# Print list of Lambda functions
echo -e "\n List of Lambda Functions:" >> $OUTPUT_FILE
aws lambda list-functions | jq '.Functions[] | {FunctionName, Runtime, LastModified}' >> $OUTPUT_FILE

# Print list of IAM users
echo -e "\n List of IAM Users:" >> $OUTPUT_FILE
aws iam list-users | jq '.Users[] | {UserName, CreateDate}' >> $OUTPUT_FILE

echo -e "\n AWS Resource Tracking Complete.\n" >> $OUTPUT_FILE