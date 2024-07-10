"""
TokenCountingHandler is passed to ServiceContext
"""
import tiktoken
from llama_index import ServiceContext
from llama_index.callbacks import CallbackManager, TokenCountingHandler
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

token_counter = TokenCountingHandler(
    tokenizer = tiktoken.encoding_for_model("text-embedding-ada-002").encode,  # ada IS A embedding model
    verbose = True,
)
callback_manager = CallbackManager([token_counter])
service_context = ServiceContext.from_defaults(callback_manager=callback_manager


try:
    storage_context = StorageContext.from_defaults(persist_dir='storage/sleep')
    index = load_index_from_storage(storage_context)
    print('loading from disk')
except:
    documents = SimpleDirectoryReader('assets/AndrewHuberman/sleep').load_data()
    # index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)  # <<<<<<<<<<
    index.storage_context.persist(persist_dir='storage/sleep/')

# counting tokens when creating an index
print(token_counter.total_embedding_token_count)

# counting tokens when querying
token_counter.reset_counts()
response = index.as_query_engine().query("How does sleep enhance learning memory?")
print('Embedding tokens: ', token_counter.total_embedding_token_count, '\n',
       'LLM prompts: ', token_counter.prompt_llm_token_count, '\n',
       'LLM completitions: ', token_counter.completion_llm_token_count, '\n',
       'Total LLM token count: ', token_counter.total_llm_token_count, '\n',
)
print(response)

