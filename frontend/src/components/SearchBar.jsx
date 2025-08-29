
import React, { useState } from 'react'
import { search } from '../api'

export default function SearchBar({ meetingId }){
  const [q, setQ] = useState('')
  const [results, setResults] = useState([])

  const run = async (e)=>{
    e.preventDefault()
    const res = await search(q, meetingId)
    setResults(res)
  }

  return (
    <div className="bg-white rounded-2xl p-4 shadow-sm">
      <form onSubmit={run} className="flex gap-2">
        <input value={q} onChange={e=>setQ(e.target.value)} placeholder="Search transcript…"
               className="border rounded-xl px-3 py-2 flex-1"/>
        <button className="px-4 py-2 rounded-xl bg-black text-white">Search</button>
      </form>
      <ul className="mt-3 space-y-2">
        {results.map((r, i)=>(
          <li key={i} className="text-sm p-2 border rounded-xl">
            <div>{r.text}</div>
            <div className="text-xs text-gray-500">distance: {r.distance.toFixed(3)} • meeting: {r.meeting_id}</div>
          </li>
        ))}
      </ul>
    </div>
  )
}
