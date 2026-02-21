/**
 * 生成AI API
 */
import apiClient from './client';

export interface GenerateRequest {
  prompt: string;
  model?: string;
  max_tokens?: number;
  temperature?: number;
}

export interface RAGRequest {
  query: string;
  collection?: string;
  context?: string;
}

export interface ReasoningRequest {
  question: string;
  context?: string;
  reasoning_steps?: number;
}

export const generativeAiApi = {
  async generate(request: GenerateRequest) {
    const response = await apiClient.post('/api/v1/generative-ai/generate', request);
    return response.data;
  },

  async rag(request: RAGRequest) {
    const response = await apiClient.post('/api/v1/generative-ai/rag', request);
    return response.data;
  },

  async reasoning(request: ReasoningRequest) {
    const response = await apiClient.post('/api/v1/generative-ai/reasoning', request);
    return response.data;
  },
};
