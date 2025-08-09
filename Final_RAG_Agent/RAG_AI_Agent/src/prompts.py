from typing import List, Dict
from langchain_core.documents import Document

class GenerationPrompts():
    INPUT_VALIDATION_SYSTEM = """ You are a meticulous reviewer of words and phrases. """

    @staticmethod
    def input_validation_user(query: str) -> str:
        return f""" Topic: {query}
                Determine whether the query is inappropriate or contains harmful requests.

                Only respond with True if it does or False if it doesnt

                """
    
    BIODATA_SYNOPSIS_SYSTEM = """ You are a health specialist. Extract important information that
                               could be used to provide valuable advice about user issues.
                               """
    
    @staticmethod
    def biodata_synopsis_user(heart_rate: str, mood: str, did_exercise: str, sleep_description: str, docs: Dict[str, List[Document]]) -> str:
        return f""" User Biometric Data: 
                - Heart rate: {heart_rate} 
                - Heart rate content: {docs["heart_rate"]}

                - Mood: {mood} 
                - Mood content: {docs["mood"]}

                - Did user exercise today?: {did_exercise} 
                - Exercise content: {docs["did_exercise"]}

                - How user slept: {sleep_description}
                - Sleep content: {docs["sleep_description"]}

                Using the above user biometrics and their respective content provide a brief synopsis of the users health.
                Provide either motivation or concern depending on users biometric data and add any information from the content
                data that might be valuable to the user.
                
                """
    
    ADVICE_GENERATION_SYSTEM = """ You are a medical professional providing motivational or concerned advice on patient health 
                               data and queries.
                               """
    
    @staticmethod
    def advice_generation_user(query_docs: List[Document], query: str, synopsis: str) -> str:
        return f"""Query: {query}
                Content: {query_docs}

                - Based on the content provided write a paragraph containing some professional wellness advice to answer the users query.

                Synopsis: {synopsis}

                Next provide a summary based on the users synopsis
                """
    
