export async function fetchModelTypes() {
  const res = await fetch('/api/models')
  return res.json()
}

export async function fetchModelsByType(type) {
  const res = await fetch(`/api/models/${type}`)
  return res.json()
}

export async function fetchActiveModel() {
  const res = await fetch('/api/models/active')
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
