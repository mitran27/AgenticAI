# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 18:31:31 2025

@author: mitran
"""

from langchain_groq import ChatGroq  # Import ChatGroq class
from autogen import ConversableAgent, LLMConfig, AssistantAgent
import os , dotenv
dotenv.load_dotenv()



import tempfile
from autogen.coding import LocalCommandLineCodeExecutor



llm_config = LLMConfig(
    api_type="groq", 
    model="deepseek-r1-distill-llama-70b", 
    api_key=os.getenv("GROQ_API_KEY")  
)




executor = LocalCommandLineCodeExecutor(
    timeout=60,
    work_dir="coding",
)

code_executor_agent = ConversableAgent(
    name="code_executor_agent",
    llm_config=False,
    code_execution_config={"executor": executor},
    human_input_mode="ALWAYS",
    default_auto_reply=
    "Please continue. If everything is done, reply 'TERMINATE'.",
)

code_writer_agent = AssistantAgent(
    name="code_writer_agent",
    llm_config=llm_config,
    code_execution_config=False,
    human_input_mode="NEVER",

)

import datetime

today = datetime.datetime.now().date()
message = f"Today is {today}. "\
"Create a plot showing stock gain YTD for NVDA and TLSA. "\
"Make sure the code is in markdown code block and save the figure"\
" to a file ytd_stock_gains.png."""

chat_result = code_executor_agent.initiate_chat(
    code_writer_agent,
    message=message,
)


