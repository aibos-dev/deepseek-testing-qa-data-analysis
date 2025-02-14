# QA Category Analysis Project

A tool for analyzing question-answer pairs using GPU-accelerated large language models. This project processes data in batches, monitors GPU usage, and generates detailed categorized analysis.

## Overview

This tool performs automated analysis of question-answer data using LLMs, with features including:
- Batch processing of QA data entries
- Real-time GPU usage monitoring
- Detailed categorization and analysis
- Automated result merging and statistics generation

## Prerequisites

- Docker with NVIDIA Container Toolkit
- NVIDIA GPU with CUDA support (minimum 24GB VRAM recommended)
- Docker Compose (for development container)

## Project Structure

```
qa_data_analysis/
├── .devcontainer/                  # Development container configuration
│   └── devcontainer.json          # VS Code dev container settings
├── src/
│   ├── run.sh                     # Main execution script
│   ├── put_label.py               # LLM inference for labeling
│   ├── merge.py                   # Merges analysis results
│   └── count.py                   # Processes result counts
├── Dockerfile                      # Container definition
├── pyproject.toml                  # Project dependencies and metadata
├── uv.lock                        # Dependency lock file
└── README.md
```

## Development Environment

The project uses a custom Docker development container with the following specifications:

### Base Configuration
- Base Image: `nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04`
- Python Version: 3.12.4
- Package Manager: UV
- Time Zone: Africa/Nairobi
- Character Encoding: UTF-8

### Container Features
- CUDA 11.8 with cuDNN 8 support
- Custom Python build with optimizations
- UV package manager pre-installed
- Non-root user setup (`devuser`)
- Workspace mounted at `/workspace`

### Setting Up Development Environment

1. Ensure Docker and NVIDIA Container Toolkit are installed:
```bash
# Verify NVIDIA Docker installation
docker run --gpus all nvidia/cuda:11.8.0-base nvidia-smi
```

2. Build and start the development container:
```bash
# Using VS Code
1. Open the project in VS Code
2. Install "Remote - Containers" extension
3. Press F1 and select "Remote-Containers: Reopen in Container"

# Or using Docker directly
docker build -t qa-analysis-dev .
docker run --gpus all -v $(pwd):/workspace qa-analysis-dev
```

### Dependencies Management

Dependencies are managed using UV package manager inside the container:

```bash
# Sync dependencies from pyproject.toml
uv sync
```

## Model Requirements

Place the following models in `/workspace/models/`:
- DeepSeek-R1-Distill-Llama-70B-IQ2_XS-00001-of-00002.gguf
- DeepSeek-R1-Distill-Llama-70B-IQ3_S-00001-of-00003.gguf

## Usage

### Running the Analysis

From within the container:

```bash
cd /workspace
./src/run.sh output_folder
```

### Processing Flow

The tool will:
1. Process QA data in batches of 5 entries
2. Generate up to 10 analysis files
3. Monitor GPU usage throughout processing
4. Automatically run merge and count analysis upon completion

### Output Files

The tool generates several types of output:
- Analysis files: `output_folder/YYYYMMDD_HHMMSS.txt`
- GPU monitoring: `output_folder/gpu_usage.log`
- Merged results: `output_folder/merged_results.json`
- Statistics: `output_folder/analysis_counts.json`

## GPU Monitoring

### Metrics Tracked
- GPU utilization percentage
- Memory usage
- Total available memory

### Monitoring Details
- Sampling interval: 60 seconds
- Log location: `output_folder/gpu_usage.log`
- Automatic cleanup on script completion

## System Limitations

- Maximum 10 output files per run
- Processing timeout: 1 hour per batch
- Minimum GPU memory: 24GB recommended
- Single GPU support only

## Troubleshooting

### Common Issues

1. Container GPU Access
```bash
# Verify GPU access inside container
nvidia-smi
```

2. Model Loading Failures
- Verify model paths in `put_label.py`
- Ensure models are mounted correctly in the container

3. Dependencies Issues
```bash
# Refresh dependencies
uv sync
```

### Best Practices

- Monitor GPU memory usage during processing
- Keep output folder paths short to avoid path length issues
- Use the provided development container for consistent environment
- Regularly check GPU logs for performance issues

