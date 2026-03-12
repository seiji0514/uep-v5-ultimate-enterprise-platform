# UEP v5.0 Terraform メインモジュール
# 補強スキル: IaC, マルチクラウド

terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    kubernetes = {
      source  = "hashicorp/kubernetes"
      version = "~> 2.23"
    }
  }
  backend "local" {
    path = "terraform.tfstate"
  }
}

provider "aws" {
  region = var.aws_region
}

# EKS クラスターが存在する場合のみ有効化
# data "aws_eks_cluster" "main" {
#   name = var.eks_cluster_name
# }

# provider "kubernetes" {
#   host                   = data.aws_eks_cluster.main.endpoint
#   cluster_ca_certificate = base64decode(data.aws_eks_cluster.main.certificate_authority[0].data)
#   exec {
#     api_version = "client.authentication.k8s.io/v1beta1"
#     command     = "aws"
#     args        = ["eks", "get-token", "--cluster-name", data.aws_eks_cluster.main.name]
#   }
# }

variable "eks_cluster_name" {
  default = "uep-cluster"
}

output "project" {
  value = var.project_name
}
