"""
adding custom metadata to embbeded node (aka chunks) to give more context to the LLM

Chunking data from documents to nodes is done with node parsers.
You can set the chunk size in tokens and even the overlap between chunk nodes using TokenTextSplitter.

Documents can be quite complex.
Think of financial reports or documentation with many tables, code snippets and structures.
So the process needs to be customizable so we don't lose any information in the process of indexing

When you split documents into notes, you can split them by size, or you can write a custom splitter.
Custom splitter is handy when you have a complex data with tables, graphs, markdown code and more.
When you have a simple text like we have in our case of podcast transcripts, we can simply split them
by size.

But what is important is that you can add custom metadata to each note to give it more meaning and give
more context to the LM.
"""
import random
from llama_index import SimpleDirectoryReader
from llama_index.node_parser.extractors import (
    MetadataExtractor,
    QuestionsAnsweredExtractor,
    TitleExtractor
)
from llama_index.text_splitter import TokenTextSplitter
from llama_index.node_parser import SimpleNodeParser
from llama_index import ServiceContext, VectorStoreIndex
from llama_index.response.pprint_utils import pprint_response

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

# TODO it seems we have to read an actual doc rather than a directory!?
path = (r'..\assets\AndrewHuberman\sleep\115_Dr_Gina_Poe_Use_Sleep_to_Enhance_Learning_Memory_'
        r'&_Emotional_State_Huberman_Lab_Podcast.txt')
docs = SimpleDirectoryReader(input_files=[path]).load_data()
print(len(docs))

text_splitter = TokenTextSplitter(separator=" ",
                                  chunk_size=512,
                                  chunk_overlap=20)

metadata_extractor = MetadataExtractor(extractors=[TitleExtractor(nodes=5),
                                                   QuestionsAnsweredExtractor(questions=3)])

node_parser = SimpleNodeParser(text_splitter = text_splitter,
                               metadata_extractor=metadata_extractor)

nodes = node_parser.get_nodes_from_documents(docs)
print(len(nodes))
print(nodes[1].metadata)

sample_nodes = random.sample(nodes, 5)
for node in sample_gina_nodes:
    print(node.metadata)

# now lwt's add this metadat to our index
# recall, ServiceContext is where we configure which node parser should be used when creating an index.
# here we'll setup ServiceCOntext to include the Q's we got from node parser
# that ServiceContext will then be integrated as part of the vecor store embedding of the doc(s)
service_context = ServiceContext.from_defaults(node_parser=node_parser)
index = VectorStoreIndex.from_documents(docs,
                                        service_context=service_context)

response = index.as_query_engine().query("""
                                        How does consistent bedtime contribute to good neurological 
                                        health as we age?
                                        """)
pprint_response(response, show_source=True)
print(response.source_nodes)


