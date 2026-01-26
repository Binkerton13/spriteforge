#!/bin/bash
set -e

###############################################################################
# SpriteForge – Dependency Installer (Idempotent, Logged, Versioned)
###############################################################################

START_TIME=$(date +%s)
LOG_FILE="/workspace/pipeline/install.log"

echo "==============================================================================" | tee -a "$LOG_FILE"
echo "SpriteForge – Dependency Installation" | tee -a "$LOG_FILE"
echo "Timestamp: $(date)" | tee -a "$LOG_FILE"
echo "==============================================================================" | tee -a "$LOG_FILE"
echo "" | tee -a "$LOG_FILE"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

###############################################################################
# Marker file to skip reinstall
###############################################################################

MARKER="/workspace/pipeline/.deps_installed"

if [ -f "$MARKER" ]; then
    echo -e "${GREEN}✓ Dependencies already installed. Skipping.${NC}" | tee -a "$LOG_FILE"
    echo "To force reinstall, delete: $MARKER" | tee -a "$LOG_FILE"
    exit 0
fi

###############################################################################
# run_step wrapper with real exit-code capture
###############################################################################

run_step() {
    local label="$1"
    shift
    echo -e "${YELLOW}→ $label...${NC}" | tee -a "$LOG_FILE"
    local t0=$(date +%s)

    "$@" 2>&1 | tee -a "$LOG_FILE"
    local exit_code=${PIPESTATUS[0]}

    local t1=$(date +%s)

    if [ $exit_code -ne 0 ]; then
        echo -e "${RED}✗ FAILED: $label (exit code $exit_code)${NC}" | tee -a "$LOG_FILE"
        echo "Stopping installation." | tee -a "$LOG_FILE"
        exit $exit_code
    fi

    echo -e "${GREEN}✓ Completed: $label in $((t1 - t0))s${NC}" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
}

###############################################################################
# 1. Install HY-Motion (disabled — handled in Dockerfile)
###############################################################################

install_hymotion() {
    echo "HY-Motion installation skipped (handled in Docker build)." | tee -a "$LOG_FILE"
}

run_step "Installing HY-Motion" install_hymotion


###############################################################################
# 2. Install Custom ComfyUI Nodes
###############################################################################

run_step "Installing ComfyUI custom nodes" bash /workspace/pipeline/scripts/install_custom_nodes.sh

###############################################################################
# 3. Transformers Version Enforcement
###############################################################################

install_transformers_fix() {
    REQUIRED_VERSION="4.41.2"

    CURRENT_VERSION=$(python3 - <<EOF
import transformers
print(transformers.__version__)
EOF
)

    echo "Transformers installed: $CURRENT_VERSION" | tee -a "$LOG_FILE"

    if [ "$CURRENT_VERSION" = "$REQUIRED_VERSION" ]; then
        echo "Correct Transformers version already installed." | tee -a "$LOG_FILE"
        return 0
    fi

    echo "Installing Transformers $REQUIRED_VERSION..." | tee -a "$LOG_FILE"
    pip install --user --upgrade "transformers==$REQUIRED_VERSION"
}

run_step "Enforcing Transformers version" install_transformers_fix

###############################################################################
# 4. Activate sitecustomize override
###############################################################################

activate_sitecustomize() {
    PATCH_DIR="/workspace/pipeline/env_patches"

    mkdir -p "$PATCH_DIR"

    cat > "$PATCH_DIR/sitecustomize.py" << 'EOF'
import sys, os
USER_SITE = os.path.expanduser("~/.local/lib/python3.11/site-packages")
if USER_SITE not in sys.path:
    sys.path.insert(0, USER_SITE)
EOF

    echo "export PYTHONPATH=\"$PATCH_DIR:\$PYTHONPATH\"" >> ~/.bashrc
    export PYTHONPATH="$PATCH_DIR:$PYTHONPATH"
}

run_step "Activating sitecustomize override" activate_sitecustomize

###############################################################################
# Mark installation complete
###############################################################################

touch "$MARKER"

END_TIME=$(date +%s)
echo "==============================================================================" | tee -a "$LOG_FILE"
echo "Installation complete in $((END_TIME - START_TIME)) seconds." | tee -a "$LOG_FILE"
echo "==============================================================================" | tee -a "$LOG_FILE"
