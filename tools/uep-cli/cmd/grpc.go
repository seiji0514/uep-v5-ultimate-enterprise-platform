// grpc: gRPC クライアントサブコマンド
// UEP v5.0 補強スキル: gRPC クライアント
package cmd

import (
	"context"
	"fmt"
	"strings"
	"time"

	"github.com/spf13/cobra"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
)

var (
	grpcAddr string
	grpcCmd  = &cobra.Command{
		Use:   "grpc",
		Short: "gRPC クライアント操作",
		Long:  `UEP v5.0 gRPC サービスへの接続・疎通確認`,
	}
)

func init() {
	rootCmd.AddCommand(grpcCmd)
	grpcCmd.PersistentFlags().StringVarP(&grpcAddr, "addr", "a", "localhost:50051", "gRPC server address")

	grpcCmd.AddCommand(grpcStatusCmd)
}

var grpcStatusCmd = &cobra.Command{
	Use:   "status",
	Short: "gRPC サービス疎通確認",
	RunE:  runGrpcStatus,
}

func runGrpcStatus(cmd *cobra.Command, args []string) error {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
	defer cancel()

	conn, err := grpc.DialContext(ctx, grpcAddr,
		grpc.WithTransportCredentials(insecure.NewCredentials()),
		grpc.WithBlock(),
	)
	if err != nil {
		return fmt.Errorf("gRPC connection failed: %w", err)
	}
	defer conn.Close()

	// 接続成功時（proto 未生成時は接続確認のみ）
	switch strings.ToLower(output) {
	case "table":
		fmt.Printf("%-20s %s\n", "Address", grpcAddr)
		fmt.Printf("%-20s %s\n", "Status", "connected")
	default:
		fmt.Printf(`{"address":"%s","status":"connected","message":"gRPC service reachable"}`+"\n", grpcAddr)
	}
	return nil
}
