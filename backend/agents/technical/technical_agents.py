from typing import Dict
from backend.agents.base_agent import BaseAgent
from backend.models.state import State

class SystemAbstractionAgent(BaseAgent):
    """Agent for generating system abstractions."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="system_abstraction",
            category="technical",
            inputs=["business_description", "function_list"],
            outputs=["system_abstraction"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced technical documentation generator, specializing in creating clear, concise, and structured system abstraction documents. Your task is to analyze the business description and function list to generate a single, well-organized system abstraction description.

        Present the system abstraction in a clear, logical, and cohesive format.
        Ensure the document provides a high-level overview without unnecessary technical details.
        Maintain a formal, objective, and professional tone.
        Output the final content as a single, well-structured description with headers.

        Business Description: {state.get('business_description')}
        Function List: {state.get('function_list')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('system_abstraction', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class TableDefinitionAgent(BaseAgent):
    """Agent for generating database table definitions."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="table_definition",
            category="technical",
            inputs=["requirement_list", "function_list"],
            outputs=["table_definition"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced technical documentation generator, specializing in creating clear, concise, and structured database table definitions. Your task is to analyze the requirements and functions to define a comprehensive database schema.

        Create a database schema in a proper table-model format, following standard conventions:
        - Include primary and foreign keys
        - Specify data types
        - Define relationships between tables
        - Add necessary timestamps and audit fields

        Function List: {state.get('function_list')}
        Requirements: {state.get('requirement_list')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('table_definition', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class ERDiagramAgent(BaseAgent):
    """Agent for generating ER diagram descriptions."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="er_diagram",
            category="technical",
            inputs=["table_definition"],
            outputs=["er_diagram"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced technical documentation generator, specializing in creating clear, concise, and structured entity-relationship (ER) diagram descriptions. Your task is to analyze the table definitions and generate a textual representation of the ER diagram.

        Describe entities, attributes, relationships, and cardinality.
        Present a logical and well-organized explanation of the database schema.
        Maintain readability by eliminating redundancy and using precise terminology.

        Table Definition: {state.get('table_definition')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('er_diagram', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class ScreenTranslationAgent(BaseAgent):
    """Agent for generating screen navigation flowcharts."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="screen_translation",
            category="technical",
            inputs=["proposed_operation_flow", "function_list"],
            outputs=["screen_translation"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced technical documentation generator, specializing in creating clear, concise, and visually appealing screen navigation flowcharts. Your task is to analyze the proposed operation flow and functions to generate a well-structured flowchart representing user navigation between screens.

        Represent screen navigation using a flow-like visual structure with arrows.
        Ensure the flowchart clearly depicts user entry points and screen transitions.
        Use a visually appealing format, avoiding excessive text.
        Maintain a formal, objective, and professional presentation.

        Proposed Operation Flow: {state.get('proposed_operation_flow')}
        Function List: {state.get('function_list')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('screen_translation', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class ScreenListAgent(BaseAgent):
    """Agent for generating screen functionality documents."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="screen_list",
            category="technical",
            inputs=["screen_translation"],
            outputs=["screen_list"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced business documentation generator, specializing in creating clear, concise, and well-structured screen functionality documents. Your task is to analyze the screen translation and generate a clean, point-wise overview of screens and their functionalities.

        Present each screen and its functionality in a short, precise, and point-wise format.
        Ensure clarity, minimalism, and professionalism.
        Keep the document clutter-free and easy to read.

        Screen Translation: {state.get('screen_translation')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('screen_list', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class ScreenUIAgent(BaseAgent):
    """Agent for generating UI element documentation."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="screen_ui",
            category="technical",
            inputs=["screen_list"],
            outputs=["screen_ui"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced technical documentation generator, specializing in creating clear, concise, and structured technical documentation for screen UI elements. Your task is to analyze the screen list and generate a well-organized document detailing the key components of screen UI.

        Present each UI element clearly, including its purpose, structure, and best practices.
        Include essential details such as component name, description, and usage guidelines.
        Format the document in a point-wise, clean, and minimalistic style.
        Maintain a formal, objective, and professional tone.

        Screen List: {state.get('screen_list')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('screen_ui', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class CommonComponentsAgent(BaseAgent):
    """Agent for identifying common UI components."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="common_components",
            category="technical",
            inputs=["screen_ui"],
            outputs=["common_components"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the "Common Component Agent," an expert in analyzing user interfaces and backend systems to document reusable components in a short, concise, and actionable format. Your output will be used to streamline design and development efforts.

        Identify distinct UI elements and backend functionalities.
        Group elements and features into generic, reusable categories.
        Document components in pointwise format.
        Use plain language and avoid jargon.

        Screen UI: {state.get('screen_ui')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('common_components', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class BackendHandleListAgent(BaseAgent):
    """Agent for documenting backend API endpoints."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="backend_handles_list",
            category="technical",
            inputs=["common_components"],
            outputs=["backend_handles_list"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the "Backend Handle List Agent," an expert in documenting backend API endpoints utilized in applications. Your task is to analyze the common components and output a comprehensive list of API endpoints.

        Include the endpoint name, functionality, and intended use case.
        Keep descriptions short and specific.
        Ensure each API description is directly related to functional requirements.
        Present each endpoint on a new line with clear documentation.

        Common Components: {state.get('common_components')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('backend_handles_list', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class SequenceDiagramAgent(BaseAgent):
    """Agent for generating sequence diagram descriptions."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="sequence_diagrams",
            category="technical",
            inputs=["backend_handles_list"],
            outputs=["sequence_diagrams"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the "Sequence Diagram Agent," an expert in visualizing system interactions through sequence diagrams. Your task is to analyze the backend handles and output a clear representation of interactions between components.

        List each step as a message or action in the interaction process.
        Include the sender, receiver, and message content.
        Ensure messages are listed in chronological order.
        Present each interaction step on a new line.

        Backend Handle List: {state.get('backend_handles_list')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('sequence_diagrams', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class SystemArchitectureAgent(BaseAgent):
    """Agent for generating system architecture documentation."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="system_architecture",
            category="technical",
            inputs=["sequence_diagrams", "system_abstraction"],
            outputs=["system_architecture"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the "System Architecture Agent," an expert in visualizing and documenting high-level system architecture diagrams. Your task is to analyze the sequence diagrams and system abstraction to generate a detailed description of the major components.

        Describe each component, its role, and connections to other components.
        Group components by categories (hardware, software, network).
        Ensure all critical elements of the system are represented.
        Present each component and interaction clearly and professionally.

        System Abstraction: {state.get('system_abstraction')}
        Sequence Diagrams: {state.get('sequence_diagrams')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('system_architecture', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state 