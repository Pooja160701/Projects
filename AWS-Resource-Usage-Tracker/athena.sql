-- Create Database

CREATE DATABASE aws_tracker;

-- Create Table

CREATE EXTERNAL TABLE aws_tracker.resources (
    resource_type string,
    resource_id string,
    region string,
    metadata map<string,string>,
    timestamp string
)
PARTITIONED BY (date string)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://aws-resource-tracker-pooja/bronze/';

-- Load Partitions

MSCK REPAIR TABLE aws_tracker.resources;

-- Query Examples

-- Count EC2 instances

SELECT count(*) 
FROM aws_tracker.resources 
WHERE resource_type = 'ec2';

-- Running EC2 only

SELECT resource_id, metadata['state']
FROM aws_tracker.resources
WHERE resource_type = 'ec2'
AND metadata['state'] = 'running';

-- Resources by type

SELECT resource_type, count(*)
FROM aws_tracker.resources
GROUP BY resource_type;
ve Your SQL (More Insightful)

-- Count by date (trend)

SELECT date, resource_type, count(*)
FROM aws_tracker.resources
GROUP BY date, resource_type
ORDER BY date;

-- Fix Column Name

SELECT resource_type, count(*) AS total_resources
FROM aws_tracker.resources
GROUP BY resource_type;