'use client'

import React from 'react'

interface RiskGaugeProps {
  riskScore: number // 0-1
  riskLevel: 'LOW' | 'MODERATE' | 'HIGH'
}

export default function RiskGauge({ riskScore, riskLevel }: RiskGaugeProps) {
  const percentage = Math.round(riskScore * 100)
  
  // Color based on risk level
  const colorMap = {
    LOW: 'bg-risk-low',
    MODERATE: 'bg-risk-moderate',
    HIGH: 'bg-risk-high',
  }
  
  const textColorMap = {
    LOW: 'text-risk-low',
    MODERATE: 'text-risk-moderate',
    HIGH: 'text-risk-high',
  }
  
  // Calculate angle for gauge (0-180 degrees, where 0 = left, 180 = right)
  const angle = riskScore * 180
  
  return (
    <div className="flex flex-col items-center">
      {/* Gauge Visualization */}
      <div className="relative w-64 h-32 mb-4">
        {/* Background arc */}
        <svg className="w-full h-full" viewBox="0 0 200 100">
          {/* Low risk zone (green) */}
          <path
            d="M 20 80 A 80 80 0 0 1 100 0"
            fill="none"
            stroke="#10b981"
            strokeWidth="20"
            strokeLinecap="round"
          />
          {/* Moderate risk zone (yellow) */}
          <path
            d="M 100 0 A 80 80 0 0 1 140 40"
            fill="none"
            stroke="#f59e0b"
            strokeWidth="20"
            strokeLinecap="round"
          />
          {/* High risk zone (red) */}
          <path
            d="M 140 40 A 80 80 0 0 1 180 80"
            fill="none"
            stroke="#ef4444"
            strokeWidth="20"
            strokeLinecap="round"
          />
          
          {/* Needle */}
          <line
            x1="100"
            y1="80"
            x2={100 + 80 * Math.cos((180 - angle) * Math.PI / 180)}
            y2={80 - 80 * Math.sin((180 - angle) * Math.PI / 180)}
            stroke="#1f2937"
            strokeWidth="3"
            strokeLinecap="round"
          />
          
          {/* Center dot */}
          <circle cx="100" cy="80" r="5" fill="#1f2937" />
        </svg>
      </div>
      
      {/* Risk Score Display */}
      <div className="text-center">
        <div className={`text-5xl font-bold ${textColorMap[riskLevel]} mb-2`}>
          {percentage}%
        </div>
        <div className={`text-2xl font-semibold ${textColorMap[riskLevel]} mb-1`}>
          {riskLevel} RISK
        </div>
        <div className="text-sm text-gray-600">
          Injury Probability
        </div>
      </div>
    </div>
  )
}
