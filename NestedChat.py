# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:19:42 2025

@author: mitran
"""
import os,dotenv

from autogen import ConversableAgent, UserProxyAgent, AssistantAgent, LLMConfig
dotenv.load_dotenv()

llm_config = LLMConfig(
    api_type="groq", 
    model="llama3-8b-8192", 
    api_key=os.getenv("GROQ_API_KEY")  
)


# Individual chats

writer = AssistantAgent(
    name="Writer",
    llm_config=llm_config,
    system_message="""
    You are a professional writer, known for your insightful and engaging articles.
    You shpoul write a content for 5 lines based on the given content.
    You should improve the quality of the content you gave if you recieve a feedback from user.
    """,
)


user_proxy = UserProxyAgent(
    name="User",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    code_execution_config={
        "last_n_messages": 1,
        "work_dir": "tasks",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
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

# user -> writer - >user - >critic- > user - > writer - > user
"""
user_proxy.register_nested_chats(
    [{"recipient": critic, "message": extract_message, "summary_method": "last_msg", "max_turns": 1}],
    trigger=writer,  # condition=my_condition,
)


res = user_proxy.initiate_chat(recipient=writer, message="Write a concise but engaging blogpost about Google.", max_turns=2, summary_method="last_msg")
"""

"""
writer.register_nested_chats(
	trigger=user_proxy,
	chat_queue=[
    	{
        	"sender": critic,
        	"recipient": writer,
        	"summary_method": "last_msg",
        	"max_turns": 2,
    	}
	],
)

# user-> crite-> witer-> critic->writer->user

res = user_proxy.initiate_chat(recipient=writer, message="Write a concise but engaging blogpost about Google.", max_turns=2, summary_method="last_msg")
"""


# with tool

tool_agent = ConversableAgent(
    name="Tool",
    llm_config=False,
    is_termination_msg=lambda msg: msg.get("content") is not None and "TERMINATE" in msg["content"],
    human_input_mode="NEVER",
)


from typing_extensions import Annotated

def check_harmful_content(content: Annotated[str, "Content to check if harmful keywords."]):
    # List of harmful keywords for demonstration purposes
    harmful_keywords = ["violence", "hate", "bullying", "death"]

    # Normalize the input text to lower case to ensure case-insensitive matching
    text = content.lower()

    print(f"Checking for harmful content...{text}", "yellow")
    # Check if any of the harmful keywords appear in the text
    for keyword in harmful_keywords:
        if keyword in text:
            return "Denied. Harmful content detected:" + keyword  # Harmful content detected

    return "Approve. TERMINATE"  # No harmful content detected


tool_agent.register_for_execution(name="check_harmful_content")(check_harmful_content)
critic.register_for_llm(name="check_harmful_content", description="Check if content contain harmful keywords.")(check_harmful_content)

def reflection_message_no_harm(recipient, messages, sender, config):
    print("Reflecting...", "yellow")
    return f"Reflect and provide critique on the following writing. Ensure it does not contain harmful content. You can use tools to check it. \n\n {recipient.chat_messages_for_summary(sender)[-1]['content']}"



user_proxy.register_nested_chats(
	trigger=writer,
	chat_queue=[
    	{
        	"sender": tool_agent,
        	"recipient": critic,
            "message": reflection_message_no_harm,
        	"summary_method": "last_msg",
        	"max_turns": 2,
    	}
	],
)

res = user_proxy.initiate_chat(recipient=writer, message="Write a concise but engaging blogpost about Google.", max_turns=2, summary_method="last_msg")
