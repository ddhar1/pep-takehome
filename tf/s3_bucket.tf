resource "aws_s3_bucket" "bucket" {
  bucket = "dd-peptakehome"
  force_destroy = true
  tags = {
    Project = var.tag__project_name
  }
}

resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.process_site_data_dynamo.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucket.arn

}

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


