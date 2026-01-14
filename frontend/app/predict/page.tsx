'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { predictInjuryRisk } from '@/lib/api'
import type { PredictionRequest, TrainingWeek, AthleteProfile } from '@/lib/types'

export default function PredictPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const [athlete, setAthlete] = useState<AthleteProfile>({
    age: 30,
    experience_years: 5,
    baseline_weekly_load: 25.0,
  })
  
  const [trainingHistory, setTrainingHistory] = useState<TrainingWeek[]>([
    { week: 1, weekly_load: 20.0, daily_loads: [3.0, 4.0, 0.0, 5.0, 0.0, 4.0, 4.0] },
    { week: 2, weekly_load: 22.0, daily_loads: [3.5, 4.5, 0.0, 5.5, 0.0, 4.5, 4.0] },
    { week: 3, weekly_load: 24.0, daily_loads: [4.0, 5.0, 0.0, 6.0, 0.0, 5.0, 4.0] },
    { week: 4, weekly_load: 26.0, daily_loads: [4.5, 5.5, 0.0, 6.5, 0.0, 5.5, 4.0] },
  ])
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    
    try {
      const request: PredictionRequest = {
        athlete,
        training_history: trainingHistory,
      }
      
      const result = await predictInjuryRisk(request)
      
      // Store result in sessionStorage and navigate to results page
      sessionStorage.setItem('predictionResult', JSON.stringify(result))
      router.push('/results')
    } catch (err: any) {
      setError(err.response?.data?.detail || err.message || 'Prediction failed')
      console.error('Prediction error:', err)
    } finally {
      setLoading(false)
    }
  }
  
  const addWeek = () => {
    const newWeek = trainingHistory.length + 1
    setTrainingHistory([
      ...trainingHistory,
      {
        week: newWeek,
        weekly_load: 20.0,
        daily_loads: [3.0, 4.0, 0.0, 5.0, 0.0, 4.0, 4.0],
      },
    ])
  }
  
  const removeWeek = (index: number) => {
    setTrainingHistory(trainingHistory.filter((_, i) => i !== index))
  }
  
  const updateWeek = (index: number, field: keyof TrainingWeek, value: any) => {
    const updated = [...trainingHistory]
    updated[index] = { ...updated[index], [field]: value }
    setTrainingHistory(updated)
  }
  
  return (
    <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 py-12">
      <div className="container mx-auto px-4 max-w-4xl">
        <h1 className="text-4xl font-bold text-gray-900 mb-8 text-center">
          Predict Injury Risk
        </h1>
        
        <form onSubmit={handleSubmit} className="bg-white p-8 rounded-lg shadow-lg">
          {/* Athlete Profile Section */}
          <section className="mb-8">
            <h2 className="text-2xl font-bold mb-4">Athlete Profile</h2>
            <div className="grid md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Age
                </label>
                <input
                  type="number"
                  min="18"
                  max="100"
                  value={athlete.age}
                  onChange={(e) =>
                    setAthlete({ ...athlete, age: parseInt(e.target.value) })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Experience (years)
                </label>
                <input
                  type="number"
                  min="0"
                  value={athlete.experience_years}
                  onChange={(e) =>
                    setAthlete({
                      ...athlete,
                      experience_years: parseInt(e.target.value),
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Baseline Weekly Load (miles)
                </label>
                <input
                  type="number"
                  min="0.1"
                  step="0.1"
                  value={athlete.baseline_weekly_load}
                  onChange={(e) =>
                    setAthlete({
                      ...athlete,
                      baseline_weekly_load: parseFloat(e.target.value),
                    })
                  }
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  required
                />
              </div>
            </div>
          </section>
          
          {/* Training History Section */}
          <section className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold">Training History</h2>
              <button
                type="button"
                onClick={addWeek}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Add Week
              </button>
            </div>
            
            <div className="space-y-4">
              {trainingHistory.map((week, index) => (
                <div
                  key={index}
                  className="border border-gray-200 rounded-lg p-4"
                >
                  <div className="flex justify-between items-center mb-3">
                    <h3 className="font-semibold">Week {week.week}</h3>
                    {trainingHistory.length > 1 && (
                      <button
                        type="button"
                        onClick={() => removeWeek(index)}
                        className="text-red-600 hover:text-red-800"
                      >
                        Remove
                      </button>
                    )}
                  </div>
                  <div className="grid md:grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Weekly Load (miles)
                      </label>
                      <input
                        type="number"
                        min="0.1"
                        step="0.1"
                        value={week.weekly_load}
                        onChange={(e) =>
                          updateWeek(index, 'weekly_load', parseFloat(e.target.value))
                        }
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                        required
                      />
                    </div>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Daily Loads (comma-separated, 7 values)
                      </label>
                      <input
                        type="text"
                        value={week.daily_loads.join(', ')}
                        onChange={(e) => {
                          const values = e.target.value
                            .split(',')
                            .map((v) => parseFloat(v.trim()) || 0)
                          updateWeek(index, 'daily_loads', values)
                        }}
                        placeholder="3.0, 4.0, 0.0, 5.0, 0.0, 4.0, 4.0"
                        className="w-full px-3 py-2 border border-gray-300 rounded-md"
                        required
                      />
                    </div>
                  </div>
                </div>
              ))}
            </div>
            
            <p className="text-sm text-gray-600 mt-4">
              💡 Tip: At least 4 weeks of data recommended for accurate ACWR calculation
            </p>
          </section>
          
          {/* Error Display */}
          {error && (
            <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-red-800">{error}</p>
            </div>
          )}
          
          {/* Submit Button */}
          <button
            type="submit"
            disabled={loading}
            className="w-full bg-blue-600 text-white py-3 px-6 rounded-lg font-semibold hover:bg-blue-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors"
          >
            {loading ? 'Predicting...' : 'Predict Injury Risk'}
          </button>
        </form>
      </div>
    </main>
  )
}
