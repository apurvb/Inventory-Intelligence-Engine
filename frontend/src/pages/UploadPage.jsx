import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { useDropzone } from 'react-dropzone'
import { uploadCSV } from '../api/inventory'
import useInventoryStore from '../store/useInventoryStore'

export default function UploadPage() {
  const navigate = useNavigate()
  const { setSessionId, setUploadData } = useInventoryStore()
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0]
    if (!file) return
    setError(null)
    setLoading(true)
    try {
      const data = await uploadCSV(file)
      setSessionId(data.session_id)
      setUploadData(data)
      navigate('/analysis')
    } catch (err) {
      setError(err.response?.data?.detail || 'Upload failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop, accept: { 'text/csv': ['.csv'] }, maxFiles: 1
  })

  return (
    <div className="min-h-screen bg-gray-950 flex flex-col items-center justify-center p-8">
      <div className="mb-10 text-center">
        <h1 className="text-4xl font-bold text-white mb-2">Inventory Intelligence Engine</h1>
        <p className="text-gray-400 text-lg">Multi-agent AI powered inventory optimization</p>
      </div>

      <div className="w-full max-w-2xl">
        <div {...getRootProps()} className={`border-2 border-dashed rounded-2xl p-16 text-center cursor-pointer transition-all duration-200
          ${isDragActive ? 'border-blue-400 bg-blue-950/30' : 'border-gray-700 bg-gray-900 hover:border-gray-500 hover:bg-gray-800'}`}>
          <input {...getInputProps()} />
          <div className="text-5xl mb-4">📦</div>
          {loading ? (
            <p className="text-blue-400 text-lg font-medium">Uploading and parsing CSV...</p>
          ) : isDragActive ? (
            <p className="text-blue-400 text-lg font-medium">Drop your CSV here</p>
          ) : (
            <>
              <p className="text-white text-lg font-medium mb-2">Drag & drop your inventory CSV</p>
              <p className="text-gray-500 text-sm">or click to browse files</p>
            </>
          )}
        </div>

        {error && (
          <div className="mt-4 p-4 bg-red-900/40 border border-red-700 rounded-xl text-red-300 text-sm">
            {error}
          </div>
        )}

        <div className="mt-8 p-6 bg-gray-900 rounded-2xl border border-gray-800">
          <p className="text-gray-400 text-sm font-medium mb-3">Required CSV columns:</p>
          <div className="grid grid-cols-2 gap-2">
            {['sku_id','location','current_stock','avg_daily_demand',
              'demand_std_dev','lead_time_days','lead_time_std_dev','unit_cost'].map(col => (
              <span key={col} className="text-xs font-mono bg-gray-800 text-blue-300 px-3 py-1 rounded-lg">{col}</span>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}