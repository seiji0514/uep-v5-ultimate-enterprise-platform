# UEP v5.0 Terraform

補強スキル: IaC, マルチクラウド

## 構成

- `main.tf` - メイン設定、EKS 参照
- `variables.tf` - 変数定義
- `modules/eks/` - EKS モジュール（スケルトン）

## 実行

```bash
cd infrastructure/terraform
terraform init
terraform plan
terraform apply
```

## 環境変数

- `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY` - AWS 認証
- または `aws configure` で設定
