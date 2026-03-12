# EKS モジュール（スケルトン）
# 本番では aws_eks_cluster リソースを定義

variable "cluster_name" {
  type = string
}

variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

output "cluster_endpoint" {
  value = "https://placeholder.eks.ap-northeast-1.amazonaws.com"
}
