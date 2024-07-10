"""
https://medium.com/how-ai-built-this/llamaindex-comprehensive-guide-on-storage-99ca9851be9c
https://github.com/run-llama/llama_index/issues/7110 about dimension mismatch

TODO note when installing sentence-transformer it meeses up llam-index and openai versions
as a result you have to run pip install --upgrade llama-index afterwards
"""
import os
import Indexing
import chromadb
from llama_index.response.pprint_utils import pprint_response
from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, OpenAIEmbedding
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext

openaikey = api_key=os.getenv('OPENAI_API_KEY')

# Load documents
directory_path = r'..\\assets\\AndrewHuberman\\sleep\\'
documents = SimpleDirectoryReader(input_dir=directory_path, filename_as_id=True).load_data()
print(documents[0].id_)
print(f"Number of documents loaded: {len(documents)}")

embed_model = OpenAIEmbedding(api_key=openaikey)

# Create a collection with the specified embedding function
chroma_client = chromadb.PersistentClient(path="./storage/chroma/sleep")
chroma_collection = chroma_client.get_or_create_collection(name='andrew_sleep_db')


# Iterate over the documents and populate the lists
for i, doc in enumerate(documents):
    chroma_collection.add(
        embeddings=embed_model.get_text_embedding(str(doc))
        , ids=f'doc_{i}')
    # break


# Create vector store and index
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
service_context = ServiceContext.from_defaults(embed_model=embed_model,
                                               chunk_size=1000,
                                               chunk_overlap=200)

index = VectorStoreIndex.from_documents(documents,
                                       storage_context=storage_context,
                                       service_context=service_context)
# Create llamaindex query engine
"""default embedding model is text-embedding-ada-002 model from OpenAI"""
query_engine = index.as_query_engine()

# Perform a query
prompt = 'summarise document in one sentence'
response = query_engine.query(prompt)
pprint_response(response)

