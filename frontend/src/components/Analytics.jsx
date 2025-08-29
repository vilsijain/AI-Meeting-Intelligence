
import React from 'react'

export default function Analytics({ participants = [] }){
  // Simple analytics: total speakers and total time
  const totalTime = (participants || []).reduce((s,p)=> s + (p.spoke_time_sec || 0), 0)
  return (
    <div className="bg-white rounded-2xl p-4 shadow-sm">
      <h2 className="font-semibold mb-2">Analytics</h2>
      <div className="text-sm">Participants: {participants?.length || 0}</div>
      <div className="text-sm">Total speaking time: {Math.round(totalTime)} sec</div>
      <p className="text-xs text-gray-500 mt-2">Add charts later (e.g., Recharts) for speaking-time distribution, action-item owners, etc.</p>
    </div>
  )
}
