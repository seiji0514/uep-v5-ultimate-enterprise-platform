/**
 * GraphQL API クライアント
 * バックエンドの GraphQL エンドポイントと通信
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
const GRAPHQL_URL = `${API_BASE_URL.replace(/\/$/, '')}/graphql`;

export interface GraphQLResponse<T> {
  data?: T;
  errors?: Array<{ message: string; locations?: unknown }>;
}

/**
 * GraphQL クエリを実行
 */
export async function graphqlQuery<T>(
  query: string,
  variables?: Record<string, unknown>
): Promise<GraphQLResponse<T>> {
  const token = localStorage.getItem('access_token');
  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  const res = await fetch(GRAPHQL_URL, {
    method: 'POST',
    headers,
    body: JSON.stringify({ query, variables }),
  });

  if (!res.ok) {
    throw new Error(`GraphQL request failed: ${res.status} ${res.statusText}`);
  }

  return res.json();
}

/** 利用可能なクエリ例 */
export const QUERIES = {
  hello: `query { hello }`,
  health: `query { health { status version service } }`,
  services: `query { services { name url status } }`,
};
