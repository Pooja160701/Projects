output "instance_public_ip" {
  value = aws_instance.ec2.public_ip
}

output "sns_topic_arn" {
  value = aws_sns_topic.alerts.arn
}