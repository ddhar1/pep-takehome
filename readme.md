# How To run

## Set up Parts 1-3
The included terraform files will allow you to 1) simulate the site data Feed, 2) process the data feed data from S3 3) create the dynamo db it will be placed in
```
cd tf
terraform init
terraform plan # check to make sure 13 number of resources are being made
terraform apply
```

## Run the API
I ran the API on python 3.10.11 on a Windows machine with Powershell
You'll need to set up a local python environment, activate it, and then install requirements.txt file
```
python -m venv venv
.\venv\Scripts\Activate.ps1 # source venv/bin/activate on unix
```

Then install the requirements package, go into the `/api` dir and run the application

```
python -m pip install -r requirements.txt
cd api
flask run
```

## TODO: visualization

# At larger volumes
* Data simulator `.py` is currently deployed with AWS Lambda. 
    * If we were scraping large zip files from a website (which I have done to get ISO data): lambda probably would not be a good fit due to run time (15 min) and memory constraints (10 GB tops) limit of a lambda function. 
    * **TODO**: aws lambda trigger limits - if a lot of s3 puts at one time?

* API (app.py):



# Other things
* I initially attempted to blindly query the API dynamodb requires that numbers be stored as a decimal. however boto3's dynambodb.table.query function doesn't know how to handle Decimals. I found a package online to address this issue
    * In order to convert decimal to float, There's an extra O(N) iteration through the entire output of the API. This may not be ideal if this data needs to appear somewhere quickly

# if I had more time
* annotate the API code endpoints with swagger yaml format info about the API - and creae an endpoint where the swagger documentation could autogenerate
* 


