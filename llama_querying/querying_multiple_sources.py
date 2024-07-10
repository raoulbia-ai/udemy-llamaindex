"""
when querying multiple sources, use a subquery engine
pip install youtube_transcript_api
"""
import os
import openai  # for api keu
import llama_querying
from llama_hub.youtube_transcript import YoutubeTranscriptReader
from llama_index import VectorStoreIndex
from llama_index.query_engine import SubQuestionQueryEngine
from llama_index.tools import QueryEngineTool, ToolMetadata
from llama_index.response.pprint_utils import pprint_response

openai.api_key = os.getenv('OPENAI_API_KEY')

loader=YoutubeTranscriptReader()

youtube_documents = loader.load_data(ytlinks=['https://www.youtube.com/watch?v=jITPOcBQQW8', 'https://www.youtube.com/watch?v=xFfnJhZeL_Y', 'https://www.youtube.com/watch?v=g_LNu6Aaxvk'])
print(youtube_documents)

vector_indices = {}
vector_query_engines = {}

breeds = ["Savanah", "Ragdol", "Maine Coon"]

for breed, youtube in zip(breeds, youtube_documents):
    vector_index = VectorStoreIndex.from_documents([youtube])
    query_engine = vector_index.as_query_engine(similarity_top_k=3)
    vector_indices[breed] = vector_index
    vector_query_engines[breed] = query_engine

query_engine_tools = []
for breed in breeds:
    query_engine = vector_query_engines[breed]

    query_engine_tool = QueryEngineTool(
        query_engine=query_engine,
        metadata=ToolMetadata(
            name=breed,
            description=f"Provides information about the cat breed {breed}"
        ),
    )
    query_engine_tools.append(query_engine_tool)

subquestion_engine = SubQuestionQueryEngine.from_defaults(query_engine_tools=query_engine_tools)

response = subquestion_engine.query("Tell me the difference between Ragdoll and Maine Coon cat.")

pprint_response(response)