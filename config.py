import os
import dotenv

dotenv.load_dotenv()

# Configuration list containing parameters for different services
config_list = [
    {
        "model": "bedrock/anthropic.claude-3-5-sonnet-20240620-v1:0",
        "base_url": "http://localhost:4000/",
        "api_key": "NULL",
    }
]
qdrant_config_list = [
    {
        # Parameters for the second service (QDRANT)
        "uri": os.getenv("uri"),
        "api_key": os.getenv("api_key"),  # API key for the QDRANT service
    }
]
