#### A note on evaluating LLM's

LMS vary widely in their properties and functionalities.

Evaluating the performance of large language models is a critical aspect of their adaptation, with
different models that are suited for different tasks.

How do you choose the right one? Evaluation involves multidimensional assessments. Understanding tools, frameworks and leaderboards help guide the assessment, ensuring that the selected models align with the specific needs and objectives.

#### GPT-4
GPT-4's deep understanding of complex reasoning, coding abilities and human level performance has
made it the first on the list. It can both process text and images. GPT four is a huge leap forward in maintaining factual accuracy.

#### Lama2
Lama2 is a second generation open source large language model from Meta.

Lama2 models generally perform better than existing open source models and are close behind closed source models like ChatGPT.

#### Orca
Orca is an LLM developed by Microsoft. It is based on llama with fine tuning on complex explanation traces obtained from GPT-4. It has 13 billion parameters and it's designed to run on a laptop.


#### Claude2 from Anthropic
Is a next generation assistant based on anthropic research into training helpful, honest and harmless AI systems. Substantially outperforms GPT-4 in accurately generating, comprehending and explaining code snippets. It offers advanced coding intelligence. 

Claude is unfortunately not available in Europe at this time.


### LaMDA.
LaMDA was developed by Google brain and is a family of LMS became famous last year for its unique architecture.

#### Palm
Google also developed Palm to Palm to carves out a unique niche, focusing on common sense reasoning,
formal logic and mathematics and coding in over 20 languages.

Its performance in reasoning, evaluations and multilingual capabilities make it a standout model.

#### OpenAI Codex
OpenAI Codex is a specialized model for programming, writing and data analysis. OpenAI Codex is known for its proficiency and multiple programming languages. Its partnership with GitHub for GitHub Copilot has demonstrated its potential as a next generation coding assistant.

#### Cohere
Cohere was founded by former Google brain team members. It targets enterprise customers with a range of models varying in size and specialization. Known for accuracy and robustness, coherence models are leveraged by corporations like Spotify, Jasper and Hyper.

#### Alpaca
Stanford's Alpaca aims to facilitate customer chat bots that function locally. It's a powerful tool for conversing, writing and analyzing code. 

#### Gopher
Deepmind's Gopher is a versatile model that shines in the fields like math, science, technology, humanities and medicine. Its ability to simplify complex subjects makes it valuable tool for various tasks. 

#### BERT
Bert was introduced by Google in 2018. Bert is a transformer based model with 342 million parameters.
It played a key role in improving Google Search in 2019.


#### LLM leaderboard

A leaderboard ranks large language models using specific metrics.

Leaderboards provide a standardized way to compare and evaluate different large language models.
By using metrics, you can understand how well a model performs in comparison to others.

Some leaderboards are a joint community effort, encouraging collaboration and contribution.
This fosters an open and transparent environment where models can be openly compared and discussed.
The leaderboards are often updated with the new models and metrics allowing the community to track
the progress of large language models over time. This can help in identifying trends and enhancements in the field.

By understanding where a model ranks on the leaderboard, developers can identify areas for improvement
and focus on enhancing specific aspects of their models.

There are different platforms and communities that host leaderboards.

* https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard
* https://llm-leaderboard.streamlit.app/
* https://weightwatcher.ai/leaderboard.html


#### Leaderboard benchmarks

* HelllaSwag is a benchmark designed to evaluate a model's common sense reasoning. It presents scenarios and requires the model to predict or complete sentence logically. The challenges lies in understanding the context and applying common sense to select the most appropriate ending. HelllaSwag is basically a challenging dataset for evaluating common sense that it's especially hard for
the state of art models.

  Example: 
  
  Scenario, a person puts a turkey into a oven competition option.
  The turkey cooks. And the second one, the turkey goes for a walk and needs to select the correct answer

* Lambada is a language modeling benchmark that tests the ability of a model to predict the final
word of a sentence, given the entire sentence except for the last word. It's designed to evaluate the model's understanding of a broader context and long range dependencies within a text. So the model's assignment is to recover the last word of the sentence.

  Example:
  
  She opened the door and found a big surprise waiting for her. A ...

* Massice Multitask Language Understanding (MMLU) is a multiple choice question test that evaluates a model across 57 general knowledge domains grouped into categories like humanities, social sciences and Stem. It assesses the model's ability to understand various subjects and select the correct answers from a given options. It is a new benchmark designed to measure knowledge acquired during Pre-training.

* AI2 Reasoning Challenge (Arc) consists of a grade school level. Multiple choice science Questions is designed to evaluate a model's ability to reason and answer questions that require an understanding of scientific concepts.

* TruthfulQA is a benchmark that focuses on evaluating the truthfulness of a model's responses. It presents questions and requires the model to generate answers that are not only relevant but also
accurate.
