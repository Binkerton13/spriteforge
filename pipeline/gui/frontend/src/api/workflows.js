// src/api/workflows.js
export async function loadWorkflow(type, project_id) {
  const res = await fetch(`/api/workflow/${type}/load?project_id=${project_id}`)
  return res.json()
}

export async function saveWorkflow(type, project_id, workflow) {
  const res = await fetch(`/api/workflow/${type}/save`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ project_id, workflow })
  })
  return res.json()
}
