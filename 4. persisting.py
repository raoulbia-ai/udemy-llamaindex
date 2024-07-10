"""
purpose: not to have to recreate the index each time you issue a query
"""
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(), override=True)

try:
    storage_context = StorageContext.from_defaults(persist_dir='storage/sleep')
    index = load_index_from_storage(storage_context)
    print('loading from disk')
except:
    documents = SimpleDirectoryReader('assets/AndrewHuberman/sleep').load_data()
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index.storage_context.persist(persist_dir='storage/sleep/')


if __name__ == "__main__":
    pass
