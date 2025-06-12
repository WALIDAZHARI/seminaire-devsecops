# DevSecOps Workshop Project

# DevSecOps Pipeline Workshop

This repository contains a simple DevSecOps pipeline demonstration project for educational purposes. The project showcases a complete CI/CD pipeline with security testing integration and monitoring capabilities, designed for a webinar/workshop setting.

## What is DevSecOps?

DevSecOps integrates security practices within the DevOps process. It involves introducing security earlier in the software development lifecycle through automation and collaboration between development, security, and operations teams.

## System Architecture

The project consists of the following components:

```
┌─────────────────────────────────────────────────────────────────────────┐
│                          DevSecOps Pipeline                              │
└───────────────────────────────────┬─────────────────────────────────────┘
                                    │
┌───────────────────────┐   ┌───────┴───────┐   ┌───────────────────────┐
│    Source Code        │   │   CI/CD       │   │     Deployment         │
│                       │   │               │   │                        │
│  ┌───────────────┐    │   │  ┌─────────┐ │   │   ┌─────────────┐     │
│  │ User Service  │────┼───┼─▶│ Jenkins │─┼───┼──▶│ Kubernetes  │     │
│  └───────────────┘    │   │  └────┬────┘ │   │   └─────────────┘     │
│                       │   │       │      │   │                        │
│  ┌───────────────┐    │   │       │      │   │                        │
│  │Product Service│────┼───┼───────┘      │   │                        │
│  └───────────────┘    │   │              │   │                        │
└───────────────────────┘   └──────┬───────┘   └───────────────────────┘
                                   │
         ┌─────────────────────────┼─────────────────────────┐
         │                         │                         │
┌────────┴────────┐      ┌────────┴────────┐      ┌─────────┴───────┐
│  Security Tests  │      │  Monitoring     │      │  Containerization│
│                  │      │                 │      │                  │
│ ┌─────────────┐  │      │ ┌─────────────┐ │      │ ┌─────────────┐ │
│ │  SonarQube  │  │      │ │ Prometheus  │ │      │ │   Docker    │ │
│ └─────────────┘  │      │ └─────────────┘ │      │ └─────────────┘ │
│                  │      │                 │      │                  │
│ ┌─────────────┐  │      │ ┌─────────────┐ │      │                  │
│ │    Trivy    │  │      │ │   Grafana   │ │      │                  │
│ └─────────────┘  │      │ └─────────────┘ │      │                  │
│                  │      │                 │      │                  │
│ ┌─────────────┐  │      │                 │      │                  │
│ │   Nuclei    │  │      │                 │      │                  │
│ └─────────────┘  │      │                 │      │                  │
└──────────────────┘      └─────────────────┘      └──────────────────┘
```

## Project Components

### 1. Microservices
- **User Service**: Python Flask service for user management (port 5555)
  - Endpoints: `/health`, `/users`, `/users/<id>`
  - Simple CRUD operations for user data

- **Product Service**: Python Flask service for product management (port 5556)
  - Endpoints: `/health`, `/products`, `/products/<id>`, `/products/user/<id>`
  - Demonstrates service-to-service communication by calling User Service

### 2. CI/CD Pipeline
- **Jenkins**: Orchestrates the entire pipeline
  - Automated build, test, security scan, and deployment stages
  - Integration with security tools

### 3. Security Testing
- **SonarQube**: Static Application Security Testing (SAST)
  - Code quality and security analysis
  - Identifies code vulnerabilities, bugs, and code smells

- **Trivy**: Container vulnerability scanning
  - Scans container images for vulnerabilities
  - Identifies package vulnerabilities in dependencies

- **Nuclei**: Dynamic Application Security Testing (DAST)
  - Tests running applications for security issues
  - Uses templates to identify common vulnerabilities

### 4. Deployment
- **Kubernetes**: Container orchestration
  - Deployments, Services, and Ingress resources
  - Scalable and resilient application deployment

### 5. Monitoring
- **Prometheus**: Metrics collection
  - Scrapes metrics from all services
  - Provides time-series data for monitoring

- **Grafana**: Visualization and dashboards
  - Pre-configured dashboards for service health
  - CPU, memory, and disk usage monitoring

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Git
- Kubernetes cluster (Minikube for local development)

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/seminaire-devsecops.git
   cd seminaire-devsecops
   ```

2. Run the setup script to prepare the environment and start all services:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```
   
   This script will:
   - Create necessary directories
   - Set appropriate permissions
   - Start all services using Docker Compose
   - Configure Jenkins with admin/admin credentials automatically (no need for initial setup)

