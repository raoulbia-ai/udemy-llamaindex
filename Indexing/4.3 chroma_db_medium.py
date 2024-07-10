"""
https://medium.com/how-ai-built-this/llamaindex-comprehensive-guide-on-storage-99ca9851be9c
"""
import Indexing

from langchain.embeddings import HuggingFaceEmbeddings
from llama_index import LangchainEmbedding, ServiceContext, StorageContext, download_loader, LLMPredictor
from langchain.chat_models import ChatOpenAI
from llama_index.vector_stores import ChromaVectorStore

import chromadb
from chromadb.config import Settings

from llama_index import GPTVectorStoreIndex, SimpleDirectoryReader

# init Chroma collection
# chroma_client = chromadb.PersistentClient(path="./storage/chroma/")

## create collection
# chroma_collection = chroma_client.create_collection("apple_10k_report")
chroma_client = chromadb.PersistentClient(path="./storage/chroma")

chroma_collection = chroma_client.get_or_create_collection("apple_10k_report")  # create only if it doesn't exist yet

## I use OpenAI ChatAPT as LLM Model. This will cost you money
llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2,
                                            max_tokens=512,
                                            model_name='gpt-3.5-turbo'))

## by default, LlamIndex use OpenAI's embedding, we will use HuggingFace's embedding instead
embed_model = LangchainEmbedding(HuggingFaceEmbeddings())

## init ChromaVector storage for storage context
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

## init service context
service_context = ServiceContext.from_defaults(
      llm_predictor=llm_predictor,
      embed_model=embed_model
)


# load document
directory_path = '../assets/AndrewHuberman/sleep'
# documents = SimpleDirectoryReader(input_files='./data/Apple-10k-Q1-2023.pdf').load_data()
documents = SimpleDirectoryReader(directory_path, filename_as_id=True).load_data()
# use GPTVectorStoreIndex, it will call embedding mododel and store the
# vector data (embedding data) in the your storage folder
index = GPTVectorStoreIndex.from_documents(documents=documents,
                                           storage_context=storage_context,
                                           service_context=service_context)

## save index
index.set_index_id("gptvector_apple_finance")
index.storage_context.persist('./storage/index_storage/apple/')


## load index
from llama_index import load_index_from_storage
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.index_store import SimpleIndexStore

## create ChromaClient again
# chroma_client = chromadb.PersistentClient(path="./storage/chroma/")

# load the collection
collection = chroma_client.get_collection("apple_10k_report")

## construct storage context
load_storage_context = StorageContext.from_defaults(
    vector_store=ChromaVectorStore(chroma_collection=collection),
    index_store=SimpleIndexStore.from_persist_dir(persist_dir="./storage/index_storage/apple/"),
)

## init LLM Model
llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.2, max_tokens=512, model_name='gpt-3.5-turbo'))

## init embedding model
embed_model = LangchainEmbedding(HuggingFaceEmbeddings())

## construct service context
load_service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor,embed_model=embed_model)

## finally to load the index
load_index = load_index_from_storage(service_context=load_service_context,
                                     storage_context=load_storage_context)

query = load_index.as_query_engine()
response = query.query("how does light affect sleep")
print(response)
