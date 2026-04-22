# Security Group

resource "aws_security_group" "ssh" {
  name = "allow_ssh"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Project = "Alert-Automation"
  }
}

# EC2 Instance

resource "aws_instance" "ec2" {
  ami           = "ami-0c02fb55956c7d316"
  instance_type = var.instance_type

  key_name = "terraform-key"

  vpc_security_group_ids = [aws_security_group.ssh.id]

  tags = {
    Name    = "cpu-alert-instance"
    Project = "Alert-Automation"
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
  endpoint  = var.email
}

# IAM Role for Lambda

resource "aws_iam_role" "lambda_role" {
  name = "lambda-ec2-restart-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
  })
}

# IAM Policy (Least Privilege)

resource "aws_iam_policy" "lambda_policy" {
  name = "lambda-ec2-reboot-policy"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = ["ec2:RebootInstances"]
      Resource = aws_instance.ec2.arn
    }]
  })
}

# Attach Policy

resource "aws_iam_role_policy_attachment" "lambda_attach" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.lambda_policy.arn
}

# Add Logging Permission

resource "aws_iam_role_policy_attachment" "lambda_logs" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# Lambda Function

resource "aws_lambda_function" "restart_ec2" {
  function_name = "restart-ec2"

  filename         = "lambda_function.zip"
  handler          = "lambda_function.lambda_handler"
  runtime          = "python3.10"
  role             = aws_iam_role.lambda_role.arn

  source_code_hash = filebase64sha256("lambda_function.zip")

  depends_on = [
    aws_iam_role_policy_attachment.lambda_attach
  ]
}

# SNS → Lambda Trigger

resource "aws_sns_topic_subscription" "lambda_sub" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "lambda"
  endpoint  = aws_lambda_function.restart_ec2.arn
}

# Allow SNS to invoke Lambda

resource "aws_lambda_permission" "sns_invoke" {
  statement_id  = "AllowExecutionFromSNS"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.restart_ec2.function_name
  principal     = "sns.amazonaws.com"
  source_arn    = aws_sns_topic.alerts.arn
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
  threshold           = 70   # realistic threshold

  dimensions = {
    InstanceId = aws_instance.ec2.id
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
}