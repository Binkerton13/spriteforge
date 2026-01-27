export async function fetchStyles() {
  const res = await fetch('/api/styles')
  return res.json()
}

export async function fetchModels() {
  const res = await fetch('/api/models')
  return res.json()
}

export async function generateSprites(payload) {
  const res = await fetch('/api/sprites/generate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  return res.json()
}

export async function assembleSheet(payload) {
  const res = await fetch('/api/sprites/assemble', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload)
  })
  return res.json()
}

export async function fetchFrames() {
  const res = await fetch('/api/preview/frames')
  return res.json()
}

export function sheetPreviewUrl() {
  return '/api/preview/sheet'
}
