ssh-keygen -t ed25519 -C "thesociaalhive@gmail.com"
clear
ssh-keygen -t ed25519 -C "thesociaalhive@gmail.com"
/Users/akhilsajan/Documents/pepper
clear
ssh-keygen -t ed25519 -C "thesociaalhive@gmail.com"
ls -la ~/.ssh
# Display your existing public key
cat ~/.ssh/id_ed25519.pub
# OR if you have RSA key:
cat ~/.ssh/id_rsa.pub
clear
# Clone Luna with all submodules
git clone --recurse-submodules https://github.com/Akhil0736/luna-instagram-ai.git
# Navigate to Luna directory
cd luna-instagram-ai
# Verify repository structure
ls -la
# Create environment variables file
cat > .env << 'EOF'
RIONA_API_TOKEN=placeholder_token
APIFY_TOKEN=
SCRAPEDO_API_KEY=
TAVILY_API_KEY=
EOF

# Verify .env file created
cat .env
# Build and start all 5 services (Ollama, OpenManus, Riona, Frontend, Redis)
docker compose up -d --build
# Wait 30 seconds for services to initialize
sleep 30
# Check running containers
docker ps
# Open the file for editing
nano docker-compose.yml
# Clean up any failed containers
docker compose down
# Build and start all services
docker compose up -d --build
# Wait for services to initialize
sleep 30
# Check running containers
docker ps
clear
# Edit docker-compose.yml
nano docker-compose.yml
# Clean up previous attempts
docker compose down
# Deploy core Luna services
docker compose up -d --build
# Wait for initialization
sleep 30
# Check running containers
docker ps
# Check if riona directory exists
ls -la ./integration/riona/
# Check for specific files
ls -la ./integration/riona/Dockerfile
ls -la ./integration/riona/requirements.txt
ls -la ./integration/riona/app.py
cat > ./integration/riona/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Start command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
EOF

cat > ./integration/riona/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
requests==2.31.0
python-multipart==0.0.6
python-dotenv==1.0.0
aiofiles==23.2.1
httpx==0.25.2
EOF

cat > ./integration/riona/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8080

# Start command
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]
EOF

# Clean up previous attempts
docker compose down
# Build all services including Riona
docker compose up -d --build
# Wait for initialization
sleep 30
# Check all running containers
docker ps
# Check OpenManus container logs
docker logs openmanus --tail 30
# Check Riona container logs  
docker logs riona --tail 30
# Navigate to OpenManus source
cd ~/luna-instagram-ai/integration/openmanus_service
# Edit the problematic app.py file
nano app.py
# Go back to project root
cd ~/luna-instagram-ai
# Rebuild OpenManus container with the fix
docker compose build openmanus
# Restart all containers
docker compose up -d
# Check container status
docker ps
docker logs riona --tail 100
# Create minimal working FastAPI app
cat > ./integration/riona/app.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Riona Instagram Automation", version="0.1.0")

# CORS setup
origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "service": "Riona Instagram Automation",
        "version": "0.1.0",
        "status": "operational"
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/tasks/post")
async def create_post_task(task_data: dict):
    return {
        "status": "task_created",
        "task_id": f"post_{hash(str(task_data))}",
        "message": "Instagram post task created"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
EOF

# Create minimal requirements.txt
cat > ./integration/riona/requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
EOF

# Check if Dockerfile exists and has correct content
cat ./integration/riona/Dockerfile
# Clean up and rebuild
docker compose down
docker compose build riona --no-cache
docker compose up -d
# Check status
docker ps
# Watch logs in real-time
docker logs riona -f
clear
# Test OpenManus backend health
curl http://localhost:8000/
# Test Riona automation service  
curl http://localhost:8080/
# Test Luna's semantic understanding (the revolutionary feature!)
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "I want to grow my fitness Instagram from 500 to 5000 followers in 60 days"}'
# Check OpenManus logs for errors
docker logs openmanus --tail 50
# Check if it's a memory issue
docker stats --no-stream
# Restart OpenManus and watch logs live
docker restart openmanus
docker logs -f openmanus
# Download semantic embedding model (this takes 5-10 minutes)
docker exec -it ollama ollama pull mxbai-embed-large &
# Check download progress
docker exec -it ollama ollama list
# Navigate to OpenManus source directory
cd ~/luna-instagram-ai/integration/openmanus_service
# Edit the problematic app.py file
nano app.py
# Go back to Luna project root
cd ~/luna-instagram-ai
# Rebuild OpenManus container with the fix
docker compose build openmanus
# Restart all containers
docker compose up -d
# Check if OpenManus is now running successfully
docker ps
# Check OpenManus logs for success
docker logs openmanus --tail 10
# Test the API
curl http://localhost:8000/
clear
docker exec -it ollama ollama pull mxbai-embed-large
# Restart OpenManus so it can connect to the downloaded model
docker restart openmanus
# Check logs to verify model loading
docker logs openmanus --tail 20
# Test semantic availability
curl http://localhost:8000/
# Test Luna's revolutionary semantic understanding
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "I want to grow my fitness Instagram from 500 to 5000 followers in 60 days"}'
# Add OpenAI package to OpenManus requirements
cat >> ./integration/openmanus_service/requirements.txt << 'EOF'
openai==1.3.0
httpx==0.25.2
ollama==0.1.7
EOF

