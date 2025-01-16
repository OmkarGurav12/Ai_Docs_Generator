from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from langchain_google_vertexai import VertexAI
import vertexai
from .config.settings import get_settings
from .models.workflow import WorkflowInput, WorkflowOutput
from .graphs.workflow_graph import DocumentationWorkflow
from .utils.document_manager import DocumentManager
import uvicorn

settings = get_settings()

# Initialize Vertex AI
vertexai.init(
    project=settings.GOOGLE_PROJECT_ID,
    location=settings.GOOGLE_LOCATION
)

# Initialize the LLM
llm = VertexAI(
    project=settings.GOOGLE_PROJECT_ID,
    location=settings.GOOGLE_LOCATION,
    temperature=0.7,
    model_name=settings.GEMINI_MODEL_NAME
)

# Initialize the workflow
workflow = DocumentationWorkflow(llm)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001"],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize necessary resources on startup."""
    DocumentManager.initialize_directories()

@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "Welcome to AI Documentation Generator API"}

@app.post(f"{settings.API_V1_STR}/generate", response_model=WorkflowOutput)
async def generate_documentation(input_data: WorkflowInput):
    """Generate documentation based on input data.
    
    Args:
        input_data: Project title and description
        
    Returns:
        Paths to generated documents
        
    Raises:
        HTTPException: If documentation generation fails
    """
    try:
        document_paths = await workflow.run(
            title=input_data.title,
            description=input_data.description
        )
        return WorkflowOutput(document_paths=document_paths)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate documentation: {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 
