"""
import llama_agents
import os
from pathlib import Path
from llama_index import download_loader, VectorStoreIndex, load_index_from_storage, SummaryIndex
from llama_index.storage.storage_context import StorageContext
import openai

from llama_index.indices.postprocessor import KeywordNodePostprocessor  # to exclude keywords
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.tools import QueryEngineTool, ToolMetadata

# Assuming the use of some functions and classes based on the imports
class RecursiveOpenAIAgent:
    def __init__(self):
        # Initialize components from llama_index
        self.storage_context = StorageContext()
        self.vector_store = VectorStoreIndex()
        self.summary_index = SummaryIndex()
        self.retriever = VectorIndexRetriever()
        self.query_engine = RetrieverQueryEngine()
        self.tool = QueryEngineTool()

        # Initialize OpenAI API (assuming API key is set in environment)
        openai.api_key = os.getenv("OPENAI_API_KEY")

    def download_and_load_indices(self):
        # Code to download and load indices using llama_index functions
        pass

    def process_query(self, query):
        # Code to process a query using llama_index's RetrieverQueryEngine
        pass

    def perform_openai_operations(self, text):
        # Code to interact with OpenAI's API, e.g., text generation or analysis
        pass

    # Additional methods as required for the functionality of the agent

# Main execution
if __name__ == "__main__":
    agent = RecursiveOpenAIAgent()
    # Example usage of the agent's methods

"""
import llama_agents
import os
from pathlib import Path
from llama_index import download_loader, VectorStoreIndex, load_index_from_storage, SummaryIndex
from llama_index.storage.storage_context import StorageContext
import openai

from llama_index.indices.postprocessor import KeywordNodePostprocessor  # to exclude keywords
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.tools import QueryEngineTool, ToolMetadata

from llama_index.agent import OpenAIAgent
from llama_index.llms import OpenAI
from llama_index.response.pprint_utils import pprint_response

openai.api_key = os.getenv('OPENAI_API_KEY')

PDFReader = download_loader("PDFReader")

loader = PDFReader()

class PodcastTitle:
    def __init__(self, name, about, file, key):
        self.name = name
        self.about = about
        self.file = file
        self.key = key

# title: name, about, file, key
podcast_titles = [
    PodcastTitle("10 Tools for Managing Stress and Anxiety with Huberman", "manage stress and anxiety", "behaviour/10_Tools_for_Managing_Stress_&_Anxiety_Huberman_Lab_Podcast_10.pdf", "tools_for_stress"),
    PodcastTitle("The Science of Setting and Achieving Goals with Huberman", "set and achieve goals", "behaviour/55_The_Science_of_Setting_&_Achieving_Goals_Huberman_Lab_Podcast_55.pdf", "setting_goals"),
    PodcastTitle("Dr Chris Palmer Diet and Nutrition for Mental Health with Huberman", "have healthy diet for mental health", "food/99_Dr_Chris_Palmer_Diet_&_Nutrition_for_Mental_Health_Huberman_Lab_Podcast_99.pdf", "diet_nutrition"),
]

podcast_vector_index = {}
podcast_summary_index = {}
for podcast in podcast_titles:
    # try/except to read documents only the first time
    try:
        storage_context = StorageContext.from_defaults(persist_dir=f".\\storage\\cache\\{podcast.key}_vector")
        podcast_vector_index[podcast.key] = load_index_from_storage(storage_context)

        storage_context = StorageContext.from_defaults(persist_dir=f".\\storage\\cache\\{podcast.key}_summary")
        podcast_summary_index[podcast.key] = load_index_from_storage(storage_context)

    except:
        documents = loader.load_data(file=Path(f"..\\assets\\AndrewHuberman\\{podcast.file}"))
        vector_index = VectorStoreIndex.from_documents(documents)

        podcast_vector_index[podcast.key] = VectorStoreIndex.from_documents(documents)
        # now persist it
        vector_index.storage_context.persist(persist_dir=f".\\storage\\cache\\{podcast.key}_vector")

        podcast_summary_index[podcast.key] = SummaryIndex.from_documents(documents)
        # now persist it
        podcast_summary_index[podcast.key].storage_context.persist(persist_dir=f"./storage/cache/{podcast.key}_summary")

# exclude keywords
node_processor = KeywordNodePostprocessor(
    exclude_keywords=["supplements", "LMNT", "InsideTracker", "Helix", "ROKA", "Athletic Greens", "Thesis", "Eight Sleep"]
)

agents = {}
podcats_vector_engines = {}
podcats_summary_engines = {}

for podcast in podcast_titles:
    retriever = VectorIndexRetriever(
        index = podcast_vector_index[podcast.key],
        similarity_top_k=3,
    )

    podcats_vector_engines[podcast.key] = RetrieverQueryEngine(
        retriever = retriever,
        node_postprocessors=[node_processor]
    )

    # make engine: convert the summary index to a query engine
    podcats_summary_engines[podcast.key] = podcast_summary_index[podcast.key].as_query_engine()

    query_engine_tools = []

    # tool for vector index
    new_tool = QueryEngineTool(
        query_engine=podcats_vector_engines[podcast.key],
        metadata = ToolMetadata(
            name=f"{podcast.key}_vector_tool",
            description=f"Useful for retrieving specific context from a podcast {podcast.name}. "
            f"Use when you need information related to {podcast.about}.",
        )

    )
    query_engine_tools.append(new_tool)

    # tool for summary index
    new_tool = QueryEngineTool(
        query_engine=podcats_summary_engines[podcast.key],  # pass in the summary engince as a query engine
        metadata = ToolMetadata(
            name=f"{podcast.key}_summary_tool",
            description=f"Useful for summary of the podcast '{podcast.name}'"
            f"Use when you need overview information about how to {podcast.about}. ",
        )

    )
    query_engine_tools.append(new_tool)

    # now the agent part
    from llama_index.agent import OpenAIAgent
    from llama_index.llms import OpenAI

    agent = OpenAIAgent.from_tools(query_engine_tools,
                                   llm=OpenAI(temperature=0,
                                              model="gpt-3.5-turbo-0613"),
                                   verbose=True)

    # now add it to the list of agents
    agents[podcast.key] = agent


from llama_index.schema import IndexNode

nodes = []
for podcast in podcast_titles:
    podcast_summary = (
        f"This content contains podcast transcript: '{podcast.name}'. "
        f"Use this index if you need to lookup specific information about {podcast.about}.\n"
    )
    node = IndexNode(text = podcast_summary, index_id=podcast.key)
    nodes.append(node)

vector_index = VectorStoreIndex(nodes)
vector_retriever = vector_index.as_retriever(similarity_top_k=1)  # sim == 1 so that retriever will pick only one agent!

from llama_index.retrievers import RecursiveRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.response_synthesizers import get_response_synthesizer

# RecursiveRetriever is especially useful for docs with hierarchical relationships
recursive_retriever = RecursiveRetriever(
    "vector",
    retriever_dict={"vector": vector_retriever},
    query_engine_dict=agents,  # these are all the agents
    verbose=True,
)

# needed for RetrieverQueryEngine
response_syntesizer = get_response_synthesizer(
    response_mode="compact"
)

# this is the final RetrieverQueryEngine
query_engine = RetrieverQueryEngine.from_args(
    recursive_retriever,
    response_synthesizer=response_syntesizer,
)

openai.log = "debug"

# a lot of calls will be made to OpenAI to write a summary
# if i change prompt this to a Q rather than asking for a summary, it will switch as required
response = query_engine.query("Give me a summary of the podcast 'Dr Chris Palmer: Diet and Nutrition for Mental health'")
pprint_response(response)