# Rebuild OpenManus with new dependencies
docker compose build openmanus
docker compose up -d
# Check logs for semantic engine startup
docker logs openmanus --tail 20
# Test semantic intelligence
curl http://localhost:8000/
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "I want to grow my fitness Instagram from 500 to 5000 followers in 60 days"}'
# Remove conflicting package versions
cat > ./integration/openmanus_service/requirements.txt << 'EOF'
fastapi==0.111.0
uvicorn==0.30.1
pydantic>=2.7.0
requests==2.31.0
python-multipart==0.0.6
python-dotenv==1.0.0
loguru==0.7.3
docker>=6.1.3
google-generativeai>=0.8.5
transformers>=4.56.1
torch>=2.8.0
ollama>=0.5.3
httpx>=0.25.2
openai
EOF

# Rebuild OpenManus with fixed dependencies
cd ~/luna-instagram-ai
docker compose build openmanus
docker compose up -d
# Monitor startup logs
docker logs openmanus --tail 30
# Test semantic intelligence
curl http://localhost:8000/
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "I want to grow my fitness Instagram from 500 to 5000 followers in 60 days"}'
# Verify Ollama model is ready
docker exec -it ollama ollama list
# Check current environment configuration
cat .env
# Check OpenManus logs for connection details
docker logs openmanus --tail 50
# Add Ollama connection to environment
echo "OLLAMA_HOST=http://ollama:11434" >> .env
echo "OLLAMA_MODEL=mxbai-embed-large" >> .env
# Restart OpenManus with new configuration
docker restart openmanus
# Test semantic intelligence
curl http://localhost:8000/
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "I want to grow my fitness Instagram from 500 to 5000 followers in 60 days"}'
# Check OpenManus startup logs for specific errors
docker logs openmanus --tail 50
# Verify environment variables inside OpenManus
docker exec -it openmanus env
# Test network connectivity to Ollama
docker exec -it openmanus ping -c 4 ollama
docker exec -it openmanus curl -s http://ollama:11434/
# Fix dependency conflicts in requirements.txt
cat > ./integration/openmanus_service/requirements.txt << 'EOF'
fastapi>=0.100.0
uvicorn[standard]>=0.30.0
pydantic>=2.7.0
requests>=2.31.0
python-multipart>=0.0.7
python-dotenv>=1.0.0
ollama>=0.5.3
httpx>=0.25.2
EOF

clear
cat > ./integration/openmanus_service/requirements.txt << 'EOF'
fastapi>=0.100.0
uvicorn[standard]>=0.30.0
pydantic>=2.0.0
requests>=2.31.0
python-multipart>=0.0.7
python-dotenv>=1.0.0
ollama>=0.5.0
httpx>=0.25.0
openai
EOF

# Rebuild with fixed dependencies
cd ~/luna-instagram-ai
docker compose build openmanus --no-cache
docker compose up -d
# Test semantic intelligence
curl http://localhost:8000/
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "I want to grow my fitness Instagram from 500 to 5000 followers in 60 days"}'
# Check OpenManus startup logs
docker logs openmanus --tail 50
# Verify container status
docker ps
# Check application startup
curl -v http://localhost:8000/
# If needed, restart OpenManus
docker restart openmanus
# Check Ollama environment variables in OpenManus
docker exec -it openmanus env | grep OLLAMA
# Verify Ollama API accessibility
curl http://localhost:11434/
# Check if app.py references Ollama properly
cat ./integration/openmanus_service/app.py | grep -i ollama
# Verify Ollama API accessibility
curl http://localhost:11434/
# Check OpenManus app.py for Ollama integration code
head -40 ./integration/openmanus_service/app.py
# Check OpenManus logs for semantic initialization
docker logs openmanus --tail 50
# Test network connectivity from OpenManus to Ollama
docker exec -it openmanus curl -s http://ollama:11434/
clear
# Check extended logs for semantic engine initialization
docker logs openmanus --tail 100
# Review LLM initialization code
head -40 ./integration/openmanus_service/openmanus/app/llm.py
# Test semantic endpoint directly
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "I want to grow my fitness Instagram from 500 to 5000 followers in 60 days"}'
# Create the missing LLM class for semantic intelligence
mkdir -p ./integration/openmanus_service/openmanus/app
cat > ./integration/openmanus_service/openmanus/app/llm.py << 'EOF'
import os
import requests
from typing import Dict, List, Optional

