package cmd

import (
	"fmt"
	"os"

	"github.com/spf13/cobra"
)

var (
	apiURL   string
	token    string
	output   string // json, table
	version  = "1.1.0"
)

var rootCmd = &cobra.Command{
	Use:   "uep-cli",
	Short: "UEP v5.0 CLI - ヘルスチェック、API疎通、イベント操作",
	Long:  `UEP v5.0 Ultimate Enterprise Platform 用 CLI ツール`,
}

func Execute() {
	if err := rootCmd.Execute(); err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
}

func init() {
	rootCmd.PersistentFlags().StringVarP(&apiURL, "url", "u", "http://localhost:8000", "API base URL")
	rootCmd.PersistentFlags().StringVarP(&token, "token", "t", "", "JWT token for auth")
	rootCmd.PersistentFlags().StringVarP(&output, "output", "o", "json", "Output format: json, table")
}
