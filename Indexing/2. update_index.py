"""
to only update index for files that have changed you must use filename as node ID
by files that chnaged we meean n
  - ew files being added to a directory of docs that have been index already
  - the content itself
"""
from llama_index import SimpleDirectoryReader
from llama_index.text_splitter import TokenTextSplitter
from llama_index.node_parser import SimpleNodeParser
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.response.pprint_utils import pprint_response

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

try:
    storage_context = StorageContext.from_defaults(persist_dir='storage/sleep')
    index = load_index_from_storage(storage_context)
    print('loading from disk')
except:
    documents = (SimpleDirectoryReader('../assets/AndrewHuberman/sleep',
                                       filename_as_id=True  # << filename will be used as node ID
                                       )
                 .load_data())
    index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index.storage_context.persist(persist_dir='storage/sleep/')

text_splitter = TokenTextSplitter()
node_parser = SimpleNodeParser(text_splitter=text_splitter)
nodes = node_parser.get_nodes_from_documents(documents)
print(nodes)

documents = SimpleDirectoryReader('../assets/AndrewHuberman/sleep', filename_as_id=True).load_data()

index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist(persist_dir='./storage/cache/andrew/sleep')

# this method will compare documents to the current index
# note update_kwargs is optional
# when testing this make sure not to immediately rebuild index afte adding docs
# try thid out first to see this in action
refreshed_docs = index.refresh_ref_docs(documents, 
                                        update_kwargs={"delete_kwargs": {'delete_from_docstore': True}})
print(refreshed_docs)
print('Num of inserted/refreshed documents: ', sum(refreshed_docs))