class LLM:
    def __init__(self):
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        self.embed_model = os.getenv("OLLAMA_EMBED_MODEL", "mxbai-embed-large")
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        try:
            response = requests.get(f"{self.ollama_host}", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def is_available(self) -> bool:
        return self.available
    
    def understand_text(self, text: str) -> Dict:
        """Process Instagram growth goals with semantic understanding"""
        try:
            # Basic semantic analysis
            result = {
                "understood": True,
                "text": text,
                "analysis": self._analyze_instagram_goal(text)
            }
            return result
        except Exception as e:
            return {"understood": False, "error": str(e)}
    
    def _analyze_instagram_goal(self, text: str) -> Dict:
        """Analyze Instagram growth goals"""
        text_lower = text.lower()
        analysis = {
            "goal_type": "instagram_growth",
            "platform": "instagram"
        }
        
        # Extract follower numbers
        import re
        followers_match = re.search(r'(\d+)\s*(?:to\s*)?(\d+)\s*followers?', text_lower)
        if followers_match:
            analysis["current_followers"] = int(followers_match.group(1))
            analysis["target_followers"] = int(followers_match.group(2))
        
        # Extract timeframe
        time_match = re.search(r'(\d+)\s*(days?|weeks?|months?)', text_lower)
        if time_match:
            analysis["timeframe"] = f"{time_match.group(1)} {time_match.group(2)}"
        
        # Extract niche
        niches = ["fitness", "fashion", "food", "travel", "business", "lifestyle"]
        for niche in niches:
            if niche in text_lower:
                analysis["niche"] = niche
                break
                
        return analysis

# Create __init__.py files for proper module structure
EOF

# Create __init__.py files
mkdir -p ./integration/openmanus_service/openmanus
touch ./integration/openmanus_service/openmanus/__init__.py
touch ./integration/openmanus_service/openmanus/app/__init__.py
# Update app.py to handle semantic availability
cat > ./integration/openmanus_service/app.py << 'EOF'
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

app = FastAPI(
    title="OpenManus Service", 
    description="Luna AI semantic intelligence and strategy generation",
    version="0.1.0"
)

# CORS configuration
origins = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LLM
try:
    from openmanus.app.llm import LLM
    llm = LLM()
    semantic_available = llm.is_available()
except Exception as e:
    llm = None
    semantic_available = False

class SemanticRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {
        "service": "OpenManus Service",
        "version": "0.1.0",
        "semantic_available": semantic_available
    }

@app.post("/semantic/understand")
async def semantic_understand(request: SemanticRequest):
    """Luna's revolutionary semantic understanding of Instagram goals"""
    if not semantic_available or not llm:
        raise HTTPException(status_code=503, detail="Semantic engine not available")
    
    result = llm.understand_text(request.text)
    if not result.get("understood"):
        raise HTTPException(status_code=500, detail="Failed to process semantic request")
    
    return result

@app.post("/luna/process-goal")
async def process_goal(goal_data: dict):
    """Process Instagram growth goal and generate strategy"""
    return {
        "goal_processed": True,
        "strategy": {
            "posting_frequency": "daily",
            "content_types": ["carousel", "reel", "story"],
            "engagement_tactics": ["strategic_follows", "targeted_likes", "authentic_comments"],
            "hashtag_strategy": "niche_specific_trending"
        },
        "timeline": "60_days",
        "expected_growth": "400%"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

# Rebuild and restart OpenManus
docker compose build openmanus
docker compose up -d
# Test semantic intelligence
curl http://localhost:8000/
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "I want to grow my fitness Instagram from 500 to 5000 followers in 60 days"}'
# Stop current containers
docker compose down
# Create complete LLM class with proper Python syntax
cat > ./integration/openmanus_service/openmanus/app/llm.py << 'EOF'
import os
import requests
from typing import Dict, List, Optional
import re

class LLM:
    def __init__(self):
        self.ollama_host = os.getenv("OLLAMA_HOST", "http://ollama:11434")
        self.embed_model = os.getenv("OLLAMA_EMBED_MODEL", "mxbai-embed-large")
        self.available = self._check_availability()
    
    def _check_availability(self) -> bool:
        try:
            response = requests.get(f"{self.ollama_host}", timeout=5)
            return response.status_code == 200
        except:
            return False
    
    def is_available(self) -> bool:
        return self.available
    
    def understand_text(self, text: str) -> Dict:
        """Process Instagram growth goals with semantic understanding"""
        try:
            result = {
                "understood": True,
                "text": text,
                "analysis": self._analyze_instagram_goal(text)
            }
            return result
        except Exception as e:
            return {"understood": False, "error": str(e)}
    
    def _analyze_instagram_goal(self, text: str) -> Dict:
        """Analyze Instagram growth goals with semantic intelligence"""
        text_lower = text.lower()
        analysis = {
            "goal_type": "instagram_growth",
            "platform": "instagram",
            "intent": "follower_growth"
        }
        
        # Extract follower numbers
        followers_match = re.search(r'(\d+)\s*(?:to\s*)?(\d+)\s*followers?', text_lower)
        if followers_match:
            analysis["current_followers"] = int(followers_match.group(1))
            analysis["target_followers"] = int(followers_match.group(2))
            growth = int(followers_match.group(2)) - int(followers_match.group(1))
            analysis["growth_target"] = growth
            analysis["growth_percentage"] = f"{(growth / int(followers_match.group(1))) * 100:.0f}%"
        
        # Extract timeframe
        time_match = re.search(r'(\d+)\s*(days?|weeks?|months?)', text_lower)
        if time_match:
            analysis["timeframe"] = f"{time_match.group(1)} {time_match.group(2)}"
            analysis["timeframe_days"] = self._convert_to_days(time_match.group(1), time_match.group(2))
        
        # Extract niche/vertical
        niches = ["fitness", "fashion", "food", "travel", "business", "lifestyle", "beauty", "tech", "music"]
        for niche in niches:
            if niche in text_lower:
                analysis["niche"] = niche
                analysis["industry"] = niche
                break
                
        return analysis
    
    def _convert_to_days(self, number: str, unit: str) -> int:
        """Convert time units to days"""
        days = int(number)
        if "week" in unit:
            days *= 7
        elif "month" in unit:
            days *= 30
        return days
EOF

# Create __init__.py files for proper Python module structure
touch ./integration/openmanus_service/openmanus/__init__.py
touch ./integration/openmanus_service/openmanus/app/__init__.py
# Rebuild and restart Luna platform
docker compose build openmanus
docker compose up -d
# Wait for startup
sleep 10
# Test complete Luna platform
echo "Testing Luna's Revolutionary Semantic Intelligence..."
curl http://localhost:8000/
echo -e "\nTesting Luna's Instagram Growth Understanding..."
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "I want to grow my fitness Instagram from 500 to 5000 followers in 60 days"}'
echo -e "\nLuna Platform Status:"
docker ps
clear
cd ~/luna-instagram-ai/integration/openmanus_service
cat > logging_config.py << 'EOF'
import logging
import logging.config
import os
from typing import Any, Dict

