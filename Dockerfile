# Base image with CUDA and cuDNN support
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04

# Build arguments for customization
ARG PYTHON_VERSION=3.12.4
ARG PYTHON_MAJOR=3.12
ARG UID=1001
ARG GID=${UID}
ARG USERNAME=devuser
ARG GROUPNAME=devgroup

# Environment variables for localization and build configuration
ENV TZ=Africa/Nairobi \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8 \
    PYTHONIOENCODING=utf-8 \
    DEBIAN_FRONTEND=noninteractive \
    # UV package manager configuration
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PYTHON=python$PYTHON_MAJOR \
    UV_PROJECT_ENVIRONMENT="/workspace/qa-category-analysis" 

# Install system dependencies and Python
WORKDIR /tmp/
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && apt-get update && apt-get install -y --no-install-recommends \
       sudo \
       git \
       zip \
       wget \
       curl \
       make \
       llvm \
       ffmpeg \
       tzdata \
       tk-dev \
       graphviz \
       xz-utils \
       zlib1g-dev \
       libssl-dev \
       libbz2-dev \
       libffi-dev \
       liblzma-dev \
       libsqlite3-dev \
       libgl1-mesa-dev \
       libreadline-dev \
       libncurses5-dev \
       libncursesw5-dev \
       build-essential \
    && cd /usr/local/ && wget https://www.python.org/ftp/python/$PYTHON_VERSION/Python-$PYTHON_VERSION.tar.xz \
    && tar xvf Python-$PYTHON_VERSION.tar.xz \
    && cd /usr/local/Python-$PYTHON_VERSION \
    && ./configure --enable-optimizations \
    && make install \
    && rm /usr/local/Python-$PYTHON_VERSION.tar.xz \
    && cd /usr/local/Python-$PYTHON_VERSION \
    && ln -fs /usr/local/Python-$PYTHON_VERSION/python /usr/bin/python \
    && apt-get autoremove -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/* /usr/local/src/* /tmp/*

# Install UV package manager
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
RUN chmod +x /usr/local/bin/uv && uv --version

# Create non-root user and set up workspace
RUN groupadd -g ${GID} ${GROUPNAME} -f && \
    useradd -m -s /bin/bash -u ${UID} -g ${GID} -c "Docker image user" ${USERNAME} && \
    usermod -aG sudo ${USERNAME} && \
    echo "${USERNAME} ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers && \
    chown -R ${USERNAME}:${GROUPNAME} /opt && \
    chown -R ${USERNAME}:${GROUPNAME} /usr/local && \
    mkdir -p /workspace && \
    chown -R ${USERNAME}:${GROUPNAME} /workspace

USER ${USERNAME}:${GROUPNAME}
WORKDIR /workspace

# (Optional) Copy your entire project into /workspace if not already mounted by devcontainer
COPY . /workspace

# Default command
CMD ["bash"]
