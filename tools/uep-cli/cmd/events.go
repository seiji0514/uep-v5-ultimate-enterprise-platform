package cmd

import (
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	"github.com/spf13/cobra"
)

var eventsCmd = &cobra.Command{
	Use:   "events",
	Short: "イベント操作",
}

var eventsListCmd = &cobra.Command{
	Use:   "list",
	Short: "トピック一覧取得",
	RunE:  runEventsList,
}

var eventsOutboxCmd = &cobra.Command{
	Use:   "outbox",
	Short: "未公開アウトボックス一覧",
	RunE:  runEventsOutbox,
}

func init() {
	rootCmd.AddCommand(eventsCmd)
	eventsCmd.AddCommand(eventsListCmd)
	eventsCmd.AddCommand(eventsOutboxCmd)
}

func runEventsList(cmd *cobra.Command, args []string) error {
	req, err := http.NewRequest("GET", apiURL+"/api/v1/events/topics", nil)
	if err != nil {
		return err
	}
	addAuth(req)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("request failed: %s", resp.Status)
	}
	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)
	return printOutput(result)
}

func runEventsOutbox(cmd *cobra.Command, args []string) error {
	req, err := http.NewRequest("GET", apiURL+"/api/v1/events/outbox/unpublished", nil)
	if err != nil {
		return err
	}
	addAuth(req)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		return fmt.Errorf("request failed: %s", resp.Status)
	}
	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)
	return printOutput(result)
}

func addAuth(req *http.Request) {
	if token != "" {
		req.Header.Set("Authorization", "Bearer "+token)
	}
}

func printOutput(v interface{}) error {
	switch strings.ToLower(output) {
	case "table":
		if m, ok := v.(map[string]interface{}); ok {
			for k, val := range m {
				fmt.Printf("%s: %v\n", k, val)
			}
		}
	default:
		out, _ := json.MarshalIndent(v, "", "  ")
		fmt.Println(string(out))
	}
	return nil
}
