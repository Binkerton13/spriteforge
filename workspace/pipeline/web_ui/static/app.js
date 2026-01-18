// 3D Character Pipeline - Web UI JavaScript

// Global state
let currentProject = null;
let scene, camera, renderer, controls;
let currentModel = null;
let wireframeMode = false;
let gridHelper = null;
const API_BASE = window.location.origin;

// ===================================
// Initialization
// ===================================

document.addEventListener('DOMContentLoaded', () => {
    initViewer3D();
    loadProjects();
    checkSystemStatus();
    setInterval(checkSystemStatus, 30000); // Check every 30s
});

// ===================================
// 3D Viewer Setup
// ===================================

function initViewer3D() {
    const container = document.getElementById('viewer3d');
    
    // Scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x0a0a0a);
    
    // Camera
    camera = new THREE.PerspectiveCamera(
        50,
        container.clientWidth / container.clientHeight,
        0.1,
        1000
    );
    camera.position.set(3, 2, 3);
    
    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(container.clientWidth, container.clientHeight);
    renderer.shadowMap.enabled = true;
    container.appendChild(renderer.domElement);
    
    // Controls
    controls = new THREE.OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.dampingFactor = 0.05;
    
    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
    directionalLight.position.set(5, 10, 5);
    directionalLight.castShadow = true;
    scene.add(directionalLight);
    
    const directionalLight2 = new THREE.DirectionalLight(0x4a9eff, 0.3);
    directionalLight2.position.set(-5, 5, -5);
    scene.add(directionalLight2);
    
    // Grid
    gridHelper = new THREE.GridHelper(10, 10, 0x3a3a3a, 0x2a2a2a);
    scene.add(gridHelper);
    
    // Handle window resize
    window.addEventListener('resize', onWindowResize);
    
    // Animation loop
    animate();
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

function onWindowResize() {
    const container = document.getElementById('viewer3d');
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
}

// ===================================
// 3D Model Loading
// ===================================

function loadModelIntoViewer(file) {
    const fileExtension = file.name.split('.').pop().toLowerCase();
    const reader = new FileReader();
    
    reader.onload = (e) => {
        // Remove existing model
        if (currentModel) {
            scene.remove(currentModel);
        }
        
        if (fileExtension === 'fbx') {
            const loader = new THREE.FBXLoader();
            loader.load(e.target.result, (fbx) => {
                setupModel(fbx, file.name);
            });
        } else if (fileExtension === 'obj') {
            const loader = new THREE.OBJLoader();
            loader.load(e.target.result, (obj) => {
                setupModel(obj, file.name);
            });
        }
    };
    
    reader.readAsDataURL(file);
}

function setupModel(model, filename) {
    currentModel = model;
    
    // Center and scale model
    const box = new THREE.Box3().setFromObject(model);
    const center = box.getCenter(new THREE.Vector3());
    const size = box.getSize(new THREE.Vector3());
    
    const maxDim = Math.max(size.x, size.y, size.z);
    const scale = 2 / maxDim;
    model.scale.multiplyScalar(scale);
    
    model.position.sub(center.multiplyScalar(scale));
    
    // Add material
    model.traverse((child) => {
        if (child.isMesh) {
            child.material = new THREE.MeshStandardMaterial({
                color: 0x808080,
                metalness: 0.3,
                roughness: 0.7
            });
            child.castShadow = true;
            child.receiveShadow = true;
        }
    });
    
    scene.add(model);
    
    // Update stats
    updateModelStats(model);
    
    // Reset camera
    resetCamera();
}

function updateModelStats(model) {
    let vertices = 0;
    let faces = 0;
    
    model.traverse((child) => {
        if (child.isMesh) {
            if (child.geometry.attributes.position) {
                vertices += child.geometry.attributes.position.count;
            }
            if (child.geometry.index) {
                faces += child.geometry.index.count / 3;
            }
        }
    });
    
    document.getElementById('vertexCount').textContent = `Vertices: ${vertices.toLocaleString()}`;
    document.getElementById('faceCount').textContent = `Faces: ${Math.floor(faces).toLocaleString()}`;
    document.getElementById('meshFormat').textContent = `Format: ${currentModel.type}`;
}

// ===================================
// Viewer Controls
// ===================================

function resetCamera() {
    camera.position.set(3, 2, 3);
    camera.lookAt(0, 0, 0);
    controls.target.set(0, 0, 0);
}

function toggleWireframe() {
    wireframeMode = !wireframeMode;
    if (currentModel) {
        currentModel.traverse((child) => {
            if (child.isMesh) {
                child.material.wireframe = wireframeMode;
            }
        });
    }
}

function toggleGrid() {
    gridHelper.visible = !gridHelper.visible;
}

// ===================================
// File Upload Handling
// ===================================

function handleDragOver(event) {
    event.preventDefault();
    event.currentTarget.classList.add('drag-over');
}

function handleDragLeave(event) {
    event.currentTarget.classList.remove('drag-over');
}

function handleDrop(event, type) {
    event.preventDefault();
    event.currentTarget.classList.remove('drag-over');
    
    const files = event.dataTransfer.files;
    if (files.length > 0) {
        processFiles(files, type);
    }
}

function handleFileSelect(event, type) {
    const files = event.target.files;
    if (files.length > 0) {
        processFiles(files, type);
    }
}

function processFiles(files, type) {
    if (!currentProject) {
        showError('Please select or create a project first');
        return;
    }
    
    switch(type) {
        case 'mesh':
            if (files.length > 0) {
                uploadFile(files[0], type);
                loadModelIntoViewer(files[0]);
            }
            break;
        case 'udim':
            Array.from(files).forEach(file => uploadFile(file, type));
            break;
        case 'reference':
            Array.from(files).forEach(file => uploadFile(file, type));
            break;
    }
}

async function uploadFile(file, type) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);
    formData.append('project', currentProject);
    
    try {
        showUploadProgress(true, `Uploading ${file.name}...`);
        
        const response = await fetch(`${API_BASE}/api/upload`, {
            method: 'POST',
            body: formData
        });
        
        const result = await response.json();
        
        if (result.status === 'success') {
            showUploadProgress(false);
            updateFileDisplay(file, type);
            showSuccess(`Uploaded ${file.name}`);
        } else {
            showError(`Upload failed: ${result.message}`);
        }
    } catch (error) {
        showError(`Upload error: ${error.message}`);
    }
}

