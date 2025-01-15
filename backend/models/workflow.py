from typing import Dict
from pydantic import BaseModel

class WorkflowInput(BaseModel):
    """Input data for the workflow."""
    title: str
    description: str

class WorkflowOutput(BaseModel):
    """Output data from the workflow."""
    document_paths: Dict[str, str]

class WorkflowState(BaseModel):
    """Schema for the workflow state."""
    title: str
    description: str
    document_paths: Dict[str, str] = {} 