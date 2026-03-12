package cmd

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"strings"

	"github.com/spf13/cobra"
)

var graphqlQuery string

var graphqlCmd = &cobra.Command{
	Use:   "graphql",
	Short: "GraphQL クエリ実行",
}

var graphqlQueryCmd = &cobra.Command{
	Use:   "query [query]",
	Short: "GraphQL クエリを実行",
	RunE:  runGraphQLQuery,
}

func init() {
	rootCmd.AddCommand(graphqlCmd)
	graphqlCmd.AddCommand(graphqlQueryCmd)
	graphqlQueryCmd.Flags().StringVarP(&graphqlQuery, "query", "q", "", "GraphQL query string")
}

func runGraphQLQuery(cmd *cobra.Command, args []string) error {
	q := graphqlQuery
	if q == "" && len(args) > 0 {
		q = strings.Join(args, " ")
	}
	if q == "" {
		q = `{ hello health { status version } }`
	}
	body := map[string]string{"query": q}
	b, _ := json.Marshal(body)
	req, err := http.NewRequest("POST", apiURL+"/graphql", bytes.NewReader(b))
	if err != nil {
		return err
	}
	req.Header.Set("Content-Type", "application/json")
	addAuth(req)
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		return err
	}
	defer resp.Body.Close()
	var result map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&result)
	out, _ := json.MarshalIndent(result, "", "  ")
	fmt.Println(string(out))
	return nil
}
