# Pod Integration Guide

## Project Name Initialization Strategies for 3D-AI-Workstation + Pod

This document describes different approaches for collecting a project name from the user (on their workstation) and applying it to the pod-based pipeline.

---

## 📋 Overview of Approaches

### 1. **Pre-Pod Initialization (Recommended)**
User provides project name → Workstation creates structure → Structure mounted to pod

### 2. **Environment Variable Passing**
User provides project name → Workstation sets env var → Pod reads on startup

### 3. **Post-Pod Initialization**
Pod starts with default → User provides name → Structure renamed

### 4. **API-Based Configuration**
Pod exposes API → Workstation sends project name → Pod creates structure

---

## 🎯 Strategy 1: Pre-Pod Initialization (Recommended)

**Best for:** Complete control, fastest startup, no pod-side changes needed

### Workflow:
```
[User] → [Workstation: Prompt for name]
         ↓
     [Create structure locally]
         ↓
     [Mount to pod as volume]
         ↓
     [Pod uses existing structure]
```

### Implementation:

#### On Workstation (before pod starts):
```python
# In 3D-AI-Workstation startup script
from pipeline.project_init import init_project_with_name

# Prompt user for project name
project_name = input("Enter project name: ")

# Create structure locally
workspace = Path("e:/2D Programs/ComfyUI_Ext_Output/3D_AI_Inputs")
project_root = init_project_with_name(workspace, project_name)

# Mount this to pod
pod_volume = f"{project_root}:/workspace/{project_name}"
```

#### Pod Configuration:
```bash
# No special initialization needed - structure already exists
# Pod startup script just uses the mounted volume

cd /workspace/${PROJECT_NAME}
python pipeline/one_click.py
```

### Advantages:
- ✅ No pod-side modifications needed
- ✅ Fastest pod startup (no structure creation)
- ✅ User sees structure immediately
- ✅ Works with any pod provider

### Disadvantages:
- ❌ Requires workstation to have write access
- ❌ Must mount correct volume to pod

---

## 🌐 Strategy 2: Environment Variable Passing

**Best for:** Pod-managed initialization, clean separation

### Workflow:
```
[User] → [Workstation: Collect name]
         ↓
     [Set PROJECT_NAME env var]
         ↓
     [Start pod with env var]
         ↓
     [Pod creates structure on startup]
```

### Implementation:

#### On Workstation:
```python
# In 3D-AI-Workstation
import subprocess

# Prompt user
project_name = input("Enter project name: ")

# Start pod with environment variable
subprocess.run([
    "runpod",
    "create",
    "--env", f"PROJECT_NAME={project_name}",
    "--image", "3d-ai-pipeline:latest"
])
```

#### Pod Startup Script:
```bash
#!/bin/bash
# /workspace/startup.sh

# Initialize project from environment variable
cd /workspace
python pipeline/project_init.py --from-env

# Verify initialization
if [ -d "/workspace/${PROJECT_NAME}" ]; then
    echo "✓ Project ${PROJECT_NAME} initialized"
    cd /workspace/${PROJECT_NAME}
else
    echo "✗ Project initialization failed"
    exit 1
fi

# Ready to run pipeline
python pipeline/one_click.py
```

#### Pod Dockerfile:
```dockerfile
FROM nvidia/cuda:11.8.0-base-ubuntu22.04

# Install dependencies
RUN apt-get update && apt-get install -y python3 python3-pip blender

# Copy pipeline code
COPY pipeline/ /workspace/pipeline/

# Set startup script
COPY startup.sh /workspace/startup.sh
RUN chmod +x /workspace/startup.sh

# Run on container start
CMD ["/workspace/startup.sh"]
```

### Advantages:
- ✅ Clean separation of concerns
- ✅ Pod manages its own structure
- ✅ Easy to validate/sanitize project name
- ✅ Standard Docker pattern

### Disadvantages:
- ❌ Slower pod startup (creates structure)
- ❌ Requires pod restart to change project

---

## 🔄 Strategy 3: Post-Pod Initialization

**Best for:** Pods that start with default structure, flexible naming

### Workflow:
```
[Pod starts] → [Creates default "Exhibition" structure]
     ↓
[User provides name via workstation]
     ↓
[Workstation sends rename command]
     ↓
[Pod renames structure]
```

### Implementation:

#### Pod Startup (creates default):
```bash
#!/bin/bash
# /workspace/startup.sh

# Create default structure
cd /workspace
python pipeline/project_init.py --project Exhibition

# Start API server that can accept rename commands
python pipeline/api_server.py &

# Wait for user input
tail -f /dev/null
```

#### Workstation Command:
```python
# In 3D-AI-Workstation
import requests

# Prompt user
project_name = input("Enter project name: ")

# Send to pod API
response = requests.post(
    f"http://{pod_ip}:8080/rename",
    json={
        "old_name": "Exhibition",
        "new_name": project_name
    }
)

if response.ok:
    print(f"✓ Project renamed to {project_name}")
```

