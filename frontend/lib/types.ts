/**
 * TypeScript types matching the API schemas
 */

export interface TrainingWeek {
  week: number;
  weekly_load: number;
  daily_loads: number[];
}

export interface AthleteProfile {
  age: number;
  experience_years: number;
  baseline_weekly_load: number;
}

export interface PredictionRequest {
  athlete: AthleteProfile;
  training_history: TrainingWeek[];
}

export interface PredictionResponse {
  risk_level: 'LOW' | 'MODERATE' | 'HIGH';
  risk_score: number;
  acwr: number;
  monotony?: number;
  strain?: number;
  week_over_week_change?: number;
  recommendations: string[];
  feature_contributions?: Record<string, number>;
}

export interface HealthResponse {
  status: string;
  model_loaded: boolean;
  version: string;
}

export interface ModelInfoResponse {
  model_type: string;
  accuracy?: number;
  recall?: number;
  features: string[];
  last_trained?: string;
}
