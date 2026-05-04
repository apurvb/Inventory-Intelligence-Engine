import axios from 'axios'

const client = axios.create({
  baseURL: 'http://localhost:8000/api',
  timeout: 120000,
})

export default client