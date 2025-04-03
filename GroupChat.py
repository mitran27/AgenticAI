# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 19:49:07 2025

@author: mitran
"""

import os,dotenv

from autogen import ConversableAgent, UserProxyAgent, AssistantAgent, LLMConfig, GroupChat,GroupChatManager
from autogen.coding import LocalCommandLineCodeExecutor
dotenv.load_dotenv()

llm_config = LLMConfig(
    api_type="groq", 
    model= "llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")  
)


client = ConversableAgent(
    name="Admin",
    system_message="Give the task, and send "
    "instructions to writer to refine the blog post.",
    code_execution_config=False,
    llm_config=llm_config,
    human_input_mode="ALWAYS",
)


architect = ConversableAgent(
    name="architect",
    system_message="Given a task, please determine "
    " what is the required data to be fetched , write a two line developer requriement"
    "after retrieving data instruct the writer to write the content on the topic. ",
    description="Planner. Given a task, determine what "
    "steps is needed to complete the task. "
    "After each step is done by others, check the progress and "
    "instruct the remaining steps",
    llm_config=llm_config,
)



developer = AssistantAgent(
    name="Developer",
    llm_config=llm_config,
    system_message="Youare supposed to only write code,do not hallocinate on any data",
    description="Write simple code based on the developer requirement and return the executed data"
    "provided by the architect.",
)


contentWriter = ConversableAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="Writer. "
    "Please write blogs in markdown format (with relevant titles)"
    " and put the content in pseudo ```md``` code block. "
    "You shpoul write a content for 5 lines based on the given content."
    "You should improve the quality of the content you gave if you recieve a feedback from user",
    description="After all the info is available, "
    "write blogs based on the code execution results and take "
    "feedback from the admin to refine the blog. ",
)




executor = ConversableAgent(
    name="Executor",
    description="Execute the code written by the "
    "developer and report the result.",
    human_input_mode="NEVER",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "coding",
        "use_docker": False,
    },
)

def developer_logic(x):
    print("hooooking")
    print(x)


groupchat = GroupChat(
    agents=[architect,developer,contentWriter,client],
    messages=[],
    max_round=5,
    allowed_or_disallowed_speaker_transitions={
       architect: [developer, contentWriter,client],
       developer: [architect],
       contentWriter: [architect],
       client: [architect],
   },
   speaker_transitions_type="allowed",
)


productManager = GroupChatManager(
    groupchat=groupchat, llm_config=llm_config
)


developer.register_nested_chats(
	trigger=productManager,
	chat_queue=[
    	{
        	"recipient": executor,  
            "sender": developer,
        	"summary_method": "last_msg",
        	"max_turns": 2,
    	}
	],
)

critic = AssistantAgent(
    name="Critic",
    llm_config=llm_config,
    system_message="""
    You are a critic, known for your thoroughness and commitment to standards.
    Your task is to scrutinize content for any harmful elements or regulatory violations, ensuring
    all materials align with required guidelines.
    """,
)


def extract_message(recipient, messages, sender, config):
    print("Reflecting...", "yellow")
    return f"Reflect and provide critique on the following writing. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"

contentWriter.register_nested_chats(
    [{"recipient": critic, "message": extract_message, "summary_method": "last_msg", "max_turns": 2}],
    trigger=productManager,  # condition=my_condition,
)



requirement = "Write a blogpost about the stock price performance of "\
"Nvidia for past 30 days from  2025-04-02."


client.initiate_chat(
    productManager,
    message=requirement,
)
