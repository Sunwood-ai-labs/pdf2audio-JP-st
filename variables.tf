# variables.tf
# このファイルは、Terraformプロジェクトで使用される変数を定義します。
# これらの変数は、main.tfで参照され、terraform.tfvarsで値が設定されます。

variable "aws_region" {
  description = "AWSリージョン"
  type        = string
}

variable "project_name" {
  description = "プロジェクト名"
  type        = string
}

variable "vpc_cidr" {
  description = "VPCのCIDRブロック"
  type        = string
}

variable "public_subnet_cidr" {
  description = "パブリックサブネットのCIDRブロック"
  type        = string
}

variable "ami_id" {
  description = "使用するAMIのID"
  type        = string
}

variable "instance_type" {
  description = "EC2インスタンスタイプ"
  type        = string
}

variable "key_name" {
  description = "EC2インスタンスに使用するキーペア名"
  type        = string
}

variable "docker_image" {
  description = "使用するDockerイメージ"
  type        = string
}
