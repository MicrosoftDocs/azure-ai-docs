---
title: Azure AI Search transparency note
titleSuffix: Azure AI Search
description: Azure AI Search basics, use cases, and terms
author: haileytap
ms.author: haileytapia
manager: nitinme
ms.service: azure-ai-search
ms.topic: concept-article
ms.date: 05/16/2025
---

# Transparency note: Azure AI Search

[!INCLUDE [non-english-translation](../includes/non-english-translation.md)]

## What is a Transparency Note?

An AI system includes not only the technology, but also the people who will use it, the people who will be affected by it, and the environment in which it is deployed. Creating a system that is fit for its intended purpose requires an understanding of how technology works, what its capabilities and limitations are, and how to achieve the best performance. Microsoft's Transparency Notes are intended to help you understand how our AI technology works, the choices system owners can make that influence system performance and behavior, and the importance of thinking about the whole system, including the technology, the people, and the environment. You can use Transparency Notes when developing or deploying your own system or share them with the people who will use or be affected by your system. 


Microsoft's Transparency Notes are part of a broader effort at Microsoft to put our AI Principles into practice. To find out more, see the [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai).

## The basics of Azure AI Search

### Introduction

Azure AI Search gives developers tools, APIs, and SDKs for building a rich search experience over private, heterogeneous content in web, mobile, and enterprise applications. Search is foundational to any application that surfaces data to users. Common scenarios include catalog or document search, online retail stores, or data exploration over proprietary content. 

Searchable data can be in the form of text or vectors and ingested as-is from a data source or enriched by using AI to improve the overall search experience. Developers can convert data int into numerical representations  (called vectors), by choosing to call an external machine learning models (known as embedding models). Indexers can optionally include skill sets that support a powerful suite of data enrichment via several [Azure Language in Foundry Tools](/azure/ai-services/language-service/overview) capabilities, such as [Named Entity Recognition (NER)](/azure/ai-services/language-service/named-entity-recognition/overview) and [personally identifiable information (PII) detection](/azure/ai-services/language-service/personally-identifiable-information/overview), and [Azure Vision in Foundry Tools](/azure/ai-services/computer-vision/overview) capabilities, including [optical character recognition (OCR)](/azure/ai-services/computer-vision/overview-ocr) and [image analysis](/azure/ai-services/computer-vision/overview-image-analysis).

See the following tabs for more information about how Azure AI Search improves the search experience by using Foundry Tools or other AI systems to better understand the intent, semantics, and implied structure of a customer's content. 

#### [AI enrichment](#tab/enrichment)

[AI enrichment](/azure/search/cognitive-search-concept-intro) is the application of machine learning models from Foundry Tools over content that is not easily searchable in its raw form. Through enrichment, analysis and inference are used to create searchable content and structure where none previously existed.

AI enrichment is an optional extension of the Azure AI Search indexer pipeline that connects to Foundry Tools in the same region as a customer's search service. An enrichment pipeline has the same core components as a typical indexer (indexer, data source, index), plus a skill set that specifies the atomic enrichment steps. A skill set can be assembled by using built-in skills based on the Foundry Tools APIs, such as [Vision](/azure/ai-services/computer-vision/overview-image-analysis) and [Language](/azure/ai-services/language-service/overview), or [custom skills](/azure/search/cognitive-search-create-custom-skill-example) that run external code that you provide.

#### [Vector search](#tab/vector)

Vector search is a method of information retrieval where documents and queries are represented in an index as vectors instead of plain text. In vector search, machine learning models, hosted externally from Azure AI Search, generate the vector representations of source inputs, which can be text, images, audio, or video content. This mathematical and normalized representation of content, called vector embeddings, provides a common basis for search scenarios.

When everything is a vector, a query can find a match in vector space, even if the associated original content is in a different media type, such as images versus text, or language than the query. The search engine scans the index looking for vector content that is most similar, that is, the closest, to the vector in the query. Matching on a mathematical vector representation instead of keywords makes it far more likely to find matches that share semantic meaning but are textually distinct, such as "car" and "auto," for example. This gives a more detailed introduction to vector embeddings and how the similarity algorithm works.



### Key terms

