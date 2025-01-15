from pathlib import Path
from datetime import datetime
from backend.config.settings import get_settings

settings = get_settings()

class DocumentManager:
    """Manages document storage and retrieval."""
    
    @staticmethod
    def initialize_directories():
        """Create necessary directories if they don't exist."""
        docs_dir = settings.DOCS_DIR
        business_dir = docs_dir / "business"
        technical_dir = docs_dir / "technical"
        
        # Create directories
        for directory in [docs_dir, business_dir, technical_dir]:
            directory.mkdir(parents=True, exist_ok=True)
    
    @staticmethod
    def save_document(content: str, doc_type: str, category: str) -> str:
        """Save a document and return its path.
        
        Args:
            content: Document content
            doc_type: Type of document
            category: Document category (business/technical)
            
        Returns:
            Path to saved document
        """
        # Create timestamp for unique filenames
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create filename
        filename = f"{doc_type}_{timestamp}.md"
        
        # Get category directory
        category_dir = settings.DOCS_DIR / category
        
        # Ensure directory exists
        category_dir.mkdir(parents=True, exist_ok=True)
        
        # Full file path
        file_path = category_dir / filename
        
        # Save content
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return str(file_path.relative_to(settings.BASE_DIR)) 