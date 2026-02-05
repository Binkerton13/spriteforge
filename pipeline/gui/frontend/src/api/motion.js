// src/api/motion.js
export async function suggestMotion(prompt, preset = {}) {
  const res = await fetch('/api/ai/motion/suggest', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, preset })
  })
  return res.json()
}

export async function refineMotion(prompt, existing_motion) {
  const res = await fetch('/api/ai/motion/refine', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ prompt, existing_motion })
  })
  return res.json()
}

export async function styleMotion(style, existing_motion) {
  const res = await fetch('/api/ai/motion/style', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ style, existing_motion })
  })
  return res.json()
}

export async function translateMotion(existing_motion, target_language) {
  const res = await fetch('/api/ai/motion/translate', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ existing_motion, target_language })
  })
  return res.json()
}
