#!/bin/bash
set -e

###############################################################################
# SpriteForge – ComfyUI Custom Node Installer (Idempotent, Clean, Modular)
###############################################################################

COMFYUI_DIR="${COMFYUI_DIR:-/workspace}"
CUSTOM_NODES_DIR="$COMFYUI_DIR/custom_nodes"

echo "=========================================="
echo "SpriteForge – Installing ComfyUI Custom Nodes"
echo "Custom Nodes Directory: $CUSTOM_NODES_DIR"
echo "=========================================="
echo ""

mkdir -p "$CUSTOM_NODES_DIR"
cd "$CUSTOM_NODES_DIR"

###############################################################################
# Helper: Install or update a custom node repo
###############################################################################

install_node() {
    local name="$1"
    local repo_url="$2"
    local folder="$CUSTOM_NODES_DIR/$name"

    echo "→ Installing $name..."

    if [ -d "$folder" ]; then
        echo "  Updating existing repo..."
        git -C "$folder" pull
    else
        echo "  Cloning repo..."
        git clone "$repo_url" "$folder"
    fi

    if [ -f "$folder/requirements.txt" ]; then
        echo "  Installing Python requirements..."
        python -m pip install --upgrade -r "$folder/requirements.txt"
    fi

    echo "  ✓ $name installed"
    echo ""
}

###############################################################################
# 1. AnimateDiff-Evolved (temporal consistency)
###############################################################################
install_node "ComfyUI-AnimateDiff-Evolved" \
    "https://github.com/Kosinkadink/ComfyUI-AnimateDiff-Evolved.git"

###############################################################################
# 2. IP-Adapter Plus (character identity locking)
###############################################################################
install_node "ComfyUI_IPAdapter_plus" \
    "https://github.com/cubiq/ComfyUI_IPAdapter_plus.git"

###############################################################################
# 3. ControlNet Aux (OpenPose, Depth, Normal, Canny preprocessors)
###############################################################################
install_node "comfyui_controlnet_aux" \
    "https://github.com/Fannovel16/comfyui_controlnet_aux.git"

###############################################################################
# 4. Advanced ControlNet (weight scheduling)
###############################################################################
install_node "ComfyUI-Advanced-ControlNet" \
    "https://github.com/Kosinkadink/ComfyUI-Advanced-ControlNet.git"

###############################################################################
# 5. Background Removal (rembg + essentials)
###############################################################################

echo "→ Installing rembg (GPU if available)..."
python -m pip install rembg[gpu] 2>/dev/null || python -m pip install rembg
echo "  ✓ rembg installed"
echo ""

# Essentials already installed in Dockerfile, but ensure updated:
install_node "ComfyUI_essentials" \
    "https://github.com/cubiq/ComfyUI_essentials.git"

###############################################################################
# 6. Frame Interpolation (smooth animation)
###############################################################################
install_node "ComfyUI-Frame-Interpolation" \
    "https://github.com/Fannovel16/ComfyUI-Frame-Interpolation.git"

###############################################################################
# Summary
###############################################################################

echo "=========================================="
echo "SpriteForge Custom Node Installation Complete!"
echo "=========================================="
echo ""
echo "Installed custom nodes:"
echo "  ✓ AnimateDiff-Evolved"
echo "  ✓ IP-Adapter Plus"
echo "  ✓ ControlNet Aux"
echo "  ✓ Advanced ControlNet"
echo "  ✓ ComfyUI_essentials + rembg"
echo "  ✓ Frame Interpolation"
echo ""
echo "These nodes support:"
echo "  • Temporal consistency"
echo "  • Character identity locking"
echo "  • Pose/depth/normal preprocessing"
echo "  • Weight scheduling"
echo "  • Background removal"
echo "  • Smooth animation interpolation"
echo ""
