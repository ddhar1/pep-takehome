data "archive_file" "s3_to_dynamo_script" {
  type       = "zip"
  source_file= "./lambda_s3_to_dynamo/${var.lambda_s3_to_dynamo_file_name}.py"
  output_path = "./${var.lambda_s3_to_dynamo_file_name}.zip"
}

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

