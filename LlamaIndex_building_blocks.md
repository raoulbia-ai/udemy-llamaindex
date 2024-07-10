LlamaIndex generates queryable indexes that can be used for querying, chatting or tools for the agents.

### RAG
Retrieval Augmented generation is basically a pattern that works with pre-trained large language models and your custom data to come up with the best responses.

RAG means that upon getting a prompt, your system searches for relevant information from your data
sources. For example, apps, documents, data sources and APIs to retrieve relevant information for enhanced content that you can then send along with a prompt and query to any LLM. An LLM then generates a response based on the enhanced content and its own data to return a generated text.

And this is what LlamaIndex is doing. LlamaIndex generates queryable indexes that can be used for querying, chatting or tools for the agents.

#### Indexing

LlamaIndex support many index types. LlamaIndex indexes are most useful for synthesizing an answer that combines information across multiple data sources.

The most commonly used index is **vector store index**. They are are the most common and simple to use. They allow answering a query over a large corpus of data.

A **tree index** is useful for summarizing a collection of documents.

And finally, we have a **keyword table index** that is useful for routing queries to a dispatched data
source.


#### embeddings
LlamaIndex can use OpenAI embeddings, longchain embeddings, Azure embeddings or custom embeddings.

#### Service context
Service context is one of the most important classes in LlamaIndex. It's a bundle of commonly used resources used during the indexing and querying stage in retrieval.

Augmented generation is basically a pattern that works with pre-trained large language models
and your custom data to come up with the best responses.

In the service context, you can change the LM prompt helper node parser and callbacks.

LlamaIndex has its own prompts it uses when communicating with an LLM, but you can modify these prompts
with a prompt helper.

You can use service context as a global configuration or just use it as a local configuration at specific parts of the pipeline.


#### Vector Store index
Vector Store index uses an **in-memory** simple vector store that's initialized as part of the default storage context. This is a simple in-memory vector store that is great for quick experimentation, but LlamaIndex supports different vector stores.

Vector store options include Pinecone, Weaviate and Chroma.

#### Query Engines
LlamaIndex has several types of query engines from 

* Graph Query Engine
* Multi-step Query Engine Retriever
* Query Engine Transform
* Query Engine Router
* Query Engine Retriever
* Route Query Engine and many more.

Each of them serves a different use cases.

Query engines can be configured and these configurations include 

* retrievers
* node post-processor and
* response synthesizers

Depending on the type of the query engine, you can also have parameters like 

* transformers response modes
* selectors
* service contexts
* SQL query tools

for more see `ContextChatEngine` vs `ReactChatEngine`

<br>

#### React

React is a paradigm combining reasoning and acting capabilities in language models.

This means the model can think, reason and then act based on the reasoning.

React Chat Engine is basically an agent-based chat mode built on top of a query engine over your data for each chat interaction. The agent enters a react loop. It first decides whether to use query engine tool and come up with the appropriate input. Then it optionally uses the query engine tool and observes its inputs, and then it decides whether to repeat or give a final response.

This approach is flexible since it can choose between querying the knowledge base. However, the performance is more dependent on the quality of the LLM. The openai cheat engine uses OpenAIAgent under the hood.

The condensed question mode is a simple chat mode built on top of query engine over your data. For each chat interaction, it first generates a standalone question from conversation, context and last message, and then it
queries the query engine with a condensed question for the response.

This works for questions directly related to the knowledge base. Since it always queries the knowledge base, it can have difficulty answering meta questions like What did I ask you before?

<br>

#### Retrievers

But if we go back to query engines, one thing that is important is **smart retrieval of relevant data**.
Here is where retrievers come into place.

A retrievers job is to efficiently retrieve relevant contacts from an index when given a query. Retrievers are responsible for fetching the most relevant notes. Retrievers can be used independently from a query engine when you want to fetch the most relevant context given the user query without needing the full pipeline. **This can be useful in a scenario where you need to retrieve relevant information and don't require response generation components**.

So you need to remember that the retriever is the key in query engines and chat engines for retrieving
relevant context. The specific retrieval logic differs for different indices. The most popular is **dense retrieval against a vector index**. Retrieved nodes are then passed to the language model along with a query to synthesize a response. 

An index can have different index-specific retrieval modes. For example, 

* a list index supports the default retrieval retrieves all the nodes
* list index embedding retrieval retrieves the top K nodes for embedding similarity

After a retriever fetches relevant nodes, a response synthesizer synthesizes the final response by combining the information.ost

In some cases you want to filter or rerank the retrieved nodes. In this case, **node postprocessor** steps in. A node postprocessor takes a set of nodes and applies transformation. For example, it filters the nodes or re-ranks them.

Node postprocessors are applied after the retrieval and before the response synthesizes step.

