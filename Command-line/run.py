import re
import os
import json
from langchain_ollama import ChatOllama
from typing import List

from dotenv import load_dotenv
load_dotenv()
ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
# PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')

provider = "qwen"
version = "2.5"
num_parameters = "7b"
model_name = f"{provider}{version}:{num_parameters}"
llm = ChatOllama(model=model_name)

required_values = [
    "num_agents",
    "num_tools",
    "agent_list",
    "prompt_list",
    "tool_list",
    "tool_description_list",
    "agent_graph"
]

class Tool:
    def __init__(self,tool_name,tool_description):
        self.tool_name = tool_name
        self.tool_description = tool_description
        self._generate_code()
    def extract_code(self,s):
        s1 = re.search("```python",s)
        if s1 is None:
            return ""
        a = s1.end()
        s2 = re.search("```",s[a:])
        if s2 is None:
            return ""
        b = s2.start()
        return s[a:a+b]
    def _generate_code(self):
        query = f"""Given the following function name and description, generate code
        function name: {self.tool_name}
        function description: {self.tool_description}
        
        Output format:
        ```python
        def {self.tool_name}(list of arguments):
            function definition
        ```
        Do not create any driver functions
        """
        response = llm.invoke(query)
        self.code = self.extract_code(response.content)
    def print_tool(self):
        self.tool_name

class Agent:
    def __init__(self,agent_name:str, agent_prompt:str, tools:List[Tool] = []):
        self.agent_name = agent_name
        self.agent_prompt = agent_prompt
        self.tools = tools

num_tools = int(input("Number of tools: "))
num_agents = int(input("Number of agents: "))

TOOLS = {}
for i in range(num_tools):
    tool_name = input("Tool Name: ")
    tool_desc = input("Tool Description: ")
    tool = Tool(tool_name=tool_name,tool_description=tool_desc)
    TOOLS[tool_name] = tool

AGENTS = []
for i in range(num_agents):
    agent_name = input("Agent Name: ")
    agent_prompt = input("Agent Prompt: ")
    agent_tools = []
    for tool in TOOLS:
        is_tool = input(f"{TOOLS[tool].code}\n\nIs {TOOLS[tool].tool_name} part of the tool list for this agent (Y/N)")
        if is_tool.lower() in ["y","yes"]:
            agent_tools += [TOOLS[tool]]
    agent = Agent(agent_name=agent_name, agent_prompt=agent_prompt, tools=agent_tools)
    AGENTS += [agent]

class Graph:
    def __init__(self, agents):
        self.agents = agents  # List of Agent objects
        self.edges = []       # List of tuples containing pairs of Agent objects
        self._build_graph()
        
    def _build_graph(self):
        print("\nDetermining edges between agents...")
        # Generate all possible pairs of agents
        for i in range(len(self.agents)):
            for j in range(i+1, len(self.agents)):
                agent1 = self.agents[i]
                agent2 = self.agents[j]
                
                # Ask if there's an edge between this pair
                response = input(f"Is there an edge between {agent1.agent_name} and {agent2.agent_name}? (y/n): ")
                if response.lower() == 'y':
                    self.edges.append((agent1, agent2))
    
    def get_edges(self):
        return self.edges
    
    def get_agents(self):
        return self.agents

# Create graph from agents
agent_graph = Graph(AGENTS)
print("\nGraph created with", len(agent_graph.get_edges()), "edges")