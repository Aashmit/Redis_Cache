from langchain_ollama import OllamaEmbeddings
from redisvl.utils.vectorize import CustomTextVectorizer
import asyncio
from typing import List

def create_vectorizer():
    # Initialize OllamaEmbeddings
    ollama_embedder = OllamaEmbeddings(model='nomic-embed-text')

    # Define the synchronous embedding function
    def sync_embed(text: str) -> List[float]:
        return ollama_embedder.embed_query(text)

    # Define the synchronous batch embedding function
    def sync_embed_many(texts: List[str]) -> List[List[float]]:
        return ollama_embedder.embed_documents(texts)

    # Define a wrapper for async single-text embedding
    async def async_embed(text: str) -> List[float]:
        # Run the synchronous method in a separate thread
        return await asyncio.to_thread(sync_embed, text)

    # Define a wrapper for async batch embedding
    async def async_embed_many(texts: List[str]) -> List[List[float]]:
        # Run the synchronous method in a separate thread
        return await asyncio.to_thread(sync_embed_many, texts)

    # Configure and return CustomTextVectorizer
    return CustomTextVectorizer(
        embed=sync_embed,
        aembed=async_embed,
        embed_many=sync_embed_many,
        aembed_many=async_embed_many
    )

# Create a singleton instance
vectorizer = create_vectorizer()