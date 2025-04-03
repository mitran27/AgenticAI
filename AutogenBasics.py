# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 11:00:16 2025

@author: mitran
"""

from langchain_groq import ChatGroq  # Import ChatGroq class
from autogen import ConversableAgent, LLMConfig
import os , dotenv
dotenv.load_dotenv()



llm_config = LLMConfig(
    api_type="groq", 
    model="llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY")  
)





cathy = ConversableAgent(
    "cathy",
    system_message="Your name is Cathy and you are a doctor who helps to diagnize the client illness and suggest a cure.Make sure conversation is not more than three line",
    llm_config=llm_config,
    human_input_mode="NEVER",  
)

patient = ConversableAgent(
    "alan",
    system_message="Your name is Alan and you are a patient who can to doctor for your fever, telling your symptoms.Make sure conversation is not more than three line",
    llm_config=llm_config,
    human_input_mode="NEVER",  
)


result = patient.initiate_chat(cathy, message="Cathy, I am Ill.", max_turns=2)

