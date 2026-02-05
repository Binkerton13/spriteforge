export async function loadMotionPresets() {
  const res = await fetch('/api/motion-presets/')
  return res.json()
}

export async function saveAllMotionPresets(presets) {
  await fetch('/api/motion-presets/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ presets })
  })
}

export async function deleteMotionPreset(name) {
  await fetch('/api/motion-presets/delete', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name })
  })
}
