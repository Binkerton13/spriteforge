// src/api/sprites.js
export async function runSpriteWorkflow(payload) {
  const res = await fetch('/api/workflow/sprite/run', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  return res.json()
}