def get_logging_config(level: str | None = None) -> Dict[str, Any]:
    log_level = (level or os.getenv("LOG_LEVEL") or "INFO").upper()
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "format": "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
            },
        },
        "handlers": {
            "default": {
                "level": log_level,
                "class": "logging.StreamHandler",
                "formatter": "default",
            },
        },
        "loggers": {
            "": {
                "handlers": ["default"],
                "level": log_level,
            },
            "luna": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "luna.middleware": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
            "luna.llm": {
                "handlers": ["default"],
                "level": log_level,
                "propagate": False,
            },
        },
    }

def setup_logging(level: str | None = None) -> None:
    cfg = get_logging_config(level)
    logging.config.dictConfig(cfg)
    logging.getLogger("luna").info("🌙 Luna logging configured with level=%s", level or os.getenv("LOG_LEVEL") or "INFO")
EOF

cat > logging_middleware.py << 'EOF'
import logging
import time
import uuid
from typing import Awaitable, Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp

logger = logging.getLogger("luna.middleware")
SLOW_THRESHOLD_SECONDS = 2.0

class RequestIdMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        req_id = str(uuid.uuid4())[:8]
        request.state.request_id = req_id
        response = await call_next(request)
        response.headers["X-Request-ID"] = req_id
        return response

class HttpLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
        start = time.perf_counter()
        method = request.method
        url = str(request.url)
        req_id = getattr(request.state, "request_id", "-")

        logger.info("🚀 Luna REQUEST START | id=%s | %s %s", req_id, method, url)

        try:
            response = await call_next(request)
        except Exception as e:
            duration = time.perf_counter() - start
            logger.exception("❌ Luna REQUEST ERROR | id=%s | %s %s | duration=%.3fs | error=%s",
                             req_id, method, url, duration, repr(e))
            raise

        duration = time.perf_counter() - start
        if duration > SLOW_THRESHOLD_SECONDS:
            logger.warning("🐌 Luna SLOW REQUEST | id=%s | %s %s | status=%s | duration=%.3fs",
                           req_id, method, url, response.status_code, duration)
        else:
            logger.info("✅ Luna REQUEST DONE | id=%s | %s %s | status=%s | duration=%.3fs",
                        req_id, method, url, response.status_code, duration)

        return response
EOF

# Backup your current app.py
cp app.py app.py.backup
# Edit app.py to add logging
nano app.py
# Edit your LLM file
nano openmanus/app/llm.py
# Go back to Luna root directory
cd ~/luna-instagram-ai
# Edit docker-compose.yml
nano docker-compose.yml
# Create new branch
git checkout -b add-backend-logging
# Add all files
git add integration/openmanus_service/logging_config.py         integration/openmanus_service/logging_middleware.py         integration/openmanus_service/app.py         integration/openmanus_service/openmanus/app/llm.py         docker-compose.yml
# Commit
git commit -m "feat: add detailed logging middleware for diagnostics"
# Push to GitHub
git push -u origin add-backend-logging
# Create new branch
git checkout -b add-backend-logging
# Add all files
git add integration/openmanus_service/logging_config.py         integration/openmanus_service/logging_middleware.py         integration/openmanus_service/app.py         integration/openmanus_service/openmanus/app/llm.py         docker-compose.yml
# Commit
git commit -m "feat: add detailed logging middleware for diagnostics"
# Push to GitHub
git push -u origin add-backend-logging
# Switch back to main branch  
git checkout main
# Pull the merged changes
git pull origin main
# Rebuild with logging enabled
docker compose build openmanus
docker compose up -d
# Watch your enhanced logs
docker logs openmanus -f
clear
# In one terminal, watch logs
docker logs openmanus -f
clear
# In one terminal, watch logs
docker logs openmanus -f
clear
# Check if Ollama is running
docker ps | grep ollama
# Check Ollama logs
docker logs ollama --tail 20
# Test Ollama directly
curl http://localhost:11434/api/tags
nano ~/luna-instagram-ai/integration/openmanus_service/app.py
# Rebuild with new endpoints
docker compose build openmanus
docker compose up -d
# Watch logs for testing
docker logs openmanus -f
# In a new terminal, test the endpoint
curl -X POST http://localhost:8000/targeting/suggest   -H "Content-Type: application/json"   -d '{"hashtags": ["fitness", "motivation"], "location": "us"}'
clear
# Check your OpenManus environment variables
docker exec openmanus env | grep OLLAMA
# 1. Test basic connectivity from OpenManus to Ollama
docker exec -it openmanus curl -v http://ollama:11434
# 2. Test the specific API endpoint that's failing
docker exec -it openmanus curl -X POST http://ollama:11434/api/generate   -H "Content-Type: application/json"   -d '{"model": "mxbai-embed-large", "prompt": "test", "stream": false}'
# 3. Check if both containers are on the same network
docker network ls
docker network inspect luna-instagram-ai_default
cleAR
clear
# Add Phi 3 Mini - lightweight and fast for chat
docker exec ollama ollama pull phi3:mini
# Verify it's installed
docker exec ollama ollama list
# Test Phi can handle chat requests (this should work)
docker exec openmanus curl -X POST http://ollama:11434/api/chat   -H "Content-Type: application/json"   -d '{
    "model": "phi3:mini",
    "messages": [{"role": "user", "content": "Hello! I am a mindset coach."}],
    "stream": false
  }'
