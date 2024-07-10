#### About Indexing 

- By default, VectorStoreIndex uses an in-memory simple vector store as part of the default storage
- when changing embedding model
  Just remember to recreate the index as different models have unique vector sizes and embedding methods.
- In llamaindex, embedding models are usually specified in the ServiceContext object and used in a vector index
- **ServiceContext** is your go to toolbox in llama index where you can tweak the prompt helper note parser and callbacks.
  You can use service context as a global configuration or local configuration at specific parts of the pipeline.
- Many vector stores will store both the data as well as the embeddings.
  This means you will not need to use separate document or index store.
  LlamaIndex simplifies storage and provides a high level interface.
  The storage context in LlamaIndex is a utility container that store nodes, indices and vectors that
  provides a high level interface for customizing the storage of these components.
  The storage context allows you to customize where these components are stored by using different implementations
  of document stores and vector stores.
  It provides a common abstraction for interacting with all the storage components.