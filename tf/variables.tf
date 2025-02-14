/*
 Config for variables used throughout other
 tf files. Would use tfvars file if these tf files
 were meant to be more modular 
 and abstract for different usecases
*/

variable "tag__project_name" {
  type    = string
  default = "pep_takehome"
}

variable "site_data_dynamodb_table_name" {
  type = string
  default = "SitesEnergyStatsDB"
}

variable "site_data_s3_put_prefix" {
  type = string
  default = "raw/site_flow/"
}

variable "lambda_s3_to_dynamo_file_name" {
  type = string
  default = "lambda_s3_to_dynamo"
}

variable "aws_lambda_role_arn" {
  type = string
  default = "arn:aws:iam::273354667206:role/AWSLambdaRole"
}

variable "lambda_api_filename" {
  type = string
  default = "api_for_site_data"
}

# moved this to lambda config files
# variable "process_site_data_dynamo_py_script" {
#     type = string
#     default = "../lambda_scripts"
# }

# variable "process_site_data_dynamo_zip_dir" {
#     type = string
#     default = "./"
# }


