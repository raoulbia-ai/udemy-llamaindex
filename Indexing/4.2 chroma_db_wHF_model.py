"""
llm = AzureOpenAI(engine="gpt-35-turbo", model="gpt-35-turbo", temperature=0.0)
https://huggingface.co/docs/transformers/llm_tutorial
"""
import os
from dotenv import load_dotenv, find_dotenv
import chromadb
from llama_index.response.pprint_utils import pprint_response
from llama_index import SimpleDirectoryReader
from llama_index.vector_stores import ChromaVectorStore
from llama_index import VectorStoreIndex, ServiceContext
from llama_index.storage.storage_context import StorageContext
# from chromadb.utils.embedding_functions import HuggingFaceEmbeddingFunction
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from llama_index.embeddings import LangchainEmbedding


hfkey = api_key=os.getenv('HUGGINGFACEHUB_API_TOKEN')

# splitting files in chunks
def chunk_text(data, chunk_size=1024, chunk_overlap=20):
    """
    :return: list of Document objects
    """
    from langchain.document_loaders import TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter

    doc = TextLoader(data).load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    chunks = text_splitter.split_documents(doc)
    print(f'Nbr of chunks produced: {len(chunks)}')
    return chunks

# def chunk_text(text, chunk_size=100):
#     words = text.split()
#     return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]


# Load documents
directory_path = r'..\\assets\\AndrewHuberman\\sleep\\'
documents = SimpleDirectoryReader(directory_path, filename_as_id=True).load_data()
print(documents[0].id_)
print(f"Number of documents loaded: {len(documents)}")
h
embed_model = LangchainEmbedding(
    # HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2")
    HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")  # 'all-mpnet-base-v2'
)


# Create a collection with the specified embedding function
chroma_client = chromadb.EphemeralClient()

# print(chroma_client.list_collections())
collection_name = 'andrew_sleep_db'
chroma_collection = chroma_client.get_or_create_collection(name=collection_name)  # <<<<<<<<<

# Create vector store and index
service_context = ServiceContext.from_defaults(embed_model=embed_model,
                                               llm= ....)  # <<<<<<<<<<<<<<<<<<<<???
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_vector_store(vector_store=vector_store,
                                           storage_context=storage_context,
                                           service_context=service_context)

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
        chroma_collection.add(
            # embeddings=embed_model(chunk),
            documents=str(chunk)
            # , metadatas=metadata_list
            , ids=f'doc_{j}')
        break
    break



# # Create llamaindex query engine
# """the default embedding model is the text-embedding-ada-002 model from OpenAI"""
# query_engine = index.as_query_engine(embedding_model='sentence-transformers/all-MiniLM-L6-v2', show_progress=True)
#
# # Perform a query
# prompt = 'how does temperature affect sleep?'
# response = query_engine.query(prompt)
# pprint_response(response)

"""
# embed_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2') # dim 384
# embed_model = LangchainEmbedding(
#     HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"))  # dim 768
# embed_model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
# sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
# openai_ef = embedding_functions.OpenAIEmbeddingFunction(model_name="text-embedding-ada-002")
"""