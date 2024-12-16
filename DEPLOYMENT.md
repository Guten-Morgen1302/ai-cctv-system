# SecureVista Deployment Guide

## Prerequisites
- Python 3.9+
- CUDA 11.8+ (for GPU acceleration)
- 8GB RAM minimum
- Ubuntu 20.04 LTS recommended

## Installation Steps

### 1. Environment Setup
```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

### 3. Run System
```bash
python app.py
# Access at http://localhost:5002
```

## Docker Deployment
```bash
docker build -t securevista:latest .
docker run -p 5002:5002 --gpus all securevista:latest
```

## Production Deployment
- Use Gunicorn with 4+ workers
- Enable SSL/TLS termination
- Set up monitoring and alerting
- Configure log rotation

## Troubleshooting
- GPU not detected: Check CUDA installation
- Low FPS: Reduce resolution or enable frame skip
- Memory issues: Reduce batch size or enable swap

## Support
Contact: support@securevista.dev
