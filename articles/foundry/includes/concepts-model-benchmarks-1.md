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

## Model benchmarking scope

The model leaderboards feature a curated selection of text-based language models from the Foundry model catalog. Models are included based on the following criteria:

- **Azure Direct Models prioritized**: Azure Direct Models are selected for relevance to common generative AI scenarios.
- **Core benchmark applicability**: Models must support general-purpose language tasks such as reasoning, knowledge, question answering, mathematical reasoning, and coding. Specialized models (for example, protein folding or domain-specific QA) and other modalities aren't supported.

This scoping ensures the leaderboards reflect current, high-quality models relevant to core AI scenarios.

## Interpret leaderboard results

The leaderboards help you compare models across multiple dimensions so you can choose the right model for your use case. Here are some guidelines for interpreting the results:

- **Quality index**: A higher quality index indicates stronger overall performance across reasoning, coding, math, and knowledge tasks. Compare the quality index across models to identify top performers for general-purpose language tasks.
- **Safety scores**: Lower attack success rates indicate more robust models. Consider safety scores alongside quality scores, especially for customer-facing applications where harmful output is a significant concern.
- **Performance trade-offs**: Use the latency and throughput metrics to understand the real-world responsiveness of a model. A model with high quality but high latency might not suit real-time applications.
- **Cost considerations**: The estimated cost metric uses a three-to-one input-to-output token ratio. Adjust your expectations based on your actual workload's input-to-output ratio.
- **Scenario leaderboards**: If your use case maps to a specific scenario (for example, coding or math), start with the scenario leaderboard to find models optimized for that task rather than relying solely on the overall quality index.

> [!TIP]
> Leaderboard benchmarks provide standardized comparisons across models using public datasets. To evaluate model performance on your specific data and use case, see [Evaluate your generative AI apps](../how-to/evaluate-generative-ai-app.md).

## Quality benchmarks of language models

Foundry assesses the quality of LLMs and SLMs using accuracy scores from standard benchmark datasets that measure reasoning, knowledge, question answering, math, and coding capabilities.

| Index | Description |
|--|--|
| Quality index | Calculated by averaging applicable accuracy scores (`exact_match`, `pass@1`, `arena_hard`) across benchmark datasets. |

Quality index values range from zero to one, where higher values indicate better performance. The datasets included in the quality index are:

| Dataset Name | Category |
|--|--|
| [arena_hard](https://github.com/lmarena/arena-hard-auto) | QA |
| [bigbench_hard](https://github.com/suzgunmirac/BIG-Bench-Hard) (downsampled to 1,000 examples) | Reasoning |
| [gpqa](https://github.com/idavidrein/gpqa) | QA |
| [humanevalplus](https://github.com/evalplus/evalplus) | Coding |
| [ifeval](https://github.com/google-research/google-research/tree/master/instruction_following_eval) | Reasoning |
| [math](https://github.com/hendrycks/math) | Math |
| [mbppplus](https://github.com/evalplus/evalplus) | Coding |
| [mmlu_pro](https://github.com/TIGER-AI-Lab/MMLU-Pro) (downsampled to 1,000 examples) | General knowledge |

See more details in accuracy scores:

| Metric | Description |
|--|--|
| Accuracy | Accuracy scores are available at the dataset and the model levels. At the dataset level, the score is the average value of an accuracy metric computed over all examples in the dataset. The accuracy metric used is `exact_match` in all cases, except for the _HumanEval_ and _MBPP_ datasets that use a `pass@1` metric. Exact match compares model generated text with the correct answer according to the dataset, reporting one if the generated text matches the answer exactly and zero otherwise. The `pass@1` metric measures the proportion of model solutions that pass a set of unit tests in a code generation task. At the model level, the accuracy score is the average of the dataset-level accuracies for each model. |

Accuracy scores range from zero to one, where higher values are better.

## Safety benchmarks of language models

Safety benchmarks are selected through a structured filtering and validation process designed to ensure both relevance and rigor. A benchmark qualifies for onboarding if it addresses high-priority risks. The safety leaderboards include benchmarks that are reliable enough to provide meaningful signals on topics of interest as they relate to safety. The leaderboards use [HarmBench](https://github.com/centerforaisafety/HarmBench) to proxy model safety, and organize scenario leaderboards as follows:

| Dataset Name | Leaderboard Scenario | Metric | Interpretation |
|--|--|--|--|
| HarmBench (standard) | Standard harmful behaviors | Attack Success Rate | Lower values mean better robustness against attacks designed to elicit standard harmful content |
| HarmBench (contextual) | Contextually harmful behaviors | Attack Success Rate | Lower values mean better robustness against attacks designed to elicit contextually harmful content |
| HarmBench (copyright violations) | Copyright violations | Attack Success Rate | Lower values indicate stronger robustness against copyright violations |
| WMDP | Knowledge in sensitive domains | Accuracy | Higher values indicate greater knowledge in sensitive domains |
| Toxigen | Toxic content detection | F1 Score | Higher values indicate better detection performance |

### Harmful behavior detection

The [HarmBench](https://github.com/centerforaisafety/HarmBench) benchmark measures harmful behaviors using prompts designed to elicit unsafe responses. It covers seven semantic categories:

- Cybercrime and unauthorized intrusion
- Chemical and biological weapons or drugs
- Copyright violations
- Misinformation and disinformation
- Harassment and bullying
- Illegal activities
- General harm

These categories are grouped into three functional areas:

- Standard harmful behaviors
- Contextually harmful behaviors
- Copyright violations

Each functional category is featured in a separate scenario leaderboard. The evaluation uses direct prompts from HarmBench (no attacks) and HarmBench evaluators to calculate Attack Success Rate (ASR). Lower ASR values mean safer models. No attack strategies are used for evaluation, and model benchmarking is performed with Foundry Guardrails (previously content filters) turned off.

### Toxic content detection

[Toxigen](https://github.com/microsoft/TOXIGEN) is a large-scale dataset for detecting adversarial and implicit hate speech. It includes implicitly toxic and benign sentences referencing 13 minority groups. Foundry uses annotated Toxigen samples and calculates F1 scores to measure classification performance. Higher scores indicate better toxic content detection. Benchmarking is performed with Foundry Guardrails (previously content filters) turned off.

### Sensitive domain knowledge

The [Weapons of Mass Destruction Proxy](https://github.com/centerforaisafety/wmdp) (WMDP) benchmark measures model knowledge in sensitive domains including biosecurity, cybersecurity, and chemical security. The leaderboard uses average accuracy scores across cybersecurity, biosecurity, and chemical security. A higher WMDP accuracy score denotes more knowledge of dangerous capabilities (worse behavior from a safety standpoint). Model benchmarking is performed with the default Foundry Guardrails (previously content filters) on. These guardrails detect and block content harm in violence, self-harm, sexual, hate, and unfairness, but don't target categories in cybersecurity, biosecurity, and chemical security.

### Limitations of safety benchmarks

Safety is a complex topic with several dimensions. No single open-source benchmark can test or represent the full safety of a system across all scenarios. Additionally, many benchmarks suffer from saturation or misalignment between benchmark design and risk definition. Some benchmarks also lack clear documentation on how targets risks are conceptualized and operationalized, making it difficult to assess whether results accurately capture the nuances of real-world risks. These limitations can lead to either overestimating or underestimating model performance in real-world safety scenarios.
