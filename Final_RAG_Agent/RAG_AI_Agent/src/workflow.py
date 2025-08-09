import os
from pathlib import Path
from dotenv import load_dotenv
from langgraph.graph import StateGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.caches import InMemoryCache
from langchain_core.globals import set_llm_cache
from langchain_core.documents import Document
from langchain_community.document_loaders import Docx2txtLoader
from langchain_community.document_loaders.pdf import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from .models import UserState
from .prompts import GenerationPrompts




class Workflow:
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4o", temperature=0.1)
        self.prompts = GenerationPrompts()
        self.workflow = self._build_workflow()
        self.cache = InMemoryCache()
        set_llm_cache(self.cache)

    # Create LangGraph workflow
    def _build_workflow(self):
        graph = StateGraph(UserState)
        graph.add_node("check_input", self.input_validation)
        graph.add_node("load_add_docs", self.load_add_documents)
        graph.add_node("get_synopsis", self.get_bio_synopsis)
        graph.add_node("get_advice", self.generate_advice)
        graph.add_edge(START, "load_add_docs")
        graph.add_conditional_edges("load_add_docs", self.input_validation)
        graph.add_edge("get_synopsis", "get_advice")
        graph.add_edge("get_advice", END)
        return graph.compile()
    
    # Check input for inappropriate or harmful requests
    def input_validation(self, state: UserState):
        """
        Check the user's query for inappropriate or harmful content

        Args:
            state: The agent's saved information.

        Returns:
            String: The next node the agent should use.
        """
        messages = [
            SystemMessage(content=self.prompts.INPUT_VALIDATION_SYSTEM),
            HumanMessage(content=self.prompts.input_validation_user(state.query))
        ]
        response = self.llm.invoke(messages)

        # Check if the LLM considers the query to have inappropriate or harmful requests
        if response.content == "True":
            print("This prompt is innappropriate or contains a harmful request.")
            return "END"
        return "get_synopsis"
    
    def load_add_documents(self, state: UserState):
        docs = []
        embeddings = OpenAIEmbeddings()

        folder_path = os.environ.get("FOLDER_PATH")

        for file_path in Path(folder_path).iterdir():
            for file_path_next in Path(file_path).iterdir():
                if file_path_next.suffix.lower() == ".pdf":
                    loader = PyPDFLoader(str(file_path_next))
                    docs.extend(loader.load())
                elif file_path_next.suffix.lower() == ".docx":
                    loader = Docx2txtLoader(str(file_path_next))
                    docs.extend(loader.load())
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        chunks = splitter.split_documents(docs)

        vector_store = FAISS.from_documents(chunks, embeddings)

        user_biometrics = [("heart_rate", state.heart_rate), ("mood", state.mood), ("did_exercise", state.did_exercise), ("sleep_description", state.sleep_description)]

        userdata_docs = {}

        retriever = vector_store.as_retriever(search_kwargs={"k": 3})

        for data in user_biometrics:
            if data[0] == "heart_rate":
                retrieved_docs = retriever.invoke(f"my heart rate is {data[1]}")
                userdata_docs["heart_rate"] = retrieved_docs
            elif data[0] == "mood":
                retrieved_docs = retriever.invoke(f"I am {data[1]} today")
                userdata_docs["mood"] = retrieved_docs
            elif data[0] == "did_exercise":
                retrieved_docs = retriever.invoke(f"benefits of exercise")
                userdata_docs["did_exercise"] = retrieved_docs
            elif data[0] == "sleep_description":
                retrieved_docs = retriever.invoke(data[1])
                userdata_docs["sleep_description"] = retrieved_docs

        retrieved_docs = retriever.invoke(state.query)
        userdata_docs["query"] = retrieved_docs

        return {"retrieved_docs": retrieved_docs, "docs_dict": userdata_docs}

    def get_bio_synopsis(self, state: UserState):
        bio_docs = state.docs_dict

        messages = [
            SystemMessage(content=self.prompts.BIODATA_SYNOPSIS_SYSTEM),
            HumanMessage(content=self.prompts.biodata_synopsis_user(state.heart_rate, state.mood, state.did_exercise, state.sleep_description, bio_docs))
        ]

        response = self.llm.invoke(messages)
        print(f"\nBio Synopsis:\n{response.content}")
        return {"synopsis": response.content}
    
    def generate_advice(self, state: UserState):

        messages = [
            SystemMessage(content=self.prompts.ADVICE_GENERATION_SYSTEM),
            HumanMessage(content=self.prompts.advice_generation_user(state.retrieved_docs, state.query, state.synopsis))
        ]

        response = self.llm.invoke(messages)
        return {"advice": response.content}
    


    def run(self, query: str, heart_rate: str, mood: str, did_exercise: str, sleep_description: str) -> UserState:
        """
        Run the agent

        Args:
            topic: The users query to be searched.

        Returns:
            Object: The final agent state
        """
        starting_state = UserState(query=query, heart_rate=heart_rate, mood=mood, did_exercise=did_exercise, sleep_description=sleep_description)
        finished_state = self.workflow.invoke(starting_state)
        return UserState(**finished_state)