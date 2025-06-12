#!/bin/bash

# DevSecOps Workshop Setup Script
# This script helps set up the environment for the DevSecOps workshop

echo "===== DevSecOps Workshop Setup ====="
echo "Setting up environment..."

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! docker compose version &> /dev/null; then
    echo "Docker Compose plugin is not installed. Please install Docker Compose plugin first."
    exit 1
fi

# Create necessary directories if they don't exist
echo "Creating necessary directories..."
mkdir -p monitoring/grafana/data
mkdir -p monitoring/prometheus/data
mkdir -p jenkins/data
mkdir -p sonarqube/data
mkdir -p sonarqube/extensions
mkdir -p jenkins/init.groovy.d

# Set permissions for volumes
echo "Setting permissions for volumes..."
chmod -R 777 monitoring/grafana/data
chmod -R 777 monitoring/prometheus/data
chmod -R 777 jenkins/data
chmod -R 777 sonarqube/data
chmod -R 777 sonarqube/extensions

# Start the services
echo "Starting services with Docker Compose..."
docker compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 30

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
