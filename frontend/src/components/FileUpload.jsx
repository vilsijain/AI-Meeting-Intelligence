
import React, { useState } from 'react'
import { uploadFile } from '../api'

export default function FileUpload({ onUploaded }){
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = async (e) => {
    const file = e.target.files?.[0]
    if(!file) return
    setLoading(true); setError(null)
    try{
      const res = await uploadFile(file)
      onUploaded?.(res.meeting_id)
    }catch(err){
      setError(String(err))
    }finally{
      setLoading(false)
    }
  }

  return (
    <div className="p-4 border-2 border-dashed rounded-2xl bg-white shadow-sm">
      <p className="text-sm mb-2">Upload audio/video</p>
      <input type="file" onChange={handleChange} accept=".mp3,.wav,.m4a,.mp4,.mov,.mkv,.webm"/>
      {loading && <p className="text-sm mt-2">Processing…</p>}
      {error && <p className="text-sm text-red-600 mt-2">{error}</p>}
    </div>
  )
}