clear
# Edit your Luna backend
nano ~/luna-instagram-ai/integration/openmanus_service/app.py
cat luna-instagram-ai/integration/openmanus_service/app.py | pbcopy
openmanus_service/app.py | pbcopy
cat openmanus_service/app.py
cat app.py
ls -R | grep app.py
grep openmanus_service/app.py
find . -name "app.py"
cat ./integration/openmanus_service/app.py
clear
# Go to the OpenManus service directory
cd ~/luna-instagram-ai/integration/openmanus_service
# Open the file with nano text editor
nano app.py
# Rebuild the container with your changes
docker compose build openmanus
# Restart the service
docker compose up -d
# Watch the logs to see it working
docker logs openmanus -f
clear
# Stream logs in real-time - perfect for monitoring
docker logs -f openmanus
clear
docker logs openmanus -f
clear
docker logs openmanus -f
clear
docker logs -f openmanus
clear
docker logs -f openmanus
clear
docker logs -f openmanus
clear
docker logs -f openmanus
cd ~/luna-instagram-ai
cp integration/openmanus_service/.env.example .env
nano .env
# Your updated app.py + environment variables = ready to deploy!
docker compose up -d --build
# Watch the enhanced logs
docker logs openmanus -f
clear
# Check service health
curl http://localhost:8000/
# Test semantic understanding
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "I want to grow my Instagram from 500 to 5000 followers"}'
# Test current information search
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "What are the latest Instagram algorithm changes in 2025?"}'
# Test targeting suggestions
curl -X POST http://localhost:8000/targeting/suggest   -H "Content-Type: application/json"   -d '{"hashtags": ["fitness", "motivation"], "location": "us"}'
clear
# Restart to load new environment variables
docker compose down
docker compose up -d --build
# Watch the enhanced startup logs
docker logs openmanus -f
# Check environment variables are loaded correctly
docker exec openmanus env | grep -E "SCRAPEDO|TAVILY|APIFY"
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "What are the latest Instagram algorithm changes in 2025?"}'
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Analyze the most effective Instagram growth strategies for fitness coaches in 2025"}'
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "How do I write engaging Instagram captions?"}'
clear
cd ~/luna-instagram-ai/integration/openmanus_service
head -20 app.py
# Check your current app.py length
wc -l app.py
# Backup current version
cp app.py app.py.backup
# Replace with enhanced version (I'll provide complete code)
nano app.py
echo "tavily-python" >> requirements.txt
# Rebuild with enhanced routing
docker compose build openmanus
docker compose up -d
# Watch enhanced logs
docker logs openmanus -f
clear
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "What are the latest Instagram algorithm changes in 2025?"}'
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Analyze the most effective Instagram growth strategies for fitness coaches in 2025"}'
clear
# Check what models are currently in Ollama
docker exec ollama ollama list
# Pull DeepSeek Coder model (best for research tasks)
docker exec ollama ollama pull deepseek-coder
# Verify it's installed
docker exec ollama ollama list
# Check current models in Ollama
docker exec ollama ollama list
# Pull DeepSeek Coder (best for research/analysis)
docker exec ollama ollama pull deepseek-coder
# Alternative: DeepSeek V3 (if available)
docker exec ollama ollama pull deepseek-v3
# Download the three most important models
docker exec ollama ollama pull qwen:7b && docker exec ollama ollama pull qwen2-vl:7b && docker exec ollama ollama pull qwen:14b
# Verify and restart
docker exec ollama ollama list
docker restart ollama
# Try removing the model directly (works for most cases)
docker exec ollama ollama rm deepseek-v3
# Verify it's gone
docker exec ollama ollama list
# Stop Ollama container
docker stop ollama
# Find Ollama data directory and remove partial model
sudo rm -rf /var/lib/docker/volumes/luna-instagram-ai_ollama_models/
# Or find the specific model directory
sudo find /var/lib/docker/volumes -name "*deepseek*" -type d
sudo rm -rf [path_to_deepseek_directory]
# Restart Ollama
docker start ollama
# Verify cleanup
docker exec ollama ollama list
# Check current disk usage
df -h
# Find largest directories consuming space
sudo du -h / --max-depth=1 | sort -hr | head -10
# Emergency Docker cleanup (will free significant space)
sudo docker system prune -a --volumes
# The key issue - recreate the deleted Ollama volume
docker volume create luna-instagram-ai_ollama_models
# Verify it exists
docker volume ls | grep ollama
# Navigate to your Luna directory
cd ~/luna-instagram-ai
# Bring down everything cleanly
docker compose down
# Start fresh with recreated volume
docker compose up -d
# Wait for services to initialize
sleep 30
# Check all containers are healthy
docker compose ps
# Test Luna backend
curl http://localhost:8000/
# Should return service info without errors
docker volume ls
# Create the missing Ollama volume
docker volume create luna-instagram-ai_ollama_models
# Verify it was created
docker volume ls | grep ollama
# Create the volume directory if it doesn't exist
sudo mkdir -p /var/lib/docker/volumes/luna-instagram-ai_ollama_models/_data
# Set correct ownership (ollama typically runs as user 1000)
sudo chown -R 1000:1000 /var/lib/docker/volumes/luna-instagram-ai_ollama_models/
# Edit your docker-compose.yml
nano ~/luna-instagram-ai/docker-compose.yml
# Remove the deprecated "version" line at the top:
# Delete this line: version: "3.9"
cd ~/luna-instagram-ai
# Bring everything down cleanly
docker compose down
# Start fresh with fixed volume
docker compose up -d
# Wait for services to initialize
sleep 30
# Check all containers are running
docker compose ps
# Test Luna backend (should work now)
curl http://localhost:8000/
# Should return Luna service information
# Add your primary text model
docker exec ollama ollama pull phi3:mini
# Add embeddings model
docker exec ollama ollama pull mxbai-embed-large
# Verify models are loaded
docker exec ollama ollama list
# 1. Core embedding model
docker exec ollama ollama pull mxbai-embed-large  # 669MB (if not already installed)
# 2. Lightweight Gemma for fast tasks
docker exec ollama ollama pull gemma:2b           # 1.4GB - Fast lightweight model
# 3. Small Qwen for balanced performance
docker exec ollama ollama pull qwen2:1.5b         # 934MB - Efficient text model
# Monitor disk space after each
df -h
# 4. Standard Qwen for better quality
docker exec ollama ollama pull qwen2:7b           # 4.4GB - Balanced performance
# 5. Llama for coding and complex tasks
docker exec ollama ollama pull llama3.2:3b        # 2.0GB - Code generation
# Check space and model list
df -h && docker exec ollama ollama list
# 6. Large Qwen for research
docker exec ollama ollama pull qwen2.5:14b        # 8.7GB - High-quality responses
# 7. Vision-Language model
docker exec ollama ollama pull qwen2-vl:7b        # 4.4GB - Image understanding
# 8. Premium Llama model
docker exec ollama ollama pull llama3.1:8b        # 4.7GB - Advanced reasoning
#!/bin/bash
echo "🚀 Installing Luna AI Models Suite..."
# Function to check disk space
check_space() {     AVAILABLE=$(df / | tail -1 | awk '{print $4}');     echo "Available space: ${AVAILABLE}KB";     if [ $AVAILABLE -lt 5000000 ]; then         echo "⚠️ Low disk space warning!";         read -p "Continue? (y/n): " continue_install;         if [ "$continue_install" != "y" ]; then             exit 1;         fi;     fi; }
# Phase 1: Essential Models
echo "📦 Phase 1: Installing essential models..."
check_space
echo "Installing Gemma 2B..."
docker exec ollama ollama pull gemma:2b
sleep 2
echo "Installing Qwen 1.5B..."
docker exec ollama ollama pull qwen2:1.5b
sleep 2
# Phase 2: Mid-Range Models
echo "📦 Phase 2: Installing mid-range models..."
check_space
echo "Installing Qwen 7B..."
docker exec ollama ollama pull qwen2:7b
sleep 2
echo "Installing Llama 3.2 3B..."
docker exec ollama ollama pull llama3.2:3b
sleep 2
# Phase 3: High-Performance (Optional)
read -p "Install high-performance models? (y/n): " install_premium
if [ "$install_premium" = "y" ]; then     echo "📦 Phase 3: Installing high-performance models...";     check_space;          echo "Installing Qwen Vision...";     docker exec ollama ollama pull qwen2-vl:7b;     sleep 2;          echo "Installing Llama 3.1 8B...";     docker exec ollama ollama pull llama3.1:8b; fi
# Verify installation
echo "✅ Installation complete! Installed models:"
docker exec ollama ollama list
# Check final disk usage
echo "💾 Final disk usage:"
df -h | head -1
df -h | grep -E "/$"
echo "🎉 Luna model suite installation complete!"
# Restart Ollama to recognize all new models
docker restart ollama
# Wait for initialization
sleep 20
# Verify all models loaded successfully
docker exec ollama ollama list
# Check all containers healthy
docker compose ps
# Test enhanced Luna backend
curl http://localhost:8000/
# Should show enhanced capabilities with all search providers
clear
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Quick Instagram tip for engagement?"}'
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Quick Instagram tip for engagement?"}'
clear
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Quick Instagram tip for engagement?"}'
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Comprehensive analysis of Instagram algorithm changes and fitness influencer growth strategies for 2025"}'
clear
docker exec ollama ollama list
nano ~/luna-instagram-ai/integration/openmanus_service/app.py
cd ~/luna-instagram-ai
docker compose build openmanus
docker compose up -d
# Test lightning-fast chat (Gemma 2B)
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Quick Instagram tip?"}'
# Test deep research (Qwen 14B + Web Search)
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Comprehensive Instagram algorithm analysis for 2025"}'
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Quick Instagram tip?"}'
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Comprehensive Instagram algorithm analysis for 2025"}'
clear
cp ~/luna-instagram-ai/integration/openmanus_service/app.py ~/luna-instagram-ai/integration/openmanus_service/app.py.backup
nano ~/luna-instagram-ai/integration/openmanus_service/app.py
cd ~/luna-instagram-ai
docker compose build openmanus && docker compose up -d
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Comprehensive Instagram algorithm analysis for 2025"}'
clear
nano ~/luna-instagram-ai/integration/openmanus_service/app.py
cd ~/luna-instagram-ai && docker compose build openmanus && docker compose up -d
curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "Comprehensive Instagram algorithm analysis for 2025"}'
clear
# Navigate to your Luna directory
cd ~/luna-instagram-ai/integration/openmanus_service
# Install BeautifulSoup for HTML parsing
pip install beautifulsoup4 lxml
# Or add to requirements.txt if you have one
echo "beautifulsoup4" >> requirements.txt
echo "lxml" >> requirements.txt
apt install python3-pip
# Install BeautifulSoup for HTML parsing
pip install beautifulsoup4 lxml
# Or add to requirements.txt if you have one
echo "beautifulsoup4" >> requirements.txt
echo "lxml" >> requirements.txt
clear
pip install requests urllib3
# Navigate to your Luna project
cd ~/luna-instagram-ai/integration/openmanus_service
# Create virtual environment
python3 -m venv venv
# Activate it
source venv/bin/activate
# Install your scraping dependencies
pip install requests urllib3 beautifulsoup4 lxml
# Update requirements for Docker
echo "requests" >> requirements.txt
echo "urllib3" >> requirements.txt
echo "beautifulsoup4" >> requirements.txt
echo "lxml" >> requirements.txt
# Test Scrape.do integration
python your_scraping_script.py
clear
# Install python3-venv and python3-full
sudo apt update
sudo apt install python3-venv python3-full -y
# Navigate to your Luna project
cd ~/luna-instagram-ai/integration/openmanus_service
# Create virtual environment (should work now)
python3 -m venv venv
# Activate it
source venv/bin/activate
# Your prompt should change to show (venv)
# Now install your packages in the virtual environment
pip install requests urllib3 beautifulsoup4 lxml
# Update requirements.txt
echo "requests" >> requirements.txt
echo "urllib3" >> requirements.txt  
echo "beautifulsoup4" >> requirements.txt
echo "lxml" >> requirements.txt
# Check that packages are installed
pip list
# Test imports
clear
nano ~/luna-instagram-ai/integration/openmanus_service/app.py
clear
docker logs openmanus -f
clear
cd ~/luna-instagram-ai
# Build with the corrected Scrape.do integration
docker compose build openmanus
# Deploy the updated service
docker compose up -d
# Wait for services to start
curl -X POST http://localhost:8000/semantic/understand \
  -H "Content-Type: application/json" \
  -d '{"text": "Instagram algorithm analysis for 2025"}'

