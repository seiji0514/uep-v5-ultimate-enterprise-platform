/**
 * MLOps API
 */
import apiClient from './client';

export interface MLPipeline {
  id: string;
  name: string;
  description?: string;
  stages: string[];
  status: string;
  created_at: string;
  created_by: string;
  updated_at?: string;
}

/** バックエンドのバージョン構造 */
export interface ModelVersion {
  version: string;
  model_path?: string;
  metrics?: Record<string, number>;
  status?: string;
  created_at: string;
  created_by: string;
}

/** バックエンドのモデル構造（versions 配列 + current_version） */
export interface MLModelBackend {
  id: string;
  name: string;
  description?: string;
  model_type?: string;
  framework: string;
  versions: ModelVersion[];
  current_version?: string;
  created_at: string;
  updated_at?: string;
  created_by: string;
}

/** 表示用のモデル（フラット構造） */
export interface MLModel {
  id: string;
  name: string;
  version: string;
  status: string;
  framework: string;
  accuracy?: number;
  created_at: string;
  created_by: string;
}

export interface Experiment {
  id: string;
  name: string;
  description?: string;
  status: string;
  metrics?: Record<string, number>;
  created_at: string;
  created_by: string;
}

/** バックエンドのモデル構造を表示用に正規化 */
function normalizeModel(m: MLModelBackend): MLModel {
  const ver = m.versions?.find((v) => v.version === m.current_version) ?? m.versions?.[0];
  const status = ver?.status ?? '-';
  const accuracy = ver?.metrics?.accuracy;
  return {
    id: m.id,
    name: m.name,
    version: m.current_version ?? ver?.version ?? '-',
    status: typeof status === 'string' ? status : String(status ?? '-'),
    framework: m.framework,
    accuracy,
    created_at: m.created_at,
    created_by: m.created_by,
  };
}

export const mlopsApi = {
  async getPipelines(): Promise<MLPipeline[]> {
    const response = await apiClient.get<MLPipeline[]>('/api/v1/mlops/pipelines');
    return response.data;
  },

  async getModels(): Promise<MLModel[]> {
    const response = await apiClient.get<MLModelBackend[]>('/api/v1/mlops/models');
    return response.data.map(normalizeModel);
  },


  async getExperiments(): Promise<Experiment[]> {
    const response = await apiClient.get<Experiment[]>('/api/v1/mlops/experiments');
    return response.data;
  },
};
