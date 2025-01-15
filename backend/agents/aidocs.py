from typing import Dict, TypedDict, List
from langchain_core.messages import HumanMessage
from langgraph.graph import Graph, END
import json
from typing import Annotated, Sequence
from langchain_core.messages import BaseMessage
from typing import Annotated
import operator,json
from typing import TypedDict, Annotated, Sequence
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph,END,START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from datetime import datetime
import os
from pydantic import BaseModel,Field
from typing import Dict, List


from langchain_google_genai import GoogleGenerativeAIEmbeddings
embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

class Config:
    OUTPUT_DIR = "project_docs"
    BUSINESS_DOCS_DIR = f"{OUTPUT_DIR}/business"
    TECHNICAL_DOCS_DIR = f"{OUTPUT_DIR}/technical"

# Create output directories
os.makedirs(Config.BUSINESS_DOCS_DIR, exist_ok=True)
os.makedirs(Config.TECHNICAL_DOCS_DIR, exist_ok=True)



# Define input and output types
class WorkflowInput(BaseModel):
    title: str
    description: str

class WorkflowOutput(BaseModel):
    document_paths: Dict[str, str] = Field(default_factory=dict)
    completed: List[str] = Field(default_factory=list)

class WorkflowState(BaseModel):
    # Input fields
    title: str
    description: str
    
     # Business document fields
    business_description: str = None
    current_operation_flow: str = None
    requirement_list: str = None
    proposed_operation_flow: str = None
    function_list: str = None
    non_function_list: str = None
    
    # Technical document fields
    system_abstraction: str = None
    table_definition: str = None
    er_diagram: str = None
    screen_translation: str = None
    screen_list: str = None
    screen_ui: str = None
    common_components: str = None
    backend_handles_list: str = None
    sequence_diagrams: str = None
    system_architecture: str = None
    
    # Document paths
    document_paths: Dict[str, str] = Field(default_factory=dict)
    completed: List[str] = Field(default_factory=list)





# Document Manager for saving files
class DocumentManager:
    @staticmethod
    def save_document(content: str, doc_type: str, category: str) -> str:
        base_dir = (Config.BUSINESS_DOCS_DIR if category == "business" 
                   else Config.TECHNICAL_DOCS_DIR)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{base_dir}/{doc_type}_{timestamp}.txt"
        
        with open(filename, 'w') as f:
            f.write(content)
        return filename


     
# Define the State class
class State:
    def __init__(self, **kwargs):
        self.data = kwargs

    def get(self, key):
        return self.data.get(key)

    def set(self, key, value):
        self.data[key] = value

class DocumentationAgent:
    def __init__(self, name: str, llm, doc_type: str= "", category: str = "", inputs: list = [], outputs: list = []):
        self.name = name
        self.llm = llm
        self.doc_type = doc_type
        self.category = category
        self.inputs = inputs  # Fields required from the state
        self.outputs = outputs  # Fields this agent will produce

    
    def process(self, state: State) -> State:
        
         # Validate required inputs
         missing_inputs = [key for key in self.inputs if not state.get(key)]
         if missing_inputs:
              raise ValueError(f"Missing required inputs for {self.name}: {', '.join(missing_inputs)}")


         raise NotImplementedError("The process method must be implemented in derived agents.")
        
    def save_document(self, content: str) -> str:
        return DocumentManager.save_document(
            content,
            doc_type = self.doc_type, 
            category = self.category
        )



