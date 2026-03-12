package cmd

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	"github.com/spf13/cobra"
)

var healthCmd = &cobra.Command{
	Use:   "health",
	Short: "API ヘルスチェック",
	RunE:  runHealth,
}

func init() {
	rootCmd.AddCommand(healthCmd)
}

func runHealth(cmd *cobra.Command, args []string) error {
	req, err := http.NewRequest("GET", apiURL+"/api/v1/health", nil)
	if err != nil {
		return err
	}
	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()

	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("health check failed: %s", resp.Status)
	}

	var result map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&result); err != nil {
		return err
	}

	switch strings.ToLower(output) {
	case "table":
		printHealthTable(result)
	default:
		out, _ := json.MarshalIndent(result, "", "  ")
		fmt.Println(string(out))
	}
	fmt.Println("OK: Backend is healthy")
	return nil
}

func printHealthTable(m map[string]interface{}) {
	for k, v := range m {
		fmt.Printf("%-15s %v\n", k, v)
	}
}
