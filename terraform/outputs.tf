# outputs.tf

output "db_host" {
  value       = aws_db_instance.museum-db.address
}

output "db_name" {
  value       = aws_db_instance.museum-db.db_name
}

output "db_user" {
  value       = aws_db_instance.museum-db.username
}

output "db_password" {
  value       = aws_db_instance.museum-db.password
  sensitive   = true
}

output "db_port" {
  value       = aws_db_instance.museum-db.port
}

output "ec2_public_ip" {
  value = aws_instance.c17-dana-museum-ec2.public_ip
}
