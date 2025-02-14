# Design Decisions

## 1. Simulator of Data Feed: 
* Tf that set up the lambda function simulating the data is `tf\lambda_01_data_sim.tf`
    * python code used is in `tf\data_sim\data_sim.py`
* S3 Bucket where data is saved to: `tf\s3_bucket.tf`

I decided to use AWS Eventbridge (formally known as AWS Cloudwatch Events) to launch the data simulator since it's free, and allows me to not set up anything locally. 

Lambda was used since, even with the function created in Part 2, the usage will still be within the free tier.

If this lambda function was being used to scrape and download large zip files from a website (which I have done to get ISO data): Lambda may not be a good fit due to memory constraints (10 GB tops)


### At Scale
Let's say that there are 20K sites (instead of 20 sites)
* therefore each file placed is much larger - 2KB for 20 sites means 2MB file for 20K sites
* the put and storage costs in s3 will still be small

However, let's say that each site's data is saved seperately? 
* each file for each site, saved every 5 min is 1KB
* The total for the puts would be 1 KB * 12 times per hour * 20K sites * 24 hrs = 5.8M requests
* Cost in S3 will still be small - ~$30 

TODO: issues with perf at scale?

## 2. AWS Lambda Fx for Processing
* tf: `tf\lambda_02_s3_to_dynamo.tf`
* python code: `tf\lambda_s3_to_dynamo\lambda_s3_to_dynamo.py`

### At scale
If we only have 1 put every 5 minutes, we won't need to worry about cost of triggers the lambda function. If each lambda runs for 10 seconds, with the lowest amt of memory used, the costs of running the lambda function runs will be small.

However, let's once again hypothesize the cost when there are 20K sites, with seperate puts every 5 minutes
* lambda triggers: $36 = 170 M runs per month * 1M requests is .20 = 20,000 sites * 12 times per hour * 24 hrs * 30 days = 172,800,000
* lambda run costs: $3.7K = 170 M runs per month, 10 S (10K MS) per invocation. Assume the bear min allocated memory of 128 M is enough to process the data

At 20K puts per 5 minutes, It may make more sense to periodically check the S3 bucket for more data, instead of have an s3 put trigger invoke many lambda runs.

## 4. API
* `api\app.py`
The prompt asked us to index the table on site, and sort by timestamp

When I realized dynamodb does not have a datetime data type, my first instinct was to use epoch timestamps (Numbers). The issue with this format is readabiliy and ease being able to query data. It's an O(N) operation to convert each epoch back to a timestamp when returning data from the API.

At scale (if there a lots of queries returning a lot items from the dynamodb database), the datetime could be maybe stored in string format (`YYYY-MM-DDTHH:MM:SS`). This would avoid an extra iteration through the results to make it more readable.
DynamoDB should be able to handle many requests at scale (assuming both the Site_id and a range for the sort key is provided in all queries)


# if I had more time
* Add proper API documentation
* I have another branch where I started to add a github action that would lint the code using pylint - so I would finish that.

