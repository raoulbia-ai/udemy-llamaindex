### Refining prompts with user and system role propmpt

When you want to change both system and user prompts to an LLM query, you can use the following code:

````
from llama_index.prompts import ChatPromptTemplate, ChatMessage, MessageRole
 
message_templates = [
    ChatMessage(content="You are a breathing exercises specialist. You are writing a 
book about breathing exercises. You aim to speak in a clear and easy to understand language. Your tone is profesional and friendly.", role=MessageRole.SYSTEM),
    ChatMessage(
        content=(
            "Context information is below.\n"
            "---------------------\n"
            "{context_str}\n"
            "---------------------\n"
            "Given the context information and your prior knowledge, "
            "write a part of the book that will answer the question: {query_str}\n"
        ),
        role=MessageRole.USER,
    ),
]
text_qa_template = ChatPromptTemplate(message_templates=message_templates)
 
index.as_query_engine(text_qa_template=text_qa_template).query("How do breathing exercises effect immune system?")
````

<br>

Prompt template can also be passed when you are creating a query engine at a lower level:

````
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.response_synthesizers import get_response_synthesizer
 
response_synthesizer = get_response_synthesizer(
	text_qa_template=text_qa_template, 
)
query_engine = RetrieverQueryEngine(
	response_synthesizer=response_synthesizer,
	retriever=retriever,
)
````