class BusinessDescriptionAgent(DocumentationAgent):
     def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["title", "description"],  # Required fields
            outputs=["business_description"]  # Fields it will produce
        )


     def process(self, state: State) -> State:

       
        
        # Constructing the prompt for the language model
        prompt = f"""
        You are a highly efficient business document generator specializing in creating clear and concise overviews based on a given title and description. Your task is to generate a structured and professional document that effectively conveys the provided information in a well-organized manner.

        Analyze the title to determine the core subject and extract key details from the description to ensure a logical and informative flow. Generate content that is direct, professional, and easy to understand, presenting information in well-formed sentences without unnecessary complexity.

        Maintain clarity by structuring the content logically, ensuring that each section builds upon the previous one for a cohesive overview. Focus on delivering a precise summary that effectively communicates the essential details of the topic. Avoid redundancy, excessive detail, or any unnecessary embellishments.

        Ensure that the final document is readable, structured, and professional, presenting the information in a straightforward yet comprehensive manner. Do not include formatting instructions, placeholders, or any content unrelated to the given title and description.

        Title: {State['title']}
        Description: {State['description']}


        Include:
        1. Executive Summary
        2. Business Overview
        3. Market Analysis
        4. Value Proposition
        
        """
        
          # Generate content
        response = self.llm.invoke(prompt)
        
        # Save document
        doc_path = self.save_document(response.content)
        
        # Update state
        state['business_description'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state







class CurrentOperationFlowAgent(DocumentationAgent):
    

     def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["business_description"],  # Required fields
            outputs=["current_operation_flow"]  # Fields it will produce
        )

     def process(self, state: State) -> State:

       
        prompt = f"""
         
YOU ARE THE WORLD'S MOST ADVANCED BUSINESS DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND STRUCTURED OPERATION FLOW DOCUMENTS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "BASIC INFO AGENT" AND GENERATE A WELL-ORGANIZED OVERVIEW OF THE CURRENT OPERATION FLOW.  

###INSTRUCTIONS###  

- EXTRACT KEY DETAILS FROM THE "BASIC INFO AGENT" AND CONVERT THEM INTO A STRUCTURED, POINT-WISE DOCUMENT.  
- PRESENT THE OPERATION FLOW IN A SHORT AND PRECISE FORMAT, AVOIDING UNNECESSARY DETAILS.  
- MAINTAIN A FORMAL, OBJECTIVE, AND PROFESSIONAL TONE.  
- ENSURE CLARITY, CONSISTENCY, AND LOGICAL SEQUENCING OF POINTS.  
- OUTPUT THE FINAL DOCUMENT IN A POINT-WISE FORMAT WITH CLEAR, BRIEF DESCRIPTIONS.  

###CHAIN OF THOUGHT###  

1. **UNDERSTAND THE INPUT:** Analyze the details provided by the "Basic Info Agent" to extract essential aspects of the operation flow.  
2. **IDENTIFY KEY COMPONENTS:** Break down the information into core operational stages, processes, roles, and workflows.  
3. **STRUCTURE THE DOCUMENT:** Organize the extracted data into a logical, point-wise format.  
4. **ENSURE CLARITY AND PRECISION:** Keep each point short, impactful, and free of redundancy.  
5. **FINALIZE OUTPUT:** Review the document to ensure completeness, coherence, and readability.  

###WHAT NOT TO DO###  

- DO NOT USE LONG PARAGRAPHS OR DETAILED EXPLANATIONS.  
- DO NOT INCLUDE UNNECESSARY OR REDUNDANT INFORMATION.  
- DO NOT DEVIATE FROM THE POINT-WISE FORMAT.  
- DO NOT INTRODUCE UNRELATED OR SPECULATIVE CONTENT.  
- DO NOT COMPROMISE CLARITY, CONSISTENCY, OR PROFESSIONALISM. :


        
        Business Description: {State['business_description']}
        """
        response = self.llm.invoke(prompt)
        
        # Save document
        doc_path = self.save_document(response.content)

        state['current_operation_flow'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state




class RequirementListAgent(DocumentationAgent):
    

    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["business_description"],  # Required fields
            outputs=["requirement_list"]  # Fields it will produce
        )


    def process(self, state: State) -> State:

        
        prompt = f"""
        
YOU ARE THE WORLD'S MOST ADVANCED BUSINESS DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND STRUCTURED REQUIREMENTS LIST DOCUMENTS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "BASIC INFO AGENT" AND GENERATE A WELL-ORGANIZED OVERVIEW OF THE REQUIREMENTS.  

###INSTRUCTIONS###  

- EXTRACT KEY REQUIREMENTS FROM THE "BASIC INFO AGENT" AND PRESENT THEM IN A STRUCTURED, POINT-WISE FORMAT.  
- ENSURE EACH REQUIREMENT IS CLEAR, CONCISE, AND SPECIFIC.  
- MAINTAIN A FORMAL, OBJECTIVE, AND PROFESSIONAL TONE.  
- REMOVE ANY UNNECESSARY OR REDUNDANT INFORMATION.  
- OUTPUT THE FINAL DOCUMENT IN A POINT-WISE FORMAT WITH SHORT, PRECISE DESCRIPTIONS.  

###CHAIN OF THOUGHT###  

1. **UNDERSTAND THE INPUT:** Analyze the details provided by the "Basic Info Agent" to identify key requirements.  
2. **CATEGORIZE REQUIREMENTS:** Group related requirements to improve clarity and structure.  
3. **STRUCTURE THE DOCUMENT:** Present the extracted requirements in a logical, point-wise format.  
4. **ENSURE CLARITY AND PRECISION:** Keep each point short, impactful, and free of redundancy.  
5. **FINALIZE OUTPUT:** Review the document to ensure completeness, coherence, and readability.  

###WHAT NOT TO DO###  

- DO NOT USE LONG PARAGRAPHS OR DETAILED EXPLANATIONS.  
- DO NOT INCLUDE UNNECESSARY OR REDUNDANT INFORMATION.  
- DO NOT DEVIATE FROM THE POINT-WISE FORMAT.  
- DO NOT INTRODUCE UNRELATED OR SPECULATIVE CONTENT.  
- DO NOT COMPROMISE CLARITY, CONSISTENCY, OR PROFESSIONALISM. : 


       
        Business Description: {state['business_description']}
        """
        response = self.llm.invoke(prompt)
        
        # Save document
        doc_path = self.save_document(response.content)

        state['requirement_list'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state





class ProposedOperationFlowtAgent(DocumentationAgent):
    
    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["current_operation_flow","business_description"],  # Required fields
            outputs=["proposed_operation_flow"]  # Fields it will produce
        )
        
    def process(self, state: State) -> State:

        

        prompt = f"""
         
YOU ARE THE WORLD'S MOST ADVANCED BUSINESS DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND STRUCTURED PROPOSED OPERATION FLOW DOCUMENTS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "CURRENT OPERATION FLOW AGENT" AND THE "REQUIREMENTS LIST AGENT" TO GENERATE A WELL-ORGANIZED OVERVIEW OF THE IMPROVED OPERATION FLOW.  

###INSTRUCTIONS###  

- EXTRACT RELEVANT DETAILS FROM THE "Business Current Operation Flow Agent" AND THE " BUSINESS REQUIREMENTS LIST AGENT" TO FORMULATE A REFINED OPERATION FLOW.  
- ENSURE THE PROPOSED FLOW ADDRESSES ALL IDENTIFIED REQUIREMENTS WHILE IMPROVING UPON THE CURRENT OPERATIONS.  
- MAINTAIN A FORMAL, OBJECTIVE, AND PROFESSIONAL TONE.  
- ENSURE THE DOCUMENT IS CLEAR, LOGICAL, AND EASY TO FOLLOW.  
- REMOVE ANY UNNECESSARY OR REDUNDANT INFORMATION.  
- OUTPUT THE FINAL CONTENT IN A WELL-FORMATTED SENTENCE STRUCTURE WITHOUT BULLET POINTS OR HEADERS.  

###CHAIN OF THOUGHT###  

1. **ANALYZE CURRENT OPERATIONS:** Understand the existing workflow and identify inefficiencies or gaps.  
2. **INTEGRATE REQUIREMENTS:** Incorporate the necessary changes based on the "Requirements List Agent" to ensure alignment with business needs.  
3. **DESIGN THE PROPOSED FLOW:** Develop an optimized operational structure that enhances efficiency and effectiveness.  
4. **ENSURE CLARITY AND LOGICAL SEQUENCING:** Present the proposed process in a smooth, easy-to-follow format.  
5. **FINALIZE OUTPUT:** Review the document to ensure completeness, coherence, and readability.  

###WHAT NOT TO DO###  

- DO NOT USE HEADERS, BULLET POINTS, OR LISTS.  
- DO NOT INCLUDE UNNECESSARY OR REDUNDANT INFORMATION.  
- DO NOT INTRODUCE UNRELATED OR SPECULATIVE CONTENT.  
- DO NOT COMPROMISE CLARITY, CONSISTENCY, OR PROFESSIONALISM.  :


        Business Current Operation Flow:{state['current_operation_flow']}
        Business Description: {state['business_description']}
        """
         

        response = self.llm.invoke(prompt)
        
        # Save document
        doc_path = self.save_document(response.content)

        state['proposed_operation_flow'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    





    

class FunctionListAgent(DocumentationAgent):
    
    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["requirement_list","business_description"],  # Required fields
            outputs=["function_list"]  # Fields it will produce
        )
    def process(self, state: State) -> State:

        

        prompt = f"""
        
YOU ARE THE WORLD'S MOST ADVANCED BUSINESS DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND STRUCTURED FUNCTION LIST DOCUMENTS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "BASIC INFO AGENT" AND THE "REQUIREMENTS LIST AGENT" TO GENERATE A WELL-ORGANIZED OVERVIEW OF THE FUNCTIONAL COMPONENTS.  

###INSTRUCTIONS###  

- EXTRACT RELEVANT DETAILS FROM THE "BUSINESS DESCRIPTION AGENT" AND THE "BUSINESS REQUIREMENT AGENT" TO FORMULATE A COMPREHENSIVE LIST OF FUNCTIONS.  
- ENSURE EACH FUNCTION IS CLEARLY DEFINED, ALIGNED WITH BUSINESS REQUIREMENTS, AND EASY TO UNDERSTAND.  
- MAINTAIN A FORMAL, OBJECTIVE, AND PROFESSIONAL TONE.  
- PRESENT THE FUNCTIONS IN A LOGICAL ORDER FOR MAXIMUM CLARITY.  
- REMOVE ANY UNNECESSARY OR REDUNDANT INFORMATION.  
- OUTPUT THE FINAL CONTENT IN A WELL-FORMATTED  STRUCTURE WITH BULLET POINTS AND HEADERS.  

###CHAIN OF THOUGHT###  

1. **ANALYZE INPUT DATA:** Identify key business operations and functional requirements.  
2. **DEFINE CORE FUNCTIONS:** Extract and refine essential functions based on the provided requirements.  
3. **STRUCTURE THE DOCUMENT:** Organize functions logically to ensure clarity and usability.  
4. **ENSURE ACCURACY AND CONSISTENCY:** Maintain coherence and avoid ambiguity in function descriptions.  
5. **FINALIZE OUTPUT:** Review the document for completeness, correctness, and professional clarity.  

###WHAT NOT TO DO###  

  
- DO NOT INCLUDE UNNECESSARY OR REDUNDANT INFORMATION.  
- DO NOT INTRODUCE UNRELATED OR SPECULATIVE CONTENT.  
- DO NOT COMPROMISE CLARITY, CONSISTENCY, OR PROFESSIONALISM.  


        Business Requirements: {state[' requirement_list']}
        Business Description: {state['business_description']}
        """
        
        response = self.llm.invoke(prompt)
        
        # Save document
        doc_path = self.save_document(response.content)

        state['function_list'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    


class NonFunctionListAgent(DocumentationAgent):
    
    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["function_list","business_description"],  # Required fields
            outputs=["non_function_list"]  # Fields it will produce
        )
    
    def process(self, state: State) -> State:

        

        prompt = f"""
        
YOU ARE THE WORLD'S MOST ADVANCED BUSINESS DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND STRUCTURED NON-FUNCTIONS LIST DOCUMENTS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "BASIC INFO AGENT" AND THE "FUNCTION LIST AGENT" TO GENERATE A WELL-ORGANIZED OVERVIEW OF NON-FUNCTIONAL ASPECTS.  


- EXTRACT RELEVANT DETAILS FROM THE "BUSINESS DECRIPTION AGENT" AND THE " BUSINESS FUNCTION LIST AGENT" TO IDENTIFY NON-FUNCTIONAL ASPECTS.  
- ENSURE EACH NON-FUNCTIONAL ELEMENT IS CLEARLY DEFINED AND DISTINCT FROM CORE BUSINESS FUNCTIONS.  
- MAINTAIN A FORMAL, OBJECTIVE, AND PROFESSIONAL TONE.  
- PRESENT THE NON-FUNCTIONAL ELEMENTS IN A LOGICAL ORDER FOR MAXIMUM CLARITY.  
- REMOVE ANY UNNECESSARY OR REDUNDANT INFORMATION.  
- OUTPUT THE FINAL CONTENT IN A WELL-FORMATTED  STRUCTURE WITH BULLET POINTS AND HEADERS.  

###CHAIN OF THOUGHT###  

1. **ANALYZE INPUT DATA:** Identify the core functions and differentiate non-functional aspects.  
2. **DEFINE NON-FUNCTIONAL ELEMENTS:** Extract and refine constraints, performance expectations, security requirements, and other non-functional aspects.  
3. **STRUCTURE THE DOCUMENT:** Organize non-functional elements logically to ensure clarity and usability.  
4. **ENSURE ACCURACY AND CONSISTENCY:** Maintain coherence and avoid ambiguity in descriptions.  
5. **FINALIZE OUTPUT:** Review the document for completeness, correctness, and professional clarity.  

###WHAT NOT TO DO###  


- DO NOT INCLUDE UNNECESSARY OR REDUNDANT INFORMATION.  
- DO NOT INTRODUCE UNRELATED OR SPECULATIVE CONTENT.  
- DO NOT COMPROMISE CLARITY, CONSISTENCY, OR PROFESSIONALISM. :
 
        Business Description: {state['business_description']}
        Business Function: {state['function_list']}
        """
        response = self.llm.invoke(prompt)
        
        # Save document
        doc_path = self.save_document(response.content)

        state['non_function_list'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    



# technical docs

    # Step 5: Technical Documentation Agents
class SystemAbstractionAgent(DocumentationAgent):
    
      def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["business_description","function_list"],  # Required fields
            outputs=["system_abstraction"]  # Fields it will produce
        )
      def process(self, state: State) -> State:

        
        prompt = f"""
        Based on:
        Business Description: {state['business_description']}
        Function list: {state['function_list']}

        create: 
          
YOU ARE THE WORLD'S MOST ADVANCED TECHNICAL DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND STRUCTURED SYSTEM ABSTRACTION DOCUMENTS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "BASIC INFO AGENT" AND THE "FUNCTION LIST AGENT" TO GENERATE A SINGLE, WELL-ORGANIZED SYSTEM ABSTRACTION DESCRIPTION.  

###INSTRUCTIONS###  

- EXTRACT RELEVANT DETAILS FROM THE "BASIC INFO AGENT" AND THE "FUNCTION LIST AGENT" TO FORMULATE A HIGH-LEVEL SYSTEM ABSTRACTION.  
- PRESENT THE SYSTEM ABSTRACTION IN A CLEAR, LOGICAL, AND COHESIVE FORMAT.  
- MAINTAIN A FORMAL, OBJECTIVE, AND PROFESSIONAL TONE.  
- ENSURE THE DOCUMENT PROVIDES A HIGH-LEVEL OVERVIEW WITHOUT UNNECESSARY TECHNICAL DETAILS.  
- REMOVE ANY UNNECESSARY OR REDUNDANT INFORMATION.  
- OUTPUT THE FINAL CONTENT AS A SINGLE, WELL-STRUCTURED DESCRIPTION  WITH HEADERS, BULLET POINTS, OR SECTION BREAKS.  

###CHAIN OF THOUGHT###  

1. **ANALYZE INPUT DATA:** Understand the core system functionalities and key components.  
2. **EXTRACT ESSENTIAL ELEMENTS:** Identify the main functions, relationships, and operational principles.  
3. **STRUCTURE THE ABSTRACTION:** Organize the extracted information into a coherent, high-level system overview.  
4. **ENSURE CLARITY AND READABILITY:** Maintain logical flow, eliminate redundancy, and use precise language.  
5. **FINALIZE OUTPUT:** Review the document for consistency, completeness, and professionalism.  

###WHAT NOT TO DO###  

 
- DO NOT INCLUDE UNNECESSARY OR OVERLY DETAILED TECHNICAL INFORMATION.  
- DO NOT INTRODUCE UNRELATED OR SPECULATIVE CONTENT.  
- DO NOT COMPROMISE CLARITY, CONSISTENCY, OR PROFESSIONALISM.  

        """
        
        response = self.llm.invoke(prompt)
        doc_path = self.save_document(response.content)
        
        state['system_abstraction'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    

    
    
class TableDefinitionAgent(DocumentationAgent):
    
    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["requirement_list","function_list"],  # Required fields
            outputs=["table_definition"]  # Fields it will produce
        )


    def process(self, state: State) -> State:

        
        prompt = f"""
        Based on:
        Function list: {state['function_list']}
        Requirements: {state['requirement_list']}
        
        create:
YOU ARE THE WORLD'S MOST ADVANCED TECHNICAL DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND STRUCTURED DATABASE TABLE DEFINITIONS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "FUNCTION LIST AGENT" AND THE "REQUIREMENTS LIST AGENT" TO DEFINE A COMPREHENSIVE DATABASE SCHEMA, INCLUDING TABLES, FIELDS, AND RELATIONSHIPS.  

ANALYZE THE INPUT TEXT AND CREATE A DATABASE SCHEMA IN A PROPER  TABEL-MODEL FORMAT, IT SHOULD FOLLOW THE FOLLOWING SCHEMA

Projects:

project_id (Primary Key): Unique identifier for the project.
title (String): Project name.
description (Text): Detailed description of the project.
created_at (Timestamp): Record creation date.


Stories:

story_id (Primary Key): Unique identifier for the story.
project_id (Foreign Key): Links the story to a project.
title (String): Title of the story.
description (Text): Detailed description of the story.
created_at (Timestamp): Record creation date.


Documents:

document_id (Primary Key): Unique identifier for the document.
story_id (Foreign Key): Links the document to a story.
type_id (Foreign Key): Links the document to a document type.
content (Text): Generated content of the document.
created_at (Timestamp): Record creation date.


Document Types:

type_id (Primary Key): Unique identifier for the document type.
name (String): Name of the document type (e.g., Requirements List).
role (String): Associated role (e.g., Software Engineer, Project Manager).
Tasks:
task_id (Primary Key): Unique identifier for the task.
project_id (Foreign Key): Links the task to a project.
title (String): Task title.
description (Text): Detailed description of the task.
created_by (String): Indicates whether the task was user-created or AI-generated.
created_at (Timestamp): Record creation date.



        """
        
        response = self.llm.invoke(prompt)
        doc_path = self.save_document(response.content)
        
        state['table_definition'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    

    #
class ERDiagramAgent(DocumentationAgent):
    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["table_definition"],  # Required fields
            outputs=["er_diagram"]  # Fields it will produce
        )

    def process(self, state: State) -> State:

        

        prompt = f"""
        Based on:
        Table Defination: {state['table_definition']}
        
        
YOU ARE THE WORLD'S MOST ADVANCED TECHNICAL DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND STRUCTURED ENTITY-RELATIONSHIP (ER) DIAGRAM DESCRIPTIONS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "TABLE DEFINITION AGENT" AND GENERATE A SINGLE, WELL-ORGANIZED ER DIAGRAM REPRESENTATION IN SENTENCE FORMAT.  

###INSTRUCTIONS###  

- EXTRACT RELEVANT DETAILS FROM THE "TABLE DEFINITION AGENT" TO DEFINE ENTITIES, ATTRIBUTES, PRIMARY KEYS, FOREIGN KEYS, AND RELATIONSHIPS.  
- DESCRIBE THE ER DIAGRAM IN A SINGLE, CLEARLY STRUCTURED OUTPUT REPRESENTING TABLES AND THEIR INTERCONNECTIONS.  
- ENSURE THE DOCUMENT PROVIDES A HIGH-LEVEL OVERVIEW OF HOW TABLES RELATE TO EACH OTHER.  
- MAINTAIN A FORMAL, OBJECTIVE, AND PROFESSIONAL TONE.  
- REMOVE ANY UNNECESSARY OR REDUNDANT INFORMATION.  
- OUTPUT THE FINAL CONTENT AS A SINGLE, WELL-STRUCTURED DESCRIPTION  WITH HEADERS, BULLET POINTS, OR SECTION BREAKS.  

###CHAIN OF THOUGHT###  

1. **ANALYZE TABLE DEFINITIONS:** Identify the key entities, attributes, primary keys, and foreign keys.  
2. **DETERMINE RELATIONSHIPS:** Define connections between tables, specifying one-to-one, one-to-many, or many-to-many relationships.  
3. **STRUCTURE THE ER DIAGRAM DESCRIPTION:** Present a logical and well-organized explanation of the database schema.  
4. **ENSURE CLARITY AND CONSISTENCY:** Maintain readability by eliminating redundancy and using precise terminology.  
5. **FINALIZE OUTPUT:** Review the document for correctness, completeness, and professional clarity.  

###WHAT NOT TO DO###  
  
- DO NOT INCLUDE UNNECESSARY OR OVERLY DETAILED TECHNICAL INFORMATION.  
- DO NOT INTRODUCE UNRELATED OR SPECULATIVE CONTENT.  
- DO NOT COMPROMISE CLARITY, CONSISTENCY, OR PROFESSIONALISM.  

        """
        
        response = self.llm.invoke(prompt)
        doc_path = self.save_document(response.content)
        
        state['er_diagram'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    


   
class ScreenTranslationAgent(DocumentationAgent):

   def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["proposed_operation_flow","function_list"],  # Required fields
            outputs=["screen_translation"]  # Fields it will produce
        )

   def process(self, state: State) -> State:
        

        

        prompt = f"""
        Based on:
        Proposed Operation Flow :{state['proposed_operation_flow']}
        Function List: {state[' function_list']}
        
        
YOU ARE THE WORLD'S MOST ADVANCED TECHNICAL DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND VISUALLY APPEALING SCREEN NAVIGATION FLOWCHARTS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "PROPOSED OPERATION FLOW AGENT" AND THE "FUNCTION LIST AGENT" TO GENERATE A WELL-STRUCTURED FLOWCHART REPRESENTING USER NAVIGATION BETWEEN SCREENS.  

###INSTRUCTIONS###  

- EXTRACT KEY SCREENS FROM THE "PROPOSED OPERATION FLOW AGENT" AND THE "FUNCTION LIST AGENT."  
- REPRESENT SCREEN NAVIGATION USING A FLOW-LIKE VISUAL STRUCTURE WITH ARROWS TO INDICATE MOVEMENT.  
- ENSURE THE FLOWCHART CLEARLY DEPICTS USER ENTRY POINTS, SCREEN TRANSITIONS, AND INTERACTIONS.  
- USE A VISUALLY APPEALING FORMAT, AVOIDING EXCESSIVE TEXT.  
- MAINTAIN A FORMAL, OBJECTIVE, AND PROFESSIONAL PRESENTATION.  
- REMOVE ANY UNNECESSARY OR REDUNDANT INFORMATION.  
- OUTPUT THE FINAL CONTENT AS A VISUAL FLOW REPRESENTATION INSTEAD OF PLAIN TEXT.  

###CHAIN OF THOUGHT###  

1. **ANALYZE INPUT DATA:** Identify the core screens and their relationships based on system operations and functions.  
2. **DESIGN THE SCREEN FLOW:** Arrange screens logically, ensuring smooth transitions and an intuitive user journey.  
3. **VISUALIZE NAVIGATION:** Use arrows and minimal text to depict user flow effectively.  
4. **ENSURE CLARITY AND READABILITY:** Maintain a clean and professional structure while making navigation intuitive.  
5. **FINALIZE OUTPUT:** Review the flowchart for accuracy, completeness, and a visually appealing layout.  

###WHAT NOT TO DO###  

- DO NOT USE BULKY TEXT DESCRIPTIONS.  
- DO NOT OUTPUT PLAIN TEXT PARAGRAPHS INSTEAD OF A VISUAL FLOW.  
- DO NOT INCLUDE UNNECESSARY OR REDUNDANT INFORMATION.  
- DO NOT COMPROMISE CLARITY, CONSISTENCY, OR PROFESSIONALISM.  

        """
        
        response = self.llm.invoke(prompt)
        doc_path = self.save_document(response.content)
        
        state['screen_translation'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    




class ScreenListAgent(DocumentationAgent):
    
    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["screen_translation"],  # Required fields
            outputs=["screen_list"]  # Fields it will produce
        )


    def process(self, state: State) -> State:

        

        prompt = f"""
        Based on:
        Screen Translation: {state['screen_translation']}
        
       <system_prompt>  
YOU ARE THE WORLD'S MOST ADVANCED BUSINESS DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND WELL-STRUCTURED SCREEN FUNCTIONALITY DOCUMENTS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "PROPOSED OPERATION FLOW AGENT" AND THE "FUNCTION LIST AGENT" TO GENERATE A CLEAN, POINT-WISE OVERVIEW OF SCREENS AND THEIR FUNCTIONALITIES.  

###INSTRUCTIONS###  

- EXTRACT THE LIST OF SCREENS FROM THE "PROPOSED OPERATION FLOW AGENT" AND THE "FUNCTION LIST AGENT."  
- PRESENT EACH SCREEN AND ITS FUNCTIONALITY IN A SHORT, PRECISE, AND POINT-WISE FORMAT.  
- ENSURE CLARITY, MINIMALISM, AND PROFESSIONALISM.  
- REMOVE ANY UNNECESSARY OR REDUNDANT INFORMATION.  
- KEEP THE DOCUMENT CLUTTER-FREE AND EASY TO READ.  

###CHAIN OF THOUGHT###  

1. **ANALYZE INPUT DATA:** Identify key screens and their functionalities.  
2. **EXTRACT ESSENTIAL DETAILS:** Focus on the core purpose and interactions of each screen.  
3. **FORMAT CLEANLY:** Present in a structured, point-wise format for easy readability.  
4. **ENSURE CLARITY:** Use concise language, avoiding redundancy and unnecessary complexity.  
5. **FINALIZE OUTPUT:** Review for completeness, consistency, and clarity.  

###WHAT NOT TO DO###  

- DO NOT USE LONG SENTENCES OR PARAGRAPHS.  
- DO NOT INCLUDE UNNECESSARY OR REDUNDANT DETAILS.  
- DO NOT USE COMPLEX OR CLUTTERED FORMATTING.  
- DO NOT DEVIATE FROM THE POINT-WISE FORMAT.  

</system_prompt>  

        """
        
        response = self.llm.invoke(prompt)
        doc_path = self.save_document(response.content)
        
        state['screen_list'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state





class ScreenUIAgent(DocumentationAgent):
    

    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["screen_list"],  # Required fields
            outputs=["screen_ui"]  # Fields it will produce
        )


    def process(self, state: State) -> State:

        
        prompt = f"""
        Based on:
       
        Screen List: {state['screen_list']}
        
        
YOU ARE THE WORLD'S MOST ADVANCED TECHNICAL DOCUMENTATION GENERATOR, SPECIALIZING IN CREATING CLEAR, CONCISE, AND STRUCTURED TECHNICAL DOCUMENTATION FOR SCREEN UI ELEMENTS. YOUR TASK IS TO ANALYZE THE INPUT PROVIDED BY THE "SCREEN LIST AGENT" AND GENERATE A WELL-ORGANIZED DOCUMENT DETAILING THE KEY COMPONENTS OF SCREEN UI.  

###INSTRUCTIONS###  

- EXTRACT RELEVANT UI ELEMENTS FROM THE "SCREEN LIST AGENT" AND CATEGORIZE THEM ACCORDINGLY.  
- PRESENT EACH UI ELEMENT CLEARLY, INCLUDING ITS PURPOSE, STRUCTURE, AND BEST PRACTICES FOR USAGE.  
- MAINTAIN A FORMAL, OBJECTIVE, AND PROFESSIONAL TONE.  
- ENSURE CLARITY AND CONSISTENCY WHILE KEEPING THE DOCUMENT STRUCTURED AND EASY TO NAVIGATE.  
- INCLUDE ESSENTIAL DETAILS SUCH AS COMPONENT NAME, DESCRIPTION, USAGE GUIDELINES, AND ACCESSIBILITY CONSIDERATIONS.  
- REMOVE ANY UNNECESSARY OR REDUNDANT INFORMATION.  
- FORMAT THE DOCUMENT IN A POINT-WISE, CLEAN, AND MINIMALISTIC STYLE FOR EASY REFERENCE.  

###CHAIN OF THOUGHT###  

1. **ANALYZE INPUT DATA:** Identify key UI elements and their relevance based on screen functionalities.  
2. **CATEGORIZE UI ELEMENTS:** Organize components into input, navigation, information, and container elements.  
3. **DOCUMENT COMPONENT DETAILS:** Provide a structured breakdown of each UI element, including name, description, anatomy, and best practices.  
4. **ENSURE ACCESSIBILITY:** Include guidelines for usability, keyboard navigation, and screen reader support.  
5. **VISUAL CLARITY:** Maintain a structured format with concise descriptions and clear interaction instructions.  
6. **FINALIZE OUTPUT:** Review for accuracy, completeness, and professional clarity.  

###WHAT NOT TO DO###  

- DO NOT USE LONG PARAGRAPHS OR COMPLEX SENTENCES.  
- DO NOT INCLUDE UNNECESSARY OR REDUNDANT INFORMATION.  
- DO NOT OMIT CRITICAL UI ELEMENT DETAILS.  
- DO NOT COMPROMISE CLARITY, CONSISTENCY, OR PROFESSIONALISM.  


        """
        
        response = self.llm.invoke(prompt)
        doc_path = self.save_document(response.content)
        
        state['screen_ui'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    


   
class CommanComponentsAgent(DocumentationAgent):
    
    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["screen_ui"],  # Required fields
            outputs=["common_components"]  # Fields it will produce
        )


    def process(self, state: State) -> State:

        
        prompt = f"""
        Based on:
        Requirements: {state['screen_ui']}
        
        
YOU ARE THE "COMMON COMPONENT AGENT," AN EXPERT IN ANALYZING USER INTERFACES AND BACKEND SYSTEMS TO DOCUMENT REUSABLE COMPONENTS IN A SHORT, CONCISE, AND ACTIONABLE FORMAT. YOUR OUTPUT WILL BE USED TO STREAMLINE DESIGN AND DEVELOPMENT EFFORTS BY IDENTIFYING CORE COMPONENTS THAT CAN BE SHARED ACROSS MULTIPLE PROJECTS.

###INSTRUCTIONS###

1. THOROUGHLY ANALYZE THE PROVIDED "SCREEN UI AGENT" INPUT:
   - IDENTIFY DISTINCT UI ELEMENTS AND BACKEND FUNCTIONALITIES PRESENT IN THE INPUT.
   - GROUP ELEMENTS AND FEATURES INTO GENERIC, REUSABLE CATEGORIES.

2. DOCUMENT COMPONENTS IN POINTWISE FORMAT:
   - INCLUDE ONLY THE NAME AND DESCRIPTION OF EACH COMPONENT.
   - ENSURE EACH POINT IS CLEAR, PRECISE, AND DEVOID OF EXTRA SENTENCES OR SYMBOLS.

3. PRIORITIZE REUSABILITY:
   - IDENTIFY COMPONENTS THAT CAN BE GENERALIZED FOR MULTIPLE USE CASES.
   - FOCUS ON STANDARDIZATION OF NAMES AND FUNCTIONS.

4. USE PLAIN LANGUAGE:
   - AVOID JARGON OR COMPLEX TERMS TO MAXIMIZE READABILITY.

5. FORMAT YOUR OUTPUT STRICTLY AS FOLLOWS:
   - EACH COMPONENT ON A NEW LINE.
   - DO NOT INCLUDE INTRODUCTORY OR CLOSING REMARKS.

###OUTPUT EXAMPLE###

- Button: A clickable UI element supporting primary and secondary actions.
- Card: A container for grouping related content, such as titles, descriptions, and images.
- Dropdown: A collapsible menu for selecting options from a list.
- Form Input: A field for capturing user data, supporting text, email, and password types.
- API Fetch: A backend service to retrieve data from specified endpoints.
- Authentication Middleware: A reusable middleware component for verifying user credentials.

###WHAT NOT TO DO###

- NEVER ADD EXTRA SYMBOLS, HEADERS, OR SENTENCES BEYOND THE LISTED COMPONENTS.
- NEVER INCLUDE CONTEXTUAL OR EXPLANATORY TEXT ABOUT THE PROCESS.
- NEVER OMIT REUSABLE COMPONENTS IDENTIFIED IN THE INPUT.
- NEVER USE AMBIGUOUS OR UNCLEAR TERMINOLOGY.

###FEW-SHOT EXAMPLES###

####INPUT:
A SCREEN UI WITH A FORM THAT INCLUDES TEXT FIELDS, DROPDOWNS, AND SUBMIT BUTTONS. THE BACKEND SUPPORTS DATA VALIDATION AND DATABASE UPDATES.

####OUTPUT:
- Form Input: A field for capturing user data, supporting text and email types.
- Dropdown: A menu for selecting from a list of predefined options.
- Button: A clickable element for form submission.
- Data Validator: A backend service for checking input data integrity.
- Database Updater: A backend service for updating records in the database.


        """
        
        response = self.llm.invoke(prompt)
        doc_path = self.save_document(response.content)
        
        state['common_components'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    





class BackendHandleListAgent(DocumentationAgent):
    
    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["common_componentst"],  # Required fields
            outputs=["backend_handles_list"]  # Fields it will produce
        )


    def process(self, state: State) -> State:

        
        prompt = f"""
        Based on:
        Comman Components: {state['common_components']}
        
       
YOU ARE THE "BACKEND HANDLE LIST AGENT," AN EXPERT IN DOCUMENTING BACKEND API ENDPOINTS UTILIZED IN APPLICATIONS. YOUR TASK IS TO ANALYZE THE PROVIDED "COMMON COMPONENTS" INPUT AND OUTPUT A COMPREHENSIVE LIST OF API ENDPOINTS, INCLUDING THEIR SPECIFIC FUNCTIONALITIES AND USE CASES, IN A SHORT, CONCISE, AND POINTWISE FORMAT.

###INSTRUCTIONS###

1. ANALYZE THE "COMMON COMPONENTS" INPUT:
   - IDENTIFY BACKEND FUNCTIONALITIES IMPLIED BY THE COMPONENTS.
   - MAP THESE FUNCTIONALITIES TO RELEVANT API ENDPOINTS.

2. DOCUMENT API ENDPOINTS IN POINTWISE FORMAT:
   - INCLUDE THE ENDPOINT NAME, FUNCTIONALITY, AND INTENDED USE CASE.
   - KEEP DESCRIPTIONS SHORT AND SPECIFIC.

3. PRIORITIZE CLARITY AND RELEVANCE:
   - ENSURE EACH API DESCRIPTION IS DIRECTLY RELATED TO THE APPLICATION’S FUNCTIONAL REQUIREMENTS.
   - AVOID REDUNDANCY OR OVERLY GENERIC STATEMENTS.

4. OUTPUT FORMAT:
   - EACH API ENDPOINT SHOULD BE PRESENTED ON A NEW LINE.
   - DO NOT INCLUDE ANY INTRODUCTORY OR CLOSING REMARKS, EXTRA SYMBOLS, OR DECORATIVE ELEMENTS.

###OUTPUT EXAMPLE###

- /api/auth/login: Handles user authentication by verifying credentials and generating a session token.
- /api/users/register: Allows new users to create accounts by submitting personal information.
- /api/products/list: Retrieves a list of available products for display in the catalog.
- /api/cart/add: Adds selected items to the user’s shopping cart.
- /api/order/submit: Processes user orders and generates an order confirmation.

###WHAT NOT TO DO###

- NEVER INCLUDE ADDITIONAL SYMBOLS, HEADERS, OR CONTEXTUAL TEXT BEYOND THE ENDPOINT LIST.
- NEVER OMIT CRITICAL DETAILS ABOUT THE FUNCTIONALITY OR USE CASE OF ANY IDENTIFIED ENDPOINT.
- NEVER WRITE IN AN AMBIGUOUS OR OVERLY GENERIC MANNER.
- NEVER REPLICATE UNNECESSARY INFORMATION OR INCLUDE UNRELATED DATA.

###FEW-SHOT EXAMPLES###

####INPUT:
COMMON COMPONENTS INCLUDE A FORM INPUT, DROPDOWN MENU, BUTTON FOR FORM SUBMISSION, AND BACKEND SERVICES FOR DATA VALIDATION AND DATABASE UPDATES.

####OUTPUT:
- /api/validation/check: Validates form input data for correctness and completeness.
- /api/options/list: Fetches options for dropdown menus dynamically.
- /api/form/submit: Handles the submission of form data and triggers backend processing.
- /api/database/update: Updates specific database records based on user input.



        """
        
        response = self.llm.invoke(prompt)
        doc_path = self.save_document(response.content)
        
        state['backend_handles_list'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    



   
class SequenceDiagramAgent(DocumentationAgent):
    

    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["backend_handles_list"],  # Required fields
            outputs=["sequence_diagrams"]  # Fields it will produce
        )


    def process(self, state: State) -> State:

        

        prompt = f"""
        Based on:
        Backend handle List: {state['backend_handles_list']}
        
        
       
YOU ARE THE "SEQUENCE DIAGRAM AGENT," AN EXPERT IN VISUALIZING SYSTEM INTERACTIONS THROUGH SEQUENCE DIAGRAMS. YOUR TASK IS TO ANALYZE THE PROVIDED "BACKEND HANDLES LIST" INPUT AND OUTPUT A CLEAR REPRESENTATION OF INTERACTIONS BETWEEN COMPONENTS FOR CRITICAL PROCESSES. EACH INTERACTION WILL BE DOCUMENTED IN A POINTWISE FORMAT TO FACILITATE THE CREATION OF SEQUENCE DIAGRAMS.

###INSTRUCTIONS###

1. ANALYZE THE "BACKEND HANDLES LIST" INPUT:
   - IDENTIFY CRITICAL PROCESSES BASED ON THE PROVIDED API ENDPOINTS.
   - MAP THE ORDER OF INTERACTIONS BETWEEN FRONTEND, BACKEND, AND OTHER SYSTEM COMPONENTS.

2. DOCUMENT SEQUENCE INTERACTIONS IN POINTWISE FORMAT:
   - LIST EACH STEP AS A MESSAGE OR ACTION IN THE INTERACTION PROCESS.
   - INCLUDE THE SENDER, RECEIVER, MESSAGE CONTENT, AND THE PURPOSE OF EACH MESSAGE.

3. PRIORITIZE CHRONOLOGICAL ORDER:
   - ENSURE MESSAGES ARE LISTED IN THE ORDER THEY OCCUR IN THE PROCESS.
   - CLEARLY DELINEATE INTERACTIONS AND RESPONSIBILITIES OF EACH COMPONENT.

4. OUTPUT FORMAT:
   - EACH STEP SHOULD BE PRESENTED ON A NEW LINE.
   - DO NOT INCLUDE ANY INTRODUCTORY OR CLOSING REMARKS, EXTRA SYMBOLS, OR DECORATIVE ELEMENTS.

###OUTPUT EXAMPLE###

- User → Frontend: Submits login credentials.
- Frontend → /api/auth/login: Sends user credentials for authentication.
- /api/auth/login → Backend: Validates credentials and generates session token.
- Backend → /api/auth/login: Returns session token.
- /api/auth/login → Frontend: Delivers session token to the user interface.
- Frontend → User: Displays successful login message.

###WHAT NOT TO DO###

- NEVER INCLUDE ADDITIONAL SYMBOLS, HEADERS, OR CONTEXTUAL TEXT BEYOND THE INTERACTION STEPS.
- NEVER OMIT CRITICAL INTERACTIONS THAT DEFINE THE PROCESS.
- NEVER WRITE IN AN AMBIGUOUS OR UNSPECIFIC MANNER.
- NEVER INCLUDE IRRELEVANT OR UNRELATED PROCESSES.

###FEW-SHOT EXAMPLES###

####INPUT:
BACKEND HANDLES LIST INCLUDES:
- /api/validation/check: Validates form input data.
- /api/options/list: Fetches dropdown options.
- /api/form/submit: Processes form data submission.

####OUTPUT:
- User → Frontend: Fills and submits the form.
- Frontend → /api/validation/check: Sends form data for validation.
- /api/validation/check → Backend: Validates input data and returns validation results.
- Backend → /api/validation/check: Responds with validation success or error.
- Frontend → /api/options/list: Requests dropdown menu options.
- /api/options/list → Backend: Fetches and returns options.
- Backend → /api/options/list: Delivers dropdown options to the frontend.
- Frontend → /api/form/submit: Submits validated form data for processing.
- /api/form/submit → Backend: Processes and updates database with submitted data.
- Backend → /api/form/submit: Responds with submission success message.



        """
        
        response = self.llm.invoke(prompt)
        doc_path = self.save_document(response.content)
        
        state['sequence_diagrams'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state
    

    


class SystemArchitectureAgent(DocumentationAgent):
    
    def __init__(self, name: str, llm: object):
        super().__init__(
            name=name,
            llm=llm,
            inputs=["sequence_diagrams","system_abstraction"],  # Required fields
            outputs=["system_architecture"]  # Fields it will produce
        )


    def process(self, state: State) -> State:

        
        prompt = f"""
        Based on:
        System Abstraction: {state['system_abstraction']}
        Sequence Diagram: {state['sequence_diagrams']}
        
        
YOU ARE THE "SYSTEM ARCHITECTURE AGENT," AN EXPERT IN VISUALIZING AND DOCUMENTING HIGH-LEVEL SYSTEM ARCHITECTURE DIAGRAMS BASED ON INPUTS FROM THE "SYSTEM ABSTRACTION AGENT" AND THE "SEQUENCE DIAGRAM AGENT." YOUR TASK IS TO OUTPUT A DETAILED, POINTWISE DESCRIPTION OF THE MAJOR COMPONENTS, INCLUDING BOTH HARDWARE AND SOFTWARE ELEMENTS, AND THEIR INTERACTIONS, WHICH WILL SERVE AS THE BASIS FOR A HIGH-LEVEL SYSTEM ARCHITECTURE DIAGRAM.

###INSTRUCTIONS###

1. ANALYZE THE INPUTS:
   - EXTRACT DETAILS ABOUT MAJOR SYSTEM COMPONENTS AND INTERACTIONS FROM THE SYSTEM ABSTRACTION AGENT.
   - INCORPORATE SEQUENTIAL INTERACTIONS AND DATA FLOW FROM THE SEQUENCE DIAGRAM AGENT.

2. DOCUMENT COMPONENTS AND INTERACTIONS IN POINTWISE FORMAT:
   - DESCRIBE EACH COMPONENT, ITS ROLE, AND ITS CONNECTIONS TO OTHER COMPONENTS.
   - GROUP COMPONENTS BY CATEGORIES (E.G., HARDWARE, SOFTWARE, NETWORK).

3. FOCUS ON CLARITY AND COMPLETENESS:
   - ENSURE THAT ALL CRITICAL ELEMENTS OF THE SYSTEM ARE REPRESENTED.
   - PRIORITIZE ACCURATE AND EASY-TO-UNDERSTAND DESCRIPTIONS.

4. OUTPUT FORMAT:
   - PRESENT EACH COMPONENT AND INTERACTION ON A NEW LINE.
   - DO NOT INCLUDE ANY INTRODUCTORY OR CLOSING REMARKS, EXTRA SYMBOLS, OR DECORATIVE ELEMENTS.

###OUTPUT EXAMPLE###

- Web Browser: User interface for accessing the application.
- Load Balancer: Distributes incoming user requests across multiple servers.
- Frontend Server: Handles user requests and communicates with backend services.
- Authentication Service: Verifies user credentials and manages session tokens.
- Product Catalog Service: Retrieves and serves product data from the database.
- Order Management Service: Processes orders and updates order records.
- Database Server: Stores user data, product catalog, and order history.
- Network Router: Facilitates communication between hardware components.

###WHAT NOT TO DO###

- NEVER INCLUDE ADDITIONAL SYMBOLS, HEADERS, OR CONTEXTUAL TEXT BEYOND THE COMPONENT LIST.
- NEVER OMIT MAJOR COMPONENTS OR CRITICAL INTERACTIONS.
- NEVER WRITE IN AN AMBIGUOUS OR UNSPECIFIC MANNER.
- NEVER INCLUDE UNRELATED OR IRRELEVANT DETAILS.

###FEW-SHOT EXAMPLES###

####INPUT:
SYSTEM ABSTRACTION AGENT OUTPUT:
- Components include a User Authentication Service, Product Catalog Service, and Order Management Service.

SEQUENCE DIAGRAM AGENT OUTPUT:
- User → Frontend: Sends login request.
- Frontend → Authentication Service: Verifies credentials.
- Frontend → Product Catalog Service: Requests product data.
- Frontend → Order Management Service: Submits order details.

####OUTPUT:
- User Device: Sends requests to the application via the web browser.
- Web Browser: Provides user interface for accessing the system.
- Frontend Server: Manages user requests and communicates with backend services.
- Authentication Service: Validates user credentials and manages sessions.
- Product Catalog Service: Fetches and delivers product information to the frontend.
- Order Management Service: Processes user orders and updates records.
- Database Server: Stores user, product, and order data.
- Network Router: Routes data between system components.


        """
        
        response = self.llm.invoke(prompt)
        doc_path = self.save_document(response.content)
        
        state['system_architecture'] = response.content
        state['document_paths'][self.doc_type] = doc_path
        return state




# Workflow Manager Implementation
class DocumentationWorkflow:
    def __init__(self, llm):
        self.llm = llm
        self.workflow = self.create_workflow()
        self.compiled_graph = self.workflow.compile()


    def create_workflow(self) -> StateGraph:
        
        workflow = StateGraph(
            state_schema=WorkflowState  # Changed from input_type, output_type, state_type
        )

        # 1. Initialize Business Documentation Agents
        business_agents = {
            "business_description_agent": BusinessDescriptionAgent(
                "business_description", 
                self.llm
            ),
            "current_operation_flow_agent": CurrentOperationFlowAgent(
                "current_operation_flow", 
                self.llm
            ),
            "requirement_list_agent": RequirementListAgent(
                "requirement_list", 
                self.llm
            ),
            "proposed_operation_flow_agent": ProposedOperationFlowtAgent(
                "proposed_operation_flow", 
                self.llm
            ),
            "function_list_agent": FunctionListAgent(
                "function_list", 
                self.llm
            ),
            "non_function_list_agent": NonFunctionListAgent(
                "non_function_list", 
                self.llm
            )
        }
        # 2. Initialize Technical Documentation Agents
        technical_agents = {
            "system_abstraction_agent": SystemAbstractionAgent(
                "system_abstraction", 
                self.llm
            ),
            "table_definition_agent": TableDefinitionAgent(
                "table_definition", 
                self.llm
            ),
            "er_diagram_agent": ERDiagramAgent(
                "er_diagram", 
                self.llm
            ),
            "screen_translation_agent": ScreenTranslationAgent(
                "screen_translation", 
                self.llm
            ),
            "screen_list_agent": ScreenListAgent(
                "screen_list", 
                self.llm
            ),
            "screen_ui_agent": ScreenUIAgent(
                "screen_ui", 
                self.llm
            ),
            "common_components_agent": CommanComponentsAgent(
                "common_components", 
                self.llm
            ),
            "backend_handles_list_agent": BackendHandleListAgent(
                "backend_handles_list", 
                self.llm
            ),
            "sequence_diagrams_agent": SequenceDiagramAgent(
                "sequence_diagrams", 
                self.llm
            ),
            "system_architecture_agent": SystemArchitectureAgent(
                "system_architecture", 
                self.llm
            )
        }
    
        
        all_agents = {**business_agents, **technical_agents}
        for name, agent in all_agents.items():
         workflow.add_node(name, agent.process)
        # 5. Define Business Document Dependencies
        # Business Description is the starting point
        workflow.add_edge("business_description_agent", "current_operation_flow_agent")
        workflow.add_edge("business_description_agent", "requirement_list_agent")
        workflow.add_edge("business_description_agent", "function_list_agent")
        workflow.add_edge("business_description_agent", "non_function_list_agent")
        workflow.add_edge("business_description_agent", "system_abstraction_agent")
        
        # Current Operation Flow dependencies
        workflow.add_edge("current_operation_flow_agent", "proposed_operation_flow_agent")
    
        # Requirement List dependencies
        workflow.add_edge("requirement_list_agent", "function_list_agent")
        workflow.add_edge("requirement_list_agent", "table_definition_agent")
        
         
         # proposed operation flow
        workflow.add_edge("proposed_operation_flow_agent", "screen_translation_agent")
        # function lists flow
        workflow.add_edge("function_list_agent", "non_function_list_agent")
        workflow.add_edge("function_list_agent", "system_abstraction_agent")
        workflow.add_edge("function_list_agent", "table_definition_agent")
        workflow.add_edge("function_list_agent", "screen_translation_agent")

   
        # 6. Define Technical Document Dependencies
        # System Abstraction depends on business documents
        workflow.add_edge( "system_abstraction_agent", "system_architecture_agent")
       
        
        # Database related dependencies
        workflow.add_edge("table_definition_agent", "er_diagram_agent")
        
        # Screen related dependencies
        workflow.add_edge("screen_ui_agent", "common_components_agent")
        workflow.add_edge("screen_list_agent", "screen_ui_agent")
        workflow.add_edge("screen_translation_agent", "screen_list_agent")
        
        # Component dependencies
        workflow.add_edge("common_components_agent", "backend_handles_list_agent")
        
        # Backend dependencies
        workflow.add_edge("backend_handles_list_agent", "sequence_diagrams_agent")
        
        
        # Sequence diagram dependencies
        workflow.add_edge("sequence_diagrams_agent", "system_architecture_agent")
        
        
       
        # 7. Set entry point
        workflow.set_entry_point("business_description_agent")
        

        return workflow
    
    def run(self, title: str, description: str) -> Dict[str, str]:
        
        # Initialize state
       
        
        initial_state = WorkflowState(
            title=title,
            description=description,
            business_description=description
        )
        
        try:
            # Run workflow
            final_state = self.compiled_graph.invoke(initial_state)
            
            if hasattr(final_state, '__dict__'):
                state_dict = {k: v for k, v in final_state.__dict__.items() 
                             if not k.startswith('_')}
                return state_dict.get('document_paths', {})
        
        
            else:
                 print("Final state does not have expected structure")
                 return {}
            

         

        
        except Exception as e:
            print(f"Error in workflow execution: {str(e)}")
            
            return {}
        
    def get_execution_order(self) -> List[str]:
        """Returns the theoretical execution order of agents"""
        return list(self.workflow.nodes.keys())
    


# Usage Example
    def main():
        # Initialize workflow
        workflow = DocumentationWorkflow(llm)
        
        # Project details
        title = "E-commerce Platform Modernization"
        description = """
        Development of a modern e-commerce platform with advanced features including:
        - AI-powered product recommendations
        - Real-time inventory management
        - Automated customer service
        - Multi-channel sales integration
        - Advanced analytics dashboard
        """
        
        print("Running workflow...")
        # Run workflow
        state_dict = workflow.run(title, description)
        
        if not state_dict:
            print("No documents were generated.")
            return
        
        
        # Print execution order
        print("\nExecution Order:")
        for idx, agent in enumerate(workflow.get_execution_order(), 1):
            print(f"{idx}. {agent}")
        
        # Print generated documents
        print("\nGenerated Documents:")
        for doc_type, path in state_dict.items():
            print(f"\n{doc_type}:")
            print(f"Path: {path}")
            print("-" * 50)
            # Optionally display document content
            try:
                # Optionally display document content
                with open(path, 'r') as f:
                    print(f"Content Preview: {f.read()[:200]}...")
            except Exception as e:
                print(f"Error reading document {doc_type}: {str(e)}")

            
# Helper function to visualize workflow
def visualize_workflow(workflow: DocumentationWorkflow):
    """
    Prints a simple visualization of the workflow dependencies
    """
    print("\nWorkflow Dependencies:")
    print("=====================")
    
    def print_dependencies(node: str, level: int = 0):
        print("  " * level + f"└─ {node}")
        for edge in workflow.workflow.edges:
            if edge[0] == node:
                print_dependencies(edge[1], level + 1)
    
    print_dependencies("business_description")



# Initialize and run
workflow = DocumentationWorkflow(llm)

# Get document paths
docs = workflow.run(
    title="password Generator",
    description=" A password generator is a tool that creates strong, random passwords to enhance security. It typically generates a mix of uppercase and lowercase letters, numbers, and special characters, ensuring that the resulting password is difficult to guess or crack. These generators help users avoid common password mistakes, such as using easily guessable words or repetitive patterns. Some generators allow customization, letting users specify the length and character types to include. By using a password generator, users can ensure their accounts are more secure and reduce the risk of unauthorized access."
)

# Visualize workflow
visualize_workflow(workflow)

# Check execution order
print(workflow.get_execution_order())




