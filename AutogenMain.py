# Importing necessary modules
import autogen
import dotenv
import os
from logger import logger
from autogen.agentchat.contrib.qdrant_retrieve_user_proxy_agent import (
    QdrantRetrieveUserProxyAgent,
)
from autogen.agentchat.contrib.retrieve_assistant_agent import RetrieveAssistantAgent
from qdrant_client import QdrantClient
from config import config_list, qdrant_config_list

dotenv.load_dotenv()

logger.info("use meta.llama3-70b-instruct-v1:0")
qdrant_client = None
logger.info(os.getenv("CUSTOMIZED_PROMPT"))


# Function to initiate autogen setup
def initiate_autogen():
    global qdrant_client

    # Check if the client has already been instantiated
    if qdrant_client is None:
        # Initiate Qdrant client if not already created
        qdrant_client = QdrantClient(
            url=qdrant_config_list[0]["uri"], api_key=qdrant_config_list[0]["api_key"]
        )
        print("Qdrant client initiated")

    if os.getenv("CUSTOMIZED_PROMPT"):
        customized_prompt = f"""{os.getenv("CUSTOMIZED_PROMPT")}"""
    else:
        customized_prompt = """ 
            I'll provide you with some additional context about the problem, This context can be used to enhance your existing knowledge base.
            If you think the additional context improves the answer quality then use it otherwise dont use it.
            
            Additional context that can be used along with your own knowledge to answer the question is: {input_context}

            You are a Retrieve Augmented Chatbot capable of answering user questions related to provided books or completely independent topics.

            Let's define how you should proceed:

            Identify the Question Type:
            If the user input question is in JSON format, treat it as a networking problem.
            If the user input question is not in JSON format, treat it as a direct query.
            
            After identifying the question type pass it to an agent. Please note that one user input question should be given only to one agent for getting the answer

            Responding to the Question:
            When user input is in JSON format (networking agent), provide a detailed and relevant response based on the given data.
            When user input is not in JSON format (direct agent), start the answer directly without writing anything about the question format provide a clear and direct answer using your knowledge and the provided context.
            

            User question: {input_question}


        """
    # Retrieve Config for User Proxy Agent
    retrieve_config = {
        "model": config_list[0]["model"],
        "client": qdrant_client,
        "embedding_model": "sentence_transformers/all-MiniLM-L6-v2",
        "overwrite": True,
        "chunk_token_size": 1000,
        "customized_prompt": customized_prompt,
    }
    print("retrieve_config")
    # Configuration for LLM (Language Model)
    llm_config = {
        "timeout": 1200,
        "cache_seed": None,
        "config_list": config_list,
        "temperature": 0.2,
    }

    # Creating Qdrant Retrieve User Proxy Agent
    ragproxyagent = QdrantRetrieveUserProxyAgent(
        name="ragproxyagent",
        human_input_mode="NEVER",
        retrieve_config=retrieve_config,
        code_execution_config=False,
    )

    # Creating Retrieve Assistant Agent for direct queries
    if os.getenv('assistant1_name') and os.getenv('assistant1_description') and os.getenv('assistant1_system_message'):

        assistant = RetrieveAssistantAgent(
            name=os.getenv('assistant1_name'),
            is_termination_msg=lambda x: x.get("content", "")
            and x.get("content", "").rstrip().endswith("NEVER"),
            max_consecutive_auto_reply=1,
            system_message=os.getenv('assistant1_system_message'),
            description=os.getenv('assistant1_description'),
            human_input_mode="NEVER",
            llm_config=llm_config,
        )
    else:
        assistant = RetrieveAssistantAgent(
            name="Direct",
            is_termination_msg=lambda x: x.get("content", "")
            and x.get("content", "").rstrip().endswith("NEVER"),
            max_consecutive_auto_reply=1,
            system_message="""
            Start addressing the question directly using your knowledge base. Provide detailed answers covering every aspect of the question. 
            Respond as you typically would in a question-answer scenario, drawing from your existing knowledge base. Refrain from answering when presented with JSON formats.
            """,
            description="""
            An AI agent designed to answer user input questions that are not in JSON format. You can not understand inputs that are in JSON Format. 
            """,
            human_input_mode="NEVER",
            llm_config=llm_config,
        )

    if os.getenv('assistant2_name') and os.getenv('assistant2_description') and os.getenv('assistant2_system_message'):

            assistant2 = RetrieveAssistantAgent(
            name=os.getenv('assistant2_name'),
            is_termination_msg=lambda x: x.get("content", "")
            and x.get("content", "").rstrip().endswith("NEVER"),
            max_consecutive_auto_reply=1,
            system_message=os.getenv('assistant2_system_message'),
            description=os.getenv('assistant2_description'),
            human_input_mode="NEVER",
            llm_config=llm_config,
        )
    else:
        # Creating Retrieve Assistant Agent for network issues
        assistant2 = RetrieveAssistantAgent(
        name="Network",
        is_termination_msg=lambda x: x.get("content", "")
        and x.get("content", "").rstrip().endswith("NEVER"),
        max_consecutive_auto_reply=1,
        system_message="""
        When presented with JSON objects, troubleshoot them for network issues, providing in-depth inference analysis of the logs. Inference analysis based on the data is crucial. 
        Conduct a thorough review after inferring the logs. If issues are found, offer detailed troubleshooting. If no issues are found, reply "Your network seems okay." 
        Your interaction is solely for JSON inputs; remain unresponsive to direct queries.
        """,
        description="""
        An AI agent designed to analyze and troubleshoot user input questions in the form of JSON format, providing valuable inferencing and troubleshooting capabilities. You can not
        understand inputs that are not in JSON Format 
        """,
        llm_config=llm_config,
        human_input_mode="NEVER",
    )

    
    groupchat = autogen.GroupChat(
        agents=[ragproxyagent, assistant, assistant2],
        messages=[],
        speaker_selection_method="auto",
        max_round=4,
    )

    # Creating Group Chat Manager
    group_chat_manager = autogen.GroupChatManager(
        groupchat=groupchat, llm_config=llm_config
    )

    return ragproxyagent, group_chat_manager
