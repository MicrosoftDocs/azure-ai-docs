---
title: "Reinforcement fine-tuning"
description: Learn how to use reinforcement fine-tuning with reasoning models
author: mrbullwinkle
ms.author: mbullwin
manager: nitinme
ms.date: 02/11/2026
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: how-to
monikerRange: 'foundry-classic || foundry'
ms.custom:
  - build-2025
ai-usage: ai-assisted
---

# Reinforcement fine-tuning

Reinforcement fine-tuning (RFT) is a technique for improving reasoning models by training them through a reward-based process, rather than relying only on labeled data. RFT helps models develop better reasoning and problem-solving skills, especially in cases where labeled examples are limited or complex behaviors are desired.

> [!NOTE]
> The fine-tuning service automatically pauses RFT jobs once they hit $5,000 in total training costs (training + grading). You can deploy the most recent checkpoint or resume the training job. If you decide to resume the job, billing continues for the job with no further cost-based limits.


## Model support

Reinforcement fine-tuning is supported for the following models:

| Model | Version | RFT support | Status |
|-------|---------|-------------|--------|
| `o4-mini` | `2025-04-16` | Yes | GA |
| `gpt-5` | `2025-08-07` | Yes | Private preview |

> [!NOTE]
> GPT-5 support for reinforcement fine-tuning is in private preview and might not be available in your subscription.

## Requirements

Reinforcement fine-tuning (RFT) requires training and validation data formatted as JSONL and containing a `messages` array using the chat completions format.

However, RFT has more requirements:

- **Data**
  - The final "message" in the data must be assigned a `user` role.
  - The data can contain extra fields and values for use by a grader.
  - Both a training and a validation dataset must be provided.
- **Graders** 
  - A grader must be defined to score the quality of your fine-tuned model and guide learning.
  - Only a single grader can be provided, but multiple graders can be combined using a multigrader.

## Example training data

The following example shows how to present prompts to the model and include ground truth accessible to a grader.

```json
{
  "messages": [
    {
      "role": "developer",
      "content": "Your task is to solve logic puzzles. The user will provide an expression with ?'s as placeholders for arithmetic operations. Replace the ?'s with arithmetic operation signs (+, -, *, /) to obtain a valid equation."
    },
    {
      "role": "user",
      "content": "1 ? 2 ? 3 ? 4 ? 5 ? 6 ? 7 ? 8 ? 9 = 100"
    }
  ],
  "solution": "1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 * 9 = 100"
}
```

> [!NOTE] 
> This example is split across multiple lines for demonstration purposes only. It must be a single line in your JSONL file.

## Graders

Graders provide the reward function used during training and have access to any user-supplied fields in the dataset. Multiple types of graders are available:

- **text comparison**: score response content based on its text
- **model**: score responses using a language model and prompt
- **custom code**: score responses using custom code
- **multigrader**: score based on a combination of scores from other graders

Most graders perform substitution of runtime data via templates. Any input or reference properties can include variable substitution enclosed in double curly braces (`{{ }}`) containing a reference to a variable.

Each template reference must be namespaced using a pattern like `{{ namespace.variable }}`. For any complex, nested data, a JSON-path like syntax is supported.

The following namespaces are supported:

- `sample` - model output to be graded appears under the `sample` namespace in a format similar to a chat completions response.
- `item` - optional, extra fields provided in training data appear under the `item` namespace.

Some examples of template substitution that use the above namespaces:

- `{{ sample.output_text }}` - substitute the model output as a string
- `{{ sample.output_json }}` - if the model produced structured outputs, reference it as JSON
- `{{ item.answer }}` - substitute the "answer" field in the dataset
- `{{ item.ground_truth.date }}` - substitute the "date" field of a "ground_truth" object defined in the dataset

The following sections document individual graders and provide their JSON specification for defining via the API.

### Text comparison graders

Use text comparison graders when the use case requires the model output either a definitive label or if the output must resemble a known ground truth answer.

#### String-check-grader 

String-check graders apply a given operation to the input and a reference to return a `0` or `1`, providing a simple pass/fail function.

```json
{
    "type": "string_check",
    "name": string,
    "operation": "eq" | "ne" | "like" | "ilike",
    "input": string,
    "reference": string,
}
```

*Operations:*

| Operation | Returns 1 when | Case-sensitive |
|-----------|----------------|----------------|
| `eq` | Input matches reference | Yes |
| `ne` | Input doesn't match reference | Yes |
| `like` | Input contains reference | Yes |
| `ilike` | Input contains reference | No |

