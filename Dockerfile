FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    WORKSPACE=/workspace

# -----------------------------
# 1. Base system setup
# -----------------------------
RUN apt-get update && apt-get install -y --no-install-recommends \
    git git-lfs \
    wget curl \
    ca-certificates \
    ffmpeg \
    python3 python3-venv python3-dev python3-pip \
    build-essential \
    unzip \
    libgl1 \
    libglib2.0-0 \
    libxrender1 libxext6 libsm6 \
    libx11-6 libxi6 libxrandr2 libxxf86vm1 libxfixes3 libxcursor1 libxinerama1 \
    mesa-utils \
    libopenexr-dev \
    libjpeg-dev libpng-dev libtiff-dev \
    libavcodec-dev libavformat-dev libavutil-dev \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir -p ${WORKSPACE}
WORKDIR ${WORKSPACE}

# -----------------------------
# 2. Global Python venv
# -----------------------------
RUN python3 -m venv ${WORKSPACE}/venv && \
    ${WORKSPACE}/venv/bin/pip install --upgrade pip wheel setuptools

ENV VIRTUAL_ENV=${WORKSPACE}/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# -----------------------------
# 3. PyTorch (CUDA 12.1)
# -----------------------------
RUN pip install --no-cache-dir \
    torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Core Python deps
RUN pip install --no-cache-dir \
    numpy scipy pillow opencv-python \
    matplotlib scikit-image scikit-learn \
    trimesh pygltflib

# -----------------------------
# 4. ComfyUI
# -----------------------------
RUN git clone https://github.com/comfyanonymous/ComfyUI.git ${WORKSPACE}/comfyui

RUN mkdir -p ${WORKSPACE}/comfyui/custom_nodes && \
    cd ${WORKSPACE}/comfyui/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git && \
    git clone https://github.com/cubiq/ComfyUI_essentials.git && \
    git clone https://github.com/WASasquatch/was-node-suite-comfyui.git

RUN cd ${WORKSPACE}/comfyui && \
    pip install --no-cache-dir -r requirements.txt

RUN mkdir -p ${WORKSPACE}/models/checkpoints \
             ${WORKSPACE}/models/loras \
             ${WORKSPACE}/models/vae \
             ${WORKSPACE}/models/controlnet \
             ${WORKSPACE}/models/unet

# -----------------------------
# 5. Blender (CLI + headless)
# -----------------------------
ARG BLENDER_VERSION=4.0.2
RUN mkdir -p /opt && \
    cd /opt && \
    wget -q https://download.blender.org/release/Blender${BLENDER_VERSION%.*}/blender-${BLENDER_VERSION}-linux-x64.tar.xz && \
    tar -xf blender-${BLENDER_VERSION}-linux-x64.tar.xz && \
    rm blender-${BLENDER_VERSION}-linux-x64.tar.xz && \
    ln -s /opt/blender-${BLENDER_VERSION}-linux-x64/blender /usr/local/bin/blender

# -----------------------------
# 6. UniRig
# -----------------------------
RUN git clone https://github.com/VAST-AI-Research/UniRig.git ${WORKSPACE}/unirig

RUN sed -i '/bpy/d' ${WORKSPACE}/unirig/requirements.txt
RUN sed -i '/flash_attn/d' ${WORKSPACE}/unirig/requirements.txt

RUN pip install --no-cache-dir -r ${WORKSPACE}/unirig/requirements.txt

# -----------------------------
# 7. Hy-Motion
# -----------------------------
RUN git clone https://github.com/Tencent-Hunyuan/HY-Motion-1.0.git ${WORKSPACE}/hy-motion

RUN if [ -f "${WORKSPACE}/hy-motion/requirements.txt" ]; then \
        pip install --no-cache-dir -r ${WORKSPACE}/hy-motion/requirements.txt; \
    fi

# -----------------------------
# 8. TripoSR
# -----------------------------
RUN git clone https://github.com/VAST-AI-Research/TripoSR.git ${WORKSPACE}/triposr

RUN sed -i '/torchmcubes/d' ${WORKSPACE}/triposr/requirements.txt

RUN if [ -f "${WORKSPACE}/triposr/requirements.txt" ]; then \
        pip install --no-cache-dir -r ${WORKSPACE}/triposr/requirements.txt; \
    fi

RUN mkdir -p ${WORKSPACE}/triposr/models \
             ${WORKSPACE}/triposr/outputs \
             ${WORKSPACE}/triposr/scripts

# -----------------------------
# 9. Workspace scaffold
# -----------------------------
RUN mkdir -p \
    ${WORKSPACE}/models/3d \
    ${WORKSPACE}/models/textures \
    ${WORKSPACE}/models/rigged \
    ${WORKSPACE}/renders \
    ${WORKSPACE}/animations \
    ${WORKSPACE}/scripts

# -----------------------------
# 10. Startup script (foreground ComfyUI)
# -----------------------------
RUN mkdir -p /workspace/scripts && \
    echo '#!/usr/bin/env bash'                                   >  /workspace/scripts/start.sh && \
    echo 'set -e'                                               >> /workspace/scripts/start.sh && \
    echo 'source "/workspace/venv/bin/activate"'                >> /workspace/scripts/start.sh && \
    echo 'python - <<EOF'                                       >> /workspace/scripts/start.sh && \
    echo 'import torch'                                         >> /workspace/scripts/start.sh && \
    echo 'print("CUDA available:", torch.cuda.is_available())'  >> /workspace/scripts/start.sh && \
    echo 'print("Device:", torch.cuda.get_device_name(0) if torch.cuda.is_available() else "None")' >> /workspace/scripts/start.sh && \
    echo 'EOF'                                                  >> /workspace/scripts/start.sh && \
    echo 'cd "/workspace/comfyui"'                              >> /workspace/scripts/start.sh && \
    echo 'python main.py --listen 0.0.0.0 --port 8188'          >> /workspace/scripts/start.sh && \
    chmod +x /workspace/scripts/start.sh

EXPOSE 8188

# -----------------------------
# 11. Runpod-compatible CMD
# -----------------------------
CMD ["/bin/bash", "/workspace/scripts/start.sh"]