| **Term** | **Definition** |
| --- | --- |
| [Vector embeddings](/azure/search/vector-search-overview#embeddings-and-vectorization) | A highly optimized way to represent data that reflects meaning and understanding extracted by a machine learning model from images, audio, video, or text. Content is converted to vector embeddings both at indexing and query time. Vector search amounts to taking embeddings provided in a query and looking for the most similar embeddings in the index. Results are then typically sorted by the degree of similarity. |
| [Embedding space](/azure/search/vector-search-overview#what-is-the-embedding-space) | All vectors in the corpus for a single field occupy the same embedding space where similar items are located close to each other, and dissimilar items are farther apart. Higher dimensionality of the embedding space can include more information in a single vector and greatly improve the search experience, but at significant cost of index storage size and higher query latency. |

#### [Semantic ranker](#tab/ranker)

Semantic ranker uses the context or semantic meaning of a query to compute a new relevance score that promotes results that are semantically closest to the intent of the original query to the top. The initial result set can come from a keyword search with [BM25](/azure/search/index-similarity-and-scoring) ranking, [vector](/azure/search/vector-search-ranking#vector-similarity) search, or a [hybrid search](/azure/search/vector-search-ranking#hybrid-search) that includes both. It also creates and returns "captions" by extracting verbatim content found in the result and "highlights" to call attention to important content within the result. It can also return an "answer" if the query has the characteristics of a question ("what is the freezing point of water") and the result contains text having the characteristics of an answer ("water freezes at 0°C or 32°F").

### Key terms

| **Term** | **Definition** |
| --- | --- |
| [Semantic ranker](/azure/search/semantic-ranking) | Uses the context and semantic meaning of a query to improve search relevance by using language understanding to re-rank search results. |
| [Semantic captions and highlights](/azure/search/semantic-how-to-query-request) | Extracts sentences and phrases from a document that best summarize the content, with highlights over key passages for easy scanning. Captions that summarize a result are useful when individual content fields are too dense for the results page. Highlighted text elevates the most relevant terms and phrases so that users can quickly determine why a match was considered relevant. |
| [Semantic answers](/azure/search/semantic-answers) | Provides an optional and additional substructure returned from a semantic query. It provides a direct answer to a query that looks like a question. It requires that a document has text with the characteristics of an answer. |

#### [Query rewriting](#tab/query)

Query rewriting creates synthetic queries, which are queries that are artificially created or generated from actual customer input to improve the recall (the fraction of relevant documents retrieved out of the total number available documents) of [BM25 ranking](/azure/search/index-similarity-and-scoring), [vector search](/azure/search/vector-search-ranking#vector-similarity), or a [hybrid search](/azure/search/vector-search-ranking#hybrid-search). The original query is combined with the synthetic queries to provide optimal recall from the search engine. 


#### [GenAI Prompt skill](#tab/genai)

The GenAI Prompt skill is part of Azure AI Search's catalog of skills, enabling customers to enhance their search indexes with AI-generated content based on their data. By using the customer’s organization’s own data and preferences, this skill helps produce tailored summaries, answers, or insights that align with their specific needs.

This means when the end user searches the customers’ content via AI Search, the AI-generated content can provide more informative and context-aware results, making it easier for users to find the information they're looking for. 

### Key terms

| **Term** | **Definition** |
| --- | --- |
| Skills | An Azure AI Search skill is a modular processing component within the Azure AI Search enrichment pipeline. These skills apply AI-driven transformations to raw content—such as text, images, or documents—during indexing, enabling the extraction of structured, searchable information from unstructured data.  |
|Prompt | The text you send to the service in the API call. This text is then input into the model. For example, one might input the following prompt:<br><br> Convert the questions to a command: <br>Q: Ask Constance if we need some bread <b>A: send-msg `find constance` Do we need some bread? <br>Q: Send a message to Greg to figure out if things are ready for Wednesday.<br>A: Send-msg `find greg` all ready for Wednesday? |
|Search Indexes | In Azure AI Search, an index is the data structure that holds your searchable content, defines how it’s stored, and controls how the service will interpret it when you run a query. |

#### [Agentic retrieval](#tab/ar)

Agentic retrieval is a parallel query processing architecture that uses a conversational large language model (LLM) as a "query planner." The LLM turns a user’s conversation history into one or several focused subqueries, as needed. These subqueries run simultaneously on your Azure AI Search index, and the service merges the top results, returning:
- A single content string that contains the most relevant passages (grounding data). 
- A references array (optional) that exposes the full source documents or chunks. 
- An activity array that lists every operation, token count, and latency to aid cost tracking and debugging. 

### Key terms

| **Term** | **Definition** |
| --- | --- |
|
Agentic retrieval |This refers to an AI agent planning and executing a sequence of steps to retrieve information from grounding sources. This involves activities such as querying and refining searches to obtain the most relevant information for the query. |
|Grounding data |Set of documents/information returned by Agentic Retrieval. Serves as the factual basis that an external LLM can cite or transform into a natural‑language answer, ensuring traceability and reducing hallucination risk. |
|Query planner |Breaks down conversational history into subqueries to find the most relevant grounding data for the underlying search query. |
|Subquery |A single query generated by an LLM. Subqueries are based on user questions, chat history, and parameters on the request. The subqueries target your indexed documents (plain text and vectors) in Azure AI Search. |


---

## Capabilities

#### [AI enrichment](#tab/enrichment)

### System behavior

Several [built-in skills](/azure/search/cognitive-search-predefined-skills) for AI enrichment in Azure AI Search take advantage of Foundry Tools. See the Transparency Notes for each built-in skill linked below for considerations when choosing to use a skill:

- Key Phrase Extraction Skill: [Language - Key Phrase Extraction](/azure/ai-foundry/responsible-ai/language-service/transparency-note-key-phrase-extraction)
- Language Detection Skill: [Language - Language Detection](/azure/ai-foundry/responsible-ai/language-service/transparency-note-language-detection)
- Entity Linking Skill: [Language - Entity Linking](/azure/ai-foundry/responsible-ai/language-service/guidance-integration-responsible-use)
- Entity Recognition Skill: [Language - Named Entity Recognition (NER)](/azure/ai-foundry/responsible-ai/language-service/transparency-note-named-entity-recognition)
- PII Detection Skill: [Language - PII Detection](/azure/ai-foundry/responsible-ai/language-service/transparency-note-personally-identifiable-information)
- Sentiment Skill: [Language - Sentiment Analysis](/azure/ai-foundry/responsible-ai/language-service/transparency-note-sentiment-analysis)
- Image Analysis Skill: [Vision - Image Analysis](/azure/ai-foundry/responsible-ai/computer-vision/image-analysis-transparency-note)
- OCR Skill: [Vision - OCR](/azure/ai-foundry/responsible-ai/computer-vision/ocr-transparency-note)
- Document Layout Skill: [Document Intelligence](/azure/ai-foundry/responsible-ai/document-intelligence/transparency-note)

See the documentation for each skill to learn more about their respective capabilities, limitations, performance, evaluations, and methods for integration and responsible use. Note that using these skills in combination may lead to compounding effects (for example, errors introduced when using OCR will carry through when using key phrase extraction).

### Use cases

#### Example use cases

Because Azure AI Search is a full text search solution, the purpose of AI enrichment is to improve the search utility of unstructured content. Here are some examples of content enrichment scenarios supported by the built-in skills:

- **Translation** and **language detection** enable multilingual search.
- **Entity recognition** extracts **people** , **places** , and **other entities** from large chunks of text.
- **Key phrase extraction** identifies and then outputs important terms.
- **OCR** recognizes printed and handwritten text in binary files.
- **Image analysis** describes image content and outputs the descriptions as searchable text fields.
- **Integrated vectorization** is a preview feature that calls the Azure OpenAI embeddings model to vectorize data and store embeddings in Azure AI Search for similarity search.


#### [Vector search](#tab/vector)

### System behavior

In vector search, the search engine looks for vectors within the embedding space in the index to find those close to the query vector. This technique is called [nearest neighbor search](/azure/search/vector-search-overview#nearest-neighbors-search). This also helps quantify the degree of similarity, or distance, between items. A high degree of vector similarity indicates that the original data was similar too. The two vector search algorithms supported by Azure AI Search have different approaches to this problem, trading off different characteristics such as latency, throughput, recall, and memory.

Finding the true set of "k" nearest neighbors requires comparing the input vector exhaustively against all vectors in the dataset. While each vector similarity calculation is relatively fast, performing these exhaustive comparisons across large datasets is computationally expensive and slow because of the sheer number of comparisons that are required. Also, the higher the dimensionality of each vector, the more complex and slower the calculations on each vector will be.

To address this challenge, approximate nearest neighbor (ANN) search methods are used to trade off recall for speed. These methods can efficiently find a small set of candidate vectors that are most likely to be similar to the query vector, reducing the total number of vector comparisons. Azure AI Search uses the Hierarchical Navigable Small World (HNSW) algorithm to organize high-dimensional data points into a probabilistic hierarchical graph structure that enables fast similarity search while allowing a tunable trade-off between search accuracy and computational cost.

Azure AI Search also supports multiple similarity metrics to determine nearest neighbor and score of each vector result These include cosine, "Euclidean" (also known as "l2 norm"), and "dot product." Cosine calculates the angle between two vectors. Euclidean calculates the Euclidean distance between two vectors, which is the l2-norm of the difference of the two vectors. Dot product is affected by both vectors' magnitudes and the angle between them. For normalized embedding spaces, dot product is equivalent to the cosine similarity but is more efficient.

### Use cases

#### Example use cases

There are many scenarios where vector search is useful, and they're limited only by the capabilities of the model used to generate vector embeddings. Here are some general use cases where vector search can be used:

- **Semantic search**: Extract semantic understanding from text by using a model, like using models such as the [Azure OpenAI Service embeddings models](/azure/ai-foundry/openai/concepts/models#embeddings-models-1).
- **Search across different data types (multimodal)**: Encode content coming from images, text, audio, and video, or a mix, and do a single search across all of them.
- **Multilingual search**: Use a multilingual embeddings model to represent your document in multiple languages to find results in supported languages.
- **Hybrid search**: Vector search is implemented at the field level, which means you can build queries that include vector fields and searchable text fields. The queries run in parallel, and the results are merged into a single response. Hybrid search results with semantic ranking have been shown to provide the best qualitative results.
- **Filtered vector search**: A query can include a vector query and filter expression. Filters applied to other data types are useful for including or excluding documents based on other criteria.
- **Vector database**: This pure vector store is for long-term memory or an external knowledge base for Large Language Models (LLMs). For example, use Azure AI Search as a vector index in Azure Machine Learning prompt flow for Retrieval Augmented Generation (RAG) applications.

#### Considerations when choosing a use case

There may be considerations and concerns associated with the specific model you choose to generate vector embeddings. Each model could have its own issues with bias and fairness and should be evaluated before being used in your application. Azure AI Search does not provide any models to vectorize content as part of the service. See the [Azure OpenAI Service Transparency Note](/azure/ai-foundry/responsible-ai/openai/transparency-note) for examples of these considerations. Other third-party or OSS models have considerations of their own to review.

#### [Semantic ranker](#tab/ranker)

### System behavior

Ranking the results of the first layer retrieval step is a highly resource-intensive process. To complete the ranker’s processing within the expected latency of a query operation, only the top 50 results from the retrieval engine are sent to the semantic ranker as inputs. If too long, the 50 results are first sent to a summarization step that extracts the most relevant content from each result before running the semantic ranker.

In the summarization step, the retrieved document is first put through a preparation process that concatenates the different document inputs into a single long string. If the string is too long, a trimming exercise takes place, with particular emphasis placed on retaining content contained within fields added to the [semantic configuration](/azure/search/semantic-how-to-query-request#2---create-a-semantic-configuration). After strings are prepared, they're passed through machine reading comprehension and language representation models to determine which sentences and phrases provide the best summary, relative to the query. This phase extracts content from the string that will be passed forward to the semantic ranking stage and optionally outputs a [semantic caption](/azure/search/semantic-how-to-query-request) or [semantic answer](/azure/search/semantic-answers).

The final step, semantic ranking, determines the relevance of the content extracted in the prior step to the user’s query and outputs a semantic ranking score ranging from 4 (highly relevant) to 0 (irrelevant). This step is based on the query text and on the summarized text and involves more complex computations than those of the retrieval layer.

### Use cases

#### Example use cases

Semantic ranker can be used in multiple scenarios. The system's intended use cases include:

- **Retrieval Augmented Generation (RAG)**: Semantic ranker enables you to ground responses from your generative AI applications in relevant search results that meet the relevancy score threshold that you define. For example, the Azure OpenAI Service on your data uses Azure AI Search to augment Azure OpenAI models with your data. You can use semantic ranker within this service to improve the relevancy of the information fed to the Azure OpenAI model.
- **Content search**: Semantic ranker allows you to search for relevant content within your data by analyzing text and metadata. For example, search on the [learn.microsoft.com](/) website uses semantic ranker to improve the search relevance for software developers who search for Microsoft technical documentation.
- **eCommerce search**: Semantic ranker enables eCommerce businesses to enhance their search experience by providing relevant product results based on semantic relevance. For example, online retailers use semantic ranker to optimize their eCommerce experience by providing relevant search results for their online shoppers.
- **QnA**: Azure AI Search enables organizations to provide a conversational experience for their users by answering questions based on the information available in their databases. For example, a manufacturer can use semantic ranker to augment information available to a chatbot. Engineers can use this chatbot to ask questions and retrieve highly relevant internal documents related to their query and instant answers within the retrieved documents.

#### Considerations when choosing a use case

We encourage customers to use semantic ranker in their innovative solutions or applications. However, here are some considerations when choosing a use case:

- **Sensitive information** : The machine learning models that enable semantic ranker process the data retrieved in a search query, including sensitive information such as personal details and financial information. Consider any privacy and security implications before you implement semantic ranker for such use cases.
- **Bias and fairness** : Semantic ranker is powered by deep learning models. These deep learning models were trained by using public content. Customer data is scored by the semantic ranker models. Evaluate the output of semantic ranker when you select use cases, especially for use cases that have implications for fairness and equity, such as hiring and recruitment.
- **Regulation compliance**: Some industries, such as healthcare and finance, are highly regulated and may have restrictions on the use of AI and machine learning. Before you use semantic ranker in such industries, ensure that the solution complies with relevant regulations and guidelines.


#### [Query rewriting](#tab/query)

### System behavior

The original query is sent to a [fine-tuned Small Language Model (SLM)]( /azure/ai-foundry/openai/concepts/fine-tuning-considerations) hosted by Azure AI Search. This model was trained by using public content. The SLM transforms the original query into a set of synthetic queries. These synthetic queries are semantically close to the intent of the original query but include a different set of terms to improve recall from the search engine. 

The synthetic queries are then combined with the original query and sent to the search engine. When it performs [BM25 ranking]( /azure/search/index-similarity-and-scoring), key terms from the synthetic queries are combined with the original query. When it performs [vector search]( /azure/search/vector-search-ranking#vector-similarity), the original query is concatenated with the synthetic queries before the [vector embedding]( /azure/search/vector-search-overview#embeddings-and-vectorization) step. 

### Use cases
#### Example use cases

Query rewriting can be used in multiple scenarios. Query rewriting requires use of [semantic ranker]( /azure/search/semantic-ranking). 
- **Chat interaction with your data**: Query rewriting allows you to ground responses from your generative AI applications in relevant search results that meet the relevancy score threshold that you define. For example, the Azure OpenAI Service On Your Data uses Azure AI Search to augment Azure OpenAI models with your data. You can use query rewriting within this service to improve the relevancy of the results of the information fed to the Azure OpenAI model.  
- **Conversational Questions and Answers (QnA)**: Azure AI Search enables organizations to provide a conversational experience for their users by answering questions based on the information available in their databases. For example, a manufacturer can use semantic ranker to augment information available to a chatbot. Engineers can use this chatbot to ask questions and retrieve highly relevant internal documents related to their query and instant answers within the retrieved documents. 

#### Considerations when choosing a use case

We encourage customers to use query rewriting in their innovative solutions or applications. However, here are some considerations when choosing a use case: 
- **Sensitive information and PII**: The fine-tuned SLM—which enables query rewriting—processes the search query, which may contain sensitive information. Consider any privacy and security implications before you implement query rewriting for such use cases. 
- **Redact personal information to reduce unconscious bias.** For example, during a company's resume review process, they may want to block a candidate’s name, address, or phone number to help reduce unconscious gender or other biases during the search. 
- **Legal and regulatory considerations.** Organizations need to evaluate potential specific legal and regulatory obligations when using any AI Search, which may not be appropriate for use in every industry or scenario. Restrictions may vary based on regional or local regulatory requirements. Additionally, AI Search is not designed for and may not be used in ways prohibited in applicable terms of service and relevant codes of conduct.    


#### [GenAI Prompt skill](#tab/genai)

The GenAI Prompt skill allows customers to pass their document content, existing in their data sources, and custom prompts to a language model they own, hosted on Microsoft Foundry. The language model processes the input and returns enriched content, which is then ingested into the search index alongside the original document content. This process enables the augmentation of search indexes with AI-generated summaries, image captions, and entity extraction, among others, based on customer-defined criteria. 

The following examples show how the GenAI Prompt skill works.

**Zero-shot ticket summarization**

Goal: Let support agents skim multi-page email threads in seconds. 

How it works:
- During indexing, every long ticket conversation is divided into logical segments (initial request, follow up questions, diagnostic logs, etc.). 
- For each segment, the language model is instructed to "summarize this section in three crisp sentences." 
- The resulting abstracts replace the raw text during retrieval so agents—and downstream RAG pipelines—see only the distilled essence. 

Why it helps: Concise, segment-level summaries reduce prompt size, accelerate response generation, and help agents focus on the customer’s core issue. 

**Few-shot entity extraction**

Goal: Support queries like "Show me all tickets where Product X crashed with error 500." 

How it works 
- The full ticket text is sent to the skill together with one worked example that shows the desired output format (a list of key entities such as product name, error code, operating system, and severity). 
- The model extracts every occurrence of 〈product, error_code, platform, severity. 
- This structured list is stored with the document, enabling instant filters that surface, for instance, all high severity crashes on iOS. 

Why it helps: Precomputed entities turn freeform customer messages into filterable data, letting support leads spot patterns and prioritize fixes without manual parsing. 


**One-shot ticket routing classification** 

Goal: Automatically route each ticket to the right queue. 

How it works:
- Each ticket is analyzed with a prompt that lists five support categories—Billing, Technical Issue, Account Access, Feature Request, and General Feedback—plus one reference example ("Example ticket → Billing"). 
- The model assigns exactly one label, based on the five support categories above, to every ticket that enters the AI Search system as input. 
- The help desk system uses the label to send billing queries to finance specialists, technical crashes to engineers, and so on. 

Why it helps: Fast, consistent labeling reduces mis-routed tickets, shortens resolution time, and improves customer satisfaction. 

**Chain-of-thought resolution suggestion** 

Goal: Provide support agents with the single best next step to resolve the issue. 

How it works 
- The entire ticket—or its most recent customer message—is passed to the language model. 
- The user message instructs the model after the system prompt: "Think step-by-step internally, but output only the recommended next action." 
- The returned guidance might be: "Ask the customer to clear the cache and reinstall version 3.2.1." 
- Agents can copy the suggestion directly or refine it before responding. 

Why it helps: Agents receive an actionable recommendation without the model’s private reasoning chain, saving time while keeping troubleshooting steps concise and relevant. In certain cases, the support agent is not inundated with unnecessary information.  

### Use cases

#### Example use cases

The GenAI Prompt skill enhances data enrichment within Azure AI Search, helping with response relevance to align with user intent and expectations. By integrating AI-generated content into search indexes, this skill enables more accurate and contextually appropriate search results. Key applications include: 
- **Generating concise summaries of lengthy documents to facilitate quicker information retrieval**: A legal firm processes extensive contracts and uses the GenAI Prompt skill to create brief summaries highlighting key clauses, making it easier for lawyers to review essential information without reading entire documents.
- **Creating textual descriptions for images to improve searchability and accessibility**: A media company manages a vast library of images. By applying the GenAI Prompt skill, they generate descriptive captions for each image, enabling efficient search and organization within their digital asset management system.
- **Identifying and extracting specific entities or facts from documents based on custom criteria**: A research institution analyzes scientific papers to extract mentions of chemical compounds and their properties. The GenAI Prompt skill automates this extraction, populating a structured database for researchers to access relevant data swiftly.
- **Classifying documents into defined categories for better organization and retrieval**: An insurance company receives numerous types of documents daily. Using the GenAI Prompt skill, they automatically classify these documents into categories like Claims, Policy Updates, and Customer Feedback. This streamlines their document management process and makes it easier to locate specific documents when needed.

While these are common applications, the skill is flexible, allowing customers to define prompts tailored to their unique requirements. 

#### Considerations when choosing a use case

It's important to note that the content, prompts, and language model deployments are entirely customer-managed resources. Foundry supports content safety filters for model deployments, and customers are responsible for configuring these filters as needed. Beyond the configurations available in Foundry, Azure AI Search does not apply additional content safety filters within the GenAI Prompt skill. 

When implementing the GenAI Prompt skill, consider the following: 
- **Implement processes for human review of AI-generated content**, especially when applying prompt transformations that could impact information reliability. Utilize Azure AI Search's [debug sessions tool](/azure/search/cognitive-search-how-to-debug-skillset) to test prompts on sample documents before full-scale deployment.
- **Avoid scenarios where use or misuse of the system could result in significant physical or psychological injury to an individual**. For example, scenarios that diagnose patients or prescribe medications have the potential to cause significant harm. Incorporating meaningful human review and oversight into the scenario can help reduce the risk of harmful outcomes.
- **Carefully consider all generative use cases**. Content generation scenarios may be more likely to produce unintended outputs and these scenarios require careful consideration and mitigations.
- **Legal and regulatory considerations**. Organizations need to evaluate potential specific legal and regulatory obligations when using any AI Search, which may not be appropriate for use in every industry or scenario. Restrictions may vary based on regional or local regulatory requirements. Additionally, AI Search is not designed for and may not be used in ways prohibited in applicable terms of service and relevant codes of conduct. 

#### [Agentic retrieval](#tab/ar)

### System behavior

The original conversation or search query is sent to a customer’s owned Azure OpenAI model to execute the query-planning steps. Query planning breaks down the conversation into a series of optimized subqueries that reflect the user’s underlying intent with corrected spelling and expanded synonyms. Azure AI Search then processes all subqueries at once across the full search retrieval system. Subqueries are first processed by a [hybrid combination](/azure/search/hybrid-search-overview) of keyword search and vector search. [Keyword search](/azure/search/search-lucene-query-architecture) finds the documents in the search index with similar keywords to the subqueries. [Vector search](/azure/search/vector-search-overview) finds documents in the search index that may have different keywords, but similar underlying meaning to the subqueries. The results of this hybrid search are then re-ranked by [semantic ranker](/azure/search/semantic-search-overview) to find the documents with the best match to intent of the subquery. The service then merges and removes duplicates from the ranked results, applying response limits like the maximum output length before sending back the final response. 

### Use cases

#### Example use cases

- **Grounding data for custom chatbots**. Link the chatbot to the company’s official HR policies and employee handbook so that when someone asks, "How many vacation days do I get?" the chatbot pulls the answer straight from those documents rather than guessing. 
- **Equip enterprise knowledge assistants to respect user context, filters, and chat history**. For example, when an employee asks about the goals for a specific period, the assistant uses their role, the current filters (for example, region: US), and the ongoing conversation (for example, the last topic was "Q2 pipeline") to generate a personalized response. 
- **Tackle complex information-seeking tasks where a single keyword query has low recall**. Such tasks can include troubleshooting guides, medical-literature research, or product comparisons. For instance, if a technician simply searches "device error" and receives generic results, an agentic retriever can factor in the entire conversation history which may include device model, software version, maintenance history, and network status to surface precise, relevant articles. 
- **Ensure full transparency into what was retrieved, why, and at what cost**. For example, when summarizing regulatory documents and past audit findings, it is critical to know the exact sources (for example, "SEC filing from Q2 2023"), the selection rationale (for example, "matched keywords: risk disclosure, derivatives"), and the associated costs (for example, token usage). 

#### Considerations when choosing a use case 

- **Latency**: Adding a second LLM call for query planning inevitably extends the request’s round‑trip time. Even with fast models, you should benchmark the extra delay under peak traffic and verify that the overall experience remains acceptable for your users. Where latency is critical, consider caching frequent queries or using smaller, faster planning models. 
- **Cost**: Charges accrue on two dimensions—OpenAI model tokens and Search ranking tokens. The query‑planner call is billed by Azure OpenAI for both input and output tokens, while each subquery is billed by Azure AI Search for the tokens it must rank. Ranking tokens are free in the initial phase of the public preview. Estimate both model and ranking token numbers for your workload in advance. 
- **Sensitive inputs**: The entire conversation history is forwarded to the planner model, meaning any personally identifiable or business‑sensitive data leaves your immediate trust boundary. Strip, mask, or redact such data before invoking the LLM, and document that mitigation in your data‑protection posture. 
- **Region and preview limits**: Agentic retrieval is only available in regions where semantic ranker is available. An individual agent can point to just one Search index. Confirm that the region hosting your data and model supports agentic retrieval, and plan separate agents if you need to span multiple indexes or geographies. 
- **Compliance**: Confirm that using an LLM‑driven query planner complies with sector‑specific or regional requirements (for example, data‑residency, privacy, or automated‑decision rules in healthcare or finance). Ensure adequate human oversight and control. Consider including controls to help developers verify, review and/or approve actions in a timely manner, which may include reviewing planned tasks or calls to external data sources. 
- **Legal and regulatory considerations**: Users need to evaluate potential specific legal and regulatory obligations when using any Foundry Tools and solutions, which may not be appropriate for use in every industry or scenario. Additionally, Foundry Tools or solutions are not designed for and may not be used in ways prohibited in applicable terms of service and relevant codes of conduct. 

---

## Limitations

#### [AI enrichment](#tab/enrichment)

AI enrichment in Azure AI Search uses the indexer and data source features of the service to call Foundry Tools to perform the content enrichment. Limitations of the indexers and data sources used in this process will apply. Review the [indexer and data source documentation](/azure/search/search-limits-quotas-capacity#indexer-limits) for more information about these related limitations. The limitations of each Foundry Tool used by the AI enrichment pipeline in Azure AI Search will also apply. See the [transparency notes for each service](/azure/ai-services/responsible-use-of-ai-overview) for more information about these limitations.

#### [Vector search](#tab/vector)

### Technical limitations, operational factors, and ranges

All vectors uploaded to Azure AI Search must be generated externally from the service by using a model of your choice. It is your responsibility to consider the technical limitations and operating factors of each model, and whether the embeddings it creates are optimized or even appropriate for your use case. This includes both the inferences of meaning extracted from content, and the dimensionality of the vector embedding space.

The vectorization model creates an embeddings space that defines the resulting end user search experience of an application. There could be downsides to a model that negatively affects both functionality and performance if a model does not align well with a desired use case or the embeddings generated are poorly optimized.

While many limitations of vector search stem from the model used to generate embeddings, there are some additional options you should consider at query time. You can choose from two algorithms to determine relevance for vector search results: Exhaustive k-nearest neighbors (KNN) or Hierarchical Navigable Small World. Exhaustive k-nearest neighbors (KNN) performs a brute-force search of the entire vector space for matches that are most similar to the query by calculating the distances between all pairs of data points and finding the exact k nearest neighbors of a query point. While more precise, this algorithm can be slow. If low latency is the primary goal, consider using the Hierarchical Navigable Small World (HNSW) algorithm. HNSW performs an efficient approximate nearest neighbor (ANN) search in high-dimensional embedding spaces. See the [vector search documentation](/azure/search/vector-search-ranking) for more information about these options.

### Best practices for improving system performance

- Do spend time A/B testing your application with the different content and query types you expect your application to support. Figure out which query experience is best for your needs.
- Do spend time testing your models with a full range of input content to understand how it behaves in many situations. This content could include potentially sensitive input to understand whether there is any bias inherent in the model. The [Azure OpenAI Responsible AI](/azure/ai-foundry/responsible-ai/openai/overview) overview provides guidance for how to responsibly use AI.
- Do consider adding [Azure AI Content Safety](/azure/ai-services/content-safety/overview) to your application architecture. It includes an API to detect harmful user-generated and AI-generated text or images in applications and services.

## Evaluating and integrating vector search for your use

To ensure optimal performance, conduct your own evaluations of the solutions you plan to implement by using vector search. Follow an evaluation process that: (1) uses some internal stakeholders to evaluate results, (2) uses A/B experimentation to roll out vector search to users, (3) incorporates key performance indicators (KPIs) and metrics monitoring when the service is deployed in experiences for the first time, and (4) tests and tweaks the semantic ranker configuration and/or index definition, including the surrounding experiences like user interface placement or business processes.

Microsoft has rigorously evaluated vector search both in terms of latency and recall and relevance by using diverse datasets to measure the speed, scalability, and accuracy of results returned. The primary focus of your evaluation efforts should be on selecting the appropriate model for your specific use case, understanding the limitations and biases of the model, and rigorously testing the end to end vector search experience.

#### [Semantic ranker](#tab/ranker)

### Technical limitations, operational factors, and ranges

There may be cases where semantic results, captions, and answers may not appear to be correct. The models used by semantic ranker are trained on various data sources (including open source and selections from the Microsoft Bing corpus). Semantic ranker supports [a broad range of languages](/rest/api/searchservice/preview-api/search-documents#querylanguage) and attempts to match user queries to content from your search results. Semantic ranker is also a premium feature at additional cost which should be considered when projecting the overall cost of your end-to-end solution.

Semantic ranker is most likely to improve relevance over content that is semantically rich, such as articles and descriptions. It looks for context and relatedness among terms, elevating matches that make more sense given the query. Language understanding "finds" summarizations or captions and answers within your content, but unlike generative models like Azure OpenAI Service models GPT-3.5 or GPT-4, it does not create them. Only verbatim text from source documents is included in the response, which can then be rendered on a search results page for a more productive search experience.

State-of-the-art, pre-trained models are used for summarization and ranking. To maintain the fast performance that users expect from search, semantic summarization and ranking are applied to just the top 50 results, as scored by the default scoring algorithm. Inputs are derived from the content in the search result. It cannot reach back to the search index to access other fields in the search document that weren't returned in the query response. Inputs are subject to a token length of 8,960. These limits are necessary to maintain millisecond response times.

The default scoring algorithm is from Bing and Microsoft Research and integrated into the Azure AI Search infrastructure as an add-on feature. The models are used internally, are not exposed to the developer, and are non-configurable. For more information about the research and AI investments backing semantic ranker, see [How AI from Bing is powering Azure AI Search (Microsoft Research Blog).](https://www.microsoft.com/research/blog/the-science-behind-semantic-search-how-ai-from-bing-is-powering-azure-cognitive-search/)

Semantic ranker also offers answers, captions, and highlighting within the response. For example, if the model classifies a query as a question and is 70% confident in the answer, the model returns a semantic answer. Additionally, semantic captions provide the most relevant content within the results and provide a brief snippet highlighting the most relevant words or phrases within that snippet.

Semantic ranker results are based off the data in the underlying search index, and the models provide relevance ranking, answers, and captions based on the information retrieved from the index. Prior to using semantic ranker in a production environment, it is important to do further testing and to ensure that the dataset is accurate and appropriate for the intended use case. For more information and examples of how to evaluate semantic ranker, see the [content and appendix here](https://techcommunity.microsoft.com/t5/azure-ai-services-blog/azure-cognitive-search-outperforming-vector-search-with-hybrid/ba-p/3929167).

## System performance

In many AI systems, performance is often defined in relation to accuracy—that is, how often the AI system offers a correct prediction or output. With large-scale natural language models, two different users may look at the same output and have different opinions of how useful or relevant it is, which means that performance for these systems must be defined more flexibly. Here, we broadly consider performance to mean that the application performs as you and your users expect, including not generating harmful outputs.

Semantic ranker was trained on public content. As a result, the semantic relevance varies based on the documents in the index and the queries issued against it. It is important to use your own judgment and research when you use this content for decision making.

#### Best practices for improving system performance

- Do spend time A/B testing your application with different query types, such as keyword versus hybrid plus semantic ranker. Figure out which query experience is best for your needs.
- Do expend a reasonable effort to set up your semantic configuration in accordance with the [feature documentation](/azure/search/semantic-how-to-query-request?tabs=portal%2Cportal-query#2---create-a-semantic-configuration).
- Do not trust the semantic answers if you do not have confidence in the accuracy of the information within the search index.
- Do not always trust semantic captions because they are extracted from customer content through a series of models that predicts the most relevant answers in a brief snippet.

## Evaluation of Semantic ranker

### Evaluation methods

Semantic ranker was evaluated through internal testing, including automated and human judgment on multiple datasets as well as feedback from internal customers. Testing includes the ranking of documents by scoring them as relevant or not relevant along with ranking documents in priority order of relevance. Likewise, the captions and answers functionality were also ranked via internal testing.

### Evaluation results

We strive to ship all model updates regression-free (that is, the updated model should only improve the current production model). Each candidate is compared directly to the current production model by using metrics suitable for the feature being evaluated (for example, [Normalized Discounted Cumulative Gain](https://wikipedia.org/wiki/Discounted_cumulative_gain) for ranking and precision/recall for answers). Semantic ranker models are trained, tuned, and evaluated by using a wide range of training data that is representative of documents that have different properties (language, length, formatting, styles, and tones) to support the broadest array of search scenarios. Our training and test data are drawn from:

Sources of documents:

- Academic and industry benchmarks
- Customer data (testing only, performed with customer permission)
- Synthetic data

Sources of queries:

- Benchmark query sets
- Customer-provided query sets (testing only, performed with customer permission)
- Synthetic query sets
- Human-generated query sets

Sources of labels for scoring query and document pairs:

- Academic and industry benchmark labels
- Customer labels (testing only, performed with customer permission)
- Synthetic data labels
- Human-scored labels

## Evaluating and integrating semantic ranker for your use

The performance of semantic ranker varies depending on the real-world uses and conditions in which people use it. The quality of the relevance provided through the deep learning models that power semantic ranker capabilities is directly correlated with the data quality of your search index. For example, the models currently have token limitations that consider only the top 8,960 tokens for semantic answers. Therefore, if the semantic answer to a search query is found toward the end of a long document (beyond the 8,960 token limit), the answer will not be provided. The same rule applies for captions. Also, the semantic configuration lists relevant search fields in priority order. You can reorder the fields in this list to help tailor relevance to better suit your needs.

To ensure optimal performance in their scenarios, customers should conduct their own evaluations of the solutions they implement by using semantic ranker. Customers should generally follow an evaluation process that: (1) uses some internal stakeholders to evaluate results, (2) uses A/B experimentation to roll out semantic ranker to users, (3) incorporates KPIs and metrics monitoring when the service is deployed in experiences for the first time, and (4) tests and tweaks the semantic ranker configuration and/or index definition, including the surrounding experiences like user interface placement or business processes.

**If you are developing an application in a high-stakes domain or industry**, such as healthcare, human resources, education, or the legal field, assess how well the application works in your scenario, implement strong human oversight, evaluate how well users understand the limitations of the application, and comply with all relevant laws. Consider other mitigations based on your scenario.

#### [Query rewriting](#tab/query)
### Technical limitations, operational factors, and ranges

 There may be cases where synthetic queries are incorrect, come with too many restrictions, or are too expensive. Query rewriting supports [a broad range of languages](/rest/api/searchservice/preview-api/search-documents#querylanguage) and attempts to rewrite user queries to maximize recall, it is required to specify the query language as  an input. Query rewriting is a part of Semantic Ranker (Azure AI Search feature to improve search relevance), which is a premium feature with an additional cost. This should be considered when projecting the overall expenses of your end-to-end solution. Query rewriting can only be used if you have semantic ranker enabled. 

Prior to using query rewriting in a production environment (live version of your application), it is important to do further testing and to ensure that the synthetic queries are appropriate for the intended use case. For more information and examples of how to evaluate query rewriting, see the [content and appendix here](https://techcommunity.microsoft.com/blog/azure-ai-services-blog/raising-the-bar-for-rag-excellence-query-rewriting-and-new-semantic-ranker/4302729). 





## System performance

With large-scale natural language models, two different users may look at the same output and have different opinions of how useful or relevant it is, which means that performance for these systems must be defined more flexibly. Here, we broadly consider performance to mean that the application performs as you and your users expect, including not generating harmful outputs. 

The performance of query rewriting varies depending on the real-world uses and conditions in which people use it. The quality of synthetic queries provided by the query rewriting model is directly correlated with the original search query. 

To ensure optimal performance in their scenarios, customers should conduct their own evaluations of the solutions they implement by using query rewriting. Customers should generally follow an evaluation process that:  
1. uses some internal stakeholders to evaluate results,  
1. uses A/B experimentation to roll out query rewriting to users, and  
1. incorporates KPIs and metrics monitoring when the service is deployed in experiences for the first time 

### Best practices for improving system performance


- Complete A/B testing for your application with different query types (Full text, Vector, Hybrid, or other type of queries). Figure out which query experience is best for your needs. 
- Do not always assume that every synthetic query generated by query rewriting will reflect the exact intent of the original query. Synthetic queries are generated by a fine-tuned SLM, which generates queries semantically similar to the intent of the original query but may not match the exact intent. 


## Evaluation of query rewriting

### Evaluation methods

Query rewriting was evaluated through internal testing, including automated and human judgment on multiple datasets as well as feedback from internal customers. Testing included evaluating the relevance of results of semantic ranking combined with query rewriting compared to the relevance of results with semantic ranking only. 

### Evaluation results

Each candidate model is compared directly to the currently deployed model by using metrics suitable for the feature being evaluated. Query rewriting models are tuned and evaluated by using a wide range of public data that is representative of queries that have different properties (language, length, formatting, styles, and tones) to support the broadest array of search scenarios. Our training and test data are drawn from: 

Sources of documents: 
- Academic and industry benchmarks 
- Customer data (testing only, performed with customer permission)

Sources of queries: 
- Benchmark query sets 
- Customer-provided query sets (testing only, performed with customer permission) 
- Synthetic query sets 
- Human-generated query sets

Sources of labels for scoring query and document pairs: 
- Academic and industry benchmark labels 
- Customer labels (testing only, performed with customer permission) 
- Synthetic data labels 
- Human-scored labels 

## Evaluating and integrating query rewriting for your use

As Query rewriting was trained on public content, the synthetic queries will vary based on the queries issued to it. So, it is important to use your own judgment and research when you use this content for decision making. 


#### [GenAI Prompt skill](#tab/genai)

### Technical limitations, operational factors, and ranges 

While GenAI Prompt skill offers powerful capabilities, it's essential to recognize certain limitations: 
- The skill relies on customer-configured content filters within Foundry. Azure AI Search does not provide additional content safety mechanisms for this skill. 
- The quality of AI-generated content depends on the effectiveness of the prompts and the underlying language model. Thorough testing is necessary to ensure output meets the desired standards. 
- Processing large volumes of data with complex prompts may require significant computational resources and may cause latency. Plan and allocate resources wisely to not only maintain performance and cost-effectiveness, but also to prevent possible delays in data processing. 

## System performance

### Best practices for improving system performance 

To optimize the performance of the GenAI Prompt skill: 
- Utilize Azure AI Search's [debug sessions tool](/azure/search/cognitive-search-how-to-debug-skillset) to test prompts on sample documents, ensuring the AI-generated content aligns with expectations before full deployment. 
- Craft clear and detailed prompts to guide the language model effectively, reducing the likelihood of irrelevant or inaccurate outputs. 
- Monitor system performance and scale resources as needed to handle the computational demands of AI processing. 
- Encourage human oversight of outputs prior to publication or dissemination. With generative AI, there is potential for generating content that might be offensive or irrelevant to the task at hand. 

## Evaluation of GenAI Prompt skill 

### Evaluating and integrating GenAI Prompt skill for your use 

To maximize the benefits of the GenAI Prompt skill within your specific context, consider the following steps: 
- Determine the specific enrichment goals, such as generating concise summaries, extracting key entities, or creating descriptive metadata, to align the skill's application with your business needs. 
- Start with a subset of your data to assess the skill's performance and make necessary adjustments. This approach allows for controlled experimentation and refinement before full-scale deployment. 
- Establish mechanisms to monitor the quality and impact of the AI-generated content. Solicit feedback from end-users to identify areas for improvement and to ensure the enriched data meets user expectations. 


#### [Agentic retrieval](#tab/ar)

### Technical limitations, operational factors, and ranges 

There may be cases where the LLM‑generated subqueries are irrelevant, overly restrictive, or drive-up token costs. Agentic retrieval supports all languages handled by the GPT‑4o family, but the quality of the generated query plan still depends on the clarity of the user input. Because agentic retrieval relies on semantic ranker for every subquery, you must have semantic ranker enabled on the index. Semantic ranker is a premium, token‑based feature; although ranking charges are waived during the initial phase of the public preview, they will apply later and should be factored into the total cost of ownership. 

Before moving agentic retrieval into a production environment, conduct additional testing to confirm that the subqueries and returned passages are appropriate for the intended use case, that latency and cost meet your service‑level objectives, and that the grounding data does not expose sensitive or non‑compliant content. 

## System performance

As with any large‑scale language‑model system, different users can reach different judgments about the usefulness or relevance of the returned passages, so performance must be defined flexibly. For agentic retrieval, we consider good performance to mean that the end‑to‑end application delivers the content your users expect—without unacceptable latency, cost, or harmful outputs. 

The effectiveness of agentic retrieval depends on many real‑world factors:
- Prompt / chat‑history length 
- Number of LLM‑generated subqueries 
- Index size and schema (keyword, vector, hybrid) 
- Choice of planning model (GPT‑4o vs. GPT‑4o‑mini) 
- Semantic‑search configuration and score thresholds 

### Best practices for improving system performance 


- Summarize or trim older chat turns to keep token usage low. 
- Tune the ranker threshold so that only highly relevant passages are returned 
- Use filters where possible 

## Evaluation of agentic retrieval


Agentic retrieval has been evaluated through internal testing, including automated and human judgment on multiple datasets. Testing included evaluating the relevance of results of agentic retrieval compared to results with semantic ranking only. 

### Evaluation methods

Each candidate agentic‑retrieval configuration, defined by its planner prompt, model variant, subquery count, and ranking thresholds, is evaluated head‑to‑head against the production baseline. We apply a suite of relevance, safety, latency, and cost metrics chosen specifically for multi‑query retrieval scenarios. To ensure reliability across real‑world use cases, tuning and testing are performed on a broad mix of public and customer‑approved data sets that vary in language, query length, formatting, style, and conversational tone. Test material is sourced from: 

Sources of documents: 
- Academic and industry benchmarks 
- Customer data (testing only, performed with customer permission) 
- Sources of queries: 
- Benchmark query sets 
- Customer-provided query sets (testing only, performed with customer permission) 
- Synthetic query sets 
- Human-generated query sets 

Sources of labels for scoring query and document pairs: 
- Academic and industry benchmark labels 
- Customer labels (testing only, performed with customer permission) 
- Synthetic data labels 
- Human-scored labels 


### Evaluating and integrating agentic retrieval for your use

Because the agentic‑retrieval planner is trained largely on public data, the quality and relevance of its generated subqueries will vary with your domain and the specific user prompts. To maximize the benefits of agentic retrieval within your specific context, consider the following steps:
- **Validate the output before using it to drive business‑critical decisions**: Manually inspect a sample of generated subqueries and returned documents to confirm they align with domain terminology, accuracy, and compliance requirements. 
- **Provide domain-specific information to the planner**. Supply [synonym maps](/azure/search/search-synonyms), and full conversation history so the LLM can paraphrase and decompose queries in language that matches your content, improving recall and precision. 
- **Implement fallback or guardrail logic**: If the planner produces low‑confidence or out‑of‑scope subqueries, route the request to a simpler keyword or vector search, or surface a clarification prompt to the user, preventing unreliable answers from propagating downstream. 

---

## Learn more about responsible AI

- [Microsoft AI principles](https://www.microsoft.com/ai/responsible-ai)
- [Microsoft responsible AI resources](https://www.microsoft.com/ai/responsible-ai-resources)
- [Microsoft Azure Learning courses on responsible AI](/learn/paths/responsible-ai-business-principles/)

## Learn more about Azure AI Search

- [Introduction to Azure AI Search](/azure/search/search-what-is-azure-search)
- [Feature descriptions](/azure/search/search-features-list)
- [AI enrichment concepts](/azure/search/cognitive-search-concept-intro)
- [Retrieval Augmented Generation (RAG) in Azure AI Search](/azure/search/retrieval-augmented-generation-overview)