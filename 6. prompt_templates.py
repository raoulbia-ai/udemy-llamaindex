"""adding system prompt to the user prompt
You are ....

This notebook shows how if not prompted to only use the information in the indexed documents,
the LLM will incorporate information ("release of neuromodulators like norepinephrine and serotonin")
that we don't necessarily want.
Prompt engineering helps guiding the LLM model to only provide an answer based on the documents we have mebedded.
"""
import openai
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
from llama_index.prompts import PromptTemplate
from llama_index.response.pprint_utils import pprint_response

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

# openai.log = "debug"

try:
    storage_context = StorageContext.from_defaults(persist_dir='storage/sleep')
    index = load_index_from_storage(storage_context)
    print('loading from disk')
except:
    documents = SimpleDirectoryReader('assets/AndrewHuberman/sleep').load_data()
    # index = VectorStoreIndex.from_documents(documents, show_progress=True)
    index = VectorStoreIndex.from_documents(documents, service_context=service_context)  # <<<<<<<<<<
    index.storage_context.persist(persist_dir='storage/sleep/')

# prompt WITHOUT system prompt
text_qa_template_str_1 = (
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Using both the context information and also using your own knowledge, "
    "answer the question: {query_str}\n"
    "If the context isn't helpful, you can also answer the question on your own.\n"
)

# prompt WITH system prompt
text_qa_template_str_2 = (
    "You are an Andrew huberman assistant that can read Andrew Huberman podcast notes.\n"
    "Always answer the query only using the provided context information, "
    "and not prior knowledge.\n"
    "Some rules to follow:\n"
    "1. Never directly reference the given context in your answer.\n"
    "2. Avoid statements like 'Based on the context, ...' or "
    "'The context information ...' or anything along "
    "those lines."
    "Context information is below.\n"
    "---------------------\n"
    "{context_str}\n"
    "---------------------\n"
    "Answer the question: {query_str}\n"
)

templates = [text_qa_template_str_1, text_qa_template_str_2]
for template in templates:
    text_qa_template = PromptTemplate(template)

    # recall that {context_str} in template refers to the indexed documents
    response = index.as_query_engine(
        text_qa_template = text_qa_template
    ).query("How does sleep enhance learning memory?")

    # print(response)
    pprint_response(response
                    # , show_source=True
                    )
    print()

# # look under the hood
# print(response.source_nodes)
#
# # look under the hood w/pprint
# pprint_response(response, show_source=True)


