from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class StateManagementType(str, Enum):
    FULL_HISTORY = "full_history"
    LAST_INTERACTION = "last_interaction"
    CUSTOM = "custom"

class AgentConfiguration(BaseModel):
    id: str = Field(default_factory=lambda: f"agent_{datetime.now().timestamp()}")
    name: str
    llm: str
    system_prompt: str
    state_management: StateManagementType = StateManagementType.FULL_HISTORY
    api_key: Optional[str] = None
    position_x: float = 0
    position_y: float = 0
    connections: List[str] = []

    def save_to_file(self, project_path: str):
        """
        Save agent configuration to a JSON file
        
        Args:
            project_path (str): Base path for storing agent configurations
        """
        import os
        import json
        
        agent_dir = os.path.join(project_path, "agents", self.id)
        os.makedirs(agent_dir, exist_ok=True)
        
        config_path = os.path.join(agent_dir, "config.json")
        with open(config_path, 'w') as f:
            json.dump(self.model_dump(), f, indent=2)

    @classmethod
    def load_from_file(cls, file_path: str):
        """
        Load agent configuration from a JSON file
        
        Args:
            file_path (str): Path to the agent configuration file
        
        Returns:
            AgentConfiguration: Loaded agent configuration
        """
        import json
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return cls(**data)