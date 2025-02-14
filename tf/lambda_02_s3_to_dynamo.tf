/*
  Lambda function that processes data in S3, and 
  places it in DynamoDB
*/

resource "aws_lambda_function" "process_site_data_dynamo" {
  function_name = "S3_to_Dynamo"
  role          = aws_iam_role.lambda_role.arn
  filename      = data.archive_file.s3_to_dynamo_script.output_path
  source_code_hash = data.archive_file.s3_to_dynamo_script.output_base64sha256
  handler          = "${var.lambda_s3_to_dynamo_file_name}.lambda_handler"
  runtime = "python3.9"
  timeout = 30

  environment {
    variables = {
      DYNAMODB_TABLE = var.site_data_dynamodb_table_name
    }
  }
  tags = {
    Project = var.tag__project_name
  }
  #   logging_config {
  #   log_format = "Text"
  # }
}

# Python code archived for Lambda
data "archive_file" "s3_to_dynamo_script" {
  type       = "zip"
  source_file= "./lambda_s3_to_dynamo/${var.lambda_s3_to_dynamo_file_name}.py"
  output_path = "./${var.lambda_s3_to_dynamo_file_name}.zip"
}

# Config to allow s3 to dynamo fx to be triggered
resource "aws_lambda_permission" "allow_bucket" {
  statement_id  = "AllowExecutionFromS3Bucket"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.process_site_data_dynamo.arn
  principal     = "s3.amazonaws.com"
  source_arn    = aws_s3_bucket.bucket.arn
}