Llamaindex offers several node post-processors e.g.

* a similarity postprocessor which can remove nodes that are below a similarity score threshold
* a keyword node postprocessor can either include or include keywords metadata  replacement Postprocessor replaces the nodes content with a field from the node metadata.
* a sentence embedding optimizer removes all the sentences that are not relevant to the query, which helps with lowering the cost.

There are also others available, but you can also create a custom post-processor.

In the next step of the querying, a response synthesizer generates a response from using a user query and a given set of nodes from the previous step. The output of the response synthesizer is a response object. This is what you get as a returned value response. Synthesis can be done in many ways from simply iterating over all text chunks to as complex as building a tree. The main idea is to simplify the process.

Response synthesizers are typically specified through a response mode settings. The response synthesizer settings that are already implemented in Llamaindex include

* the refine mode that goes through each retrieved text chunk and makes a separate call per note
* the compact mode, which is the default mode, is similar to refine, but the chunks are concatenated and packed so they fit within the context window which results in a fewer calls.
* the summarize mode will query the LM as many times as needed so that all the concatenated chunks have been queried. These answers are then again recursively used as chunks in LM calls and so on, until there's only one
chunk left, which becomes the final answer. The tree summarization still can create a lot of calls, so you need to be mindful of token usage. 
* the simple summarize is cheaper. It truncates all the chunks to fit into a single prompt, which is still good for quick summarization, but you may lose data due to truncation.
* no text mode for debugging. This will only retrieve the fetched nodes and will and will not send them to the LM. They can be expected by checking the response dot resource nodes and then accumulate.
* the accumulate mode takes a collection of text nodes and a query. It processes the query for each node and gathers the results in the array. The final response is a single string that combines all the individual responses. It's ideal when you need to run the same query separately against each text chunk.
*Compact accumulate is, as the name suggests, similar to accumulate, but it will compact each prompt like in the compact mode and run the same query against each text chunk.


So to recap, this is how the query pipeline goes: Retrievers retrieve relevant nodes, node postprocessor apply transformations if needed, and response synthesizer construct the final response with the help of LM.

<br>

#### Routers

Index routers are versatile modules that use decision making and can be used for selecting data sources,
choosing different query engines or different retrievers or combining multiple choices. They provide flexibility and power in routing your queries to the appropriate tools or data sources.

Routers are modules that take in a user query and a set of choices and return one or more selected choices. They can be used as a standalone module or as a part of a query engine or a retriever.

There are two types of core router modules: selectors and pedantic selectors.

Selectors use LLMs to make decisions by putting the choices as a text dump into a prompt. Pedantic selectors pass choices as pedantic schemas into function, calling an endpoint and return pedantic objects.

To use routers as a query engine, you can use the router query engine module. It allows you to define query engines and initialize tools for different purposes. For example, you can define a list of query engines for summarization questions and a vector query engine for retrieving specific context. You can then initialize router query engine with a selector and the query engine tools and use it to query a user query.

Another example is the SQL Router Query engine which can route to an SQL or a vector database.

Note that the ddocumentation can be confusing. You can see many examples in the index documentation that might seem the same at first glance. For example, a SQL Router Query Engine and SQL Outer Vector Query engine. You can see that they both route between SQL and a vector query engine. They are basically the same, but the SQL router can be combined with as many indexes as you want while the  SQL outer vector router only WITH two indexes. But in general, though, the SQL outer vector is also slightly deprecated. A more flexible version is a SQL join query engine. It is more optimized for SQL.

#### Query Engine Tools.

Query Engine tools are used within routers. The query engine tool is a class representing a query engine and its metadata. It helps routers to easily switch between query engine and access relevant information.


#### Chat Engines

Basically, it's a Q&A, but with a memory of the previous interaction.

#### Agents

An agent is an automated decision maker that uses various tools. While it can function similarly to query or chat engines, it can determine the optimal sequence of actions on-the-fly instead of following a predetermined logic. This gives it additional flexibility to solve more complex tasks.

They are capable of performing automated searches and fetch data across various formats. They can also call any external services APIs, process their feedback and preserve it for future reference. They can also store conversation history.

Agents are a step beyond llamaindex query engines, as they can not only read from static sources of data, but can dynamically ingest and modify data from a variety of different tools.

Building a data agent requires 
* na reasoning loop and 
* tool abstractions

So given a task, the data agent will use a reasoning loop to decide which tool to use. The reasoning loop depends on the type of the agent Lemma index supports.

OpenAI function agents that are built on top of the OpenAI function API and it supports the React agents.
Having proper tool abstraction is the core of building data agents. You can find many tools in the LlamaHub,  from Azure Bing Search, CatchGPT Plugins, Database, Gmail, Slack, Zapier and many more are being added to the list.