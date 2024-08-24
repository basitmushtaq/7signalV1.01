from qdrant_client import QdrantClient
from config import config_list, qdrant_config_list
import logging

logging.basicConfig(level=logging.INFO)

def QDRANT(collection_name, embedding_model, customized_prompt, docs_list):
    """
    Function to configure QDRANT for question answering tasks.

    Args:
    - collection_name (str): Name of the collection.
    - embedding_model (str): Name of the embedding model to use.
    - customized_prompt (str): Customized prompt for the QA task.
    - docs_list (list): List of documents for indexing (used when the collection doesn't exist).

    Returns:
    - dict: Configuration dictionary for QDRANT.
    """
    try:
        client = QdrantClient(
                    url=qdrant_config_list[0]['uri'], 
                    api_key=qdrant_config_list[0]['api_key']
                )

        # Check if the collection exists
        collection_exists = client.collection_exists(collection_name=collection_name)
        retrieve_config = {
            "model": config_list[0]["model"],
            "client": client,
            "embedding_model": embedding_model,
            "overwrite": True,
            "chunk_token_size": 1000,
            "customized_prompt": customized_prompt
        }

        if collection_exists:
            points_count = client.get_collection(collection_name=collection_name).points_count
            if points_count == 0:
                # Handle empty existing collection (e.g., reindexing)
                logging.info(f"Collection {collection_name} exists but is empty. Deleting and reinitializing.")
                client.delete_collection(collection_name=collection_name)
                retrieve_config["docs_path"] = docs_list
        else:
            # Prepare configuration for new collection creation
            logging.info(f"Collection {collection_name} does not exist. Initializing a new collection.")
            retrieve_config["docs_path"] = docs_list

        return retrieve_config

    except Exception as e:
        logging.error(f"Failed to configure QDRANT: {str(e)}")
        return None