#### Text similarity

Text-similarity graders compute a score based on a select algorithm for quantifying similarity between the input text and a given reference text.

**Specification:**

```json
{
    "type": "text_similarity",
    "name": string,
    "input": string,
    "reference": string,
    "pass_threshold": number,
    "evaluation_metric": "fuzzy_match" | "bleu" | "gleu" | "meteor" | "rouge_1" | "rouge_2" | "rouge_3" | "rouge_4" | "rouge_5" | "rouge_l" 
}
```

*Evaluation metrics:*
- `fuzzy_match` – fuzzy string match, using the *RapidFuzz* algorithm
- `bleu` – computes BLEU (bilingual evaluation understudy) score between strings
- `gleu` – computes Google BLEU score between strings
- `meteor` – computes METEOR score between strings
- `rouge-*` - as defined by the rouge python library

### Model graders

Model graders take a prompt to a grader model instructing it how to evaluate and score a given response. This flexibility allows for prompt engineering complex graders that support explaining the reason for a given score.

The following models can be used as model graders:

| Model | Can be used as grader |
|-------|-----------------------|
| `gpt-4o-2024-08-06` | Yes |
| `o3-mini-2025-01-31` | Yes |

> [!NOTE]
> Model graders don't require model deployments in Foundry.

### Score model

Score model graders output a numeric score based on their given input and prompt. Any provided `sampling_params` control the behavior of the scoring model and allow for customizing things like temperature and reasoning effort.

```json
{
    "type": "score_model",
    "name": string,
    "input": Message[],
    "model": string,
    "pass_threshold": number,
    "range": number[],
    "sampling_params": object
}
```

### Code graders

Model graders are flexible but nondeterministic. When you need deterministic scoring, use code graders instead.

### Python grader

The Python grader allows you to execute arbitrary Python code to produce a score. 

The provided code must define a `grade` function expecting two positional arguments: `sample` and `item`. The function must return a numeric score.

```json
{
    "type": "python",
    "name": string,
    "source": "def grade(sample, item):\n    return 1.0"
}
```

The Python code executes in a constrained environment with the following limitations:

| Resource | Limit |
|----------|-------|
| Code size | 256 KB |
| Network | No access |
| Memory | 2 GB |
| Disk space | 1 GB |
| CPU | 1 core |
| Runtime | 2 minutes |

> [!TIP]
> Your code should handle any possible errors and always return a numeric value. If too many exceptions occur during the execution of the grader, the training job fails.

Within the Python runtime, the following modules and versions are made available for use by the provided code:

- numpy==2.2.4
- scipy==1.15.2
- sympy==1.13.3
- pandas==2.2.3
- rapidfuzz==3.10.1
- scikit-learn==1.6.1
- rouge-score==0.1.2
- deepdiff==8.4.2
- jsonschema==4.23.0
- pydantic==2.10.6
- pyyaml==6.0.2
- nltk==3.9.1
- sqlparse==0.5.3
- rdkit==2024.9.6
- scikit-bio==0.6.3
- ast-grep-py==0.36.2

### Endpoint grader (preview)

Endpoint graders call a remote endpoint via an HTTP API to score the model response. They're ideal for use cases requiring access to ground truth for accurate scoring or the ability to implement the grader in a language other than Python.

> While in private preview, the API for endpoint graders remains unpublished.

### Multigrader

A multigrader combines the output of multiple graders to produce a single score based on an arithmetic expression provided in `calculate_output`.

```json
{  
  "type": "multi",
  "name": string,
  "graders": dict[str, Grader],
  "calculate_output": string
}
```

When a multigrader computes the score, the `calculate_output` expression references the individual scores from the provided `graders` by the key in the `graders` object.

*Operators:*

| Operator | Description |
|----------|-------------|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `^` | Power |

*Functions:*

| Function | Description |
|----------|-------------|
| `min` | Compute the minimum of a value |
| `max` | Compute the maximum of a value |
| `abs` | Compute the absolute value |
| `floor` | Round the value down |
| `ceil` | Round the value up |
| `exp` | Compute `e` to the power of the provided value |
| `sqrt` | Take the square root of the value |
| `log` | Compute the logarithm of the provided value |

As an example, a multigrader defined with two graders, "similarity-score" and "label-checker," that must average their outputs could look like:

