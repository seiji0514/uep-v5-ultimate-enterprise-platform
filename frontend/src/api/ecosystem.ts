/**
 * Level 3 エコシステム API
 */
import apiClient from './client';

export interface Partner {
  id: string;
  name: string;
  organization: string;
  contact_email: string;
  description?: string;
  status: string;
  api_endpoint?: string;
  created_at: string;
  approved_at?: string;
}

export interface MarketplaceItem {
  id: string;
  name: string;
  description: string;
  category: string;
  partner_id: string;
  partner_name: string;
  price_type: string;
  metadata?: Record<string, unknown>;
  created_at: string;
  download_count: number;
}

export interface Plugin {
  id: string;
  name: string;
  version: string;
  description: string;
  endpoint: string;
  partner_id: string;
  status: string;
  created_at: string;
}

export interface SharedModel {
  id: string;
  name: string;
  description: string;
  model_type: string;
  source: string;
  created_by: string;
  created_at: string;
  download_count: number;
  tags: string[];
}

export interface ForumPost {
  id: string;
  title: string;
  content: string;
  category: string;
  author: string;
  created_at: string;
  comment_count: number;
  likes: number;
}

export interface ForumComment {
  id: string;
  post_id: string;
  content: string;
  author: string;
  created_at: string;
}

export interface EcosystemOverview {
  level: number;
  name: string;
  features: {
    partner_integration: { description: string; partners_count: number; marketplace_count: number; plugins_count: number };
    community: { description: string; shared_models_count: number; forum_posts_count: number };
    industry_standard: { description: string; spec_endpoint: string };
  };
}

export const ecosystemApi = {
  async getOverview(): Promise<EcosystemOverview> {
    const response = await apiClient.get<EcosystemOverview>('/api/v1/ecosystem/overview');
    return response.data;
  },

  async getPartners(status?: string): Promise<Partner[]> {
    const params = status ? { status } : {};
    const response = await apiClient.get<Partner[]>('/api/v1/ecosystem/partners', { params });
    return response.data;
  },

  async getMarketplaceItems(category?: string): Promise<MarketplaceItem[]> {
    const params = category ? { category } : {};
    const response = await apiClient.get<MarketplaceItem[]>('/api/v1/ecosystem/marketplace', { params });
    return response.data;
  },

  async getPlugins(): Promise<Plugin[]> {
    const response = await apiClient.get<Plugin[]>('/api/v1/ecosystem/plugins');
    return response.data;
  },

  async getSharedModels(modelType?: string): Promise<SharedModel[]> {
    const params = modelType ? { model_type: modelType } : {};
    const response = await apiClient.get<SharedModel[]>('/api/v1/ecosystem/shared-models', { params });
    return response.data;
  },

  async getForumPosts(category?: string): Promise<ForumPost[]> {
    const params = category ? { category } : {};
    const response = await apiClient.get<ForumPost[]>('/api/v1/ecosystem/forum/posts', { params });
    return response.data;
  },

  async getForumComments(postId: string): Promise<ForumComment[]> {
    const response = await apiClient.get<ForumComment[]>(`/api/v1/ecosystem/forum/posts/${postId}/comments`);
    return response.data;
  },
};
