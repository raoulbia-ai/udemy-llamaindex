import llama_agents
import os
from pathlib import Path
from llama_index import download_loader, VectorStoreIndex, load_index_from_storage
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
for podcast in podcast_titles:
    # try/except to read documents only the first time
    try:
        storage_context = StorageContext.from_defaults(persist_dir=f".\\storage\\cache\\{podcast.key}_vector")
        podcast_vector_index[podcast.key] = load_index_from_storage(storage_context)
    except:
        documents = loader.load_data(file=Path(f"..\\assets\\AndrewHuberman\\{podcast.file}"))
        vector_index = VectorStoreIndex.from_documents(documents)
        podcast_vector_index[podcast.key] = vector_index
        vector_index.storage_context.persist(persist_dir=f".\\storage\\cache\\{podcast.key}_vector")

# exclude keywords
node_processor = KeywordNodePostprocessor(
    exclude_keywords=["supplements", "LMNT", "InsideTracker", "Helix", "ROKA", "Athletic Greens", "Thesis", "Eight Sleep"]
)

query_engine_tools = []
podcats_vector_engines = {}

# retirever > engines > tools
# VectorIndexRetriever > RetrieverQueryEngine > QueryEngineTool
for podcast in podcast_titles:
    retriever = VectorIndexRetriever(
        index = podcast_vector_index[podcast.key],
        similarity_top_k=3,  # number of similar documents to return to the LLM
    )

    podcats_vector_engines[podcast.key] = RetrieverQueryEngine(
        retriever = retriever,
        node_postprocessors=[node_processor]  # used to filter the reurned nodes
    )

    new_tool = QueryEngineTool(
        query_engine=podcats_vector_engines[podcast.key],
        metadata = ToolMetadata(
            name=f"{podcast.key}_vector_tool",
            description=f"Useful for retrieving specific context from a podcast {podcast.name}. "
            f"Use when you need information related to {podcast.about}.",
        )

    )
    query_engine_tools.append(new_tool)

agent = OpenAIAgent.from_tools(query_engine_tools,
                               llm=OpenAI(temperature=0,
                                          model="gpt-4"),  # gpt-3.5-turbo-0613
                               verbose=True)

openai.log = "debug"
response = agent.chat("Tell me about Ketogenic diet")
# print(response.sources)
pprint_response(response)