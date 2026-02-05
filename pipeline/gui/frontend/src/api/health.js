// src/api/health.js
export async function checkHealth() {
  const res = await fetch('/api/health')
  return res.json()
}
