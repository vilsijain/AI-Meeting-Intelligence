
import React from 'react'

export default function ActionItems({ items = [] }){
  return (
    <div className="bg-white rounded-2xl p-4 shadow-sm">
      <h2 className="font-semibold mb-2">Action Items</h2>
      <ul className="space-y-2">
        {items.map((a, i)=>(
          <li key={i} className="p-3 border rounded-xl">
            <div className="text-sm">{a.description}</div>
            <div className="text-xs text-gray-500">
              Owner: {a.owner || '—'} • Due: {a.due_date || '—'} • Priority: {a.priority || '—'}
            </div>
          </li>
        ))}
      </ul>
    </div>
  )
}
