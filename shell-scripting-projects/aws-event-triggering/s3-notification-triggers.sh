#!/bin/bash

set -e
set -x

############################################
# USER CONFIGURATION
############################################

AWS_REGION="us-east-1"
BUCKET_NAME="pooja-free-tier-demo-2025"
LAMBDA_NAME="s3-lambda-function"
ROLE_NAME="s3-lambda-sns"
EMAIL_ADDRESS="poojaajithan160701@gmail.com"

############################################
# FETCH AWS ACCOUNT ID
############################################

ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
echo "Using AWS Account ID: $ACCOUNT_ID"

############################################
# CREATE IAM TRUST POLICY
############################################

cat <<EOF > trust-policy.json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "lambda.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

############################################
# CREATE IAM ROLE (idempotent)
############################################

if aws iam get-role --role-name "$ROLE_NAME" >/dev/null 2>&1; then
    echo "IAM Role already exists."
else
    aws iam create-role \
      --role-name "$ROLE_NAME" \
      --assume-role-policy-document file://trust-policy.json

    aws iam attach-role-policy \
      --role-name "$ROLE_NAME" \
      --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

    aws iam attach-role-policy \
      --role-name "$ROLE_NAME" \
      --policy-arn arn:aws:iam::aws:policy/AmazonSNSFullAccess

    echo "Waiting 10 seconds for IAM propagation..."
    sleep 10
fi

ROLE_ARN="arn:aws:iam::$ACCOUNT_ID:role/$ROLE_NAME"

############################################
# CREATE S3 BUCKET (idempotent)
############################################

if aws s3api head-bucket --bucket "$BUCKET_NAME" >/dev/null 2>&1; then
    echo "Bucket already exists."
else
    # us-east-1 CANNOT have location constraint
    aws s3api create-bucket --bucket "$BUCKET_NAME"
fi

aws s3api put-bucket-versioning \
  --bucket "$BUCKET_NAME" \
  --versioning-configuration Status=Enabled

############################################
# ZIP LAMBDA CONTENT
############################################

zip -r function.zip s3-lambda-function

############################################
# CREATE OR UPDATE LAMBDA (idempotent)
############################################

if aws lambda get-function --function-name "$LAMBDA_NAME" >/dev/null 2>&1; then
    echo "Lambda exists → updating code"
    aws lambda update-function-code \
      --function-name "$LAMBDA_NAME" \
      --zip-file fileb://function.zip
else
    echo "Creating Lambda function..."
    aws lambda create-function \
      --function-name "$LAMBDA_NAME" \
      --runtime python3.9 \
      --role "$ROLE_ARN" \
      --handler s3-lambda-function.lambda_function.lambda_handler \
      --memory-size 128 \
      --timeout 30 \
      --zip-file fileb://function.zip
fi

############################################
# ALLOW S3 TO INVOKE LAMBDA (ignore duplicates)
############################################

aws lambda add-permission \
  --function-name "$LAMBDA_NAME" \
  --statement-id allowS3Invoke \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::$BUCKET_NAME || true

############################################
# CONFIGURE S3 EVENT NOTIFICATIONS
############################################

LAMBDA_ARN="arn:aws:lambda:$AWS_REGION:$ACCOUNT_ID:function:$LAMBDA_NAME"

aws s3api put-bucket-notification-configuration \
  --bucket "$BUCKET_NAME" \
  --notification-configuration "{
    \"LambdaFunctionConfigurations\": [{
      \"LambdaFunctionArn\": \"$LAMBDA_ARN\",
      \"Events\": [\"s3:ObjectCreated:*\"]

    }]
  }"

############################################
# CREATE SNS TOPIC (idempotent)
############################################

TOPIC_ARN=$(aws sns create-topic --name s3-lambda-sns --query "TopicArn" --output text)
echo "SNS Topic ARN: $TOPIC_ARN"

############################################
# SUBSCRIBE EMAIL (SNS IGNOres duplicates)
############################################

aws sns subscribe \
    --topic-arn "$TOPIC_ARN" \
    --protocol email \
    --notification-endpoint "$EMAIL_ADDRESS" || true

############################################
# SEND TEST MESSAGE
############################################

aws sns publish \
  --topic-arn "$TOPIC_ARN" \
  --subject "SNS Test Message" \
  --message "SNS Topic + Lambda setup completed!"

echo "SETUP COMPLETE — Check your email to confirm SNS subscription!"