function updateFileDisplay(file, type) {
    if (type === 'mesh') {
        const info = document.getElementById('meshInfo');
        info.style.display = 'block';
        info.textContent = `✓ ${file.name} (${formatFileSize(file.size)})`;
    } else if (type === 'udim') {
        const list = document.getElementById('udimList');
        const item = document.createElement('div');
        item.className = 'file-item';
        item.innerHTML = `
            <span>${file.name}</span>
            <span class="file-item-remove" onclick="removeFile('${file.name}', 'udim')">✕</span>
        `;
        list.appendChild(item);
    }
}

function showUploadProgress(show, text = '') {
    const progress = document.getElementById('uploadProgress');
    const progressText = document.getElementById('progressText');
    
    if (show) {
        progress.style.display = 'block';
        progressText.textContent = text;
    } else {
        progress.style.display = 'none';
    }
}

// ===================================
// Project Management
// ===================================

async function loadProjects() {
    try {
        const response = await fetch(`${API_BASE}/api/projects`);
        const data = await response.json();
        
        const select = document.getElementById('projectSelect');
        select.innerHTML = '<option value="">Select Project...</option>';
        
        data.projects.forEach(project => {
            const option = document.createElement('option');
            option.value = project.name;
            option.textContent = project.name;
            select.appendChild(option);
        });
    } catch (error) {
        showError('Failed to load projects');
    }
}

async function loadProject(projectName) {
    if (!projectName) return;
    
    try {
        const response = await fetch(`${API_BASE}/api/projects/${projectName}`);
        const data = await response.json();
        
        if (data.status === 'success') {
            currentProject = projectName;
            document.getElementById('projectNameInput').value = projectName;
            
            // Load config if available
            if (data.config) {
                loadConfigIntoForm(data.config);
            }
            
            setStatus(`Loaded project: ${projectName}`);
        }
    } catch (error) {
        showError('Failed to load project');
    }
}

function loadConfigIntoForm(config) {
    // Texture settings
    if (config.udim_tiles && config.udim_tiles['1001']) {
        document.getElementById('texturePrompt').value = config.udim_tiles['1001'].prompt || '';
        document.getElementById('textureNegative').value = config.udim_tiles['1001'].negative || '';
        document.getElementById('textureSeed').value = config.udim_tiles['1001'].seed || 12345;
    }
    
    // Rig settings
    if (config.unirig) {
        document.getElementById('rigScale').value = config.unirig.scale || 1.0;
        document.getElementById('rigOrientation').value = config.unirig.orientation || 'Y_UP';
    }
}

