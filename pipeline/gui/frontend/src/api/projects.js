export async function fetchProjects() {
  const res = await fetch('/api/project/list')
  return res.json()
}

export async function loadProject(id) {
  const res = await fetch(`/api/project/load/${id}`)
  return res.json()
}

export async function saveProject(payload) {
  const res = await fetch('/api/project/save', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  return res.json()
}
