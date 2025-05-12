---
title: Retrieval-augmented Generation (RAG) evaluators for generative AI
titleSuffix: Azure AI Foundry
description: Learn about Retrieval-augmented Generation (RAG) evaluators for assessing relevance, groundedness, and response completeness in generative AI systems.
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: reference
ms.date: 05/19/2025
ms.reviewer: changliu2
ms.author: lagayhar
author: lgayhardt
---

# Retrieval-augmented Generation (RAG) evaluators

A retrieval-augmented generation (RAG) system tries to generate the most relevant answer consistent with grounding documents in response to a user's query. At a high level, a user's query triggers a search retrieval in the corpus of grounding documents to provide grounding context for the AI model to generate a response. It's important to evaluate:

- The relevance of the retrieval results to the user's query: use [Document Retrieval](#document-retrieval) if you have labels for query-specific document relevance, or query relevance judgement (qrels) for more accurate measurements. Use [Retrieval](#retrieval) if you only have the retrieved context, but you don't have such labels and have a higher tolerance for a less fine-grained measurement.
- The consistency of the generated response with respect to the grounding documents: use [Groundedness](#groundedness) if you want to potentially customize the definition of groundedness in our open-source LLM-judge prompt, [Groundedness Pro](#groundedness-pro) if you want a straightforward definition.
- The relevance of the final response to the query: [Relevance](#relevance) if you don't have ground truth, and [Response Completeness](#response-completeness) if you have ground truth and don't want your response to miss critical information.

A good way to think about **Groundedness** and **Response Completeness** is: groundedness is about the **precision** aspect of the response that it shouldn't contain content outside of the grounding context, whereas response completeness is about the **recall** aspect of the response that it shouldn't miss critical information compared to the expected response (ground truth).

## Model configuration for AI-assisted evaluators

For reference in the following snippets, the AI-assisted quality evaluators (except for Groundedness Pro) use a model configuration for the LLM-judge:

```python
import os
from azure.ai.evaluation import AzureOpenAIModelConfiguration
from dotenv import load_dotenv
load_dotenv()

model_config = AzureOpenAIModelConfiguration(
    azure_endpoint=os.environ["AZURE_ENDPOINT"],
    api_key=os.environ.get["AZURE_API_KEY"],
    azure_deployment=os.environ.get("AZURE_DEPLOYMENT_NAME"),
    api_version=os.environ.get("AZURE_API_VERSION"),
)
```

> [!TIP]
> We recommend using `o3-mini` for a balance of reasoning capability and cost efficiency.

## Retrieval

Retrieval quality is very important given its upstream role in RAG: if the retrieval quality is poor and the response requires corpus-specific knowledge, there's less chance your LLM model gives you a satisfactory answer. `RetrievalEvaluator` measures the **textual quality** of retrieval results with an LLM without requiring ground truth (also known as query relevance judgment), which provides value compared to `DocumentRetrievalEvaluator` measuring `ndcg`,  `xdcg`, `fidelity`, and other classical information retrieval metrics that require ground truth. This metric focuses on how relevant the context chunks (encoded as a string) are to address a query and how the most relevant context chunks are surfaced at the top of the list.

### Retrieval example

```python
from azure.ai.evaluation import RetrievalEvaluator

retrieval = RetrievalEvaluator(model_config=model_config, threshold=3)
retrieval(
    query="Where was Marie Currie born?", 
    context="Background: 1. Marie Curie was born in Warsaw. 2. Marie Curie was born on November 7, 1867. 3. Marie Curie is a French scientist. ",
)
```

### Retrieval output

The numerical score on a likert scale (integer 1 to 5) and a higher score is better. Given a numerical threshold (a default is set), we also output "pass" if the score <= threshold, or "fail" otherwise. Using the reason field can help you understand why the score is high or low.

```python
{
    "retrieval": 5.0,
    "gpt_retrieval": 5.0,
    "retrieval_reason": "The context contains relevant information that directly answers the query about Marie Curie's birthplace, with the most pertinent information placed at the top. Therefore, it fits the criteria for a high relevance score.",
    "retrieval_result": "pass",
    "retrieval_threshold": 3
}
```

## Document retrieval

Retrieval quality is very important given its upstream role in RAG: if the retrieval quality is poor and the response requires corpus-specific knowledge, there's less chance your LLM model gives you a satisfactory answer. Therefore, it's important to use `DocumentRetrievalEvaluator` to evaluate the retrieval quality but also optimize your search parameters for RAG.

- Document Retrieval evaluator measures how well the RAG retrieves the correct documents from the document store. As a composite evaluator useful for RAG scenario with ground truth, it computes a list of useful search quality metrics for debugging your RAG pipelines:

| Metric | Category | Description |
|--|--|--|
| Fidelity | Search Fidelity | How well the top n retrieved chunks reflect the content for a given query; number of good documents returned out of the total number of known good documents in a dataset |
| NDCG | Search NDCG | How good are the rankings to an ideal order where all relevant items are at the top of the list. |
| XDCG | Search XDCG | How good the results are in the top-k documents regardless of scoring of other index documents |
| Max Relevance N | Search Max Relevance | Maximum relevance in the top-k chunks |
| Holes | Search Label Sanity | Number of documents with missing query relevance judgments (Ground truth) |

- To optimize your RAG in a scenario called "parameter sweep", you can use these metrics to calibrate the search parameters for the optimal RAG results. Simply generate different retrieval results for various search parameters such as search algorithms (vector, semantic), top_k, and chunk sizes you're interested in testing. Then use `DocumentRetrievalEvaluator` to find the search parameters that yield the highest retrieval quality.

### Document retrieval example

```python
from azure.ai.evaluation import DocumentRetrievalEvaluator

retrieval_ground_truth = [
    {
        "document_id": "1",
        "query_relevance_label": 4
    },
    {
        "document_id": "2",
        "query_relevance_label": 2
    },
    {
        "document_id": "3",
        "query_relevance_label": 3
    },
    {
        "document_id": "4",
        "query_relevance_label": 1
    },
    {
        "document_id": "5",
        "query_relevance_label": 0
    },
]

# these reterieval scores 
retrieved_documents = [
    {
        "document_id": "2",
        "relevance_score": 45.1
    },
    {
        "document_id": "6",
        "relevance_score": 35.8
    },
    {
        "document_id": "3",
        "relevance_score": 29.2
    },
    {
        "document_id": "5",
        "relevance_score": 25.4
    },
    {
        "document_id": "7",
        "relevance_score": 18.8
    },
]

document_retrieval_evaluator = DocumentRetrievalEvaluator(
    ndcg_threshold = 0.5,
    xdcg_threshold = 50.0,
    fidelity_threshold = 0.5,
    top1_relevance_threshold = 50.0,
    top3_max_relevance_threshold = 50.0,
    total_retrieved_documents_threshold = 50,
    total_ground_truth_documents_threshold = 50
)
document_retrieval_evaluator(retrieval_ground_truth=retrieval_ground_truth, retrieved_documents=retrieved_documents)   
```

### Document retrieval output

The numerical score on a likert scale (integer 1 to 5) and a higher score is better. Given a numerical threshold (default to 3), we also output "pass" if the score <= threshold, or "fail" otherwise. Using the reason field can help you understand why the score is high or low.

```python
{
    "ndcg@3": 0.6461858173,
    "xdcg@3": 37.7551020408,
    "fidelity": 0.0188438199,
    "top1_relevance": 2,
    "top3_max_relevance": 2,
    "holes": 30,
    "holes_ratio": 0.6000000000000001,
    "holes_is_higher_better": False,
    "holes_ratio_is_higher_better": False,
    "total_retrieved_documents": 50,
    "total_groundtruth_documents": 1565,
    "ndcg@3_result": "pass",
    "xdcg@3_result": "pass",
    "fidelity_result": "fail",
    "top1_relevance_result": "fail",
    "top3_max_relevance_result": "fail",
}
```

## Groundedness

It's important to evaluate how grounded the response is in relation to the context, because AI models can fabricate content or generate irrelevant responses. `GroundednessEvaluator` measures how well the generated response aligns with the given context (grounding source) and doesn't fabricate content outside of it. This metric captures the **precision** aspect of response alignment with the grounding source. Lower score means the response is irrelevant to the query or fabricated inaccurate content outside the context. This metric is complementary to `ResponseCompletenessEvaluator` that captures the **recall** aspect of response alignment with the expected response.  

### Groundedness example

```python
from azure.ai.evaluation import GroundednessEvaluator

groundedness = GroundednessEvaluator(model_config=model_config, threshold=3)
groundedness(
    query="Is Marie Currie is born in Paris?", 
    context="Background: 1. Marie Curie is born on November 7, 1867. 2. Marie Curie is born in Warsaw.",
    response="No, Marie Currie is born in Warsaw."
)
```

### Groundedness output

The numerical score on a likert scale (integer 1 to 5) and a higher score is better. Given a numerical threshold (default to 3), we also output "pass" if the score <= threshold, or "fail" otherwise. Using the reason field can help you understand why the score is high or low.

```python
{
    "groundedness": 5.0,  
    "gpt_groundedness": 5.0,
    "groundedness_reason": "The RESPONSE accurately answers the QUERY by confirming that Marie Curie was born in Warsaw, which is supported by the CONTEXT. It does not include any irrelevant or incorrect information, making it a complete and relevant answer. Thus, it deserves a high score for groundedness.",
    "groundedness_result": "pass", 
    "groundedness_threshold": 3
}
```

## Groundedness Pro

AI systems can fabricate content or generate irrelevant responses outside the given context. Powered by Azure AI Content Safety, `GroundednessProEvaluator` detects whether the generated text response is consistent or accurate with respect to the given context in a retrieval-augmented generation question-and-answering scenario. It checks whether the response adheres closely to the context in order to answer the query, avoiding speculation or fabrication, and outputs a binary label.

### Groundedness Pro example

```python
import os
from azure.ai.evaluation import GroundednessProEvaluator
from dotenv import load_dotenv
load_dotenv()

## Using Azure AI Foundry Hub
azure_ai_project = {
    "subscription_id": os.environ.get("AZURE_SUBSCRIPTION_ID"),
    "resource_group_name": os.environ.get("AZURE_RESOURCE_GROUP"),
    "project_name": os.environ.get("AZURE_PROJECT_NAME"),
}
## Using Azure AI Foundry Development Platform, example: AZURE_AI_PROJECT=https://your-account.services.ai.azure.com/api/projects/your-project
azure_ai_project = os.environ.get("AZURE_AI_PROJECT")

groundedness_pro = GroundednessProEvaluator(azure_ai_project=azure_ai_project), 
groundedness_pro(
    query="Is Marie Currie is born in Paris?", 
    context="Background: 1. Marie Curie is born on November 7, 1867. 2. Marie Curie is born in Warsaw.",
    response="No, Marie Currie is born in Warsaw."
)
```

### Groundedness Pro output

The label field returns a boolean score `True` if all content in the response is completely grounded in the context and `False` otherwise. Use the reason field to understand more about the judgment behind the score.

```python
{
    "groundedness_pro_reason": "All Contents are grounded",
    "groundedness_pro_label": True
}
```

## Relevance

It's important to evaluate the final response because AI models can generate irrelevant responses with respect to a user query. To address this, you can use `RelevanceEvaluator` which measures how effectively a response addresses a query. It assesses the accuracy, completeness, and direct relevance of the response based solely on the given query. Higher scores mean better relevance.

### Relevance example

```python
from azure.ai.evaluation import RelevanceEvaluator

relevance = RelevanceEvaluator(model_config=model_config, threshold=3)
relevance(
    query="Is Marie Currie is born in Paris?", 
    response="No, Marie Currie is born in Warsaw."
)
```

### Relevance output

The numerical score on a likert scale (integer 1 to 5) and a higher score is better. Given a numerical threshold (default to 3), we also output "pass" if the score <= threshold, or "fail" otherwise. Using the reason field can help you understand why the score is high or low.

```python
{
    "relevance": 4.0,
    "gpt_relevance": 4.0, 
    "relevance_reason": "The RESPONSE accurately answers the QUERY by stating that Marie Curie was born in Warsaw, which is correct and directly relevant to the question asked.",
    "relevance_result": "pass", 
    "relevance_threshold": 3
}
```

## Response completeness

AI systems can fabricate content or generate irrelevant responses outside the given context. Given ground truth response, `ResponseCompletenessEvaluator` that captures the **recall** aspect of response alignment with the expected response. This is complementary to `GroundednessEvaluator` which captures the **precision** aspect of response alignment with the grounding source.

### Response completeness example

```python
from azure.ai.evaluation import ResponseCompletenessEvaluator

response_completeness = ResponseCompletenessEvaluator(model_config=model_config, threshold=3)
response_completeness(
    response="Based on the retrieved documents, the shareholder meeting discussed the operational efficiency of the company and financing options.",
    ground_truth="The shareholder meeting discussed the compensation package of the company CEO."
)
```

### Response completeness output

The numerical score on a likert scale (integer 1 to 5) and a higher score is better. Given a numerical threshold (default to 3), we also output "pass" if the score <= threshold, or "fail" otherwise. Using the reason field can help you understand why the score is high or low.

```python
{
    "response_completeness": 1,
    "response_completeness_result": "fail",
    "response_completeness_threshold": 3,
    "response_completeness_reason": "The response does not contain any relevant information from the ground truth, which specifically discusses the CEO's compensation package. Therefore, it is considered fully incomplete."
}
```

## Related content

- [How to run batch evaluation on a dataset](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-datasets)  
- [How to run batch evaluation on a target](../../how-to/develop/evaluate-sdk.md#local-evaluation-on-a-target)
