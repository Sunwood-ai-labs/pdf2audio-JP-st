# terraform.tfvars
# このファイルは、Terraformプロジェクトの変数に具体的な値を設定します。
# プロジェクト固有の設定をここで行います。

aws_region         = "ap-northeast-1"  # 東京リージョン
project_name       = "pdf2audio-beta"
vpc_cidr           = "10.0.0.0/16"
public_subnet_cidr = "10.0.1.0/24"
ami_id             = "ami-0d52744d6551d851e"  # Ubuntu 22.04 LTS AMI
instance_type      = "t3.medium"
key_name           = "keypair-name"  # 既存のEC2キーペア名を指定してください。存在しない場合は、AWSコンソールで作成してください。
docker_image       = "makisunwood/pdf2audio-beta:latest"  # DockerHubのイメージ
