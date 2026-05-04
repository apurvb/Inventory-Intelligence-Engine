import { create } from 'zustand'

const useInventoryStore = create((set) => ({
  sessionId: null,
  uploadData: null,
  analysisResult: null,
  isAnalyzing: false,

  setSessionId: (id) => set({ sessionId: id }),
  setUploadData: (data) => set({ uploadData: data }),
  setAnalysisResult: (result) => set({ analysisResult: result }),
  setIsAnalyzing: (val) => set({ isAnalyzing: val }),
  reset: () => set({ sessionId: null, uploadData: null, analysisResult: null, isAnalyzing: false }),
}))

export default useInventoryStore