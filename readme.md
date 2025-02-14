# See info.md for Design Decisions

---

# How To run

## Set up Parts 1-3 in AWS (lambda Functions, and DynamoDB)
The included terraform files will allow you to 1) simulate the site data Feed, 2) process the data feed data from S3 3) create the dynamo db it will be placed in
```
cd tf
terraform init
terraform plan # check to make sure 13 number of resources are being made
terraform apply
```

The user that terraform is using should at least have access t

## API
First, install the required python packages, by setting up a local python environment
```
python -m venv venv
.\venv\Scripts\Activate.ps1 # source venv/bin/activate on unix
python -m pip install -r requirements.txt
```

I ran the API on python 3.10.11 on a Windows machine with Powershell
```
cd api
flask run
```

![api output example](api/screenshot_apioutput.png)

## Visualization
Use the same python environment / requirements file.
```
cd visualization
python visualization.py
```

![avg consumption vs generated per site](visualization/visualization_output.png)


