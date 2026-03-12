# UEP v5.0 Terraform 変数定義

variable "project_name" {
  description = "プロジェクト名"
  type        = string
  default     = "uep-v5"
}

variable "environment" {
  description = "環境 (dev/staging/prod)"
  type        = string
  default     = "dev"
}

variable "aws_region" {
  description = "AWS リージョン"
  type        = string
  default     = "ap-northeast-1"
}