#### Or via SSH/CLI:
```bash
# From workstation
ssh root@pod_ip "cd /workspace && python pipeline/project_init.py --rename Exhibition MyCharacter"
```

### Advantages:
- ✅ Pod starts quickly with default
- ✅ Can change project name without restart
- ✅ Multiple projects per pod

### Disadvantages:
- ❌ Extra rename step
- ❌ Potential for orphaned default structures
- ❌ More complex workflow

---

## 🚀 Strategy 4: API-Based Configuration

**Best for:** Full-featured workstation applications, web UIs

### Workflow:
```
[Pod starts] → [Runs API server]
     ↓
[Workstation GUI] → [User enters name]
     ↓
[POST /api/projects/create]
     ↓
[Pod creates structure]
     ↓
[Returns project info to workstation]
```

### Implementation:

#### Pod API Server:
```python
# pipeline/api_server.py
from flask import Flask, request, jsonify
from project_init import init_project_with_name
from pathlib import Path

app = Flask(__name__)
workspace = Path("/workspace")

@app.route("/api/projects/create", methods=["POST"])
def create_project():
    data = request.json
    project_name = data.get("project_name")
    
    if not project_name:
        return jsonify({"error": "project_name required"}), 400
    
    project_root = init_project_with_name(workspace, project_name)
    
    if project_root:
        return jsonify({
            "status": "success",
            "project_name": project_name,
            "project_path": str(project_root)
        })
    else:
        return jsonify({"error": "Invalid project name"}), 400

@app.route("/api/projects/list", methods=["GET"])
def list_projects():
    projects = [d.name for d in workspace.iterdir() if d.is_dir()]
    return jsonify({"projects": projects})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
```

#### Workstation Client:
```python
# In 3D-AI-Workstation
class PodClient:
    def __init__(self, pod_ip):
        self.base_url = f"http://{pod_ip}:8080"
    
    def create_project(self, project_name):
        response = requests.post(
            f"{self.base_url}/api/projects/create",
            json={"project_name": project_name}
        )
        return response.json()
    
    def list_projects(self):
        response = requests.get(f"{self.base_url}/api/projects/list")
        return response.json()

# Usage
pod = PodClient("123.45.67.89")
result = pod.create_project("MyCharacter")
print(f"Created: {result['project_path']}")
```

### Advantages:
- ✅ Most flexible
- ✅ Supports multiple projects
- ✅ Web UI friendly
- ✅ RESTful pattern

### Disadvantages:
- ❌ Most complex to implement
- ❌ Requires API security considerations
- ❌ Network dependency

---

## 📊 Comparison Matrix

| Strategy | Complexity | Flexibility | Startup Speed | Best For |
|----------|------------|-------------|---------------|----------|
| Pre-Pod Init | Low | Low | Fastest | Simple workflows |
| Env Variable | Medium | Low | Fast | Standard Docker |
| Post-Init | Medium | High | Fast | Flexible naming |
| API-Based | High | Highest | Medium | Web UIs, multi-user |

---

## 💡 Recommended Implementation for 3D-AI-Workstation

**Hybrid Approach:**

1. **Workstation prompts for project name on startup**
2. **Check if pod is already running:**
   - If yes → Use API to create project
   - If no → Set env variable, start pod with project name
3. **Fallback:** If pod fails, create structure locally and mount

### Implementation:
```python
# 3D-AI-Workstation main.py
from pathlib import Path
import requests

def initialize_project():
    # Prompt user
    project_name = input("Enter project name: ")
    
    # Check pod status
    if is_pod_running():
        # Pod already running - use API
        create_via_api(pod_ip, project_name)
    else:
        # Start new pod with env variable
        start_pod_with_env(project_name)
    
    return project_name

def start_pod_with_env(project_name):
    """Start pod with PROJECT_NAME environment variable"""
    subprocess.run([
        "runpod", "create",
        "--env", f"PROJECT_NAME={project_name}",
        "--image", "3d-ai-pipeline:latest"
    ])

def create_via_api(pod_ip, project_name):
    """Send project creation request to running pod"""
    response = requests.post(
        f"http://{pod_ip}:8080/api/projects/create",
        json={"project_name": project_name}
    )
    return response.json()
```

---

## 🔧 Testing Commands

Test each strategy:

```bash
# Strategy 1: Pre-Pod Init
python pipeline/project_init.py --project TestCharacter

# Strategy 2: Environment Variable
export PROJECT_NAME="TestCharacter"
python pipeline/project_init.py --from-env

# Strategy 3: Post-Init Rename
python pipeline/project_init.py --rename Exhibition TestCharacter

# Strategy 4: API (requires server running)
curl -X POST http://localhost:8080/api/projects/create \
  -H "Content-Type: application/json" \
  -d '{"project_name": "TestCharacter"}'
```

---

## 📝 Next Steps

1. Choose strategy based on your workstation-pod architecture
2. Implement chosen strategy in 3D-AI-Workstation
3. Update pod startup scripts accordingly
4. Test end-to-end workflow
5. Add error handling and validation
