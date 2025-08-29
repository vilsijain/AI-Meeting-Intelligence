
const API = import.meta.env.VITE_API_URL || 'http://localhost:8000'

export async function uploadFile(file){
  const fd = new FormData()
  fd.append('file', file)
  const res = await fetch(`${API}/api/upload`, { method: 'POST', body: fd })
  if(!res.ok) throw new Error(await res.text())
  return res.json()
}

export async function listMeetings(){
  const res = await fetch(`${API}/api/meetings`)
  return res.json()
}

export async function getMeeting(id){
  const res = await fetch(`${API}/api/meetings/${id}`)
  return res.json()
}

export async function search(q, meeting_id){
  const params = new URLSearchParams({ q })
  if(meeting_id) params.append('meeting_id', meeting_id)
  const res = await fetch(`${API}/api/search?${params.toString()}`)
  return res.json()
}
