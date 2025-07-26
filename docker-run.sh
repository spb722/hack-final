#!/bin/bash

# Docker run script for ADK Voice Agent
# This script provides easy commands to manage the Docker deployment

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if docker-compose is available
if ! command -v docker-compose &> /dev/null; then
    print_error "docker-compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Check if required files exist
if [ ! -f "credentials.json" ]; then
    print_warning "credentials.json not found. Make sure to add your Google OAuth credentials."
fi

if [ ! -f ".env" ]; then
    print_warning ".env file not found. Make sure to add your GOOGLE_API_KEY."
fi

# Main script logic
case "${1:-}" in
    "up"|"start")
        print_status "Starting ADK Voice Agent..."
        docker-compose up -d
        print_status "Application is starting up..."
        print_status "The UI will be available at: http://localhost:8000"
        print_status "Use 'docker-compose logs -f' to view logs"
        ;;
    
    "down"|"stop")
        print_status "Stopping ADK Voice Agent..."
        docker-compose down
        print_status "Application stopped successfully"
        ;;
    
    "restart")
        print_status "Restarting ADK Voice Agent..."
        docker-compose down
        docker-compose up -d
        print_status "Application restarted successfully"
        ;;
    
    "logs")
        print_status "Showing application logs..."
        docker-compose logs -f
        ;;
    
    "build")
        print_status "Building Docker image..."
        docker-compose build --no-cache
        print_status "Docker image built successfully"
        ;;
    
    "rebuild")
        print_status "Rebuilding and starting ADK Voice Agent..."
        docker-compose down
        docker-compose build --no-cache
        docker-compose up -d
        print_status "Application rebuilt and started successfully"
        ;;
    
    "status")
        print_status "Checking application status..."
        docker-compose ps
        ;;
    
    "clean")
        print_status "Cleaning up Docker resources..."
        docker-compose down -v --remove-orphans
        docker system prune -f
        print_status "Cleanup completed"
        ;;
    
    *)
        echo "Usage: $0 {up|down|restart|logs|build|rebuild|status|clean}"
        echo ""
        echo "Commands:"
        echo "  up/start    - Start the application"
        echo "  down/stop   - Stop the application"
        echo "  restart     - Restart the application"
        echo "  logs        - Show application logs"
        echo "  build       - Build Docker image"
        echo "  rebuild     - Rebuild image and start application"
        echo "  status      - Show container status"
        echo "  clean       - Clean up Docker resources"
        exit 1
        ;;
esac