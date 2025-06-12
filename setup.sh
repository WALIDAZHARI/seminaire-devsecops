#!/bin/bash

# DevSecOps Workshop Setup Script
# This script helps set up the environment for the DevSecOps workshop

echo "===== DevSecOps Workshop Setup ====="

# Function to check if a command exists
check_command() {
    if ! command -v $1 &> /dev/null; then
        echo "$1 is not installed. Please install $1 first."
        return 1
    fi
    return 0
}

# Check for required tools
check_command docker || exit 1
if ! docker compose version &> /dev/null; then
    echo "Docker Compose plugin is not installed. Please install Docker Compose plugin first."
    exit 1
fi
check_command minikube || exit 1
check_command kubectl || exit 1

# Ask for confirmation to reset everything
read -p "Do you want to completely reset the environment? This will remove all containers, volumes, and Minikube cluster (y/n): " reset_choice
if [[ "$reset_choice" == "y" || "$reset_choice" == "Y" ]]; then
    echo "Stopping all containers..."
    docker compose down -v
    
    echo "Removing Docker volumes..."
    docker volume prune -f
    
    echo "Stopping and deleting Minikube cluster..."
    minikube stop || true
    minikube delete || true
    
    echo "Cleaning up directories..."
    rm -rf monitoring/grafana/data
    rm -rf monitoring/prometheus/data
    rm -rf jenkins/data
    rm -rf sonarqube/data
    rm -rf sonarqube/extensions
    rm -rf kubernetes/temp
    
    echo "Environment reset complete."
fi

# Create necessary directories if they don't exist
echo "Creating necessary directories..."
mkdir -p monitoring/grafana/data
mkdir -p monitoring/prometheus/data
mkdir -p jenkins/data
mkdir -p sonarqube/data
mkdir -p sonarqube/extensions
mkdir -p jenkins/init.groovy.d
mkdir -p kubernetes/temp

# Set permissions for volumes
echo "Setting permissions for volumes..."
chmod -R 777 monitoring/grafana/data
chmod -R 777 monitoring/prometheus/data
chmod -R 777 jenkins/data
chmod -R 777 sonarqube/data
chmod -R 777 sonarqube/extensions

# Start Minikube if it's not running
echo "Checking Minikube status..."
if ! minikube status | grep -q "Running"; then
    echo "Starting Minikube..."
    minikube start --driver=docker
    
    echo "Enabling Minikube addons..."
    minikube addons enable ingress
    minikube addons enable metrics-server
fi

# Start the services
echo "Starting services with Docker Compose..."
docker compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

# Install Jenkins plugins
echo "Installing Jenkins plugins..."
chmod +x jenkins/install-plugins.sh
./jenkins/install-plugins.sh

echo "===== Setup Complete ====="
echo ""
echo "Access the services at:"
echo "- Jenkins: http://localhost:8080"
echo "- SonarQube: http://localhost:9000"
echo "- Prometheus: http://localhost:9090"
echo "- Grafana: http://localhost:3000"
echo "- User Service: http://localhost:5555"
echo "- Product Service: http://localhost:5556"
echo ""
echo "Default credentials:"
echo "- Jenkins: admin/admin"
echo "- SonarQube: admin/admin"
echo "- Grafana: admin/admin"
echo ""
echo "To introduce vulnerabilities for demonstration, check the README.md file."
echo ""
echo "To stop all services: docker compose down"
