/**
 * 教育 API
 */
import apiClient from './client';

export interface Course {
  id: string;
  title: string;
  status: string;
  enrolled: number;
  completion_rate: number;
}

export interface LearningProgress {
  student_id: string;
  course: string;
  progress: number;
  last_accessed: string;
}

export interface Grade {
  student_id: string;
  course: string;
  score: number;
  grade: string;
  submitted_at: string;
}

export const educationApi = {
  async getCourses(): Promise<Course[]> {
    const res = await apiClient.get<{ items: Course[] }>('/api/v1/education/courses');
    return res.data.items;
  },
  async getLearningProgress(): Promise<LearningProgress[]> {
    const res = await apiClient.get<{ items: LearningProgress[] }>('/api/v1/education/learning-progress');
    return res.data.items;
  },
  async getGrades(): Promise<Grade[]> {
    const res = await apiClient.get<{ items: Grade[] }>('/api/v1/education/grades');
    return res.data.items;
  },
  async getDashboard(): Promise<Record<string, number>> {
    const res = await apiClient.get('/api/v1/education/dashboard');
    return res.data;
  },
};
