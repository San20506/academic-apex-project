#!/bin/bash
# Academic Apex - Oracle Cloud Deployment Script
# Deploys to Oracle Cloud Always Free Tier (ARM64 VM)

set -e

echo "🚀 Academic Apex - Oracle Cloud Deployment"
echo "=========================================="

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Docker
echo "🐳 Installing Docker..."
sudo apt install -y apt-transport-https ca-certificates curl gnupg lsb-release
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
sudo apt update
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# Install Docker Compose
echo "📦 Installing Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.20.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Ollama
echo "🤖 Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
echo "🔧 Setting up Ollama service..."
sudo systemctl enable ollama
sudo systemctl start ollama

# Wait for Ollama to start
echo "⏳ Waiting for Ollama to initialize..."
sleep 10

# Pull required AI model
echo "📥 Downloading AI model (this may take a few minutes)..."
ollama pull mistral:7b

# Clone repository (if not already present)
if [ ! -d "academic-apex-project" ]; then
    echo "📂 Cloning Academic Apex repository..."
    git clone https://github.com/yourusername/academic-apex-project.git
fi

cd academic-apex-project

# Create environment file
echo "⚙️  Setting up environment configuration..."
cat > .env << EOF
# Academic Apex - Production Configuration
OLLAMA_HOST=http://localhost:11434
DEFAULT_MODEL=mistral:7b
CURATOR_MODEL=mistral:7b
CURATOR_SERVICE_URL=http://localhost:5001
WEB_UI_PORT=5000
API_PORT=8000
OBSIDIAN_VAULT_PATH=
UPLOAD_DIR=./uploads
GENERATED_DIR=./generated
DEBUG=false
COMPOSE_PROJECT_NAME=academic_apex
EOF

# Create production Docker Compose file
echo "🐳 Setting up Docker configuration..."
cat > docker-compose.prod.yml << 'EOF'
version: '3.8'

services:
  # Academic Apex Web UI (Main Application)
  web-ui:
    build:
      context: ./agentforge_academic_apex
      dockerfile: Dockerfile
    container_name: academic_apex_web
    ports:
      - "80:5000"
      - "5000:5000"
    environment:
      - OLLAMA_HOST=http://host.docker.internal:11434
      - CURATOR_SERVICE_URL=http://curator:5001
      - WEB_UI_PORT=5000
    volumes:
      - ./generated:/app/generated
      - ./uploads:/app/uploads
    depends_on:
      - curator
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Curator Service
  curator:
    build:
      context: ./agentforge_academic_apex
      dockerfile: Dockerfile.curator
    container_name: academic_apex_curator
    ports:
      - "5001:5001"
    environment:
      - OLLAMA_HOST=http://host.docker.internal:11434
      - CURATOR_MODEL=mistral:7b
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5001/healthz"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  generated_data:
  uploads_data:

networks:
  default:
    name: academic_apex_network
EOF

# Create Dockerfile for web UI
echo "🐳 Creating Docker images..."
cat > agentforge_academic_apex/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directories
RUN mkdir -p /app/generated /app/uploads /app/static /app/logs

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run the application
CMD ["python", "web_ui.py"]
EOF

# Create Dockerfile for curator
cat > agentforge_academic_apex/Dockerfile.curator << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt flask

# Copy application files
COPY curator_service.py .
COPY ollama_adapter.py .

# Expose port
EXPOSE 5001

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:5001/healthz || exit 1

# Run the curator service
CMD ["python", "curator_service.py"]
EOF

# Set up firewall
echo "🔥 Configuring firewall..."
sudo ufw allow ssh
sudo ufw allow 80
sudo ufw allow 443
sudo ufw allow 5000
sudo ufw --force enable

# Build and start services
echo "🏗️  Building and starting Academic Apex..."
docker-compose -f docker-compose.prod.yml build
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to start
echo "⏳ Waiting for services to initialize..."
sleep 30

# Get public IP
PUBLIC_IP=$(curl -s ifconfig.me)

echo ""
echo "✅ Academic Apex deployment complete!"
echo "=========================================="
echo "🌐 Academic Apex URL: http://$PUBLIC_IP"
echo "🌐 Alternative URL: http://$PUBLIC_IP:5000"
echo "🤖 Ollama Status: $(systemctl is-active ollama)"
echo "🐳 Docker Status: $(docker ps --format 'table {{.Names}}\t{{.Status}}')"
echo ""
echo "📋 Next steps:"
echo "1. Visit your Academic Apex instance at: http://$PUBLIC_IP"
echo "2. Test quiz generation and study plans"
echo "3. Configure domain name (optional)"
echo ""
echo "🔧 Management commands:"
echo "- View logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "- Restart: docker-compose -f docker-compose.prod.yml restart"
echo "- Stop: docker-compose -f docker-compose.prod.yml down"
echo ""
echo "🎉 Academic Apex is now live on Oracle Cloud!"
