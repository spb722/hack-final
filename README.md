# ADK Voice Agent

A real-time voice assistant powered by Google ADK (Agent Development Kit) with support for both text and voice interactions. This application provides a web-based interface for interacting with AI agents using Google's latest Gemini models.

## Features

- **Real-time Voice Interaction**: Full duplex voice conversations with AI
- **Text Chat Interface**: Traditional text-based chat functionality  
- **Multi-Agent System**: Specialized agents for different financial and analytical tasks
- **WebSocket Communication**: Real-time bidirectional communication
- **Docker Support**: Easy deployment using Docker and Docker Compose
- **Google ADK Integration**: Built on Google's Agent Development Kit

## Prerequisites

- Docker and Docker Compose
- Google Cloud Platform account with API access
- Google OAuth 2.0 credentials
- Google API key for Gemini

## Quick Start with Docker

### 1. Clone and Setup

```bash
git clone <repository-url>
cd adk-voice-agent
```

### 2. Environment Configuration

Create a `.env` file in the root directory:

```bash
GOOGLE_API_KEY=your_google_api_key_here
```

Add your Google OAuth 2.0 credentials as `credentials.json` in the root directory.

### 3. Run with Docker Compose

```bash
# Start the application
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### 4. Using the Convenience Script

The project includes a helper script for easier Docker management:

```bash
# Make the script executable
chmod +x docker-run.sh

# Start the application
./docker-run.sh up

# View logs
./docker-run.sh logs

# Stop the application
./docker-run.sh down

# Rebuild and restart
./docker-run.sh rebuild
```

#### Available Script Commands:

- `up/start` - Start the application
- `down/stop` - Stop the application  
- `restart` - Restart the application
- `logs` - Show application logs
- `build` - Build Docker image
- `rebuild` - Rebuild image and start application
- `status` - Show container status
- `clean` - Clean up Docker resources

## Access the Application

Once running, access the web interface at:
- **Web UI**: http://localhost:8000

The interface provides:
- Text input for chat messages
- Voice recording toggle
- Real-time conversation display
- Connection status indicators

## Setup for ADK Web Integration

### Prerequisites for ADK

1. **Google Cloud Setup**:
   - Enable the Generative AI API
   - Create OAuth 2.0 credentials (Desktop application type)
   - Download credentials as `credentials.json`

2. **API Key**:
   - Create a Google API key with access to Generative AI API
   - Add to `.env` file as `GOOGLE_API_KEY`

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GOOGLE_API_KEY` | Your Google API key for Gemini | Yes |
| `GOOGLE_APPLICATION_CREDENTIALS` | Path to OAuth credentials (auto-set in Docker) | Yes |
| `HOST` | Application host (default: 0.0.0.0) | No |
| `PORT` | Application port (default: 8000) | No |

## Architecture

### Components

- **FastAPI Backend**: Handles WebSocket connections and HTTP requests
- **Google ADK Integration**: Manages AI agent sessions and real-time communication
- **Multi-Agent System**: Specialized agents for different domains
- **Web Frontend**: Modern web interface with voice recording capabilities

### Agent System

The application includes specialized agents:
- Financial Intelligence Agent (MCP FI Agent)
- Funny Nerd Agent
- Goal-Based Casting Agent
- Transaction Analyst
- News Analyst
- Smart Cashflow Guardian
- Stock Analyst

### WebSocket API

The application uses WebSocket for real-time communication:

- **Endpoint**: `/ws/{session_id}?is_audio={true|false}`
- **Message Format**: JSON with `mime_type`, `data`, and `role` fields
- **Supported Types**: `text/plain` and `audio/pcm`

## Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GOOGLE_API_KEY=your_api_key
export GOOGLE_APPLICATION_CREDENTIALS=./credentials.json

# Run the application
cd app
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Project Structure

```
adk-voice-agent/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── mcp_fi_agent/           # Main agent system
│   │   ├── agent.py
│   │   ├── sub_agents/         # Specialized agents
│   │   └── tools/              # Agent tools
│   └── static/                 # Web interface
│       ├── index.html
│       └── js/                 # Frontend JavaScript
├── Dockerfile                  # Docker configuration
├── docker-compose.yml          # Docker Compose setup
├── docker-run.sh              # Convenience script
├── requirements.txt           # Python dependencies
└── credentials.json           # Google OAuth credentials
```

## Troubleshooting

### Common Issues

1. **Port 8000 in use**:
   ```bash
   ./kill_port_8000.sh
   ```

2. **Missing credentials**:
   - Ensure `credentials.json` exists in root directory
   - Verify `GOOGLE_API_KEY` in `.env` file

3. **Docker build fails**:
   ```bash
   docker-compose build --no-cache
   ```

4. **Connection timeout**:
   - Check Google API key validity
   - Verify network connectivity
   - Review container logs

### Health Check

The application includes a health check endpoint accessible at `http://localhost:8000/` that verifies the service is running correctly.

## Security Notes

- Keep `credentials.json` and `.env` files secure and never commit them to version control
- The application runs on localhost by default - configure firewall rules if exposing externally
- Use HTTPS in production environments

## License

[Add your license information here]

## Contributing

[Add contribution guidelines here]
