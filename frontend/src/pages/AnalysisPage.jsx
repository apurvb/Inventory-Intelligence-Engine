import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { analyzeInventory } from '../api/inventory'
import useInventoryStore from '../store/useInventoryStore'

const STEPS = [
  { id: 1, label: 'Detecting inventory imbalances', icon: '🔍' },
  { id: 2, label: 'Diagnosing root causes with AI', icon: '🧠' },
  { id: 3, label: 'Generating recommendations', icon: '📋' },
  { id: 4, label: 'Simulating financial impact', icon: '💰' },
  { id: 5, label: 'Writing executive report', icon: '📄' },
]

export default function AnalysisPage() {
  const navigate = useNavigate()
  const { sessionId, uploadData, setAnalysisResult } = useInventoryStore()
  const [currentStep, setCurrentStep] = useState(0)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!sessionId) { navigate('/'); return }
    runAnalysis()
  }, [])

  async function runAnalysis() {
    const interval = setInterval(() => {
      setCurrentStep(prev => prev < STEPS.length - 1 ? prev + 1 : prev)
    }, 4000)
    try {
      const result = await analyzeInventory(sessionId)
      clearInterval(interval)
      setCurrentStep(STEPS.length)
      setAnalysisResult(result)
      setTimeout(() => navigate('/results'), 800)
    } catch (err) {
      clearInterval(interval)
      setError(err.response?.data?.detail || 'Analysis failed. Please try again.')
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center p-8">
      <div className="w-full max-w-lg">
        <h2 className="text-2xl font-bold text-white mb-2 text-center">Analyzing Inventory</h2>
        {uploadData && (
          <p className="text-gray-400 text-center mb-10">
            Processing {uploadData.rows_parsed} SKUs across locations
          </p>
        )}

        <div className="space-y-4">
          {STEPS.map((step, index) => {
            const done = index < currentStep
            const active = index === currentStep
            return (
              <div key={step.id} className={`flex items-center gap-4 p-4 rounded-xl border transition-all duration-500
                ${done ? 'border-green-800 bg-green-950/30' : active ? 'border-blue-700 bg-blue-950/30' : 'border-gray-800 bg-gray-900'}`}>
                <span className="text-2xl">{step.icon}</span>
                <span className={`flex-1 text-sm font-medium
                  ${done ? 'text-green-400' : active ? 'text-blue-300' : 'text-gray-600'}`}>
                  {step.label}
                </span>
                {done && <span className="text-green-400 text-lg">✓</span>}
                {active && (
                  <div className="w-5 h-5 border-2 border-blue-400 border-t-transparent rounded-full animate-spin" />
                )}
              </div>
            )
          })}
        </div>

        {error && (
          <div className="mt-6 p-4 bg-red-900/40 border border-red-700 rounded-xl text-red-300 text-sm">
            {error}
            <button onClick={() => navigate('/')} className="block mt-2 text-red-400 underline">
              Start over
            </button>
          </div>
        )}
      </div>
    </div>
  )
}