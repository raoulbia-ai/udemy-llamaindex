**Word Embeddings**: These are the simplest form of text embeddings, where each word is represented as a dense vector of real numbers. They are useful for tasks that require understanding of individual words but may not capture the context of a sentence or document well.

- **Sentence/Document Embeddings**: These embeddings represent entire sentences or documents as vectors. They are more complex than word embeddings and can capture the overall semantic meaning of a text.

- **Transformer-based Embeddings (Bert, GPT)**: These are advanced embeddings that use transformer models like Bert and GPT. They are capable of understanding the context of words in a sentence and can provide more accurate representations.

- **TF-IDF Embeddings**: These embeddings are based on the frequency of words in a document compared to their frequency in a corpus. They are useful for tasks like information retrieval and document classification.

- **Instructor Embeddings**: These are specialized embeddings that not only capture the textual information, but also consider the instructions or the context under which the text was generated. They are particularly useful for fields like science, medicine, and law where the context can greatly change the meaning of a sentence.

- **Multilingual Embeddings**: These are specialized models like multilingual BERT (mBERT) that can handle text in multiple languages. They are useful for tasks that involve multilingual data.

- **Embed ADA**: This model has a sequence length of over 8000, making it a strong competitor for tasks that require understanding of long texts. However, it is an API and using it involves sending information through this API, which may incur costs.

- **OpenAI Embeddings**: These are the default embeddings used in the Lima Index. They are recommended for most tasks unless there is a need for multilingual support or additional context.

- **Long Chain Embeddings**: These embeddings are also supported by the Lima Index. They are useful for tasks that require understanding of long sequences of text.

The video emphasizes the importance of using the same vector model for both data and search queries to get accurate results. It also highlights the use of methods like cosine similarity for semantic search and the Lima Index, which can work with multiple types of embeddings. The choice of embeddings depends on the specific requirements of the task, such as the need for multilingual support or additional context.