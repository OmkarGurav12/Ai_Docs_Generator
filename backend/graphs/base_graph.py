from typing import Dict, Any
from backend.agents.base_agent import BaseAgent
from langchain_core.language_models.base import BaseLanguageModel

class BaseGraph:
    """Base class for workflow graphs."""
    
    def __init__(self, llm: BaseLanguageModel):
        """Initialize the base graph."""
        self.llm = llm
        self.agents: Dict[str, BaseAgent] = {}
    
    def add_agent(self, agent: BaseAgent) -> None:
        """Add an agent to the graph.
        
        Args:
            agent: Agent to add
        """
        self.agents[agent.name] = agent
    
    async def process(self, state: Any) -> Any:
        """Process the workflow with given state.
        
        Args:
            state: Initial state
            
        Returns:
            Final state
        """
        # This will be implemented by child classes
        raise NotImplementedError 
