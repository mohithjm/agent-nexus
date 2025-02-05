#!/bin/bash

# Define the base directory
BASE_DIR="."

# Define the directory structure
DIRS=(
    "$BASE_DIR/backend"
    "$BASE_DIR/backend/models"
    "$BASE_DIR/backend/services"
    "$BASE_DIR/backend/routers"
    "$BASE_DIR/backend/storage/projects/agents"
    "$BASE_DIR/frontend"
    "$BASE_DIR/frontend/src"
    "$BASE_DIR/frontend/src/components"
    "$BASE_DIR/frontend/src/services"
)

# Define the files to be created
FILES=(
    "$BASE_DIR/backend/main.py"
    "$BASE_DIR/backend/config.py"
    "$BASE_DIR/backend/models/__init__.py"
    "$BASE_DIR/backend/models/agent.py"
    "$BASE_DIR/backend/models/tool.py"
    "$BASE_DIR/backend/services/__init__.py"
    "$BASE_DIR/backend/services/agent_service.py"
    "$BASE_DIR/backend/services/ollama_service.py"
    "$BASE_DIR/backend/routers/__init__.py"
    "$BASE_DIR/backend/routers/agents.py"
    "$BASE_DIR/backend/routers/tools.py"
    "$BASE_DIR/frontend/src/components/AgentNode.tsx"
    "$BASE_DIR/frontend/src/components/AgentSidebar.tsx"
    "$BASE_DIR/frontend/src/components/AgentCreationApp.tsx"
    "$BASE_DIR/frontend/src/services/apiService.ts"
)

# Create directories
for dir in "${DIRS[@]}"; do
    mkdir -p "$dir"
done

# Create empty files
for file in "${FILES[@]}"; do
    touch "$file"
done

echo "Directory structure created successfully!"
