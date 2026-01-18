#!/usr/bin/env python3
"""
api_server.py
-------------
Simple REST API server for pod-based project management.

Provides endpoints for:
- Creating new projects
- Listing existing projects
- Running pipeline operations

Usage:
    python pipeline/api_server.py
    
    # Or specify port
    python pipeline/api_server.py --port 8080
"""

import argparse
import json
import os
from pathlib import Path
from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
from project_init import (
    init_project_with_name,
    rename_existing_project,
    validate_project_name
)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size

# Configuration
WORKSPACE_ROOT = Path("/workspace")  # Default for pod
if not WORKSPACE_ROOT.exists():
    WORKSPACE_ROOT = Path.cwd().parent  # Fallback for local testing

WEB_UI_DIR = Path(__file__).parent / "web_ui"
UPLOAD_FOLDER = WEB_UI_DIR / "uploads"
UPLOAD_FOLDER.mkdir(exist_ok=True)

ALLOWED_MESH_EXTENSIONS = {'.fbx', '.obj', '.glb', '.gltf'}
ALLOWED_IMAGE_EXTENSIONS = {'.png', '.jpg', '.jpeg', '.tiff', '.exr'}


def allowed_file(filename, allowed_extensions):
    return Path(filename).suffix.lower() in allowed_extensions


# ---------------------------------------------------------
# Web UI Routes
# ---------------------------------------------------------

@app.route("/")
def index():
    """Serve the main web UI"""
    return send_file(WEB_UI_DIR / "index.html")


@app.route("/static/<path:filename>")
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    return send_from_directory(WEB_UI_DIR / "static", filename)


# ---------------------------------------------------------
# File Upload Routes
# ---------------------------------------------------------

