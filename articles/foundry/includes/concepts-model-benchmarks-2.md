---
title: Include file
description: Include file
author: lgayhardt
ms.reviewer: changliu2
ms.author: lagayhar
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 03/20/2026
ms.custom: include
---

## Cost benchmarks of language models

Cost calculations are estimates for using an LLM or SLM model endpoint hosted on the Foundry platform. Foundry supports displaying the cost of serverless API deployments and Azure OpenAI models. Because these costs are subject to change, cost calculations are refreshed periodically to reflect the latest pricing.

The cost of LLMs and SLMs is assessed across the following metrics:

| Metric | Description |
|--------|-------------|
| Cost per input tokens | Cost for serverless API deployment for 1 million input tokens |
| Cost per output tokens | Cost for serverless API deployment for 1 million output tokens |
| Estimated cost | Cost for the sum of cost per input tokens and cost per output tokens, with a ratio of 3:1. |

Foundry also displays the cost as follows:
             
| Metric | Description |
|-------|-------------|
| Cost | Estimated US dollar cost per 1 million tokens. The estimated workload uses the three-to-one ratio between input and output tokens. Lower values are better. |

## Scenario leaderboard benchmarking

Scenario leaderboards group benchmark datasets by common real-world evaluation goals so you can quickly identify a model's strengths and weaknesses by use case. Each scenario aggregates one or more public benchmark datasets.

Use the following table to find your use case in the **Scenario** column, then review the associated benchmark datasets and what the results indicate. The following table summarizes the available scenario leaderboards and their associated datasets and descriptions:

| Scenario | Datasets | Description |
|--|--|--|
| Standard harmful behavior | [HarmBench (standard)](https://github.com/centerforaisafety/HarmBench) | Attack success rate on standard harmful prompts. Lower is better. See [Harmful behavior detection](#harmful-behavior-detection). |
| Contextually harmful behavior | [HarmBench (contextual)](https://github.com/centerforaisafety/HarmBench) | Attack success rate on contextual harmful prompts. Lower is better. See [Harmful behavior detection](#harmful-behavior-detection). |
| Copyright violations | [HarmBench (copyright)](https://github.com/centerforaisafety/HarmBench) | Attack success rate for copyright violation prompts. Lower is better. See [Harmful behavior detection](#harmful-behavior-detection). |
| Knowledge in sensitive domains | [WMDP](https://github.com/centerforaisafety/wmdp) (biosecurity, chemical security, cybersecurity) | Accuracy across three sensitive domain subsets. Higher accuracy indicates more knowledge of sensitive capabilities. See [Sensitive domain knowledge](#sensitive-domain-knowledge). |
| Toxicity detection | [ToxiGen](https://github.com/microsoft/TOXIGEN) (annotated) | F1 score for toxic content detection ability. Higher is better. See [Toxic content detection](#toxic-content-detection). |
| Reasoning | [BIG-Bench Hard](https://github.com/suzgunmirac/BIG-Bench-Hard) (1000 subsample) | Reasoning capabilities assessment. Higher values are better. |
| Coding | [BigCodeBench](https://github.com/bigcode-project/bigcodebench) (instruct), [LiveBench (coding)](https://github.com/LiveBench/LiveBench), [LiveCodeBench medium](https://huggingface.co/datasets/livecodebench/code_generation_lite) [MBPPPlus](https://github.com/evalplus/evalplus) | Measures accuracy on code-related tasks.  Higher values are better.|
| General knowledge | [MMLU-Pro](https://github.com/TIGER-AI-Lab/MMLU-Pro) (1K English subsample) | 1,000‑example English-only subsample of MMLU-Pro. |
| Question & answering | [Arena-Hard](https://github.com/lmarena/arena-hard-auto), [GPQA](https://github.com/idavidrein/gpqa) (diamond) | Adversarial human preference QA (Arena-Hard) and graduate‑level multi‑discipline QA (GPQA diamond).  Higher values are better.|
| Math | [MATH](https://github.com/hendrycks/math) (500 subsample) | Measures mathematical reasoning capabilities of language models.  Higher values are better.|
| Groundedness | [TruthfulQA](https://github.com/sylinrl/TruthfulQA) (MC1) | Multiple‑choice groundedness / truthfulness assessment of language models.  Higher values are better.|

## Quality benchmarks of embedding models

The quality index of embedding models is defined as the averaged accuracy scores of a comprehensive set of serverless API benchmark datasets targeting Information Retrieval, Document Clustering, and Summarization tasks.

| Metric | Description |
|--------|-------------|
| Accuracy | Accuracy is the proportion of correct predictions among the total number of predictions processed. |
| F1 Score | F1 Score is the weighted mean of the precision and recall, where the best value is one (perfect precision and recall), and the worst is zero. |
| Mean average precision (MAP) | MAP evaluates the quality of ranking and recommender systems. It measures both the relevance of suggested items and how good the system is at placing more relevant items at the top. Values can range from zero to one, and the higher the MAP, the better the system can place relevant items high in the list. |
| Normalized discounted cumulative gain (NDCG) | NDCG evaluates a machine learning algorithm's ability to sort items based on relevance. It compares rankings to an ideal order where all relevant items are at the top of the list, where k is the list length while evaluating ranking quality. In these benchmarks, k=10, indicated by a metric of `ndcg_at_10`, meaning that the top 10 items are evaluated. |
| Precision | Precision measures the model's ability to identify instances of a particular class correctly. Precision shows how often a machine learning model is correct when predicting the target class. |
| Spearman correlation | Spearman correlation based on cosine similarity is calculated by first computing the cosine similarity between variables, then ranking these scores and using the ranks to compute the Spearman correlation. |
| V measure | V measure is a metric used to evaluate the quality of clustering. V measure is calculated as a harmonic mean of homogeneity and completeness, ensuring a balance between the two for a meaningful score. Possible scores lie between zero and one, with one being perfectly complete labeling. |

## Calculation of scores

### Individual scores

Benchmark results originate from public datasets that are commonly used for language model evaluation. In most cases, the data is hosted in GitHub repositories maintained by the creators or curators of the data. Foundry evaluation pipelines download data from their original sources, extract prompts from each example row, generate model responses, and then compute relevant accuracy metrics.
             
Prompt construction follows best practices for each dataset, as specified by the paper introducing the dataset and industry standards. In most cases, each prompt contains several _shots_, that is, several examples of complete questions and answers to prime the model for the task. The number of shots varies by dataset and follows the methodology specified in each dataset's original publication. The evaluation pipelines create shots by sampling questions and answers from a portion of the data held out from evaluation.

## Benchmark limitations

All benchmarks have inherent limitations that you should consider when interpreting results:

- **Quality benchmarks**: Benchmark datasets can become saturated over time as models are trained or tuned on similar data. Evaluation results might also vary depending on prompt construction and the number of few-shot examples used.
- **Performance benchmarks**: Metrics are collected using synthetic workloads with a fixed input-to-output token ratio and single-region deployments. Real-world performance might differ based on workload patterns, concurrency, region, and deployment configuration.
- **Cost benchmarks**: Cost estimates are based on a three-to-one input-to-output token ratio and current pricing at the time of measurement. Actual costs depend on your workload and are subject to pricing changes.
