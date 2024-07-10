import Indexing
import openai
import os
from transformers import pipeline
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction, HuggingFaceEmbeddingFunction

openaikey = api_key=os.getenv('OPENAI_API_KEY')
hfkey = api_key=os.getenv('HUGGINGFACEHUB_API_TOKEN')

# Example text
text = "Hello, world!"

# Initialize the embedding functions
openai_embedding_function = OpenAIEmbeddingFunction(api_key=openaikey)
huggingface_embedding_function = HuggingFaceEmbeddingFunction(api_key=hfkey, model_name='sentence-transformers/all-MiniLM-L6-v2')

# Get embeddings
openai_embedding = openai_embedding_function(text)
huggingface_embedding = huggingface_embedding_function(text)

# Inspect embeddings
print("OpenAI Embedding:", openai_embedding[0][:5])
print("Hugging Face Embedding:", huggingface_embedding[:5])

# Check dimensions
openai_embedding_dim = len(openai_embedding)
huggingface_embedding_dim = len(huggingface_embedding)

# Print dimensions
print("Dimension of OpenAI Embedding:", openai_embedding_dim)
print("Dimension of Hugging Face Embedding:", huggingface_embedding_dim)

