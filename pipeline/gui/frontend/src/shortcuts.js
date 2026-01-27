export function registerShortcuts(app) {
  window.addEventListener('keydown', (e) => {
    const key = e.key.toLowerCase()
    const ctrl = e.ctrlKey || e.metaKey
    const shift = e.shiftKey

    // --- Navigation ---
    if (ctrl && !shift) {
      if (key === '1') app.config.globalProperties.$router.push('/motion')
      if (key === '2') app.config.globalProperties.$router.push('/sprites')
      if (key === '3') app.config.globalProperties.$router.push('/workflows')
      if (key === '4') app.config.globalProperties.$router.push('/models')
      if (key === '5') app.config.globalProperties.$router.push('/projects')
    }

    // --- Save Project ---
    if (ctrl && key === 's') {
      e.preventDefault()
      const store = app.config.globalProperties.$projects
      if (store?.save) store.save()
    }

    // --- Generate Motion ---
    if (ctrl && key === 'g' && !shift) {
      const store = app.config.globalProperties.$motion
      if (store?.runGeneration) store.runGeneration()
    }

    // --- Generate Sprites ---
    if (ctrl && shift && key === 'g') {
      const store = app.config.globalProperties.$sprites
      if (store?.runGeneration) store.runGeneration()
    }

    // --- Close modals ---
    if (key === 'escape') {
      const store = app.config.globalProperties.$files
      if (store) store.selected = null
    }

    const topbar = document.querySelector('.topbar')
    if (topbar) {
    topbar.classList.add('flash')
    setTimeout(() => topbar.classList.remove('flash'), 300)
    }

  })
}
