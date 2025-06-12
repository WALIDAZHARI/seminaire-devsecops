# DevSecOps Pipeline Architecture

```mermaid
graph TD
    subgraph "Source Code"
        US[User Service]
        PS[Product Service]
    end

    subgraph "CI/CD Pipeline"
        J[Jenkins]
        subgraph "Security Testing"
            SQ[SonarQube - SAST]
            T[Trivy - Container Scanning]
            N[Nuclei - DAST]
        end
    end

    subgraph "Deployment"
        K[Kubernetes/Minikube]
        subgraph "Deployed Services"
            USK[User Service Pod]
            PSK[Product Service Pod]
        end
    end

    subgraph "Monitoring"
        P[Prometheus]
        G[Grafana]
    end

    US --> J
    PS --> J
    J --> SQ
    J --> T
    J --> |Build & Push| DH[Docker Hub]
    DH --> |Pull Images| K
    J --> |Deploy| K
    K --> USK
    K --> PSK
    J --> N
    USK --> P
    PSK --> P
    P --> G
    N --> |Test Deployed Apps| USK
    N --> |Test Deployed Apps| PSK
    
    classDef sourceCode fill:#e1f5fe,stroke:#01579b,stroke-width:2px;
    classDef cicd fill:#fff8e1,stroke:#ff6f00,stroke-width:2px;
    classDef security fill:#ffebee,stroke:#c62828,stroke-width:2px;
    classDef deployment fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px;
    classDef monitoring fill:#ede7f6,stroke:#4527a0,stroke-width:2px;
    
    class US,PS sourceCode;
    class J cicd;
    class SQ,T,N security;
    class K,USK,PSK deployment;
    class P,G monitoring;
```

## Components Description

### Source Code
- **User Service**: Python Flask microservice for user management
- **Product Service**: Python Flask microservice for product management that communicates with User Service

### CI/CD Pipeline
- **Jenkins**: Orchestrates the entire pipeline with stages for build, test, security scanning, and deployment
  
### Security Testing
- **SonarQube**: Static Application Security Testing (SAST) to detect code vulnerabilities
- **Trivy**: Container vulnerability scanner to detect issues in Docker images
- **Nuclei**: Dynamic Application Security Testing (DAST) to test running applications

### Deployment
- **Kubernetes/Minikube**: Local Kubernetes cluster for container orchestration
- **Deployed Services**: Containerized microservices running in Kubernetes pods

### Monitoring
- **Prometheus**: Metrics collection and monitoring
- **Grafana**: Visualization dashboards for metrics and performance monitoring

## Data Flow

1. Developers push code to the repository
2. Jenkins pipeline is triggered
3. Code is built and tested
4. Security scans are performed (SAST with SonarQube)
5. Docker images are built and scanned (with Trivy)
6. Images are pushed to Docker Hub
7. Kubernetes manifests are updated with new image tags
8. Applications are deployed to Kubernetes/Minikube
9. DAST scans are performed on the running applications (with Nuclei)
10. Metrics are collected by Prometheus and visualized in Grafana
