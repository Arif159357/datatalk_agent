# Deployment Guide

DataTalk is currently deployed on a cloud-hosted Ubuntu Virtual Machine. This document outlines the infrastructure and deployment steps taken to bring the application live.

## 🚀 Live Link
**URL:** http://36.50.41.122:8080/

## 🏗 Infrastructure Details
- **Provider:** [HexaZn](https://hexazn.com/)
- **OS:** Ubuntu
- **Hardware Specs:** 2 Core CPU, 4 GB RAM
- **Networking:** Port `8080` (Streamlit) is open via UFW firewall.

This Ubuntu VM provides a cost-effective environment tailored for a reliable deployment. The 2 Core CPU and 4 GB RAM ensure the containerized PostgreSQL database, FastAPI backend, and Streamlit frontend can run concurrently without facing out-of-memory errors or performance bottlenecks.

## 🛠 Deployment Steps Taken

### 1. Environment Preparation
The following tools were installed on the Ubuntu VM:
- Git
- Docker & Docker Compose
- Python 3.10+ & `venv`

### 2. Application Setup
The repository was cloned and initialized:
```bash
git clone https://github.com/Arif159357/datatalk_agent.git
cd datatalk_agent
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Database Startup
The PostgreSQL database was started in detached mode:
```bash
docker-compose up -d
```

### 4. Persistence with `tmux`
To ensure the application remains running after the SSH session ends, we used `tmux` to manage long-running processes:
- **Session 1 (Backend):** Running the FastAPI server.
  ```bash
  python src/api.py
  ```
- **Session 2 (Frontend):** Running the Streamlit UI on port 8080.
  ```bash
  streamlit run src/app.py --server.address=0.0.0.0 --server.port=8080
  ```

### 5. Firewall Configuration
Security was configured using `ufw` to allow external traffic to the frontend only:
```bash
sudo ufw allow 8080/tcp
sudo ufw reload
```

---
*Note: The FastAPI backend (port 5000) remains private to the VM and is accessed by the Streamlit frontend via localhost, ensuring a secure internal communication channel.*