3. Access the services:
   - Jenkins: http://localhost:8080
   - SonarQube: http://localhost:9000
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000
   - User Service: http://localhost:5555
   - Product Service: http://localhost:5556

## Running the DevSecOps Pipeline

1. Access Jenkins at http://localhost:8080
2. Login with the credentials (admin/admin)
3. The pipeline job should be automatically configured
4. Run the pipeline by clicking "Build Now"

## Demonstrating Security Vulnerabilities

For demonstration purposes, you can introduce the following vulnerabilities:

### 1. SQL Injection (for SonarQube to detect)

In the user-service/app.py file, modify the get_user function:

```python
@app.route('/users/<id>', methods=['GET'])
def get_user(id):
    # Vulnerable code - SQL injection
    query = "SELECT * FROM users WHERE id = " + id
    # Execute query...
    return jsonify({"user": {"id": id, "name": "User " + id}})
```

### 2. Dependency Vulnerability (for Trivy to detect)

Add a vulnerable dependency in requirements.txt:

```
flask==0.12.2  # Known vulnerable version
requests==2.18.0  # Known vulnerable version
```

### 3. Insecure Endpoint (for Nuclei to detect)

Add an insecure endpoint in the product-service/app.py:

```python
@app.route('/debug', methods=['GET'])
def debug():
    # Insecure debug endpoint that exposes system information
    import os
    system_info = os.popen('uname -a').read()
    return jsonify({"system_info": system_info})
```

## Workshop Presentation Guide

### 1. Introduction to DevSecOps (10 minutes)
- Explain the concept of DevSecOps
- Discuss the importance of integrating security into the CI/CD pipeline
- Present the architecture diagram

### 2. Microservices Overview (10 minutes)
- Explain the User Service and Product Service
- Show the code structure and API endpoints
- Demonstrate the services running

### 3. CI/CD Pipeline with Jenkins (15 minutes)
- Walk through the Jenkinsfile stages
- Explain how Jenkins orchestrates the pipeline
- Show a pipeline execution

### 4. Security Testing (20 minutes)
- Introduce the security vulnerabilities
- Run the pipeline to detect them
- Show how each tool (SonarQube, Trivy, Nuclei) identifies different types of vulnerabilities

### 5. Kubernetes Deployment (10 minutes)
- Explain the Kubernetes manifests
- Show the deployed services

### 6. Monitoring with Prometheus and Grafana (10 minutes)
- Show the Grafana dashboards
- Explain the metrics being collected

### 7. Q&A and Discussion (15 minutes)
- **Prometheus**: Metrics collection and alerting
- **Grafana**: Visualization and dashboarding for monitoring data

## Project Structure
```
seminaire-devsecops/
├── services/
│   ├── user-service/       # Python-based user service
│   └── product-service/    # Python-based product service
├── jenkins/                # Jenkins configuration and pipeline definitions
├── kubernetes/             # Kubernetes manifests for deployment
├── security/
│   ├── sonarqube/          # SonarQube configuration for SAST
│   ├── trivy/              # Trivy configuration for SCA
│   └── nuclei/             # Nuclei configuration for DAST
└── monitoring/
    ├── prometheus/         # Prometheus configuration
    └── grafana/            # Grafana dashboards and configuration
```

## Workshop Steps

1. **Setup Development Environment**
   - Install Docker and Docker Compose
   - Clone the repository

2. **Build Microservices**
   - Develop User and Product services in Python
   - Create Dockerfiles for each service
   - Test services locally

3. **Setup CI/CD Pipeline**
   - Configure Jenkins with Docker
   - Create Jenkinsfile with pipeline stages
   - Setup webhook integration

4. **Implement Security Testing**
   - Configure SonarQube for SAST
   - Setup Trivy for container scanning
   - Configure Nuclei for DAST

5. **Setup Kubernetes Deployment**
   - Create Kubernetes manifests
   - Configure deployment, services, and ingress

6. **Implement Monitoring**
   - Setup Prometheus for metrics collection
   - Configure Grafana dashboards
   - Implement alerting

7. **Run Complete Pipeline**
   - Trigger Jenkins pipeline
   - Observe security testing results
   - Monitor deployment in Kubernetes
   - View metrics in Grafana

## Prerequisites
- Docker and Docker Compose
- kubectl (Kubernetes CLI)
- Git

## Getting Started
Detailed instructions for each step will be provided during the workshop.
