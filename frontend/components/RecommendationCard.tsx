'use client'

import React from 'react'

interface RecommendationCardProps {
  recommendations: string[]
}

export default function RecommendationCard({ recommendations }: RecommendationCardProps) {
  if (recommendations.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md">
        <h3 className="text-xl font-bold mb-2">Recommendations</h3>
        <p className="text-gray-600">No specific recommendations at this time.</p>
      </div>
    )
  }
  
  return (
    <div className="bg-white p-6 rounded-lg shadow-md">
      <h3 className="text-xl font-bold mb-4">Recommendations</h3>
      <div className="space-y-3">
        {recommendations.map((rec, index) => (
          <div
            key={index}
            className="flex items-start p-3 bg-gray-50 rounded-lg border-l-4"
            style={{
              borderLeftColor: getRecommendationColor(rec),
            }}
          >
            <div className="flex-shrink-0 mr-3 mt-1">
              {getRecommendationIcon(rec)}
            </div>
            <div className="flex-1 text-gray-700">{rec}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

function getRecommendationColor(rec: string): string {
  if (rec.includes('HIGH RISK') || rec.includes('🚨')) return '#ef4444' // red
  if (rec.includes('MODERATE RISK') || rec.includes('⚠️')) return '#f59e0b' // yellow
  if (rec.includes('✅') || rec.includes('Keep up')) return '#10b981' // green
  return '#6366f1' // default blue
}

function getRecommendationIcon(rec: string): string {
  if (rec.includes('🚨')) return '🚨'
  if (rec.includes('⚠️')) return '⚠️'
  if (rec.includes('✅')) return '✅'
  if (rec.includes('💡')) return '💡'
  if (rec.includes('ℹ️')) return 'ℹ️'
  return '•'
}
