
import React, { useEffect, useState } from 'react'
import { getMeeting } from '../api'
import ActionItems from './ActionItems'
import Analytics from './Analytics'

export default function Dashboard({ meetingId }){
  const [data, setData] = useState(null)

  useEffect(()=>{
    if(!meetingId) return
    getMeeting(meetingId).then(setData).catch(console.error)
  }, [meetingId])

  if(!meetingId) return <div className="p-6 text-gray-500">Select or upload a meeting.</div>
  if(!data) return <div className="p-6">Loading meeting…</div>

  return (
    <div className="grid md:grid-cols-2 gap-4">
      <div className="bg-white rounded-2xl p-4 shadow-sm md:col-span-2">
        <h1 className="text-lg font-semibold">{data.title}</h1>
        <p className="text-sm text-gray-500">Created: {new Date(data.created_at).toLocaleString()}</p>
      </div>

      <div className="bg-white rounded-2xl p-4 shadow-sm md:col-span-2">
        <h2 className="font-semibold mb-2">Transcript</h2>
        <p className="text-sm whitespace-pre-wrap">{data.transcript}</p>
      </div>

      <ActionItems items={data.action_items} />
      <Analytics participants={data.participants} />

      <div className="bg-white rounded-2xl p-4 shadow-sm md:col-span-2">
        <h2 className="font-semibold mb-2">Decisions</h2>
        <ul className="list-disc ml-5 text-sm">
          {data.decisions.map((d, i)=>(<li key={i}>{d.summary}</li>))}
        </ul>
      </div>
    </div>
  )
}
