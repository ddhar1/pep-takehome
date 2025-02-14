/*
  Config for Lambda function that creates json data file
   of Energy Generation/Consumption for sites
  Also config for EventBridge rule that triggers Lambda fx
  every 5 minutes
*/

# Lambda function that creates Site Data
resource "aws_lambda_function" "create_site_data" {
  function_name = "Create_SiteData_S3"
  role          = aws_iam_role.lambda_role.arn
  filename      = data.archive_file.site_data_sim.output_path
  source_code_hash = data.archive_file.site_data_sim.output_base64sha256
  handler          = "data_sim.lambda_handler"
  runtime = "python3.9"
  timeout = 30

  environment {
    variables = {
      AWS_BUCKET_NAME =  aws_s3_bucket.bucket.bucket
      SITE_DATA_FILE_PREFIX = var.site_data_s3_put_prefix
    }
  }

  tags = {
    Project = var.tag__project_name
  }

}

# Python code for Lambda Fx
data "archive_file" "site_data_sim" {
  type       = "zip"
  source_file= "./data_sim/data_sim.py"
  output_path = "./data_sim.zip"
}

# Lambda permission to allow CloudWatch Events to invoke the function
resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowCloudWatchInvoke"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_site_data.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.every_five_minutes.arn
}

# Eventbridge rule triggering Lambda fx every 5 minutes
resource "aws_cloudwatch_event_rule" "every_five_minutes" {
  name                = "every-five-minutes"
  description         = "Trigger Lambda function every 5 minutes"
  schedule_expression = "rate(5 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.every_five_minutes.name
  target_id = "TriggerLambda"
  arn       = aws_lambda_function.create_site_data.arn
}

