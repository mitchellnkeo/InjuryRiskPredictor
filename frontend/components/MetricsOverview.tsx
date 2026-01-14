'use client'

import React from 'react'
import type { PredictionResponse } from '@/lib/types'

interface MetricsOverviewProps {
  prediction: PredictionResponse
}

export default function MetricsOverview({ prediction }: MetricsOverviewProps) {
  const metrics = [
    {
      label: 'ACWR',
      value: prediction.acwr.toFixed(2),
      description: 'Acute:Chronic Workload Ratio',
      riskZone: getACWRRiskZone(prediction.acwr),
    },
    {
      label: 'Monotony',
      value: prediction.monotony?.toFixed(2) || 'N/A',
      description: 'Training variation',
      riskZone: prediction.monotony && prediction.monotony > 2.0 ? 'high' : 'low',
    },
    {
      label: 'Strain',
      value: prediction.strain?.toFixed(1) || 'N/A',
      description: 'Training strain',
      riskZone: prediction.strain && prediction.strain > 150 ? 'high' : 'low',
    },
    {
      label: 'Week Change',
      value: prediction.week_over_week_change 
        ? `${(prediction.week_over_week_change * 100).toFixed(1)}%`
        : 'N/A',
      description: 'Week-over-week change',
      riskZone: prediction.week_over_week_change && prediction.week_over_week_change > 0.2 ? 'high' : 'low',
    },
  ]
  
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
      {metrics.map((metric, index) => (
        <div
          key={index}
          className="bg-white p-4 rounded-lg shadow-md border-l-4"
          style={{
            borderLeftColor: getRiskColor(metric.riskZone),
          }}
        >
          <div className="text-sm text-gray-600 mb-1">{metric.label}</div>
          <div className="text-2xl font-bold text-gray-900 mb-1">
            {metric.value}
          </div>
          <div className="text-xs text-gray-500">{metric.description}</div>
        </div>
      ))}
    </div>
  )
}

function getACWRRiskZone(acwr: number): 'low' | 'moderate' | 'high' {
  if (acwr < 0.8) return 'low'
  if (acwr <= 1.3) return 'low'
  if (acwr <= 1.5) return 'moderate'
  return 'high'
}

function getRiskColor(zone: 'low' | 'moderate' | 'high'): string {
  const colors = {
    low: '#10b981',      // green
    moderate: '#f59e0b', // yellow
    high: '#ef4444',     // red
  }
  return colors[zone] || '#6b7280'
}
