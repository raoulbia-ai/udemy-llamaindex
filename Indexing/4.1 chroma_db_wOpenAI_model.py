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
from llama_index import SimpleDirectoryReader
from llama_index.vector_stores import ChromaVectorStore
from llama_index import VectorStoreIndex
from llama_index.storage.storage_context import StorageContext
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

openaikey = api_key=os.getenv('OPENAI_API_KEY')

# splitting files in chunks
def chunk_text(data, chunk_size=1024, chunk_overlap=20):
    from langchain.document_loaders import TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    doc = TextLoader(data).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
                                                   chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(doc)
    print(f'Nbr of chunks produced: {len(chunks)}')
    return chunks


# Load documents
directory_path = r'..\\assets\\AndrewHuberman\\sleep\\'
documents = SimpleDirectoryReader(input_dir=directory_path, filename_as_id=True).load_data()
print(documents[0].id_)
print(f"Number of documents loaded: {len(documents)}")

"""chromadb utils:  default model_name: str = text-embedding-ada-002"""
embed_model = OpenAIEmbeddingFunction(api_key=openaikey)  # #dim 1538

# Create a collection with the specified embedding function
chroma_client = chromadb.PersistentClient(path="./storage/chroma/sleep")
chroma_collection = chroma_client.get_or_create_collection(name='andrew_sleep_db',
                                                           embedding_function=embed_model)
# chroma_collection = chroma_client.create_collection(name='andrew_sleep_db')

# Initialize lists for documents, metadatas, and ids
document_list = []
embedding_list = []
# metadata_list = []
id_list = []

# Iterate over the documents and populate the lists
for i, _ in enumerate(documents):
    # id_list.append(f'doc_{i}')
    # document_list.append(documents[i].text)
    text_chunks = chunk_text(documents[i].id_)  # pass the file path
    for j, chunk in enumerate(text_chunks):
        # print(f'adding chunk {j}')
        chroma_collection.add(
            # embeddings=embedding_list
            documents=str(chunk)
            # , metadatas=metadata_list
            , ids=f'doc_{j}')
        break
    break


# Create vector store and index
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store, storage_context=storage_context)

# Create llamaindex query engine
"""the default embedding model is the text-embedding-ada-002 model from OpenAI"""
query_engine = index.as_query_engine()

# Perform a query
prompt = 'how does temperature affect sleep?'
response = query_engine.query(prompt)
pprint_response(response)

"""
# embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2') # dim 384
# embed_model = LangchainEmbedding(
#     HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))  # dim 768
# embed_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
# sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002")
"""