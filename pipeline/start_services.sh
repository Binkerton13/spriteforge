#!/bin/bash
# Example startup script for running all services
# This demonstrates how to run ComfyUI, File Browser, and Pipeline GUI together

echo "=========================================="
echo "3D Character Pipeline - Service Startup"
echo "=========================================="
echo ""

# Configuration
WORKSPACE_ROOT="${WORKSPACE_ROOT:-/workspace}"
COMFYUI_PORT=8188
FILEBROWSER_PORT=8080
PIPELINE_GUI_PORT=7860

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if port is available
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
        echo "Port $1 is already in use"
        return 1
    fi
    return 0
}

# Start ComfyUI (if available)
if [ -d "$WORKSPACE_ROOT/ComfyUI" ]; then
    echo -e "${BLUE}[1/3]${NC} Starting ComfyUI on port $COMFYUI_PORT..."
    cd "$WORKSPACE_ROOT/ComfyUI"
    python main.py --listen 0.0.0.0 --port $COMFYUI_PORT > /tmp/comfyui.log 2>&1 &
    COMFYUI_PID=$!
    echo -e "${GREEN}✓${NC} ComfyUI started (PID: $COMFYUI_PID)"
else
    echo "⚠ ComfyUI not found, skipping..."
fi

# Start File Browser (if installed)
if command -v filebrowser &> /dev/null; then
    echo -e "${BLUE}[2/3]${NC} Starting File Browser on port $FILEBROWSER_PORT..."
    filebrowser --port $FILEBROWSER_PORT --address 0.0.0.0 --root "$WORKSPACE_ROOT" > /tmp/filebrowser.log 2>&1 &
    FILEBROWSER_PID=$!
    echo -e "${GREEN}✓${NC} File Browser started (PID: $FILEBROWSER_PID)"
else
    echo "⚠ File Browser not found, skipping..."
fi

# Start Pipeline GUI
echo -e "${BLUE}[3/3]${NC} Starting Pipeline GUI on port $PIPELINE_GUI_PORT..."
cd "$WORKSPACE_ROOT"
python pipeline/api_server.py --port $PIPELINE_GUI_PORT --host 0.0.0.0 --workspace "$WORKSPACE_ROOT" > /tmp/pipeline-gui.log 2>&1 &
PIPELINE_GUI_PID=$!
echo -e "${GREEN}✓${NC} Pipeline GUI started (PID: $PIPELINE_GUI_PID)"

# Wait for services to initialize
echo ""
echo "Waiting for services to start..."
sleep 5

# Display access information
echo ""
echo "=========================================="
echo -e "${GREEN}✓ All services started successfully!${NC}"
echo "=========================================="
echo ""
echo "Access URLs:"
echo "  📦 ComfyUI:      http://localhost:$COMFYUI_PORT"
echo "  📁 File Browser: http://localhost:$FILEBROWSER_PORT"
echo "  🎨 Pipeline GUI: http://localhost:$PIPELINE_GUI_PORT"
echo ""
echo "Logs:"
echo "  ComfyUI:      tail -f /tmp/comfyui.log"
echo "  File Browser: tail -f /tmp/filebrowser.log"
echo "  Pipeline GUI: tail -f /tmp/pipeline-gui.log"
echo ""
echo "To stop all services:"
echo "  kill $COMFYUI_PID $FILEBROWSER_PID $PIPELINE_GUI_PID"
echo "=========================================="
echo ""

# Keep script running (optional - comment out if running in background)
# wait $COMFYUI_PID $FILEBROWSER_PID $PIPELINE_GUI_PID
