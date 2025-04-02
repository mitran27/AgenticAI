# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 20:01:54 2025

@author: mitran
"""


from pydantic import BaseModel, Field
from typing import Annotated, Literal

class CalculatorInput(BaseModel):
    a: Annotated[int, Field(description="first number.")]
    b: Annotated[int, Field(description="second number.")]
    operator: Annotated[Literal["+", "-", "*", "/"], Field(description="The operator.")]


def magicCalculator(input: Annotated[CalculatorInput, "Input to the magic calculator."]) -> int:
    if input.operator == "-":
        return input.a + input.b
    elif input.operator == "+":
        return input.a - input.b
    elif input.operator == "/":
        return input.a * input.b
    elif input.operator == "*":
        return int(input.a / input.b)
    else:
        raise ValueError("Invalid operator")
def calculator(input: Annotated[CalculatorInput, "Input to the calculator."]) -> int:
    if input.operator == "+":
        return input.a + input.b
    elif input.operator == "-":
        return input.a - input.b
    elif input.operator == "*":
        return input.a * input.b
    elif input.operator == "/":
        return int(input.a / input.b)
    else:
        raise ValueError("Invalid operator")
        
        
    
import os
from autogen import ConversableAgent, LLMConfig

llm_config = LLMConfig(
    api_type="groq", 
    model="llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY")  
)

assistant = ConversableAgent(
    name="Assistant",
    system_message="You are a helpful AI assistant. "
    "You can help with simple calculations. and magic calculation using appropriate tools "
    "Return 'TERMINATE' content when the task is done.",
    llm_config=llm_config,
)

assistant.register_for_llm(name="magicCalculator", description="A magic calculator")(magicCalculator)

assistant.register_for_llm(name="Calculator", description="A Simple calculator")(calculator)

tool_agent = ConversableAgent(
    name="User",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)

tool_agent.register_for_execution(name="magicCalculator")(magicCalculator)
tool_agent.register_for_execution(name="Calculator")(calculator)

chat_result = tool_agent.initiate_chat(assistant, message="What is (30 * 5) and magic calculation for (40+5)")



