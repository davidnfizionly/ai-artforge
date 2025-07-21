🖼️ AI ArtForge – Prompt-to-Image Generator via Amazon Bedrock

AI ArtForge is a serverless, fully automated prompt-to-image generator powered by Amazon Bedrock (Stable Diffusion). This project lets users enter a prompt and generates a stunning AI image in seconds — all deployed using CI/CD and hosted on AWS.

───────────────────────────────────────────────

🚀 Live Demo  
🔗 Launch the App (after deploying to S3)

🗂️ Project Type  
AI-Powered Static Web App – Prompt-to-Image Generation using AWS services

🛠️ Technologies Used
• Amazon Bedrock – Image generation via Stable Diffusion  
• AWS Lambda – Backend to call Bedrock API  
• Amazon API Gateway – RESTful API to trigger Lambda  
• Amazon S3 – Static hosting for frontend  
• GitHub Actions – CI/CD pipelines (frontend + Lambda)  
• IAM – Secured role-based access  
• CloudWatch – Logs and monitoring  

✨ Key Features
• Text prompt → HD image generation  
• Seamless S3-hosted UI  
• Real-time Lambda/Bedrock integration  
• CI/CD pipelines with GitHub Actions  

───────────────────────────────────────────────

🧠 Architecture Overview

[ User Browser ]  
       ↓  
[ HTML/JS UI (S3) ]  
       ↓  
[ API Gateway (REST) ]  
       ↓  
[ Lambda (generateImageFromPrompt) ]  
       ↓  
[ Amazon Bedrock (Stable Diffusion) ]  
       ↓  
[ Generated Image URL → Displayed to User ]

───────────────────────────────────────────────

📦 CI/CD Workflows via GitHub Actions

1. UI Deployment (`.github/workflows/deploy-ui.yml`)
```yaml
name: Deploy UI to S3

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Sync UI to S3
        uses: jakejarvis/s3-sync-action@v0.5.1
        with:
          args: --delete
          destination: s3://${{ secrets.AWS_S3_BUCKET }}
        env:
          AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
          AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          AWS_REGION: us-east-1
```

2. Lambda Deployment (`.github/workflows/deploy-lambda.yml`)
```yaml
name: Deploy Lambda Function

on:
  push:
    paths:
      - generateImageFromPrompt/**
      - .github/workflows/deploy-lambda.yml

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3

      - name: Zip Lambda code
        run: |
          cd generateImageFromPrompt
          zip -r function.zip .

      - name: Upload to Lambda
        uses: appleboy/lambda-action@v0.1.8
        with:
          aws_access_key_id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws_secret_access_key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws_region: us-east-1
          function_name: generateImageFromPrompt
          zip_file: generateImageFromPrompt/function.zip
```

───────────────────────────────────────────────

✅ Deployment Steps
• UI built and uploaded to S3 with GitHub Actions  
• Lambda zipped and deployed via GitHub Actions  
• S3 is configured for public static website  
• CloudWatch monitors all executions  

🧪 Troubleshooting Tips
• S3 error? Check bucket permissions  
• Lambda error? Check CloudWatch logs  
• CI/CD fail? Ensure all GitHub secrets exist  

───────────────────────────────────────────────

🧹 AWS Cleanup Guide (Free Tier)

✅ Lambda function (generateImageFromPrompt)  
✅ API Gateway endpoint  
✅ S3 bucket (static site)  
✅ CloudWatch log groups  
✅ IAM roles (if not reused)

───────────────────────────────────────────────

🙌 Acknowledgments  
Built by David Nfizi as part of a real-world AWS Cloud & GenAI Portfolio.