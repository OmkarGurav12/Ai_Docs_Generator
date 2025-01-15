from typing import Dict, Any, Optional
from pydantic import BaseModel

class State(BaseModel):
    """Represents the workflow state."""
    
    title: str
    description: str
    document_paths: Dict[str, str] = {}
    business_description: Optional[str] = None
    current_operation_flow: Optional[str] = None
    requirement_list: Optional[str] = None
    proposed_operation_flow: Optional[str] = None
    function_list: Optional[str] = None
    non_function_list: Optional[str] = None
    system_abstraction: Optional[str] = None
    table_definition: Optional[str] = None
    er_diagram: Optional[str] = None
    screen_translation: Optional[str] = None
    screen_list: Optional[str] = None
    screen_ui: Optional[str] = None
    common_components: Optional[str] = None
    backend_handles_list: Optional[str] = None
    sequence_diagrams: Optional[str] = None
    system_architecture: Optional[str] = None
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a value from the state.
        
        Args:
            key: Key to get
            default: Default value if key not found
            
        Returns:
            Value from state or default
        """
        return getattr(self, key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a value in the state.
        
        Args:
            key: Key to set
            value: Value to set
        """
        setattr(self, key, value) 