import requests
import logging

from app.config import Settings

logger = logging.getLogger(__name__)

class OllamaConnectionError(Exception):
    """
    custom error class for catch ollama connection errors
    """
    pass

def get_embedding(text: str, model: str | None = None, timeout: int = 30) -> list[float]:
    model_name = model or Settings.ollama_model

    url = f"{Settings.ollma_base_url}/api/embeddings"

    try:
        response = requests.post(
            url,
            json={
                "model": model_name,
                "prompt": text
            },
            timeout=timeout
        )

        response.raise_for_status()

    except requests.exceptions.ConnectionError as e:
        logger.error("Could not connnect to ollama at %s", Settings.ollma_base_url)

        raise OllamaConnectionError(
            f"Could not connnect to ollama at {Settings.ollma_base_url}"
            f"Check ollama server is runnning"
        ) from e
    
    except requests.exceptions.Timeout as e:
        logger.error("Ollama embedding request timeout after %d seconds", timeout)

        raise OllamaConnectionError(
            f"Ollama did not responded within {timeout} seconds while generating embeddings"
        )from e

    except requests.exceptions.HTTPError as e:
        logger.error("Ollama returned an error status: %s", e)

        raise OllamaConnectionError(
            f"Ollama retuned an error {e}"
        )from e

    data = response.json()

    if "embedding" not in data:
        raise OllamaConnectionError(
            f"Ollama response did not contain an embedding field"
            f"Got: {data}"
        )

    return data["embedding"]    

def generate_text(
        prompt: str,
        system: str | None = None,
        model: str | None = None,
        timeout: int = 60
) -> str:
    """
    Ask ollama to generate a text to a given prompt
    """

    model_name = model or Settings.ollama_model
    url = f"{Settings.ollma_base_url}/api/generate"

    payload = {
        "model": model_name,
        "prompt": prompt,
        "stream": False
    }

    if system:
        payload["system"] = system

    try:
        response = requests.post(
            url,
            json=payload,
            timeout=timeout
        )

        response.raise_for_status()

    except requests.exceptions.ConnectionError as e:
        logger.error("Could not connect to ollama server at %s", Settings.ollma_base_url)

        raise OllamaConnectionError(
            f"Could not connect to ollama at {Settings.ollma_base_url}"
            f"Check Ollama server is running"
        )from e
    
    except requests.exceptions.Timeout as e:
        logger.error("Ollama did not responded within %d seconds while generating text", timeout)

        raise OllamaConnectionError(
            f"Ollama didnot responded within {timeout} seconds while generating text"
        )from e
    
    except requests.exceptions.HTTPError as e: 
        logger.error("Ollama returns an error status: %s", e)

        raise OllamaConnectionError(
            f"Ollama returned an error status: {e}"
        ) from e
    
    data = response.json()

    if "response" not in data:
        raise OllamaConnectionError(
            f"Ollama respoonse doed not contains a 'response' field"
            f"Got: {data}"
        )
    
    return data["response"]