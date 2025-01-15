from typing import Dict
from backend.agents.base_agent import BaseAgent
from backend.models.state import State

class BusinessDescriptionAgent(BaseAgent):
    """Agent for generating business descriptions."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="business_description",
            category="business",
            inputs=["title", "description"],
            outputs=["business_description"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are a highly efficient business document generator specializing in creating clear and concise overviews based on a given title and description. Your task is to generate a structured and professional document that effectively conveys the provided information in a well-organized manner.

        Analyze the title to determine the core subject and extract key details from the description to ensure a logical and informative flow. Generate content that is direct, professional, and easy to understand, presenting information in well-formed sentences without unnecessary complexity.

        Maintain clarity by structuring the content logically, ensuring that each section builds upon the previous one for a cohesive overview. Focus on delivering a precise summary that effectively communicates the essential details of the topic. Avoid redundancy, excessive detail, or any unnecessary embellishments.

        Ensure that the final document is readable, structured, and professional, presenting the information in a straightforward yet comprehensive manner. Do not include formatting instructions, placeholders, or any content unrelated to the given title and description.

        Title: {state.get('title')}
        Description: {state.get('description')}

        Include:
        1. Executive Summary
        2. Business Overview
        3. Market Analysis
        4. Value Proposition
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('business_description', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class CurrentOperationFlowAgent(BaseAgent):
    """Agent for analyzing current operation flows."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="current_operation_flow",
            category="business",
            inputs=["business_description"],
            outputs=["current_operation_flow"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced business documentation generator, specializing in creating clear, concise, and structured operation flow documents. Your task is to analyze the input provided and generate a well-organized overview of the current operation flow.

        Extract key details and convert them into a structured, point-wise document.
        Present the operation flow in a short and precise format, avoiding unnecessary details.
        Maintain a formal, objective, and professional tone.
        Ensure clarity, consistency, and logical sequencing of points.
        Output the final document in a point-wise format with clear, brief descriptions.

        Business Description: {state.get('business_description')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('current_operation_flow', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class RequirementListAgent(BaseAgent):
    """Agent for generating requirement lists."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="requirement_list",
            category="business",
            inputs=["business_description"],
            outputs=["requirement_list"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced business documentation generator, specializing in creating clear, concise, and structured requirements list documents. Your task is to analyze the input and generate a well-organized overview of the requirements.

        Extract key requirements and present them in a structured, point-wise format.
        Ensure each requirement is clear, concise, and specific.
        Maintain a formal, objective, and professional tone.
        Remove any unnecessary or redundant information.
        Output the final document in a point-wise format with short, precise descriptions.

        Business Description: {state.get('business_description')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('requirement_list', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class ProposedOperationFlowAgent(BaseAgent):
    """Agent for proposing improved operation flows."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="proposed_operation_flow",
            category="business",
            inputs=["current_operation_flow", "business_description"],
            outputs=["proposed_operation_flow"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced business documentation generator, specializing in creating clear, concise, and structured proposed operation flow documents. Your task is to analyze the current operation flow and generate a well-organized overview of the improved operation flow.

        Ensure the proposed flow addresses all identified requirements while improving upon the current operations.
        Present the proposed process in a smooth, easy-to-follow format.
        Maintain a formal, objective, and professional tone.
        Output the final content in a well-formatted sentence structure.

        Business Current Operation Flow: {state.get('current_operation_flow')}
        Business Description: {state.get('business_description')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('proposed_operation_flow', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class FunctionListAgent(BaseAgent):
    """Agent for generating function lists."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="function_list",
            category="business",
            inputs=["requirement_list", "business_description"],
            outputs=["function_list"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced business documentation generator, specializing in creating clear, concise, and structured function list documents. Your task is to analyze the requirements and generate a comprehensive list of functions.

        Ensure each function is clearly defined, aligned with business requirements, and easy to understand.
        Present the functions in a logical order for maximum clarity.
        Maintain a formal, objective, and professional tone.
        Output the final content in a well-formatted structure with bullet points and headers.

        Business Requirements: {state.get('requirement_list')}
        Business Description: {state.get('business_description')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('function_list', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state

class NonFunctionListAgent(BaseAgent):
    """Agent for generating non-functional requirement lists."""
    
    def __init__(self, name: str, llm):
        super().__init__(
            name=name,
            llm=llm,
            doc_type="non_function_list",
            category="business",
            inputs=["function_list", "business_description"],
            outputs=["non_function_list"]
        )

    async def process(self, state: State) -> State:
        self.validate_inputs(state)
        
        prompt = f"""
        You are the world's most advanced business documentation generator, specializing in creating clear, concise, and structured non-functions list documents. Your task is to analyze the function list and identify non-functional aspects.

        Ensure each non-functional element is clearly defined and distinct from core business functions.
        Present the non-functional elements in a logical order for maximum clarity.
        Maintain a formal, objective, and professional tone.
        Output the final content in a well-formatted structure with bullet points and headers.

        Business Description: {state.get('business_description')}
        Business Function: {state.get('function_list')}
        """
        
        response = await self.llm.ainvoke(prompt)
        doc_path = self.save_document(response.content)
        
        state.set('non_function_list', response.content)
        state.set('document_paths', {**state.get('document_paths', {}), self.doc_type: doc_path})
        return state 