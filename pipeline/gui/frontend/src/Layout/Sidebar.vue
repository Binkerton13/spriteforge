<template>
  <div class="sidebar">
    <h2 class="title">SpriteForge</h2>

    <nav>
      <router-link to="/motion" class="item" active-class="active">Motion</router-link>
      <router-link to="/sprites" class="item" active-class="active">Sprites</router-link>
      <router-link to="/models" class="item" active-class="active">Models</router-link>
      <router-link to="/projects" class="item" active-class="active">Projects</router-link>
      <router-link to="/workflows/graph" class="item">Workflow Graph</router-link>
    </nav>
  </div>
</template>

<style scoped>
.sidebar {
  width: 220px;
  background: var(--bg-1);
  padding: 20px;
  display: flex;
  flex-direction: column;
  border-right: 1px solid var(--border);
  color: var(--fg-0);
}

.title {
  color: var(--accent-active);
  margin-bottom: 24px;
  font-size: 20px;
  font-weight: 600;
  text-shadow: var(--glow);
  transition: color var(--transition), text-shadow var(--transition);
}

nav {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.item {
  padding: 10px 12px;
  border-radius: var(--radius);
  color: var(--fg-0);
  text-decoration: none;
  background: var(--bg-2);
  transition: background var(--transition), color var(--transition), box-shadow var(--transition);
}

.item:hover {
  background: var(--accent-teal);
  color: white;
  box-shadow: var(--glow-teal);
}

.active {
  background: var(--accent-active);
  color: white;
  font-weight: 600;
  box-shadow: var(--glow-strong);
}

</style>
