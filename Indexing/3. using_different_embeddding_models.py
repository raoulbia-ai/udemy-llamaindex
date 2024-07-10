"""all-mpnet-base-v2-model AKA sentence transformer model

Transformer-based embedding models from HuggingFace
pip install sentence-transformers
pip install langchain

they can look at all the words in a sentence at once.
This allows them to understand complex sentences and long range dependencies between words better than
any model before them.
So a sentence transformer is a python framework for the state of the art sentence, text and image embeddings.
It maps sentences and paragraphs to a 768 dimensional dense vector space and can be used for semantic search.

note:
- OpenAI Ada mode creates 1536 dimensions, while mpnet creates 768
- to use HuggingFace embeddings, install langchain
- remember the most important class in Llamaindex is ServiceContext
  we use this class to change the default embedding model

see also https://github.com/jbergant/LlamaIndexCourse/blob/main/andrewHuggingFaceEmbeddings.ipynb
"""
import Indexing

# Example embedding with default OpenAI Ada model
from llama_index.embeddings import OpenAIEmbedding
text = "Wonderful day"
embed_model = OpenAIEmbedding()
embedding = embed_model.get_text_embedding(text)
print(embedding)

# Example with HuggingFaceEmbeddings
from langchain.embeddings import HuggingFaceEmbeddings
from llama_index.embeddings import LangchainEmbedding
text = "Wonderful day"
embed_model = LangchainEmbedding(HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2")
)
embedding = embed_model.get_text_embedding(text)
print(embedding)



