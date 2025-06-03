---
title: "Groundedness detection overview"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: include
ms.date: 05/08/2025
ms.author: pafarley
---



The Groundedness detection feature detects whether the text responses of large language models (LLMs) are grounded in the source materials provided by the users. Ungroundedness refers to instances where the LLMs produce information that is non-factual or inaccurate from what was present in the source materials.

## Key terms

- **Retrieval Augmented Generation (RAG)**: RAG is a technique for augmenting LLM knowledge with other data. LLMs can reason about wide-ranging topics, but their knowledge is limited to the public data that was available at the time they were trained. If you want to build AI applications that can reason about private data or data introduced after a model’s cutoff date, you need to provide the model with that specific information. The process of bringing the appropriate information and inserting it into the model prompt is known as Retrieval Augmented Generation (RAG). For more information, see [Retrieval-augmented generation (RAG)](https://python.langchain.com/docs/tutorials/rag/).
- **Groundedness and Ungroundedness in LLMs**: This refers to the extent to which the model's outputs are based on provided information or reflect reliable sources accurately. A grounded response adheres closely to the given information, avoiding speculation or fabrication. In groundedness measurements, source information is crucial and serves as the grounding source.


## User scenarios

Groundedness detection supports text-based Summarization and QnA tasks to ensure that the generated summaries or answers are accurate and reliable.

**Summarization tasks**:
- Medical summarization: In the context of medical news articles, Groundedness detection can be used to ensure that the summary doesn't contain fabricated or misleading information, guaranteeing that readers obtain accurate and reliable medical information.
- Academic paper summarization: When the model generates summaries of academic papers or research articles, the function can help ensure that the summarized content accurately represents the key findings and contributions without introducing false claims.

**QnA tasks**:
- Customer support chatbots: In customer support, the function can be used to validate the answers provided by AI chatbots, ensuring that customers receive accurate and trustworthy information when they ask questions about products or services.
- Medical QnA: For medical QnA, the function helps verify the accuracy of medical answers and advice provided by AI systems to healthcare professionals and patients, reducing the risk of medical errors.
- Educational QnA: In educational settings, the function can be applied to QnA tasks to confirm that answers to academic questions or test prep queries are factually accurate, supporting the learning process.


Below, see several common scenarios that illustrate how and when to apply these features to achieve the best outcomes.

### Summarization in medical contexts

You're summarizing medical documents, and it’s critical that the names of patients in the summaries are accurate and consistent with the provided grounding sources.

Example API Request:

```json
{
  "domain": "Medical",
  "task": "Summarization",
  "text": "The patient name is Kevin.",
  "groundingSources": [
    "The patient name is Jane."
  ],
}
```

**Expected outcome:**

The correction feature detects that `Kevin` is ungrounded because it conflicts with the grounding source `Jane`. The API returns the corrected text: `"The patient name is Jane."`

### Question and answer (QnA) task with customer support data

You're implementing a QnA system for a customer support chatbot. It’s essential that the answers provided by the AI align with the most recent and accurate information available.

Example API Request:

```json
{
  "domain": "Generic",
  "task": "QnA",
  "qna": {
    "query": "What is the current interest rate?"
  },
  "text": "The interest rate is 5%.",
  "groundingSources": [
    "As of July 2024, the interest rate is 4.5%."
  ],
}
```
**Expected outcome:**

The API detects that `5%` is ungrounded because it doesn't match the provided grounding source `4.5%`. The response includes the correction text: `"The interest rate is 4.5%."`


### Content creation with historical data

You're creating content that involves historical data or events, where accuracy is critical to maintaining credibility and avoiding misinformation.

Example API Request:

```json
{
  "domain": "Generic",
  "task": "Summarization",
  "text": "The Battle of Hastings occurred in 1065.",
  "groundingSources": [
    "The Battle of Hastings occurred in 1066."
  ],
}
```
**Expected outcome:**

The API detects the ungrounded date `1065` and corrects it to `1066` based on the grounding source. The response includes the corrected text: `"The Battle of Hastings occurred in 1066."`


### Internal documentation summarization

You're summarizing internal documents where product names, version numbers, or other specific data points must remain consistent.

Example API Request:

```json
{
  "domain": "Generic",
  "task": "Summarization",
  "text": "Our latest product is SuperWidget v2.1.",
  "groundingSources": [
    "Our latest product is SuperWidget v2.2."
  ],
}
```

**Expected outcome:**

The correction feature identifies `SuperWidget v2.1` as ungrounded and updates it to `SuperWidget v2.2` in the response. The response returns the corrected text: `"Our latest product is SuperWidget v2.2."`