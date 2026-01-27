export async function fetchPresets() {
  const res = await fetch('/api/motion/presets')
  return res.json()
}

export async function generateMotion(payload) {
  const res = await fetch('/api/motion/generate', {
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

export function previewVideoUrl() {
  return '/api/preview/video'
}
