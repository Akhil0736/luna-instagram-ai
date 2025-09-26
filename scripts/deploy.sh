#!/bin/bash
# scripts/deploy.sh - Production deployment script

set -e

echo "🚀 Deploying Luna AI to Production..."

# Check environment
if [ ! -f ".env.production" ]; then
    echo "❌ .env.production file not found"
    exit 1
fi

# Load production environment
source .env.production

# Build and deploy
echo "🔨 Building Docker images..."
docker-compose -f docker-compose.production.yml build

echo "🚀 Starting services..."
docker-compose -f docker-compose.production.yml up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 30

# Health check
echo "🔍 Running health checks..."
if curl -f http://localhost:8000/luna/health; then
    echo "✅ Luna AI is healthy!"
else
    echo "❌ Health check failed"
    docker-compose -f docker-compose.production.yml logs
    exit 1
fi

# Clean up old images
echo "🧹 Cleaning up..."
docker system prune -f

echo "🎉 Deployment complete!"
echo "🌐 Luna AI is running at http://localhost:8000"
echo "📊 Grafana dashboard at http://localhost:3000"
echo "📈 Prometheus at http://localhost:9090"
