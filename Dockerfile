# ============================================
# STAGE 1 — BUILDER (installs Python deps, ComfyUI, HY-Motion)
# ============================================
FROM nvidia/cuda:12.1.1-cudnn8-devel-ubuntu22.04 AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    WORKSPACE=/workspace

ARG USE_CUDA=1

# Base system
RUN apt-get update && apt-get install -y --no-install-recommends \
    git git-lfs \
    wget curl \
    ca-certificates \
    ffmpeg \
    python3 python3-venv python3-dev python3-pip \
    build-essential \
    unzip \
    libgl1 libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

RUN git lfs install --system || true

# Python venv
RUN python3 -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip wheel setuptools

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="${VIRTUAL_ENV}/bin:${PATH}"

# PyTorch (CUDA or CPU)
RUN if [ "${USE_CUDA}" = "1" ]; then \
        pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121; \
    else \
        pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu; \
    fi

# Core Python deps
RUN pip install --no-cache-dir \
    numpy scipy pillow opencv-python \
    matplotlib scikit-image scikit-learn \
    trimesh pygltflib huggingface_hub \
    flask supervisor \
    && pip install --no-cache-dir --upgrade git+https://github.com/huggingface/transformers.git

# --------------------------------------------
# ComfyUI (installed in builder stage)
# --------------------------------------------
RUN git clone https://github.com/comfyanonymous/ComfyUI.git /opt/comfyui

RUN mkdir -p /opt/comfyui/custom_nodes && \
    cd /opt/comfyui/custom_nodes && \
    git clone https://github.com/ltdrdata/ComfyUI-Manager.git && \
    git clone https://github.com/cubiq/ComfyUI_essentials.git && \
    git clone https://github.com/WASasquatch/was-node-suite-comfyui.git

RUN pip install --no-cache-dir -r /opt/comfyui/requirements.txt

# --------------------------------------------
# HY-Motion
# --------------------------------------------
RUN git clone https://github.com/Tencent-Hunyuan/HY-Motion-1.0.git ${WORKSPACE}/hy-motion

RUN if [ -f "${WORKSPACE}/hy-motion/requirements.txt" ]; then \
        pip install --no-cache-dir -r ${WORKSPACE}/hy-motion/requirements.txt; \
    fi

# ============================================
# STAGE 2 — RUNTIME (minimal, clean, fast)
# ============================================
FROM nvidia/cuda:12.1.1-cudnn8-runtime-ubuntu22.04 AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    TZ=Etc/UTC \
    WORKSPACE=/workspace \
    VIRTUAL_ENV=/opt/venv \
    PATH="/opt/venv/bin:${PATH}"

# Minimal runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git git-lfs \
    ffmpeg \
    libgl1 libglib2.0-0 \
    supervisor \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN git lfs install --system || true

# Copy Python environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy ComfyUI from builder
COPY --from=builder /opt/comfyui /opt/comfyui

# Copy HY-Motion from builder
COPY --from=builder /workspace/hy-motion ${WORKSPACE}/hy-motion

# --------------------------------------------
# SpriteForge runtime folders
# --------------------------------------------
RUN mkdir -p \
    ${WORKSPACE}/models/checkpoints \
    ${WORKSPACE}/models/loras \
    ${WORKSPACE}/models/vae \
    ${WORKSPACE}/models/controlnet \
    ${WORKSPACE}/models/upscale_models \
    ${WORKSPACE}/models/clip \
    ${WORKSPACE}/models/clip_vision \
    ${WORKSPACE}/models/ipadapter \
    ${WORKSPACE}/models/embeddings \
    ${WORKSPACE}/animations \
    ${WORKSPACE}/sprites \
    ${WORKSPACE}/custom_nodes \
    ${WORKSPACE}/pipeline/logs

# --------------------------------------------
# Copy SpriteForge runtime files
# --------------------------------------------
COPY file_browser.py /usr/local/bin/file_browser.py
COPY supervisord.conf /etc/supervisord.conf

RUN chmod +x /usr/local/bin/file_browser.py


# --------------------------------------------
# Startup script (copy as last step for optimal caching)
# --------------------------------------------
COPY start.sh /usr/local/bin/start.sh
RUN chmod +x /usr/local/bin/start.sh

EXPOSE 8188 8080 5000 3000

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD curl -fsS http://127.0.0.1:${PORT:-8188}/ || exit 1

CMD ["/bin/bash", "/usr/local/bin/start.sh"]