```json
{
  "type": "multi",
  "name": "Example multigrader",
  "graders": {
    "similarity_score": {
      "type": "text_similarity",
      "name": "similarity grader",
      "input": "{{ sample.output_text }}",
      "reference": "{{ item.summary }}",
      "evaluation_metric": "bleu"
    },
    "label_checker": {
      "type": "string_check",
      "name": "label grader",
      "input": "{{ sample.output_text }}",
      "reference": "{{ item.label }}",
      "operation": "eq"
    }
  },
  "calculate_output": "(similarity_score + label_checker) / 2"
}
```

## Response format (optional)

The model can be made to produce structured outputs during training either to align to the intended use case of the model or to make grading the output easier.

The response format configuration follows the same specification as Chat Completions, either supporting text (the default) or JSON. When the model should output JSON, a JSON Schema must be provided.

To continue with the previous [example](#example-training-data), if the model must output the response in a structured format such as:

```json
{ "solution": "1 + 2 + 3 + 4 + 5 + 6 + 7 + 8 * 9 = 100" }
```

The following JSON schema describes the response format:

```json
{
  "type": "json_schema",
  "name": "puzzles_assistant",
  "schema": {
    "type" : "object",
    "properties": {
      "solution": {
        "type": "string",
        "title": "solution"
      }
    },
    "required": [
      "solution",
    ],
    "additionalProperties": false
  },
  "strict": true
}
```

## Hyperparameter selection

Reinforcement fine-tuning supports the same hyperparameters as Supervised fine-tuning. Additionally, the following hyperparameters control features specific to RFT:

| Hyperparameter name | Value | Default | Description |
|----|----|----|----|
|`eval_interval` | integer | `auto` | The number of training steps between evaluation runs. |
|`eval_samples` | integer | `auto` | The number of samples to use during evaluation. |
|`compute_multiplier` | number | `auto` | The multiplier on amount of compute use for exploring space during training. |
|`reasoning_effort`| `low`, `medium`, `high` | `medium` | The reasoning effort used by the model during training. |

> [!NOTE]
> The training service automatically replaces hyperparameters set to `auto` with defaults based on heuristics on the provided training data.


## Interpreting training results

Reinforcement fine-tuning provides both automatic evaluations of the model during training and real-time training metrics.

### Training metrics

When you monitor a running job or inspecting a completed job, the "reward" and "reasoning" metrics provide an indicator of training success.

#### Reward

Reward metrics track the resulting scores from the grader acting as the reward function.

- `train_reward_mean`: the average reward across the batch of training data at a given step. Because each batch might be different across steps, the trend of this metric is more important than comparing values across steps.
- `valid_reward_mean`: The average reward across the samples taken from the validation set at a given step.

Reward metrics should generally increase over the course of the training job. If they diverge significantly, it's a sign the model might be *reward hacking* and the grader requires more engineering.

#### Reasoning tokens

Each training job tracks the number of reasoning tokens produced by the model. Reasoning token metrics captures how the model changes its behavior over the lifetime of the training job.

- `train_reasoning_tokens_mean`: the average number of reasoning tokens produced across the batch of training data at a given step.
- `valid_reasoning_tokens_mean`: the average number of reasoning tokens produced across the validation data at a given step.

The model might learn to use fewer reasoning tokens to achieve the same reward, or it might learn to use more reasoning tokens to achieve a higher reward. These metrics typically rise and fall during the training job.

### Automatic evaluations

An evaluation is created automatically for each RFT job. At regular intervals defined by the `eval_interval` hyperparameter, the training system executes an evaluation run using the validation data. Scores for each run are available via the linked evaluation, discoverable from the Foundry user interface.

Inspecting these evaluations provides an extra data point for deciding on early-stopping. If the model exhibits learning during training, the results of each evaluation run should improve over the lifetime of the job.


## Example projects and datasets

The following example demos and datasets provide starting points for new users of reinforcement fine-tuning:

- [Countdown Demo](https://github.com/azure-ai-foundry/fine-tuning/tree/main/Demos/RFT_Countdown) - end-to-end demo of using RFT to improve mathematical reasoning.
- [MedMCQ](https://github.com/azure-ai-foundry/fine-tuning/tree/main/Sample_Datasets/Reinforcement_Fine_Tuning/MedMCQ) - sample dataset and graders for answering multiple-choice questions from the medical domain.
- [ClauseMatching](https://github.com/azure-ai-foundry/fine-tuning/tree/main/Sample_Datasets/Reinforcement_Fine_Tuning/ClauseMatching) - sample dataset and graders showcasing both summarization and content interpretation in the legal domain.
