provider "aws" {
    region = var.AWS_REGION
    secret_key = var.AWS_SECRET_KEY
    access_key = var.AWS_ACCESS_KEY
}

data "aws_vpc" "current-vpc" {
    id = "vpc-00b3f6b2893c390f2"
}

data "aws_db_subnet_group" "subnet-group" {
    name = "c17-public-subnet-group"
}

data "aws_subnet" "subnet" {
    id = var.SUBNET_ID
}

resource "aws_security_group" "db_security_group" {
    name = "c17-dana-week9-sg"
    vpc_id = data.aws_vpc.current-vpc.id
}

resource "aws_security_group" "ec2_security_group" {
    name = "c17-dana-week9-sg-ec2"
    vpc_id = data.aws_vpc.current-vpc.id
}


resource "aws_vpc_security_group_ingress_rule" "db-sg-inbound-rule"{
    security_group_id = aws_security_group.db_security_group.id
    cidr_ipv4 = "0.0.0.0/0"
    from_port = 5432
    ip_protocol = "tcp"
    to_port = 5432
}

resource "aws_vpc_security_group_egress_rule" "db-sg-inbound-rule"{
    security_group_id = aws_security_group.db_security_group.id
    cidr_ipv4 = "0.0.0.0/0"
    from_port = 5432
    ip_protocol = "tcp"
    to_port = 5432
}

resource "aws_vpc_security_group_ingress_rule" "ec2-inbound-rule" {
  security_group_id = aws_security_group.ec2_security_group.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 22
  to_port           = 22
  ip_protocol       = "tcp"
}


resource "aws_db_instance" "museum-db" {
    allocated_storage = 10
    db_name = "museum"
    identifier = "c17-dana-museum-db"
    engine = "postgres"
    engine_version = "16.8"
    instance_class = "db.t3.micro"
    publicly_accessible = true
    performance_insights_enabled = false
    skip_final_snapshot = true
    db_subnet_group_name = data.aws_db_subnet_group.subnet-group.name
    username = var.DB_USERNAME
    password = var.DB_PASSWORD
}

resource "aws_instance" "c17-dana-museum-ec2" {
  ami           = "ami-0fc32db49bc3bfbb1"
  instance_type = "t3.micro"
  subnet_id     = data.aws_subnet.subnet.id
  key_name      = var.KEY_NAME
  vpc_security_group_ids = [aws_security_group.db_security_group.id]
  associate_public_ip_address = true
  tags = {
    Name = "c17-dana-museum-ec2"
  }
}