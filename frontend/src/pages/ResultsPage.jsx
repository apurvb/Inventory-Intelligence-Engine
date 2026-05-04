import { useNavigate } from 'react-router-dom'
import useInventoryStore from '../store/useInventoryStore'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const STATUS_COLORS = {
  overstocked: '#f59e0b',
  understocked: '#3b82f6',
  critically_understocked: '#ef4444',
  healthy: '#22c55e',
}

const STATUS_LABELS = {
  overstocked: 'Overstocked',
  understocked: 'Understocked',
  critically_understocked: 'Critical',
  healthy: 'Healthy',
}

export default function ResultsPage() {
  const navigate = useNavigate()
  const { analysisResult } = useInventoryStore()

  if (!analysisResult) {
    navigate('/')
    return null
  }

  const { summary, financial, skus } = analysisResult

  const kpis = [
    { label: 'Total SKUs', value: summary.total_skus, color: 'text-white' },
    { label: 'Overstocked', value: summary.overstocked_count, color: 'text-amber-400' },
    { label: 'Understocked', value: summary.understocked_count, color: 'text-blue-400' },
    { label: 'Critical', value: summary.critical_count, color: 'text-red-400' },
    { label: 'Healthy', value: summary.healthy_count, color: 'text-green-400' },
  ]

  const financialKpis = [
    { label: 'Excess Inventory Value', value: `$${financial.total_excess_value.toLocaleString()}`, color: 'text-amber-400' },
    { label: 'Shortage Risk Value', value: `$${financial.total_shortage_value.toLocaleString()}`, color: 'text-red-400' },
    { label: 'Annual Holding Cost', value: `$${financial.total_holding_cost.toLocaleString()}`, color: 'text-orange-400' },
    { label: 'Potential Savings', value: `$${financial.potential_savings.toLocaleString()}`, color: 'text-green-400' },
  ]

  const chartData = skus.map(s => ({
    name: s.sku_id,
    current: s.current_stock,
    reorder: s.reorder_point,
    max: s.max_stock,
    status: s.status,
  }))

  return (
    <div className="min-h-screen bg-gray-950 p-8">
      <div className="max-w-7xl mx-auto">
        <div className="flex items-center justify-between mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Inventory Analysis Results</h1>
            <p className="text-gray-400 mt-1">AI-powered optimization complete</p>
          </div>
          <button onClick={() => navigate('/report')}
            className="px-6 py-3 bg-blue-600 hover:bg-blue-500 text-white rounded-xl font-medium transition-colors">
            View Executive Report →
          </button>
        </div>

        <div className="grid grid-cols-5 gap-4 mb-8">
          {kpis.map(k => (
            <div key={k.label} className="bg-gray-900 border border-gray-800 rounded-2xl p-5 text-center">
              <div className={`text-3xl font-bold ${k.color}`}>{k.value}</div>
              <div className="text-gray-500 text-sm mt-1">{k.label}</div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-4 gap-4 mb-8">
          {financialKpis.map(k => (
            <div key={k.label} className="bg-gray-900 border border-gray-800 rounded-2xl p-5">
              <div className={`text-2xl font-bold ${k.color}`}>{k.value}</div>
              <div className="text-gray-500 text-sm mt-1">{k.label}</div>
            </div>
          ))}
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-6 mb-8">
          <h2 className="text-lg font-semibold text-white mb-6">Stock Levels vs Thresholds</h2>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={chartData} margin={{ top: 5, right: 20, left: 20, bottom: 5 }}>
              <XAxis dataKey="name" stroke="#6b7280" />
              <YAxis stroke="#6b7280" />
              <Tooltip contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px' }} />
              <Bar dataKey="current" name="Current Stock" radius={[4, 4, 0, 0]}>
                {chartData.map((entry, i) => (
                  <Cell key={i} fill={STATUS_COLORS[entry.status]} />
                ))}
              </Bar>
              <Bar dataKey="reorder" name="Reorder Point" fill="#374151" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-gray-900 border border-gray-800 rounded-2xl overflow-hidden">
          <div className="p-6 border-b border-gray-800">
            <h2 className="text-lg font-semibold text-white">SKU Detail Table</h2>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b border-gray-800">
                  {['SKU', 'Location', 'Status', 'Current Stock', 'Reorder Point', 'Max Stock', 'Days of Stock', 'Excess Value', 'Shortage Value'].map(h => (
                    <th key={h} className="text-left text-gray-500 font-medium px-4 py-3">{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {skus.map((sku, i) => (
                  <tr key={i} className="border-b border-gray-800/50 hover:bg-gray-800/30 transition-colors">
                    <td className="px-4 py-3 font-mono text-blue-300">{sku.sku_id}</td>
                    <td className="px-4 py-3 text-gray-300">{sku.location}</td>
                    <td className="px-4 py-3">
                      <span className="px-2 py-1 rounded-lg text-xs font-medium"
                        style={{ backgroundColor: STATUS_COLORS[sku.status] + '33', color: STATUS_COLORS[sku.status] }}>
                        {STATUS_LABELS[sku.status]}
                      </span>
                    </td>
                    <td className="px-4 py-3 text-gray-300">{sku.current_stock.toLocaleString()}</td>
                    <td className="px-4 py-3 text-gray-300">{sku.reorder_point.toLocaleString()}</td>
                    <td className="px-4 py-3 text-gray-300">{sku.max_stock.toLocaleString()}</td>
                    <td className="px-4 py-3 text-gray-300">{sku.days_of_stock}</td>
                    <td className="px-4 py-3 text-amber-400">${sku.excess_value.toLocaleString()}</td>
                    <td className="px-4 py-3 text-red-400">${sku.shortage_value.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  )
}