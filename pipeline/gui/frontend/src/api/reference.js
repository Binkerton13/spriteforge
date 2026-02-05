// src/api/reference.js
export async function uploadReference(project_id, file) {
  const form = new FormData()
  form.append('project_id', project_id)
  form.append('file', file)

  const res = await fetch('/api/reference/upload', {
    method: 'POST',
    body: form
  })
  return res.json()
}

export async function describeReferences(paths) {
  const res = await fetch('/api/reference/describe', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ paths })
  })
  return res.json()
}
