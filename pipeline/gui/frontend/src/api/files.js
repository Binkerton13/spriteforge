// src/api/files.js
export async function listFiles(project_id, path = '') {
  const res = await fetch(`/api/files/list?project_id=${project_id}&path=${encodeURIComponent(path)}`)
  return res.json()
}

export async function uploadFile(project_id, path, file) {
  const form = new FormData()
  form.append('project_id', project_id)
  form.append('path', path)
  form.append('file', file)

  const res = await fetch('/api/files/upload', {
    method: 'POST',
    body: form
  })
  return res.json()
}
