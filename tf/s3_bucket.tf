/*
  S3 bucket, and S3 bucket trigger config
*/

resource "aws_s3_bucket" "bucket" {
  bucket = "dd-peptakehome"
  force_destroy = true
  tags = {
    Project = var.tag__project_name
  }
}

# S3 Trigger
resource "aws_s3_bucket_notification" "pep-takehome-lambda-trigger" {
  bucket = aws_s3_bucket.bucket.id
  lambda_function {
    lambda_function_arn = aws_lambda_function.process_site_data_dynamo.arn
    events              = ["s3:ObjectCreated:*"] 
    filter_prefix       = var.site_data_s3_put_prefix
    filter_suffix       = ".json"
  }

  depends_on = [aws_lambda_permission.allow_bucket]
}
