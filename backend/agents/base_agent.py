from typing import Any, Dict, List, Optional
from langchain_core.messages import BaseMessage
from langchain_google_vertexai import VertexAI

from ..models.state import State
from ..config import settings
from ..utils.document_manager import DocumentManager

class BaseAgent:
    """Base agent class for LangGraph agents."""
    
    def __init__(
        self,
        name: str,
        llm: Optional[VertexAI] = None,
        doc_type: str = "",
        category: str = "",
        inputs: List[str] = None,
        outputs: List[str] = None,
        temperature: float = 0.7,
        model_name: str = "gemini-2.0-flash-exp",
    ):
        """Initialize the base agent.
        
        Args:
            name: Name of the agent
            llm: Language model to use
            doc_type: Type of document this agent produces
            category: Category of document (business/technical)
            inputs: Required input fields from state
            outputs: Fields this agent will produce
            temperature: Temperature for the model
            model_name: Name of the model to use
        """
        self.name = name
        self.llm = llm or VertexAI(
            project=settings.GOOGLE_PROJECT_ID,
            location=settings.GOOGLE_LOCATION,
            temperature=temperature,
            model_name=model_name
        )
        self.doc_type = doc_type
        self.category = category
        self.inputs = inputs or []
        self.outputs = outputs or []
        
    def validate_inputs(self, state: State) -> None:
        """Validate that all required inputs are present in the state.
        
        Args:
            state: Current workflow state
            
        Raises:
            ValueError: If any required inputs are missing
        """
        missing_inputs = [key for key in self.inputs if not state.get(key)]
        if missing_inputs:
            raise ValueError(
                f"Missing required inputs for {self.name}: {', '.join(missing_inputs)}"
            )
    
    def save_document(self, content: str) -> str:
        """Save a document using the document manager.
        
        Args:
            content: Content to save
            
        Returns:
            Path to the saved document
        """
        return DocumentManager.save_document(
            content=content,
            doc_type=self.doc_type,
            category=self.category
        )
    
    async def process(self, state: State) -> State:
        """Process the current state and return updated state.
        
        Args:
            state: Current workflow state
            
        Returns:
            Updated workflow state
            
        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError("Subclasses must implement process method") 
