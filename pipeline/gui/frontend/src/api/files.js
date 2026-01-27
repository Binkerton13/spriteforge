export async function listFiles(path = '') {
  const res = await fetch(`/api/files/list?path=${encodeURIComponent(path)}`)
  return res.json()
}

export async function uploadFile(path, file) {
  const form = new FormData()
  form.append('file', file)

  const res = await fetch(`/api/files/upload?path=${encodeURIComponent(path)}`, {
    method: 'POST',
    body: form
  })
  return res.json()
}

export async function deleteFile(path) {
  const res = await fetch(`/api/files/delete?path=${encodeURIComponent(path)}`, {
    method: 'DELETE'
  })
  return res.json()
}
