from langchain_core.language_models.base import BaseLanguageModel
from .base_graph import BaseGraph

class DocumentationWorkflow(BaseGraph):
    def __init__(self, llm: BaseLanguageModel):
        super().__init__(llm)
    
    async def run(self, title: str, description: str) -> list[str]:
        """Run the documentation workflow.
        
        Args:
            title: Project title
            description: Project description
            
        Returns:
            List of generated document paths
        """
        # For now, return an empty list as we haven't implemented the full workflow
        return []
    
    async def process(self, state: dict) -> dict:
        """Process the workflow with given state.
        
        Args:
            state: Initial state with title and description
            
        Returns:
            Final state with generated documents
        """
        documents = await self.run(
            title=state.get("title", ""),
            description=state.get("description", "")
        )
        return {"documents": documents} 