Prompt-to-Image Generator via Amazon Bedrock

A modern AI-powered application that transforms user-written prompts into stunning images using Amazon Bedrock (Stable Diffusion). This project demonstrates a serverless, event-driven architecture deployed via GitHub Actions with seamless CI/CD, secure secret management, and responsive static hosting on Amazon S3.

Launch the App

(May take a few seconds to load depending on Bedrock responsiveness)

Project Type

AI-Powered Static Web App – Serverless prompt-to-image generation using AWS services

Technologies Used

- Amazon Bedrock (Stable Diffusion) – Text-to-image generation  
- AWS Lambda – Backend logic to call Bedrock  
- Amazon API Gateway – Public REST API for frontend-backend communication  
- Amazon S3 – Hosting the static frontend (HTML/CSS/JS)  
- GitHub Actions – CI/CD deployment for both frontend and Lambda  
- IAM – Secured role-based access between services  
- AWS CloudWatch – Logging and monitoring of Lambda executions  

Key Features

- Text prompt input from the user  
- Image generation via Bedrock’s Stable Diffusion model  
- Real-time result displayed on frontend (HTML/CSS)  
- Fully serverless and scalable architecture  
- Automatic deployment pipeline via GitHub Actions  

Architecture Overview

[ User Browser ]  
       ↓  
[ HTML/JS UI (S3) ]  
       ↓  
[ API Gateway (REST) ]  
       ↓  
[ Lambda Function (generateImageFromPrompt) ]  
       ↓  
[ Amazon Bedrock (Stable Diffusion) ]  
       ↓  
[ Generated Image URL → Displayed to User ]

Deployment Flow (CI/CD)

Frontend (artforge):  
- On push to main, the UI is automatically synced to the S3 bucket (ai-artforge-bucket)  
- Hosted publicly with static website configuration  

Backend (generateImageFromPrompt):  
- On push to code or .trigger file, Lambda is zipped and deployed to AWS  
- Logs available via CloudWatch  

Steps Completed

- Design Static UI: Done  
- Create Lambda Function: Done  
- Integrate Bedrock API: Done  
- Setup API Gateway: Done  
- Deploy to S3: Done  
- IAM Permissions Configuration: Done  
- GitHub Actions CI/CD: Done  
- Test Workflow End-to-End: Done  
- Final Cleanup & Documentation: In Progress  

CI/CD YAML Files

deploy-ui.yml – Deploy Static UI to S3

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

deploy-lambda.yml – Deploy Lambda Function on Push

name: Deploy Lambda Function  
on:  
  push:  
    paths:  
      - generateImageFromPrompt/**  
      - .github/workflows/deploy-lambda.yml  
      - .trigger  
jobs:  
  deploy:  
    runs-on: ubuntu-latest  
    steps:  
      - name: Checkout code  
        uses: actions/checkout@v3  
      - name: Zip Lambda function code  
        run: |  
          cd generateImageFromPrompt  
          zip -r ../lambda.zip .  
      - name: Deploy to AWS Lambda  
        uses: aws-actions/aws-cli-action@v1  
        with:  
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}  
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}  
          aws-region: ${{ secrets.AWS_REGION }}  
          inline-script: |  
            aws lambda update-function-code \  
              --function-name ${{ secrets.LAMBDA_FUNCTION_NAME }} \  
              --zip-file fileb://lambda.zip  

AWS Cleanup Guide (Post-Project)

To avoid Free Tier charges, you can remove these resources:

- Lambda function generateImageFromPrompt  
- API Gateway endpoint  
- S3 bucket ai-artforge-bucket (after backups if needed)  
- CloudWatch Log Groups  
- IAM roles created for GitHub and Lambda access  

Troubleshooting Tips

- Image not loading? → Check CloudWatch logs for Lambda errors  
- 403 Forbidden on S3? → Ensure bucket policy allows public read access  
- CI/CD failed? → Verify that all required GitHub secrets are correctly named:  
  - AWS_ACCESS_KEY_ID  
  - AWS_SECRET_ACCESS_KEY  
  - AWS_REGION  
  - AWS_S3_BUCKET  
  - LAMBDA_FUNCTION_NAME  

Acknowledgments

Built by David Nfizi as part of an AWS portfolio demonstrating real-world GenAI capabilities.
