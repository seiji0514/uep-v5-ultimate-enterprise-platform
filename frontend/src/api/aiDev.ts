/**
 * AI支援開発 API
 */
import apiClient from './client';

export interface CodeGenerateRequest {
  description: string;
  language?: string;
  framework?: string;
  requirements?: string[];
}

export interface CodeReviewRequest {
  code: string;
  language?: string;
  check_style?: boolean;
  check_security?: boolean;
  check_performance?: boolean;
}

export interface DocumentationRequest {
  doc_type: string;
  content: string;
  language?: string;
  project_name?: string;
  features?: string[];
}

export const aiDevApi = {
  async generateCode(request: CodeGenerateRequest) {
    const response = await apiClient.post('/api/v1/ai-dev/code/generate', request);
    return response.data;
  },

  async reviewCode(request: CodeReviewRequest) {
    const response = await apiClient.post('/api/v1/ai-dev/review', request);
    return response.data;
  },

  async generateDocumentation(request: DocumentationRequest) {
    const response = await apiClient.post('/api/v1/ai-dev/documentation/generate', request);
    return response.data;
  },
};
