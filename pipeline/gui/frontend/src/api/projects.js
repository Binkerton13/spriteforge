// src/api/projects.js
export async function listProjects() {
  const res = await fetch('/api/project/list')
  return res.json()
}

export async function createProject(name) {
  const res = await fetch('/api/project/create', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  })
  return res.json()
}

export async function loadProject(project_id) {
  const res = await fetch(`/api/project/${project_id}`)
  return res.json()
}

export async function updateProject(project_id, metadata) {
  const res = await fetch(`/api/project/${project_id}/update`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(metadata)
  })
  return res.json()
}
