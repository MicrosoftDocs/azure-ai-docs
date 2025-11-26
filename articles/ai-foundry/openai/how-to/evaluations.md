---
title: 'How to use Azure OpenAI in Microsoft Foundry Models evaluation'
titleSuffix: Azure OpenAI
description: Learn how to use evaluations with Azure OpenAI
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
ms.custom: references_regions
ms.date: 11/26/2025
author: mrbullwinkle
ms.author: mbullwin
zone_pivot_groups: openai-fine-tuning
recommendations: false
---

# Azure OpenAI Evaluation (Preview)

[!INCLUDE [classic-banner](../../includes/classic-banner.md)]

The evaluation of large language models is a critical step in measuring their performance across various tasks and dimensions. This is especially important for fine-tuned models, where assessing the performance gains (or losses) from training is crucial. Thorough evaluations can help your understanding of how different versions of the model may impact your application or scenario.

Azure OpenAI evaluation enables developers to create evaluation runs to test against expected input/output pairs, assessing the model’s performance across key metrics such as accuracy, reliability, and overall performance.

## Evaluation support

### Regional availability

- Australia East
- Brazil South
- Canada Central
- Central US
- East US 2
- France Central
- Germany West Central
- Italy North
- Japan East
- Japan West
- Korea Central
- North Central US
- Norway East
- Poland Central
- South Africa North
- Southeast Asia
- Spain Central
- Sweden Central
- Switzerland North
- Switzerland West
- UAE North
- UK South
- UK West
- West Europe
- West US
- West US 2
- West US 3

