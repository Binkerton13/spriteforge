// src/api/models.js
export async function listModels() {
  const res = await fetch('/api/models')
  return res.json()
}

export async function uploadModel(formData) {
  const res = await fetch('/api/models/upload', {
    method: 'POST',
    body: formData
  })
  return res.json()
}

export async function deleteModel(name) {
  const res = await fetch(`/api/models/delete/${encodeURIComponent(name)}`, {
    method: 'DELETE'
  })
  return res.json()
}

export async function setActiveModel(model) {
  const res = await fetch('/api/models/active', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ model })
  })
  return res.json()
}
