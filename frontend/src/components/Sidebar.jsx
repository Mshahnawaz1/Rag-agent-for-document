import { useState } from 'react'

function Sidebar({ onUpload, onClearDB, queryMode, onQueryModeChange }) {
  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    setFile(selectedFile)
  }

  const handleUploadClick = async () => {
    if (!file) {
      alert('Please select a file.')
      return
    }

    setUploading(true)
    try {
      await onUpload(file)
      setFile(null)
      // Reset file input
      const fileInput = document.getElementById('fileInput')
      if (fileInput) fileInput.value = ''
    } finally {
      setUploading(false)
    }
  }

  return (
    <aside className="sidebar">
      <h2>Controls</h2>

      <div className="sidebar-section">
        <label className="sidebar-label">
          Upload Document
        </label>
        <input
          id="fileInput"
          type="file"
          accept=".pdf,.txt,.docx"
          onChange={handleFileChange}
          className="file-input"
        />
        <button
          onClick={handleUploadClick}
          disabled={!file || uploading}
          className="btn btn-primary"
        >
          {uploading ? 'Uploading...' : 'Upload & Process'}
        </button>
      </div>

      <div className="sidebar-section">
        <button
          onClick={onClearDB}
          className="btn btn-danger"
        >
          Clear Database
        </button>
      </div>

      <div className="sidebar-section">
        <span className="sidebar-label">Question Mode</span>
        <div className="radio-group">
          <label className="radio-label">
            <input
              type="radio"
              name="queryMode"
              value="general"
              checked={queryMode === 'general'}
              onChange={(e) => onQueryModeChange(e.target.value)}
            />
            <span>Uploaded Documents</span>
          </label>
          <label className="radio-label">
            <input
              type="radio"
              name="queryMode"
              value="ncert"
              checked={queryMode === 'ncert'}
              onChange={(e) => onQueryModeChange(e.target.value)}
            />
            <span>NCERT Knowledge Base</span>
          </label>
        </div>
      </div>
    </aside>
  )
}

export default Sidebar
