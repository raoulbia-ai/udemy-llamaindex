"""
https://github.com/nlmatics/llmsherpa#layoutpdfreader
https://blog.llamaindex.ai/mastering-pdfs-extracting-sections-headings-paragraphs-and-tables-with-cutting-edge-parser-faea18870125

adding custom metadata to embbeded node (aka chunks) to give more context to the LLM
"""
import json
from llama_index import SimpleDirectoryReader
from llmsherpa.readers import LayoutPDFReader
from llama_index.llms import OpenAI
from llama_index.readers.schema.base import Document
from llama_index import VectorStoreIndex
# from IPython.core.display import display, HTML

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

# docs = SimpleDirectoryReader(input_files=[r'..\assets\pdf\climate\'])

llmsherpa_api_url = "https://readers.llmsherpa.com/api/document/developer/parseDocument?renderFormat=all"
pdf_url = r'..\assets\pdf\climate\Helsinki_Action_Plan.pdf'
pdf_reader = LayoutPDFReader(llmsherpa_api_url)
doc = pdf_reader.read_pdf(pdf_url)
print(len(doc.sections()))

# Convert to human-readable format with indentation
# pretty_json = json.dumps(doc.json, indent=2)
# print(pretty_json)

# parse json and create a txt document
# document = ""
# for block in doc.json:
#     if block['tag'] == 'header':
#         document += "\n" + " " * block['level'] * 2 + block['sentences'][0] + "\n"
#     elif block['tag'] == 'para':
#         for sentence in block['sentences']:
#             document += " " * block['level'] * 2 + sentence + "\n"
# print(document)

# selected_section = None
# for section in doc.sections():
#     # if section.title == '3 Fine-tuning BART':
#     selected_section = section
#     context = selected_section.to_html(include_children=True, recurse=True)
#     question = "give me the header of this section and summarise this section"
#     resp = OpenAI().complete(f"read this text and answer question: {question}:\n{context}")
#     print(resp.text)
#     break

index = VectorStoreIndex([])
for chunk in doc.chunks():
    index.insert(Document(text=chunk.to_context_text(), extra_info={}))
query_engine = index.as_query_engine()

# Let's run one query
response = query_engine.query("Which city is the subject of this document?")
print(response)
