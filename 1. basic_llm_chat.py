import logging
import sys
import os
import numexpr as ne
from llama_index.llms import OpenAI, ChatMessage

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(), override=True)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

os.environ['NUMEXPR_MAX_THREADS'] = '4'
os.environ['NUMEXPR_NUM_THREADS'] = '2'

llm = OpenAI(temperature=0,
             model="gpt-4",
             max_tokens=250  # this is the output limit!
             )

messages = [
    ChatMessage(role="system", content="Talk like a hippie"),
    ChatMessage(role="user", content="Tell me about AI")

]

response = llm.chat(messages)
print(response.raw)
print('\n-------------\n')
print(response)
