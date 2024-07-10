from llama_index import VectorStoreIndex, SimpleDirectoryReader, ServiceContext, OpenAIEmbedding
from llama_index.vector_stores import ChromaVectorStore
from llama_index.storage.storage_context import StorageContext
from dotenv import load_dotenv, find_dotenv
from chromadb_helper import ChromaDBHelper
from pprint import pprint
import os

_ = load_dotenv(find_dotenv())

def load_document(file):
    import os
    name, extension = os.path.splitext(file)

    if extension == '.pdf':
        from langchain.document_loaders import PyPDFLoader
        print(f'Loading {file}')
        loader = PyPDFLoader(file)
    elif extension == '.docx':
        from langchain.document_loaders import Docx2txtLoader
        print(f'Loading {file}')
        loader = Docx2txtLoader(file)
    elif extension == '.txt':
        from langchain.document_loaders import TextLoader
        loader = TextLoader(file)
    else:
        print('Document format is not supported!')
        return None

    data = loader.load()
    return data

class ChromaDBVectorizer:
    def __init__(self, fp, name):

        helper = ChromaDBHelper()
        try:
            # helper.fetch_collection(name)
            self.chroma_collection = helper.fetch_collection(name)
            print(f'collection {name} has been fetched')
        except:
            self.chroma_collection = helper.create_collection(name)
            print(f'collection {name} has been created')

        # define embedding function
        embed_model = OpenAIEmbedding(api_key=os.getenv('OPENAI_API_KEY'))

        # load documents
        self.documents = SimpleDirectoryReader(
            input_dir=fp,
            filename_as_id=True
            # required_exts=['.pdf']
        ).load_data()

        # Iterate over the documents and populate the lists
        # for i, _ in enumerate(self.documents):
        #     # print(self.documents[i].id_)
        #     data = load_document(self.documents[i].id_)
        #     text_chunks = self.chunk_data(data)
        #     for j, chunk in enumerate(text_chunks):
        #         chunk = str(chunk)
        #         self.chroma_collection.add(
        #             # embeddings=embedding_list
        #             documents=chunk
        #             # , metadatas=metadata_list
        #             , ids=f'doc_{j}')
        #         break
        #     break

        # set up ChromaVectorStore and load in data
        vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
        self.storage_context = StorageContext.from_defaults(vector_store=vector_store)

        # initialise service context with default values
        self.service_context = ServiceContext.from_defaults(embed_model=embed_model,
                                                            chunk_size=1000,
                                                            chunk_overlap=200)
        # self.index = VectorStoreIndex.from_vector_store(vector_store=vector_store,
        #                                                 storage_context=self.storage_context)

    # splitting files in chunks
    # def chunk_data(self, data, chunk_size=1024, chunk_overlap=20):
    #     from langchain.text_splitter import RecursiveCharacterTextSplitter
    #     text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,
    #                                                    chunk_overlap=chunk_overlap)
    #     chunks = text_splitter.split_documents(data)
    #     return chunks

    def save_to_database(self):
        index = VectorStoreIndex.from_documents(
            self.documents,
            storage_context=self.storage_context,
            service_context=self.service_context)
        return index

    def query(self, index, query):
        # Query Data
        query_engine = index.as_query_engine()
        response = query_engine.query(query)
        pprint(response.response)

    def peek_collection(self):
        print(self.chroma_collection.peek())


if __name__ == "__main__":
    # chroma_client = chromadb.Client()
    # collection = ChromaDBHelper()
    # collection.create_collection('sleep_collection')
    fp = r'..\\assets\\AndrewHuberman\\sleep\\'
    name = 'sleep'
    query = "The T55 fleet has accumulated how many hours of operation?"
    collection = ChromaDBVectorizer(fp, name)
    collection.peek_collection()
    index = collection.save_to_database()
    collection.query(index, query)
