"""
By default, VectorStoreIndex uses an in-memory simple vector store as part of the default storage
"""
from llama_index import VectorStoreIndex, SimpleDirectoryReader
from llama_index.response.pprint_utils import pprint_response
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine  # see Advanced 1
from llama_index.indices.postprocessor import SimilarityPostprocessor, KeywordNodePostprocessor  # see Advanced2
from llama_index.response_synthesizers import get_response_synthesizer

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

documents = SimpleDirectoryReader('assets/AndrewHuberman/sleep').load_data()
index = VectorStoreIndex.from_documents(documents, show_progress=True)


def basic_example():
    """Default Setttings"""
    query_engine = index.as_query_engine()
    response = query_engine.query('what can i do to sleep better?')
    pprint_response(response, show_source=True)


def retriever_example():
    """Advanced 1: retriever
    now let's modify retriever to get llamindex to use more than 2 nodes as context for the LLM
    when sending a prompt to OpenAI (default is 2 nodes)
    recall that all of the data retrieved from the index by the retriever is used to generate a response
    """
    retriever = VectorIndexRetriever(index=index, similarity_top_k=4)
    query_engine = RetrieverQueryEngine(retriever=retriever)
    response = query_engine.query('what can i do to sleep better?')
    pprint_response(response, show_source=True)


def node_preprocessor_example():
    """Advanced 2: node preprocessors
    use node postprocessor to set the minimum similarity threshold for all retrieved nodes to e.g. 83%
    """
    retriever = VectorIndexRetriever(index=index, similarity_top_k=4)
    sim_pprocessor = SimilarityPostprocessor(similarity_cutoff=0.83)
    kw_pprocessor = KeywordNodePostprocessor(exclude_keywords=["supplements"])  # note: could also use `include_keywords`
    query_engine = RetrieverQueryEngine(retriever=retriever,
                                        node_postprocessors=[sim_pprocessor, kw_pprocessor])
    response = query_engine.query('what can i do to sleep better?')
    pprint_response(response, show_source=True)


def response_synthesizer_example():
    """Advanced 3: response synthesizer
    check which nodes are retrieved wo/sending anything to the LLM
    - mode `compact` means they can fit within the context window
    - mode `no_text` is great for debugging, nodes will not be sent to the LLM
    """
    retriever = VectorIndexRetriever(index=index, similarity_top_k=4)
    response_synthesizer = get_response_synthesizer(response_mode="no_text")
    query_engine = RetrieverQueryEngine(retriever=retriever,
                                        response_synthesizer=response_synthesizer)
    response = query_engine.query('what can i do to sleep better?')
    pprint_response(response, show_source=True)
    # print(response.source_nodes)  # to view more detailed infor about nodes


if __name__ == "__main__":
    # basic_example()
    # retriever_example()
    # node_preprocessor_example()
    response_synthesizer_example()
