
import React, { useEffect, useState } from 'react'
import { listMeetings } from '../api'

export default function MeetingList({ onSelect }){
  const [items, setItems] = useState([])

  useEffect(()=>{
    listMeetings().then(setItems).catch(console.error)
  }, [])

  return (
    <div className="bg-white rounded-2xl p-4 shadow-sm">
      <h2 className="font-semibold mb-2">Meetings</h2>
      <ul className="divide-y">
        {items.map(m => (
          <li key={m.id} className="py-2 cursor-pointer hover:bg-gray-50 px-2 rounded"
              onClick={()=>onSelect?.(m.id)}>
            <div className="text-sm font-medium">{m.title}</div>
            <div className="text-xs text-gray-500">{new Date(m.created_at).toLocaleString()}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}
