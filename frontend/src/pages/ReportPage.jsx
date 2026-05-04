import { useNavigate } from 'react-router-dom'
import useInventoryStore from '../store/useInventoryStore'

export default function ReportPage() {
  const navigate = useNavigate()
  const { analysisResult, reset } = useInventoryStore()

  if (!analysisResult) {
    navigate('/')
    return null
  }

  const { report, recommendations, summary, financial } = analysisResult

  return (
    <div className="min-h-screen bg-gray-950 p-8">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Executive Report</h1>
            <p className="text-gray-400 mt-1">AI-generated inventory optimization summary</p>
          </div>
          <div className="flex gap-3">
            <button onClick={() => navigate('/results')}
              className="px-5 py-2 border border-gray-700 text-gray-300 hover:border-gray-500 rounded-xl transition-colors">
              ← Back to Results
            </button>
            <button onClick={() => { reset(); navigate('/') }}
              className="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl transition-colors">
              New Analysis
            </button>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
            <div className="text-2xl font-bold text-amber-400">${financial.total_excess_value.toLocaleString()}</div>
            <div className="text-gray-500 text-sm mt-1">Excess Inventory</div>
          </div>
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
            <div className="text-2xl font-bold text-red-400">${financial.total_shortage_value.toLocaleString()}</div>
            <div className="text-gray-500 text-sm mt-1">Shortage Risk</div>
          </div>
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
            <div className="text-2xl font-bold text-green-400">${financial.potential_savings.toLocaleString()}</div>
            <div className="text-gray-500 text-sm mt-1">Potential Savings</div>
          </div>
        </div>

        {recommendations && recommendations.length > 0 && (
          <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-6">
            <h2 className="text-lg font-semibold text-white mb-4">Priority Recommendations</h2>
            <div className="space-y-3">
              {recommendations.map((rec, i) => (
                <div key={i} className="flex gap-3 p-4 bg-gray-800/50 rounded-xl">
                  <span className="text-blue-400 font-bold text-sm mt-0.5">{i + 1}</span>
                  <p className="text-gray-300 text-sm leading-relaxed">{rec}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6">
          <h2 className="text-lg font-semibold text-white mb-4">Full Executive Summary</h2>
          <div className="prose prose-invert prose-sm max-w-none">
            {report?.split('\n').map((line, i) => {
              if (line.startsWith('## ')) return <h2 key={i} className="text-white font-semibold text-base mt-6 mb-2">{line.replace('## ', '')}</h2>
              if (line.startsWith('### ')) return <h3 key={i} className="text-gray-200 font-medium text-sm mt-4 mb-1">{line.replace('### ', '')}</h3>
              if (line.startsWith('**') && line.endsWith('**')) return <p key={i} className="text-white font-semibold text-sm my-1">{line.replace(/\*\*/g, '')}</p>
              if (line.startsWith('- ')) return <p key={i} className="text-gray-300 text-sm my-1 pl-4">• {line.replace('- ', '')}</p>
              if (line.trim() === '') return <div key={i} className="h-2" />
              return <p key={i} className="text-gray-300 text-sm leading-relaxed">{line}</p>
            })}
          </div>
        </div>
      </div>
    </div>
  )
}