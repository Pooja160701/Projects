provider "aws" {
  region = "us-east-1"
}

# Security Group (SSH access)

resource "aws_security_group" "ssh" {
  name = "allow_ssh"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# EC2 Instance

resource "aws_instance" "ec2" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = "t2.micro"

  key_name = "terraform-key"

  vpc_security_group_ids = [aws_security_group.ssh.id]

  tags = {
    Name = "cpu-alert-instance"
  }
}

# SNS Topic

resource "aws_sns_topic" "alerts" {
  name = "cpu-alert-topic"
}

# Email Subscription

resource "aws_sns_topic_subscription" "email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = "poojaajithan160701@gmail.com"
}

# CloudWatch Alarm

resource "aws_cloudwatch_metric_alarm" "cpu_alarm" {
  alarm_name          = "HighCPUAlarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = 60
  statistic           = "Average"
  threshold           = 20

  dimensions = {
    InstanceId = aws_instance.ec2.id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}