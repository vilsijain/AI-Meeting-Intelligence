
import React, { useState } from 'react'
import FileUpload from './components/FileUpload'
import MeetingList from './components/MeetingList'
import Dashboard from './components/Dashboard'
import SearchBar from './components/SearchBar'

export default function App(){
  const [meetingId, setMeetingId] = useState(null)

  return (
    <div className="max-w-6xl mx-auto p-6 space-y-4">
      <header className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">AI Meeting Intelligence</h1>
        <div className="text-xs text-gray-500">FastAPI + React + ChromaDB</div>
      </header>

      <div className="grid md:grid-cols-3 gap-4">
        <div className="space-y-4">
          <FileUpload onUploaded={setMeetingId} />
          <MeetingList onSelect={setMeetingId} />
          <SearchBar meetingId={meetingId} />
        </div>
        <div className="md:col-span-2">
          <Dashboard meetingId={meetingId} />
        </div>
      </div>
    </div>
  )
}
