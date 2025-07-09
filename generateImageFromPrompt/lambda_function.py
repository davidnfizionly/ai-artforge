import json
import boto3
import base64
import uuid

# Bedrock client (us-west-2)
bedrock_runtime = boto3.client("bedrock-runtime", region_name="us-west-2")

# S3 client (us-east-1)
s3_client = boto3.client("s3", region_name="us-east-1")
BUCKET_NAME = "ai-artforge-bucket"
MODEL_ID = "amazon.titan-image-generator-v1"

def lambda_handler(event, context):
    try:
        # Extract prompt
        prompt = json.loads(event["body"])["prompt"]

        # Prepare payload for Bedrock
        body = {
            "taskType": "TEXT_IMAGE",
            "textToImageParams": {
                "text": prompt
            },
            "imageGenerationConfig": {
                "numberOfImages": 1,
                "quality": "standard",
                "height": 512,
                "width": 512,
                "cfgScale": 8.0,
                "seed": 0
            }
        }

        # Call Bedrock model
        response = bedrock_runtime.invoke_model(
            modelId=MODEL_ID,
            body=json.dumps(body),
            contentType="application/json",
            accept="application/json"
        )

        # Read response and decode base64 image
        response_body = json.loads(response['body'].read())
        image_data = response_body["images"][0]
        image_bytes = base64.b64decode(image_data)

        # Generate image key in S3
        image_key = f"generated/{uuid.uuid4()}.png"

        # Upload image to S3 (no ACL)
        s3_client.put_object(
            Bucket=BUCKET_NAME,
            Key=image_key,
            Body=image_bytes,
            ContentType="image/png"
        )

        # Public URL
        image_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{image_key}"

        # Return success
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"image_url": image_url})
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "*",
                "Content-Type": "application/json"
            },
            "body": json.dumps({"error": str(e)})
        }
