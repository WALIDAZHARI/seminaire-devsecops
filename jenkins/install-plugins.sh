#!/bin/bash

# List of plugins to install
JENKINS_PLUGINS=(
  # Kubernetes integration
  "kubernetes"
  "kubernetes-credentials"
  "kubernetes-client-api"
  
  # Docker integration
  "docker-workflow"
  "docker-plugin"
  
  # Pipeline and visualization
  "pipeline-utility-steps"
  "pipeline-stage-view"
  "pipeline-graph-analysis"
  "pipeline-model-definition"
  "pipeline-build-step"
  "pipeline-milestone-step"
  "pipeline-input-step"
  
  # Git integration
  "git"
  "git-client"
  "github"
  "github-branch-source"
  "github-api"
  
  # Credentials
  "credentials-binding"
  "plain-credentials"
  "ssh-credentials"
  
  # UI and visualization
  "workflow-aggregator"
  "blueocean"
  "dashboard-view"
  
  # Utilities
  "timestamper"
  "ws-cleanup"
  "ansicolor"
  "build-timeout"
)

echo "Installing Jenkins plugins..."
# Install plugins using Jenkins CLI
for plugin in "${JENKINS_PLUGINS[@]}"
do
  echo "Installing plugin: $plugin"
  docker exec jenkins jenkins-plugin-cli --plugins "$plugin" || echo "Failed to install $plugin, continuing..."
done

# Restart Jenkins to apply plugins
echo "Restarting Jenkins to apply plugins..."
docker restart jenkins

echo "Plugin installation completed! Waiting for Jenkins to restart..."
sleep 30
echo "Jenkins should be ready now."
