/**
 * API Client for Injury Risk Predictor
 */

import axios from 'axios';
import type {
  PredictionRequest,
  PredictionResponse,
  HealthResponse,
  ModelInfoResponse,
} from './types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

/**
 * Check API health
 */
export async function checkHealth(): Promise<HealthResponse> {
  const response = await api.get<HealthResponse>('/health');
  return response.data;
}

/**
 * Predict injury risk
 */
export async function predictInjuryRisk(
  request: PredictionRequest
): Promise<PredictionResponse> {
  const response = await api.post<PredictionResponse>('/api/predict', request);
  return response.data;
}

/**
 * Get model information
 */
export async function getModelInfo(): Promise<ModelInfoResponse> {
  const response = await api.get<ModelInfoResponse>('/api/model/info');
  return response.data;
}