If your preferred region is missing, refer to [Azure OpenAI regions](/azure/ai-foundry/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#global-standard-model-availability) and check if it is one of the Azure OpenAI regional availability zones.

### Supported deployment types

- Standard
- Global standard
- Data zone standard
- Provisioned-managed
- Global provisioned-managed
- Data zone provisioned-managed

## Evaluation API (preview)

Evaluation API lets you test model outputs directly through API calls, and programmatically assess model quality and performance. To use Evaluation API, check out the [REST API documentation](/azure/ai-foundry/openai/authoring-reference-preview#evaluation---get-list). 

## Evaluation pipeline

### Test data

You need to assemble a ground truth dataset that you want to test against. Dataset creation is typically an iterative process that ensures your evaluations remain relevant to your scenarios over time. This ground truth dataset is typically handcrafted and represents the expected behavior from your model. The dataset is also labeled and includes the expected answers.

> [!NOTE]
> Some evaluation tests like **Sentiment** and **valid JSON or XML** do not require ground truth data.

Your data source needs to be in JSONL format. Below are two examples of the JSONL evaluation datasets:

### Evaluation format

# [Question & Answer Evaluation](#tab/question-eval-input)

```jsonl
{"question": "Find the degree for the given field extension Q(sqrt(2), sqrt(3), sqrt(18)) over Q.", "subject": "abstract_algebra", "A": "0", "B": "4", "C": "2", "D": "6", "answer": "B", "completion": "B"}
{"question": "Let p = (1, 2, 5, 4)(2, 3) in S_5 . Find the index of <p> in S_5.", "subject": "abstract_algebra", "A": "8", "B": "2", "C": "24", "D": "120", "answer": "C", "completion": "C"}
{"question": "Find all zeros in the indicated finite field of the given polynomial with coefficients in that field. x^5 + 3x^3 + x^2 + 2x in Z_5", "subject": "abstract_algebra", "A": "0", "B": "1", "C": "0,1", "D": "0,4", "answer": "D", "completion": "D"}
```

When you upload and select your evaluation file a preview of the first three lines will be returned:

:::image type="content" source="../media/how-to/evaluations/question-input.png" alt-text="Screenshot that shows a preview of an uploaded evaluation training file for question and answer pairs." lightbox="../media/how-to/evaluations/question-input.png":::

# [Chat Completions](#tab/summarization-input)

```jsonl
{"input": [{"role": "system", "content": "Provide a clear and concise summary of the technical content, highlighting key concepts and their relationships. Focus on the main ideas and practical implications."}, {"role": "user", "content": "Tokenization is a key step in preprocessing for natural language processing, involving the division of text into smaller components called tokens. These can be words, subwords, or characters, depending on the method chosen. Word tokenization divides text at word boundaries, while subword techniques like Byte Pair Encoding (BPE) or WordPiece can manage unknown words by breaking them into subunits. Character tokenization splits text into individual characters, useful for multiple languages and misspellings. The tokenization method chosen greatly affects model performance and its capacity to handle various languages and vocabularies."}], "output": "Tokenization divides text into smaller units (tokens) for NLP applications, using word, subword (e.g., BPE), or character methods. Each has unique benefits, impacting model performance and language processing capabilities."}      
{"input": [{"role": "system", "content": "Create a comprehensive yet concise summary that captures the essential technical details and significance of the topic."}, {"role": "user", "content": "Self-attention mechanisms are vital in modern transformer models, allowing them to evaluate the relevance of different parts of an input sequence when processing each element. In self-attention, each position in a sequence learns to focus on all other positions, forming a weighted sum of their values. Attention weights are derived using queries, keys, and values, with compatibility between a query and key determining attention to each value. This mechanism enables capturing long-range dependencies and relationships within a sequence, making it effective for tasks needing context understanding and inter-part relationships."}], "output": "Self-attention is crucial in transformers, enabling each sequence position to evaluate and collect data from all others. It uses queries, keys, and values for attention weights, effectively capturing long-range dependencies and contextual links."}      
{"input": [{"role": "system", "content": "Synthesize the technical information into a brief, accurate summary that maintains the core concepts and their significance."}, {"role": "user", "content": "The transformer architecture significantly changed natural language processing by introducing a new method for sequence processing. Unlike recurrent neural networks, transformers process whole sequences at once using self-attention. The architecture consists of an encoder and decoder, each with multiple layers of multi-head attention, feed-forward networks, and normalization layers. The encoder processes the input sequence, and the decoder produces the output sequence. Positional encodings are added to retain sequence order information since the model lacks inherent sequence position awareness. This architecture underlies many leading language models like BERT and GPT."}], "output": "Transformers are a transformative neural architecture processing sequences with self-attention instead of recurrence. Their encoder-decoder design, with multi-head attention and position encodings, is fundamental to modern language models like BERT and GPT."}      
```

When you upload and select you evaluation file a preview of the first three lines will be returned:

:::image type="content" source="../media/how-to/evaluations/summarization-input.png" alt-text="Screenshot that shows a preview of an uploaded evaluation training file for summarization tasks." lightbox="../media/how-to/evaluations/summarization-input.png":::

---

You can choose any existing previously uploaded datasets, or upload a new dataset.

### Create responses (optional)

The prompt you use in your evaluation should match the prompt you plan to use in production. These prompts provide the instructions for the model to follow. Similar to the playground experiences, you can create multiple inputs to include few-shot examples in your prompt. For more information, see [prompt engineering techniques](../concepts/advanced-prompt-engineering.md) for details on some advanced techniques in prompt design and prompt engineering.

You can reference your input data within the prompts by using the `{{input.column_name}}` format, where column_name corresponds to the names of the columns in your input file.

Outputs generated during the evaluation will be referenced in subsequent steps using the `{{sample.output_text}}` format.

> [!NOTE]
> You need to use double curly braces to make sure you reference to your data correctly.

### Model deployment

In Azure OpenAI, you need to create a model deployment to use for your evaluation. You can pick and deploy a single model, or multiple models, depending on your needs. These model deployments will be used when grading your base model or your fine-tuned model with the test criteria of your choice. You can also use the deployed models to auto-generate responses for your provided prompt. 

The deployments available in your list depend on those you created within your Azure OpenAI resource. If you can't find the desired deployment, you can create a new one from the Azure OpenAI Evaluation page.

### Testing criteria

Testing criteria is used to assess the effectiveness of each output generated by the target model. These tests compare the input data with the output data to ensure consistency. You have the flexibility to configure different criteria to test and measure the quality and relevance of the output at different levels.

:::image type="content" source="../media/how-to/evaluations/eval-testing-criteria.png" alt-text="Screenshot that shows the different testing criteria selections." lightbox="../media/how-to/evaluations/eval-testing-criteria.png":::

When you click into each testing criteria, you will see different types of graders as well as preset schemas that you can modify per your own evaluation dataset and criteria. 

:::image type="content" source="../media/how-to/evaluations/eval-testing-criteria-2.png" alt-text="Screenshot that shows the evaluations testing criteria options." lightbox="../media/how-to/evaluations/eval-testing-criteria-2.png":::

## Getting started

::: zone pivot="programming-language-studio"

[!INCLUDE [Microsoft Foundry portal fine-tuning](../includes/evaluation-foundry.md)]

::: zone-end

::: zone pivot="programming-language-python"

[!INCLUDE [Python SDK fine-tuning](../includes/evaluation-python.md)]

::: zone-end

::: zone pivot="rest-api"

[!INCLUDE [REST API fine-tuning](../includes/evaluation-rest.md)]

::: zone-end

## Types of Testing Criteria

Azure OpenAI Evaluation offers various evaluation testing criteria on top of Semantic Similarity we saw in the provided example. This section provides information about each testing criteria at much more detail.

### Factuality

Assesses the factual accuracy of a submitted answer by comparing it against an expert answer.

Factuality evaluates the factual accuracy of a submitted answer by comparing it to an expert answer. Utilizing a detailed chain-of-thought (CoT) prompt, the grader determines whether the submitted answer is consistent with, a subset of, a superset of, or in conflict with the expert answer. It disregards differences in style, grammar, or punctuation, focusing solely on factual content. Factuality can be useful in many scenarios including but not limited to content verification and educational tools ensuring the accuracy of answers provided by AI.

:::image type="content" source="../media/how-to/evaluations/factuality.png" alt-text="Screenshot of the factuality testing criteria." lightbox="../media/how-to/evaluations/factuality.png":::

You can view the prompt text that is used as part of this testing criteria by selecting the dropdown next to the prompt. The current prompt text is:

```text
Prompt
You are comparing a submitted answer to an expert answer on a given question.
Here is the data:
[BEGIN DATA]
************
[Question]: {input}
************
[Expert]: {ideal}
************
[Submission]: {completion}
************
[END DATA]
Compare the factual content of the submitted answer with the expert answer. Ignore any differences in style, grammar, or punctuation.
The submitted answer may either be a subset or superset of the expert answer, or it may conflict with it. Determine which case applies. Answer the question by selecting one of the following options:
(A) The submitted answer is a subset of the expert answer and is fully consistent with it.
(B) The submitted answer is a superset of the expert answer and is fully consistent with it.
(C) The submitted answer contains all the same details as the expert answer.
(D) There is a disagreement between the submitted answer and the expert answer.
(E) The answers differ, but these differences don't matter from the perspective of factuality.
```

### Semantic similarity

Measures the degree of similarity between model's response and the reference. `Grades: 1 (completely different) - 5 (very similar)`.

:::image type="content" source="../media/how-to/evaluations/semantic-similarity.png" alt-text="Screenshot of the semantic similarity testing criteria." lightbox="../media/how-to/evaluations/semantic-similarity.png":::

### Sentiment

Attempts to identify the emotional tone of the output.

:::image type="content" source="../media/how-to/evaluations/sentiment.png" alt-text="Screenshot of the sentiment testing criteria." lightbox="../media/how-to/evaluations/sentiment.png":::

You can view the prompt text that is used as part of this testing criteria by selecting the dropdown next to the prompt. The current prompt text is:

```text
Prompt
You will be presented with a text generated by a large language model. Your job is to rate the sentiment of the text. Your options are:

A) Positive
B) Neutral
C) Negative
D) Unsure

[BEGIN TEXT]
***
[{text}]
***
[END TEXT]

First, write out in a step by step manner your reasoning about the answer to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then print only the single character (without quotes or punctuation) on its own line corresponding to the correct answer. At the end, repeat just the letter again by itself on a new line
```

### String check

Verifies if the output matches the expected string exactly.

:::image type="content" source="../media/how-to/evaluations/string-check.png" alt-text="Screenshot of the string check testing criteria." lightbox="../media/how-to/evaluations/string-check.png":::

String check performs various binary operations on two string variables allowing for diverse evaluation criteria. It helps with verifying various string relationships, including equality, containment, and specific patterns. This evaluator allows for case-sensitive or case-insensitive comparisons. It also provides specified grades for true or false results, allowing customized evaluation outcomes based on the comparison result. Here's the type of operations supported:
- `equals`: Checks if the output string is exactly equal to the evaluation string.
- `contains`: Checks if the evaluation string is a substring of output string.
- `starts-with`: Checks if the output string starts with the evaluation string.
- `ends-with`: Checks if the output string ends with the evaluation string.

> [!NOTE]
> When setting certain parameters in your testing criteria, you have the option to choose between the *variable* and the *template*. Select *variable* if you want to refer to a column in your input data. Choose *template* if you want to provide a fixed string.

### Valid JSON or XML

Verifies if the output is valid JSON or XML.

:::image type="content" source="../media/how-to/evaluations/valid-json.png" alt-text="Screenshot of the valid json or XML testing criteria." lightbox="../media/how-to/evaluations/valid-json.png":::

### Matches schema

Ensures the output follows the specified structure.

:::image type="content" source="../media/how-to/evaluations/matches-schema.png" alt-text="Screenshot of the matches schema testing criteria." lightbox="../media/how-to/evaluations/matches-schema.png":::

### Criteria match

Assess if model's response matches your criteria. Grade: Pass or Fail.

:::image type="content" source="../media/how-to/evaluations/criteria-match.png" alt-text="Screenshot of the matches criteria test." lightbox="../media/how-to/evaluations/criteria-match.png":::

You can view the prompt text that is used as part of this testing criteria by selecting the dropdown next to the prompt. The current prompt text is:

```text
Prompt
Your job is to assess the final response of an assistant based on conversation history and provided criteria for what makes a good response from the assistant. Here is the data:

[BEGIN DATA]
***
[Conversation]: {conversation}
***
[Response]: {response}
***
[Criteria]: {criteria}
***
[END DATA]

Does the response meet the criteria? First, write out in a step by step manner your reasoning about the criteria to be sure that your conclusion is correct. Avoid simply stating the correct answers at the outset. Then print only the single character "Y" or "N" (without quotes or punctuation) on its own line corresponding to the correct answer. "Y" for yes if the response meets the criteria, and "N" for no if it does not. At the end, repeat just the letter again by itself on a new line.
Reasoning:
```

### Text quality

Evaluate quality of text by comparing to reference text.

:::image type="content" source="../media/how-to/evaluations/text-quality-general.png" alt-text="Screenshot of the text quality testing criteria." lightbox="../media/how-to/evaluations/text-quality-general.png":::

**Summary:**

- BLEU Score: Evaluates the quality of generated text by comparing it against one or more high-quality reference translations using the BLEU score.
- ROUGE Score: Evaluates the quality of generated text by comparing it to reference summaries using ROUGE scores.
- Cosine: Also referred to as cosine similarity measures how closely two text embeddings—such as model outputs and reference texts—align in meaning, helping assess the semantic similarity between them. This is done by measuring their distance in vector space.

**Details:**

BLEU (BiLingual Evaluation Understudy) score is commonly used in natural language processing (NLP) and machine translation. It's widely used in text summarization and text generation use cases. It evaluates how closely the generated text matches the reference text. The BLEU score ranges from 0 to 1, with higher scores indicating better quality.

ROUGE (Recall-Oriented Understudy for Gisting Evaluation) is a set of metrics used to evaluate automatic summarization and machine translation. It measures the overlap between generated text and reference summaries. ROUGE focuses on recall-oriented measures to assess how well the generated text covers the reference text.
The ROUGE score provides various metrics, including:

- ROUGE-1: Overlap of unigrams (single words) between generated and reference text.
- ROUGE-2: Overlap of bigrams (two consecutive words) between generated and reference text.
- ROUGE-3: Overlap of trigrams (three consecutive words) between generated and reference text.
- ROUGE-4: Overlap of four-grams (four consecutive words) between generated and reference text.
- ROUGE-5: Overlap of five-grams (five consecutive words) between generated and reference text.
- ROUGE-L: Overlap of L-grams (L consecutive words) between generated and reference text.

Text summarization and document comparison are among optimal use cases for ROUGE, particularly in scenarios where text coherence and relevance are critical.

Cosine similarity measures how closely two text embeddings—such as model outputs and reference texts—align in meaning, helping assess the semantic similarity between them. Same as other model-based evaluators, you need to provide a model deployment using for evaluation. 

> [!IMPORTANT]
> Only embedding models are supported for this evaluator:
>
> -	`text-embedding-3-small`
> -	`text-embedding-3-large`
> -	`text-embedding-ada-002`

### Custom prompt

Uses the model to classify the output into a set of specified labels. This evaluator uses a custom prompt that you'll need to define.

:::image type="content" source="../media/how-to/evaluations/custom-prompt.png" alt-text="Screenshot of the custom prompt testing criteria." lightbox="../media/how-to/evaluations/custom-prompt.png":::
