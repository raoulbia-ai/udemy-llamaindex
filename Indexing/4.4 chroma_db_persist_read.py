"""
https://medium.com/how-ai-built-this/llamaindex-comprehensive-guide-on-storage-99ca9851be9c
https://cookbook.openai.com/examples/vector_databases/chroma/using_chroma_for_embeddings_search
"""
import os
import Indexing
import chromadb
from llama_index.response.pprint_utils import pprint_response
from llama_index.vector_stores import ChromaVectorStore
from llama_index import VectorStoreIndex, ServiceContext, OpenAIEmbedding

openaikey = os.getenv('OPENAI_API_KEY')

embed_model = OpenAIEmbedding(api_key=openaikey)

chroma_client = chromadb.PersistentClient(path="./storage/chroma/sleep")
chroma_collection = chroma_client.get_collection(name='andrew_sleep_db')
# print(chroma_collection.peek())

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
service_context = ServiceContext.from_defaults()
index = VectorStoreIndex.from_vector_store(vector_store=vector_store,
                                           service_context=service_context)

prompt = 'summarise the collection in one setence'

query_engine = index.as_query_engine()
response = query_engine.query(prompt)
pprint_response(response)
