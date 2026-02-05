export function normalizeForHyMotion(value) {
  if (typeof value === 'string') {
    return value.trim()
  }

  if (Array.isArray(value)) {
    return value
      .map(step => {
        if (typeof step === 'string') return step
        if (step.timing && step.value) {
          return `${step.timing}: ${step.value}`
        }
        return JSON.stringify(step)
      })
      .join("; ")
  }

  if (typeof value === 'object' && value !== null) {
    return Object.entries(value)
      .map(([k, v]) => `${k}: ${normalizeForHyMotion(v)}`)
      .join("; ")
  }

  return String(value)
}
