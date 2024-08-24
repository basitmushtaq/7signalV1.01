
# Network Copilot 7Signal

## Overview
This project is a specialized document processing system, incorporating Streamlit, Qdrant, and AutoGen for document-based question-answering. With different modules focusing on unique tasks, it aims to deliver accurate answers and insights to user queries.

## Features
1. **Modular Architecture:** Each module is designed for specific responsibilities such as configuration, main logic orchestration, and Streamlit web interface.
2. **Streamlit Web Interface:** The `streamlit_main.py` file offers a simple yet powerful UI for submitting queries and viewing answers.
3. **AutoGen Management:** The `AutogenMain.py` script integrates with AutoGen to improve the conversational abilities of the system's agents.
4. **Configuration Flexibility:** The `config.py` file provides an easy way to manage system parameters like database credentials, paths, etc.
5. **Customizable Prompts:** The system allows dynamic customization of assistant names, descriptions, and prompts through environment variables.

## Module Overview
- **`AutogenMain.py`:** Orchestrates the interaction with AutoGen for enhancing question-answering capabilities.
- **`main.py`:** Provides APIs for interaction. Currently two endpoints are present. One responsible for feeding input to the LLM and the second for displaying the result.
- **`config.py`:** Contains customizable parameters like API keys, collection names, and now includes environment variables for prompt customization.
- **`Qdrant_.py`:** Integrates the Qdrant vector search engine for rapid data retrieval and retrieval augmented generation.
- **`streamlit_main.py`:** Provides a user-friendly web interface using Streamlit.

## Setup & Requirements
1. **Python Version:** Python 3.9 or higher is required.
2. **Dependencies:** Install all dependencies using `pip install -r requirements.txt`.
3. **Environment Setup:**
   - Ensure you have the necessary API keys and connection URLs for Qdrant or other vector stores.
   - Adjust parameters in `config.py` accordingly.
   - **Customization:** Update the following environment variables in your `.env` file to customize the prompts and assistant configurations:
     - `CUSTOMIZED_PROMPT`: main prompt for LLM
     - `assistant1_name` : name for the LLM agent that is used to answer direct queries
     - `assistant2_name` : name for the LLM agent that is used to answer network queries
     - `assistant1_description` : description for the LLM agent that is used to answer direct queries
     - `assistant2_description` : description for the LLM agent that is used to answer network queries
     - `assistant1_system_message` : System prompt for the LLM agent that is used to answer direct queries
     - `assistant2_system_message` : System prompt for the LLM agent that is used to answer network queries

## Qdrant Setup
1. **Create Account & Cluster:** Sign up at Qdrant Cloud, create a cluster, and obtain the endpoint URL and API key.
2. **Update Configurations:** Update the `.env` file with your Qdrant credentials.

## Model Information
The system now uses the `claude3.5-sonnet` model, which replaces the previous `llama` model. Ensure that your API keys and access are updated to accommodate this change.

## Docker Setup
1. **Dockerfile:** The provided Dockerfile is configured to work seamlessly with the system.
2. **Environment Variables:** Ensure the `.env` file is updated with all necessary environment variables before building the Docker image.
3. **Docker Build:** Run the following command to build the Docker image:
   - `docker build -t 7signal .`
4. **Running the Docker Container:** Use the following command to run the container:
   - `docker run -d -p 80:80 -p 8050:8050 --name 7signal-instance --env-file .env 7signal`

## Notes
- Make sure that Qdrant or any vector search engine is correctly configured and connected.
- The system logs execution times for performance monitoring.
- Make sure that no other services are running on ports 80 and 8050 on your host machine to avoid port conflicts.