@app.route("/api/upload", methods=["POST"])
def upload_file():
    """Upload files (mesh, UDIM tiles, references)"""
    try:
        if 'file' not in request.files:
            return jsonify({
                "status": "error",
                "message": "No file provided"
            }), 400
        
        file = request.files['file']
        file_type = request.form.get('type', 'unknown')
        project_name = request.form.get('project')
        
        if not project_name:
            return jsonify({
                "status": "error",
                "message": "Project name is required"
            }), 400
        
        project_path = WORKSPACE_ROOT / project_name
        if not project_path.exists():
            return jsonify({
                "status": "error",
                "message": f"Project '{project_name}' does not exist"
            }), 404
        
        if file.filename == '':
            return jsonify({
                "status": "error",
                "message": "No file selected"
            }), 400
        
        filename = secure_filename(file.filename)
        
        # Determine destination based on file type
        if file_type == 'mesh':
            if not allowed_file(filename, ALLOWED_MESH_EXTENSIONS):
                return jsonify({
                    "status": "error",
                    "message": "Invalid mesh file format"
                }), 400
            dest_folder = project_path / "0_input/meshes"
        elif file_type == 'udim':
            if not allowed_file(filename, ALLOWED_IMAGE_EXTENSIONS):
                return jsonify({
                    "status": "error",
                    "message": "Invalid image file format"
                }), 400
            dest_folder = project_path / "0_input/uv_layouts"
        elif file_type == 'reference':
            if not allowed_file(filename, ALLOWED_IMAGE_EXTENSIONS):
                return jsonify({
                    "status": "error",
                    "message": "Invalid image file format"
                }), 400
            dest_folder = project_path / "0_input/references"
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid file type"
            }), 400
        
        dest_folder.mkdir(parents=True, exist_ok=True)
        dest_path = dest_folder / filename
        
        file.save(str(dest_path))
        
        return jsonify({
            "status": "success",
            "message": f"File uploaded: {filename}",
            "path": str(dest_path),
            "size": dest_path.stat().st_size
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/files/<project_name>/<file_type>", methods=["GET"])
def list_files(project_name, file_type):
    """List uploaded files for a project"""
    try:
        project_path = WORKSPACE_ROOT / project_name
        
        if file_type == 'mesh':
            folder = project_path / "0_input/meshes"
        elif file_type == 'udim':
            folder = project_path / "0_input/uv_layouts"
        elif file_type == 'reference':
            folder = project_path / "0_input/references"
        else:
            return jsonify({
                "status": "error",
                "message": "Invalid file type"
            }), 400
        
        if not folder.exists():
            return jsonify({
                "status": "success",
                "files": []
            })
        
        files = []
        for file_path in folder.iterdir():
            if file_path.is_file():
                files.append({
                    "name": file_path.name,
                    "size": file_path.stat().st_size,
                    "path": str(file_path)
                })
        
        return jsonify({
            "status": "success",
            "files": files
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------------------------------------------------
# Pipeline Execution Routes
# ---------------------------------------------------------

@app.route("/api/pipeline/run", methods=["POST"])
def run_pipeline():
    """Start the pipeline for a project"""
    try:
        data = request.json
        project_name = data.get("project")
        
        if not project_name:
            return jsonify({
                "status": "error",
                "message": "Project name is required"
            }), 400
        
        project_path = WORKSPACE_ROOT / project_name
        if not project_path.exists():
            return jsonify({
                "status": "error",
                "message": f"Project '{project_name}' does not exist"
            }), 404
        
        # TODO: Implement actual pipeline execution
        # For now, return a mock response
        return jsonify({
            "status": "success",
            "message": "Pipeline started",
            "job_id": "mock_job_123",
            "project": project_name
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/pipeline/status/<job_id>", methods=["GET"])
def pipeline_status(job_id):
    """Get pipeline execution status"""
    # TODO: Implement actual status tracking
    return jsonify({
        "status": "success",
        "job_id": job_id,
        "stage": "texture_generation",
        "progress": 45,
        "message": "Generating UDIM textures..."
    })


# ---------------------------------------------------------
# API Endpoints (existing)
# ---------------------------------------------------------

@app.route("/health", methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "workspace": str(WORKSPACE_ROOT)
    })


@app.route("/api/projects", methods=["GET"])
def list_projects():
    """List all projects in workspace"""
    try:
        projects = []
        for item in WORKSPACE_ROOT.iterdir():
            if item.is_dir() and (item / "pipeline").exists():
                # Check if it's a valid project (has pipeline folder)
                projects.append({
                    "name": item.name,
                    "path": str(item),
                    "has_config": (item / "pipeline/config.json").exists()
                })
        
        return jsonify({
            "status": "success",
            "projects": projects,
            "count": len(projects)
        })
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/projects/create", methods=["POST"])
def create_project():
    """Create a new project"""
    try:
        data = request.json
        project_name = data.get("project_name")
        
        if not project_name:
            return jsonify({
                "status": "error",
                "message": "project_name is required"
            }), 400
        
        # Validate project name
        is_valid, error_msg = validate_project_name(project_name)
        if not is_valid:
            return jsonify({
                "status": "error",
                "message": error_msg
            }), 400
        
        # Check if already exists
        project_path = WORKSPACE_ROOT / project_name
        if project_path.exists():
            return jsonify({
                "status": "error",
                "message": f"Project '{project_name}' already exists"
            }), 409
        
        # Create project
        project_root = init_project_with_name(WORKSPACE_ROOT, project_name)
        
        if project_root:
            return jsonify({
                "status": "success",
                "project_name": project_name,
                "project_path": str(project_root),
                "message": f"Project '{project_name}' created successfully"
            }), 201
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to create project"
            }), 500
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/projects/<project_name>/rename", methods=["POST"])
def rename_project(project_name):
    """Rename an existing project"""
    try:
        data = request.json
        new_name = data.get("new_name")
        
        if not new_name:
            return jsonify({
                "status": "error",
                "message": "new_name is required"
            }), 400
        
        # Rename project
        new_path = rename_existing_project(WORKSPACE_ROOT, project_name, new_name)
        
        if new_path:
            return jsonify({
                "status": "success",
                "old_name": project_name,
                "new_name": new_name,
                "project_path": str(new_path),
                "message": f"Project renamed from '{project_name}' to '{new_name}'"
            })
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to rename project"
            }), 400
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/projects/<project_name>", methods=["GET"])
def get_project_info(project_name):
    """Get information about a specific project"""
    try:
        project_path = WORKSPACE_ROOT / project_name
        
        if not project_path.exists():
            return jsonify({
                "status": "error",
                "message": f"Project '{project_name}' not found"
            }), 404
        
        # Read config if available
        config_path = project_path / "pipeline/config.json"
        config = None
        if config_path.exists():
            config = json.loads(config_path.read_text())
        
        # Get folder structure info
        folders = {
            "input": (project_path / "0_input").exists(),
            "textures": (project_path / "1_textures").exists(),
            "rig": (project_path / "2_rig").exists(),
            "animation": (project_path / "3_animation").exists(),
            "export": (project_path / "4_export").exists(),
        }
        
        return jsonify({
            "status": "success",
            "project_name": project_name,
            "project_path": str(project_path),
            "config": config,
            "folders": folders
        })
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


@app.route("/api/projects/<project_name>/config", methods=["GET", "PUT"])
def project_config(project_name):
    """Get or update project configuration"""
    try:
        config_path = WORKSPACE_ROOT / project_name / "pipeline/config.json"
        
        if not config_path.exists():
            return jsonify({
                "status": "error",
                "message": f"Config for project '{project_name}' not found"
            }), 404
        
        if request.method == "GET":
            config = json.loads(config_path.read_text())
            return jsonify({
                "status": "success",
                "config": config
            })
        
        elif request.method == "PUT":
            new_config = request.json
            config_path.write_text(json.dumps(new_config, indent=2))
            return jsonify({
                "status": "success",
                "message": "Configuration updated"
            })
            
    except Exception as e:
        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


# ---------------------------------------------------------
# Main
# ---------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="3D Pipeline API Server")
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8080,
        help="Port to run server on (default: 8080)"
    )
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind to (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--workspace",
        type=Path,
        default=None,
        help="Workspace root directory"
    )
    
    args = parser.parse_args()
    
    global WORKSPACE_ROOT
    if args.workspace:
        WORKSPACE_ROOT = args.workspace.resolve()
    
    print(f"\n=== 3D PIPELINE API SERVER ===")
    print(f"Workspace: {WORKSPACE_ROOT}")
    print(f"Starting server on {args.host}:{args.port}...\n")
    
    app.run(host=args.host, port=args.port, debug=False)


if __name__ == "__main__":
    main()
