from fastapi import FastAPI, HTTPException, Body, Request
from pydantic import BaseModel
from AutogenMain import initiate_autogen

app = FastAPI()

# This class defines that 'logs' must be a string
class ChatLog(BaseModel):
    logs: str 


# Initialize Autogen components
ragproxyagent, group_chat_manager = initiate_autogen()

# Store chat history in the application state
chat_history = []

@app.get("/")
def welcome():
    """
    Simple endpoint to display a welcome message.

    Returns:
    - str: Welcome message.
    """
    return "Hello, World!"
from litellm import completion
@app.post("/initiate_chat/")
def initiate_chat(logs: ChatLog):  # Use the Pydantic model to parse and validate the input
    global chat_history
    try:
        # Reset chat history to an empty list
        chat_history = []

        # Extract the 'logs' field from the validated input
        chat_logs = logs.logs  # 'logs' is now an object of ChatLog, and 'logs.logs' accesses the string

        # Initiate chat using RAG proxy agent
        chat_result = ragproxyagent.initiate_chat(
            group_chat_manager,
            message=ragproxyagent.message_generator,
            problem=chat_logs.rstrip()) # Pass the extracted logs
        

        # Append user chat messages to the chat history
        if len(chat_result.chat_history) != 0:
            for chat in chat_result.chat_history:
                if chat['role'] == 'user':
                    chat_history.append(chat['content'])
        return "Chat initiated successfully"
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/analysis/")
def analysis():
    """
    Endpoint to retrieve chat analysis.
    """
    return {"Analysis": "\n\n".join(chat_history)}

