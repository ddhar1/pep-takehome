/*
- Store the processed data in a DynamoDB table with the following schema:
  - **Partition Key**: `site_id`
  - **Sort Key**: `timestamp`
  - Other attributes:
    - `energy_generated_kwh`
    - `energy_consumed_kwh`
    - `net_energy_kwh`
    - `anomaly` (boolean)
*/

resource "aws_dynamodb_table" "site_energy_stats" {
  name           = var.site_data_dynamodb_table_name
  billing_mode   = "PROVISIONED"
  read_capacity  = 20
  write_capacity = 20
  hash_key       = "site_id"
  range_key      = "timestamp"

  attribute {
    name = "site_id"
    type = "N"
  }

  attribute {
    name = "timestamp"
    type = "N"
  }

  tags = {
    Project = var.tag__project_name
  }
}