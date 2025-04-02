# -*- coding: utf-8 -*-
"""
Created on Tue Apr  1 22:18:28 2025

@author: mitran
"""

import os
from autogen import ConversableAgent, LLMConfig
import  dotenv
dotenv.load_dotenv()

llm_config = LLMConfig(
    api_type="groq", 
    model="llama3-8b-8192", 
    api_key=os.getenv("GROQ_API_KEY")  
)

start_agent = ConversableAgent(
    name="Number_Agent",
    system_message="retyrn the given number",

    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Adder Agent adds 1 to each number it receives.
adder_agent = ConversableAgent(
    name="Adder_Agent",
    system_message="add 1 to the given number",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Multiplier Agent multiplies each number it receives by 2.
multiplier_agent = ConversableAgent(
    name="Multiplier_Agent",
    system_message="multiply 2 to the given number",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Subtracter Agent subtracts 1 from each number it receives.
subtracter_agent = ConversableAgent(
    name="Subtracter_Agent",
    system_message="subtract 1 from the given number.",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

# The Divider Agent divides each number it receives by 2.
divider_agent = ConversableAgent(
    name="Divider_Agent",
    system_message="divide 2 from the given number",
    llm_config=llm_config,
    human_input_mode="NEVER",
)

"""start_agent.initiate_chats(
    [
        {
            "recipient": adder_agent,
            "message": "14",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": multiplier_agent,
            "message": "",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": subtracter_agent,
            "message": "",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
        {
            "recipient": divider_agent,
            "message": "",
            "max_turns": 2,
            "summary_method": "last_msg",
        },
    ]
)"""



adder_agent.description = "Add 1 to each input number."
multiplier_agent.description = "Multiply each input number by 2."
subtracter_agent.description = "Subtract 1 from each input number."
divider_agent.description = "Divide each input number by 2."
start_agent.description = "Return the numbers given."

allowed_transitions = {
    start_agent: [adder_agent, start_agent],
    adder_agent: [multiplier_agent, start_agent],
    subtracter_agent: [divider_agent, start_agent],
    multiplier_agent: [subtracter_agent, start_agent],
    divider_agent: [adder_agent, start_agent],
}

from autogen import GroupChat

group_chat = GroupChat(
    agents=[adder_agent, multiplier_agent, subtracter_agent, divider_agent,start_agent],
    allowed_or_disallowed_speaker_transitions=allowed_transitions,
    speaker_transitions_type="allowed",
    messages=[],
    max_round=12,
    send_introductions=True,
)


from autogen import GroupChatManager

group_chat_manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
)



chat_result = start_agent.initiate_chat(
    group_chat_manager,
    message="My number is 3, I want to turn it into 13",
    summary_method="reflection_with_llm",
)