curl -X POST http://localhost:8000/semantic/understand   -H "Content-Type: application/json"   -d '{"text": "what are the new features and updates by instagram in 2025 to gain followers"}'
clear
cd ~/luna-instagram-ai
# Stop all running containers
docker compose down
# Verify all containers are stopped
docker ps
# Remove Ollama container completely
docker container rm ollama
# Remove Ollama data volume (frees up ~25GB)
docker volume rm luna-instagram-ai_ollama_data
# Optional: Remove Ollama image to free even more space
docker image rm ollama/ollama:latest
# Check freed space
df -h
# Edit your docker-compose file
nano ~/luna-instagram-ai/docker-compose.yml
# Edit environment file
nano ~/luna-instagram-ai/.env
# Remove or comment out these lines:
# OLLAMA_HOST=http://ollama:11434
# OLLAMA_MODEL=phi3:mini
# Edit the main app file
nano ~/luna-instagram-ai/integration/openmanus_service/app.py
clear
cd ~/luna-instagram-ai
nano .env
cd ~/luna-instagram-ai
# Stop current services
docker compose down
# Rebuild with new environment variables
docker compose build openmanus
# Start with updated configuration
docker compose up -d
# Verify services are running
docker compose ps
cd ~/luna-instagram-ai
nano docker-compose.yml
nano .env
# Stop old services
docker compose down --remove-orphans
# Build with new configuration
docker compose build --no-cache
# Start Luna v2.0
docker compose up -d
# Check status
docker compose ps
# Add to your requirements.txt or install directly
pip install redis aioredis cachetools httpx
clear
# Check if virtual environment is active (should show (venv) in prompt)
source venv/bin/activate
# Test package imports
clear
# Navigate to your Luna project directory
cd /path/to/your/luna/project
# Create virtual environment
python3 -m venv venv
# Activate virtual environment
source venv/bin/activate
# Verify activation (you should see (venv) in your prompt)
which python
# Upgrade pip
pip install --upgrade pip
# Install required packages
pip install redis aioredis cachetools httpx fastapi uvicorn
clear
# Check if virtual environment is active (should show (venv) in prompt)
source venv/bin/activate
# Test package imports
python3 -c 'import redis, aioredis, cachetools, httpx; print("✅ All packages installed successfully")'
clear
# Make sure you're in your virtual environment (you should see (venv) in prompt)
source venv/bin/activate
# Install setuptools which provides distutils for Python 3.12+
pip install setuptools
# Also install wheel for better package compatibility
pip install wheel
# Verify the fix works
python3 -c "import setuptools; print('✅ Setuptools installed successfully')"
python3 -c 'import redis, aioredis, cachetools, httpx; print("✅ Ready for enhanced caching!")'
# Make sure you're in your virtual environment
source venv/bin/activate
# Uninstall the problematic aioredis
pip uninstall aioredis
# Install the modern redis package with async support
pip install redis
# Install other remaining packages
pip install cachetools httpx
# Test 1: Basic package imports
python3 -c "import redis, cachetools, httpx; print('Packages loaded')"
# Test 2: Modern redis with asyncio
python3 -c "import redis.asyncio as redis; print('Redis asyncio works')"
# Test 3: All packages together (without emoji)
python3 -c "import redis.asyncio as redis, cachetools, httpx; print('All packages ready for caching')"
clear
# Navigate to your Luna project directory
cd /path/to/your/luna/project
# Create the```che manager file
nano cache_manager.py
nano ai_client.py
nano test_cache.py
ç
python test_cache.py
python3 test_cache.py
# Make sure you're in your virtual environment
source venv/bin/activate
# Install the missing cachetools package
pip install cachetools
# Verify the installation works
python -c "import cachetools; print('✅ cachetools installed successfully')"
chmod +x install_cachetools.sh
bash install_cachetools.sh
# Make sure you're in your virtual environment
source venv/bin/activate
# Install missing packages
pip install cachetools
# Verify installation
python -c "import cachetools; print('✅ cachetools installed successfully')"
# Make sure you're in your virtual environment
source venv/bin/activate
# Run the test
python3 test_cache.py
# Update packages
sudo apt update
# Install Redis server
sudo apt install redis-server -y
# Start Redis service
sudo systemctl start redis
# Enable Redis to start on boot
sudo systemctl enable redis
# Check Redis status
sudo systemctl status redis
clear
# Check detailed error logs
sudo journalctl -xeu redis-server.service
# Check Redis configuration
sudo redis-server /etc/redis/redis.conf --test-config
# Check if port 6379 is being used
sudo lsof -i :6379
# Check specific Redis log file
sudo tail -n 50 /var/log/redis/redis-server.log
# If that file doesn't exist or is empty, check systemd logs more specifically
sudo journalctl -u redis-server.service --no-pager | tail -20
# Test Redis configuration for syntax errors
sudo redis-server /etc/redis/redis.conf --test-config
# Check if port 6379 is free (should show no output if free)
sudo lsof -i :6379
nano cache_manager_working.py
python3 test_cache.py
clear
# Make sure you're in your virtual environment
source venv/bin/activate
# Install FastAPI and Uvicorn (the web server)
pip install fastapi uvicorn
nano main.py
# Make sure you're in your virtual environment
source venv/bin/activate
# Run your Luna AI with enhanced caching
uvicorn main:app --reload --host 0.0.0.0 --port 8000
clear
curl http://localhost:8000/health
curl http://localhost:8000/
ps aux | grep uvicorn
sudo netstat -tulnp | grep :8000
# Try 127.0.0.1 instead of localhost
curl http://127.0.0.1:8000/health
# Try the exact binding address
curl http://0.0.0.0:8000/health
# Kill the old uvicorn process
sudo kill 69378
# Verify it's gone
ps aux | grep uvicorn
# Make sure you're in the right directory with your main.py
ls -la main.py
# Start your Luna AI on port 8000
uvicorn main:app --reload --host 0.0.0.0 --port 8000
clear
# In a new terminal, test your Luna AI
curl http://127.0.0.1:8000/health
# 1. Health check
curl http://127.0.0.1:8000/health
# 2. Welcome message
curl http://127.0.0.1:8000/
# 3. Cache stats (should show empty stats initially)
curl http://127.0.0.1:8000/cache/stats
# 4. Test chat endpoint (may fail without OpenRouter credits - that's expected)
curl -X POST "http://127.0.0.1:8000/chat"      -H "Content-Type: application/json"      -d '{"text": "Hello", "user_id": "test"}'
clear
# Make sure you're in your virtual environment
source venv/bin/activate
# Install PyTorch and Transformers (for SML classification)
pip install torch torchvision transformers sentence-transformers
# Install additional utilities
pip install scikit-learn numpy
nano sml_classifier.py
nano ai_client.py
nano main.py
pip install torch transformers sentence-transformers
uvicorn main:app --reload --host 0.0.0.0 --port 8000
curl http://localhost:8000/health
