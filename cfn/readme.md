# Instructions for Deployment:

This architetcure was designed with crypto in mind. Which means this architecture was built to run 24hrs 7 days per week. THIS IS NOT SOMETHING WHICH CAN BE RUN FOR FREE. YOU WILL INCUR AWS CHARGES.

### Step 1:
- Clone the repo

### Step 2:
- Sign in to the AWS console
- Go to the CloudFormation console
- Deploy s3_infra.yml ***(you will have to change the BucketName in the .yml file to something unique before deployment)***

### Step 3:
- [Create an Alpaca account to receive your API keys](https://alpaca.markets/)

### Step 4:
- Add your API keys to the corresponding lines in infra.yml
  - Your API Key ID should go on line 10 of infra.yml
  - Your API Secret Key should go on line 21 of infra.yml

### Step 5 (Optional):
- Make any necessay changes to main.py or strategies.py as you see fit. If you'd like to implement your own trading strategy you can do so.

### Step 6:
- Sign in to the AWS console
- Go to the S3 console
- upload main.py to your Bucket

### Step 7:
- Sign in to the AWS console
- Go to the CloudFormation console
- Deploy infra.yml
