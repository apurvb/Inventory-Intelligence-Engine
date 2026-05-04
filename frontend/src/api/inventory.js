import client from './client'

export const uploadCSV = async (file) => {
  const formData = new FormData()
  formData.append('file', file)
  const res = await client.post('/upload', formData)
  return res.data
}

export const analyzeInventory = async (sessionId) => {
  const res = await client.post(`/analyze/${sessionId}`)
  return res.data
}

export const getReport = async (sessionId) => {
  const res = await client.get(`/report/${sessionId}`)
  return res.data
}