function showNewProjectDialog() {
    document.getElementById('newProjectModal').classList.add('active');
    document.getElementById('newProjectName').focus();
}

function closeModal() {
    document.getElementById('newProjectModal').classList.remove('active');
}

async function createNewProject() {
    const projectName = document.getElementById('newProjectName').value.trim();
    
    if (!projectName) {
        showError('Please enter a project name');
        return;
    }
    
    // Validate project name
    if (!/^[a-zA-Z0-9_-]+$/.test(projectName)) {
        showError('Project name can only contain letters, numbers, underscores, and hyphens');
        return;
    }
    
    try {
        const response = await fetch(`${API_BASE}/api/projects/create`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project_name: projectName })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            closeModal();
            showSuccess(`Project "${projectName}" created`);
            await loadProjects();
            document.getElementById('projectSelect').value = projectName;
            loadProject(projectName);
        } else {
            showError(data.message);
        }
    } catch (error) {
        showError('Failed to create project');
    }
}

// ===================================
// Configuration
// ===================================

async function saveConfig() {
    if (!currentProject) {
        showError('No project selected');
        return;
    }
    
    const config = {
        project_name: currentProject,
        udim_tiles: {
            "1001": {
                prompt: document.getElementById('texturePrompt').value,
                negative: document.getElementById('textureNegative').value,
                seed: parseInt(document.getElementById('textureSeed').value)
            }
        },
        unirig: {
            scale: parseFloat(document.getElementById('rigScale').value),
            orientation: document.getElementById('rigOrientation').value
        },
        hy_motion_prompt: document.getElementById('animPrompt').value,
        export_formats: {
            fbx: document.getElementById('exportFBX').checked,
            gltf: document.getElementById('exportGLTF').checked,
            usd: document.getElementById('exportUSD').checked
        }
    };
    
    try {
        const response = await fetch(`${API_BASE}/api/projects/${currentProject}/config`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(config)
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showSuccess('Configuration saved');
        } else {
            showError('Failed to save configuration');
        }
    } catch (error) {
        showError('Failed to save configuration');
    }
}

// ===================================
// Pipeline Execution
// ===================================

async function startPipeline() {
    if (!currentProject) {
        showError('No project selected');
        return;
    }
    
    // Save config first
    await saveConfig();
    
    // Show pipeline modal
    showPipelineProgress();
    
    try {
        const response = await fetch(`${API_BASE}/api/pipeline/run`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ project: currentProject })
        });
        
        const data = await response.json();
        
        if (data.status === 'success') {
            showSuccess('Pipeline started');
            monitorPipeline(data.job_id);
        } else {
            showError('Failed to start pipeline');
        }
    } catch (error) {
        showError('Failed to start pipeline');
    }
}

function showPipelineProgress() {
    const modal = document.getElementById('pipelineModal');
    modal.classList.add('active');
    
    const steps = document.getElementById('pipelineSteps');
    steps.innerHTML = `
        <div class="pipeline-step active">
            <strong>1. Mesh Validation</strong>
            <p>Validating input mesh...</p>
        </div>
        <div class="pipeline-step">
            <strong>2. Texture Generation</strong>
            <p>Waiting...</p>
        </div>
        <div class="pipeline-step">
            <strong>3. Rigging</strong>
            <p>Waiting...</p>
        </div>
        <div class="pipeline-step">
            <strong>4. Animation</strong>
            <p>Waiting...</p>
        </div>
        <div class="pipeline-step">
            <strong>5. Export</strong>
            <p>Waiting...</p>
        </div>
    `;
}

function closePipelineModal() {
    document.getElementById('pipelineModal').classList.remove('active');
}

// ===================================
// System Status
// ===================================

async function checkSystemStatus() {
    try {
        const response = await fetch(`${API_BASE}/health`);
        const data = await response.json();
        
        document.getElementById('pipelineStatus').querySelector('.status-dot').classList.add('active');
    } catch (error) {
        document.getElementById('pipelineStatus').querySelector('.status-dot').classList.remove('active');
    }
}

// ===================================
// Utilities
// ===================================

function setStatus(message) {
    document.getElementById('statusText').textContent = message;
}

function showSuccess(message) {
    setStatus(`✓ ${message}`);
    setTimeout(() => setStatus('Ready'), 3000);
}

function showError(message) {
    setStatus(`✗ ${message}`);
    console.error(message);
}

function formatFileSize(bytes) {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

function removeFile(filename, type) {
    // Implementation for file removal
    console.log('Remove file:', filename, type);
}
