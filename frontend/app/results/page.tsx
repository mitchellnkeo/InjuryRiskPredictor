'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import RiskGauge from '@/components/RiskGauge'
import MetricsOverview from '@/components/MetricsOverview'
import RecommendationCard from '@/components/RecommendationCard'
import type { PredictionResponse } from '@/lib/types'

export default function ResultsPage() {
  const router = useRouter()
  const [prediction, setPrediction] = useState<PredictionResponse | null>(null)
  
  useEffect(() => {
    // Get prediction result from sessionStorage
    const stored = sessionStorage.getItem('predictionResult')
    if (stored) {
      try {
        setPrediction(JSON.parse(stored))
      } catch (e) {
        console.error('Error parsing prediction result:', e)
        router.push('/predict')
      }
    } else {
      // No prediction data, redirect to predict page
      router.push('/predict')
    }
  }, [router])
  
  if (!prediction) {
    return (
      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading results...</p>
        </div>
      </main>
    )
  }
  
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4 max-w-6xl">
        {/* Header */}
        <div className="mb-8">
          <Link
            href="/predict"
            className="text-blue-600 hover:text-blue-800 mb-4 inline-block"
          >
            ← Back to Prediction Form
          </Link>
          <h1 className="text-4xl font-bold text-gray-900">Prediction Results</h1>
        </div>
        
        {/* Risk Gauge - Prominent Display */}
        <div className="bg-white p-8 rounded-lg shadow-lg mb-8 flex justify-center">
          <RiskGauge
            riskScore={prediction.risk_score}
            riskLevel={prediction.risk_level}
          />
        </div>
        
        {/* Metrics Overview */}
        <div className="mb-8">
          <h2 className="text-2xl font-bold mb-4">Key Metrics</h2>
          <MetricsOverview prediction={prediction} />
        </div>
        
        {/* Recommendations */}
        <div className="mb-8">
          <RecommendationCard recommendations={prediction.recommendations} />
        </div>
        
        {/* Feature Contributions (if available) */}
        {prediction.feature_contributions && (
          <div className="bg-white p-6 rounded-lg shadow-md">
            <h3 className="text-xl font-bold mb-4">Top Contributing Factors</h3>
            <div className="space-y-2">
              {Object.entries(prediction.feature_contributions)
                .sort(([, a], [, b]) => b - a)
                .map(([feature, importance]) => (
                  <div key={feature} className="flex items-center">
                    <div className="w-32 text-sm text-gray-600 capitalize">
                      {feature.replace(/_/g, ' ')}
                    </div>
                    <div className="flex-1 bg-gray-200 rounded-full h-4 mr-4">
                      <div
                        className="bg-blue-600 h-4 rounded-full"
                        style={{ width: `${importance * 100}%` }}
                      ></div>
                    </div>
                    <div className="w-16 text-sm text-gray-700 text-right">
                      {(importance * 100).toFixed(1)}%
                    </div>
                  </div>
                ))}
            </div>
          </div>
        )}
        
        {/* Action Buttons */}
        <div className="mt-8 flex gap-4 justify-center">
          <Link
            href="/predict"
            className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
          >
            New Prediction
          </Link>
          <Link
            href="/"
            className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
          >
            Back to Home
          </Link>
        </div>
      </div>
    </main>
  )
}
