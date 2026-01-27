export async function fetchWorkflows() {
  const res = await fetch('/api/workflows')
  return res.json()
}

export async function loadWorkflow(name) {
  const res = await fetch(`/api/workflows/${name}`)
  return res.json()
}

export async function saveWorkflow(name, data) {
  const res = await fetch(`/api/workflows/${name}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return res.json()
}

export async function validateWorkflow(data) {
  const res = await fetch('/api/workflows/validate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  })
  return res.json()
}

export async function fetchNodes(name) {
  const res = await fetch(`/api/workflows/nodes/${name}`)
  return res.json()
}

export async function fetchNodeDetails(name, nodeId) {
  const res = await fetch(`/api/workflows/node/${name}/${nodeId}`)
  return res.json()
}
