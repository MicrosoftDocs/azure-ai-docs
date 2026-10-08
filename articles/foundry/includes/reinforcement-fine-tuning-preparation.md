---
title: Include file
description: Prepare RFT datasets and graders for the selected training interface.
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 10/07/2026
ms.custom: include
ai-usage: ai-assisted
---

## Prepare your data

Start with the [MedMCQ sample datasets on GitHub](https://github.com/microsoft-foundry/fine-tuning/tree/main/Sample_Datasets/Reinforcement_Fine_Tuning/MedMCQ), or prepare your own data.

Prepare separate training and validation files in the format supported by your selected model. Each example includes a prompt and the reference information your grader needs. Keep validation and final test examples out of the training set.

::: zone pivot="programming-language-python,rest-api"

Save the datasets as `training.jsonl` and `validation.jsonl`, with one example per line. Each record has a `messages` array ending in a `user` message, plus any fields your grader uses. The MedMCQ sample uses `reference_answer` for the expected answer label.

Reference: [RFT dataset samples](https://github.com/microsoft-foundry/fine-tuning/tree/main/Sample_Datasets/Reinforcement_Fine_Tuning).

::: zone-end

::: zone pivot="azd"

Use the dataset format and file paths in your selected [RFT CLI configuration sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/cli/finetuning/reinforcement).

::: zone-end

## Understand how graders work

A grader is the reward function for your RFT job. The model generates responses, the grader scores them, and training uses those scores to update the model.

Define the behavior you want to reward before choosing a grader. Use a reliable reference answer, an objective check, or a clear scoring rubric.

### Choose a grader type

Choose a grading approach supported by your selected model:

| Grader type | When to use it |
| --- | --- |
| String comparison | Exact answers, labels, or substring checks |
| Text similarity | Responses that should resemble a known reference |
| Model grader | Responses that require judgment against a rubric |
| Python grader | Task-specific calculations or custom checks |
| Multi-Grader | Tasks with more than one scoring criterion |

::: zone pivot="programming-language-python,rest-api,azd"

Match each example's references to your dataset and response format.

::: zone-end

#### String comparison

Compare the response with an expected answer or label. For example, award `1` for an exact match and `0` for any other response.

::: zone pivot="programming-language-python,rest-api,azd"

This definition uses the MedMCQ sample's expected answer label:

```json
{
  "name": "medmcqa_ans_grader",
  "type": "string_check",
  "input": "{{item.reference_answer}}",
  "reference": "{{sample.output_text}}",
  "operation": "eq"
}
```

Reference: [String-check grader schema](/rest/api/microsoft-foundry/azureopenai/fine-tuning#openaigraderstringcheck) and [MedMCQ grader](https://github.com/microsoft-foundry/fine-tuning/blob/main/Sample_Datasets/Reinforcement_Fine_Tuning/MedMCQ/stringcheck_grader.json).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | String | Yes | Set to `string_check` |
| `name` | String | Yes | A name for the grader |
| `input` | String | Yes | The text to test; can contain template references |
| `reference` | String | Yes | The text to compare against; can contain template references |
| `operation` | String | Yes | The comparison operation |

Choose the operation that matches your task:

| Operation | Returns `1` when | Case-sensitive |
| --- | --- | --- |
| `eq` | Input equals reference | Yes |
| `ne` | Input differs from reference | Yes |
| `like` | Input contains reference | Yes |
| `ilike` | Input contains reference | No |

For a containment check, put the generated response in `input` and the expected substring in `reference`.

::: zone-end

#### Text similarity

Compare the response with a reference using a text-similarity metric. For example, grade an extracted passage against the expected passage instead of requiring an exact match.

::: zone pivot="programming-language-python,rest-api,azd"

This definition uses the extracted-text check from the ClauseMatching sample. It requires structured output with an `extracted_text` field:

```json
{
  "name": "extracted_text_similarity",
  "type": "text_similarity",
  "input": "{{sample.output_json.extracted_text}}",
  "reference": "{{item.extracted_text}}",
  "evaluation_metric": "fuzzy_match"
}
```

Reference: [Text-similarity grader schema](/rest/api/microsoft-foundry/azureopenai/fine-tuning#openaigradertextsimilarity) and [ClauseMatching grader](https://github.com/microsoft-foundry/fine-tuning/blob/main/Sample_Datasets/Reinforcement_Fine_Tuning/ClauseMatching/multi_grader.json).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | String | Yes | Set to `text_similarity` |
| `name` | String | Yes | A name for the grader |
| `input` | String | Yes | The generated text to grade; can contain template references |
| `reference` | String | Yes | The expected text; can contain template references |
| `evaluation_metric` | String | Yes | The supported similarity metric |

Choose a metric supported by your RFT workflow:

| Metric | Comparison |
| --- | --- |
| `fuzzy_match` | Approximate string matching |
| `bleu` | BLEU n-gram overlap |
| `gleu` | Google BLEU |
| `meteor` | METEOR text alignment |
| `rouge_1` through `rouge_5` | N-gram overlap, from unigrams through five-grams |
| `rouge_l` | Longest common subsequence |

Use `cosine` for evaluations, not RFT.

::: zone-end

#### Model grader

Give a grading model a rubric for judging the response. For example, award `1` for a correct answer, `0.5` for a partially correct answer, and `0` for an incorrect answer.

::: zone pivot="programming-language-python,rest-api,azd"

Replace `<SUPPORTED_GRADER_MODEL_ID>` with a model supported for grading in your RFT workflow. Check the [grader deployment requirements](#model-grader-deployments) before creating the job.

This example adapts the documented score-model rubric to a dataset with `reference_answer`:

```json
{
  "name": "answer_quality",
  "type": "score_model",
  "model": "<SUPPORTED_GRADER_MODEL_ID>",
  "input": [
    {
      "role": "system",
      "content": "Score 1 for a match, 0.5 for a partial match, or 0."
    },
    {
      "role": "user",
      "content": "Reference: {{item.reference_answer}}"
    },
    {
      "role": "user",
      "content": "Response: {{sample.output_text}}"
    }
  ],
  "range": [0, 1],
  "sampling_params": {
    "seed": 42
  }
}
```

Reference: [Score-model grader schema](/rest/api/microsoft-foundry/azureopenai/fine-tuning#openaigraderscoremodel).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | String | Yes | Set to `score_model` |
| `name` | String | Yes | A name for the grader |
| `model` | String | Yes | The supported grading-model identifier, not the model you're training |
| `input` | Array of messages | Yes | The rubric and response to grade; messages include a `role` and `content`, which can contain template references |
| `range` | Array of numbers | No | The lower and upper score bounds; this example uses `[0, 1]` |
| `sampling_params` | Object | No | Sampling settings for the grading model, separate from training hyperparameters |

Use only sampling settings supported by the grading model:

| Parameter in `sampling_params` | Type | Description |
| --- | --- | --- |
| `seed` | Integer or null | A sampling seed; don't assume it guarantees identical scores |
| `temperature` | Number or null | Controls sampling randomness, when supported |
| `top_p` | Number or null | Controls nucleus sampling |
| `max_completions_tokens` | Integer or null | Limits tokens generated by the grading model |
| `reasoning_effort` | String | Controls reasoning effort for a grading model that supports it; accepted values depend on that model |

The example's seed is illustrative, not a recommended default. Test the rubric on responses with known scores before training.

::: zone-end

#### Python grader

Use Python code to calculate a numeric reward from the response and reference data. For example, compare the answer with its reference or implement a task-specific calculation.

::: zone pivot="programming-language-python,rest-api,azd"

Define a `grade(sample, item)` function that returns a numeric score. This helper saves an exact-answer grader as `grader.json`:

```python
import json

source = """
def grade(sample, item):
    return float(sample["output_text"] == item["reference_answer"])
"""
grader = {
    "name": "answer_match",
    "type": "python",
    "source": source,
}
with open("grader.json", "w", encoding="utf-8") as grader_file:
    json.dump(grader, grader_file)
```

Reference: [Python grader schema](/rest/api/microsoft-foundry/azureopenai/fine-tuning#openaigraderpython).

The helper encodes the function as the JSON `source` string, including its newline characters. It defines the grader, not the training job; use your selected interface to submit the job.

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | String | Yes | Set to `python` |
| `name` | String | Yes | A name for the grader |
| `source` | String | Yes | Python source defining `grade(sample, item)`; the function returns a numeric score |
| `image_tag` | String | No | A runtime image tag supported by your workflow; omit it unless you need a documented image version |

The function receives the generated response in `sample` and the dataset record in `item`. It returns `1.0` for a match and `0.0` otherwise. Ensure every record supplies `reference_answer`.

Python graders run in a constrained runtime without network access. Keep code within the [documented runtime limits](../openai/how-to/reinforcement-fine-tuning.md#python-grader), and test error cases before training.

::: zone-end

#### Multi-Grader

Combine multiple grading criteria into one reward. For example, give equal weight to the quality of an extracted passage and the correctness of its classification.

::: zone pivot="programming-language-python,rest-api,azd"

This definition combines the two checks in the ClauseMatching sample. Use the matching dataset and [structured response format](#choose-a-response-format):

```json
{
  "name": "clause_match_grader",
  "type": "multi",
  "graders": {
    "extracted_text_similarity": {
      "name": "extracted_text_similarity",
      "type": "text_similarity",
      "input": "{{sample.output_json.extracted_text}}",
      "reference": "{{item.extracted_text}}",
      "evaluation_metric": "fuzzy_match"
    },
    "clause_string_check": {
      "name": "clause_string_check",
      "type": "string_check",
      "input": "{{sample.output_json.clause_type}}",
      "reference": "{{item.clause_type}}",
      "operation": "eq"
    }
  },
  "calculate_output": "(extracted_text_similarity + clause_string_check) / 2"
}
```

Reference: [Multi-Grader schema](/rest/api/microsoft-foundry/azureopenai/fine-tuning#openaigradermulti) and [ClauseMatching Multi-Grader](https://github.com/microsoft-foundry/fine-tuning/blob/main/Sample_Datasets/Reinforcement_Fine_Tuning/ClauseMatching/multi_grader.json).

| Parameter | Type | Required | Description |
| --- | --- | --- | --- |
| `type` | String | Yes | Set to `multi` |
| `name` | String | Yes | A name for the combined grader |
| `graders` | Object | Yes | Named child-grader definitions, each using a supported grader type and its required parameters |
| `calculate_output` | String | Yes | An arithmetic expression that references child graders by their keys in `graders` |

The expression supports `+`, `-`, `*`, `/`, and `^`, plus `min`, `max`, `abs`, `floor`, `ceil`, `exp`, `sqrt`, and `log`. Choose child-grader combinations supported by your RFT workflow.

::: zone-end

### Reference model output and dataset fields

Align your grader with the response you expect and the reference information in your dataset. A grader that expects a plain answer label doesn't correctly evaluate a structured response containing that label.

::: zone pivot="programming-language-python,rest-api,azd"

Templated graders substitute these references when scoring a response:

| Reference | Content |
| --- | --- |
| `{{sample.output_text}}` | The generated response as text |
| `{{sample.output_json}}` | The generated structured response as JSON |
| `{{item.reference_answer}}` | The expected answer in the current dataset record |
| `{{item.extracted_text}}` and `{{item.clause_type}}` | Reference fields in the ClauseMatching dataset |

Every reference must match an actual response or dataset field. Python graders receive the same information through the `sample` and `item` function arguments instead of template substitution.

::: zone-end

### Model grader deployments

A model grader uses a grading model, which can differ from the model you're fine-tuning. Depending on the selected training model, Foundry hosts the grader or requires a separate grader deployment.

If your workflow requires a separate deployment, provision a supported grader model before training. Confirm access, capacity, and the grading budget.

## Configure and test the grader

Test the grader on correct, incorrect, and malformed responses. Correct answers should receive higher scores than incorrect answers. Check that superficial responses can't earn a high score without solving the task.

::: zone pivot="programming-language-studio"

Configure the grader in the fine-tuning job setup using the options available for your selected model. For an exact-answer task, use a string comparison that rewards only the expected answer.

::: zone-end

::: zone pivot="programming-language-python,rest-api"

For the exact-answer sample, save the [string-comparison definition](#string-comparison) as `grader.json`. Configure your prompts to request only the answer label.

For other tasks, use a matching configuration from the [grader samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/cli/finetuning/reinforcement).

::: zone-end

::: zone pivot="programming-language-python"

After initializing the client and loading the grader in the SDK example below, validate it with `client.fine_tuning.alpha.graders.validate(grader=grader)`. Test sample responses with `client.fine_tuning.alpha.graders.run`, providing the grader, generated response, and dataset record.

Reference: [Grader validation and test APIs](/rest/api/microsoft-foundry/azureopenai/fine-tuning).

::: zone-end

::: zone pivot="rest-api"

Use the [grader validation and test APIs](/rest/api/microsoft-foundry/azureopenai/fine-tuning) before submitting the job.

::: zone-end

::: zone pivot="azd"

Choose a [grader configuration sample](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/cli/finetuning/reinforcement) for your task. Update the grader and dataset paths in the YAML configuration, and check that its scoring rules match your dataset.

::: zone-end

## Choose a response format

Choose an output format supported by your model and compatible with the grader. Use plain text for an answer-label task, or structured JSON when your task requires named output fields.

::: zone pivot="programming-language-studio"

Set the response format in the job configuration. For structured output, provide the matching schema and use a grader that evaluates that structure.

::: zone-end

::: zone pivot="programming-language-python,rest-api"

For plain text, leave `response_format` unset and grade `{{sample.output_text}}`. For structured output, supply a schema in `method.reinforcement.response_format` and grade `{{sample.output_json}}` or its fields.

The following configuration wraps the [ClauseMatching sample schema](https://github.com/microsoft-foundry/fine-tuning/blob/main/Sample_Datasets/Reinforcement_Fine_Tuning/ClauseMatching/schema.json). Save it as `response-format.json` only when using the matching dataset and grader.

```json
{
  "type": "json_schema",
  "json_schema": {
    "name": "contract_clause",
    "strict": true,
    "schema": {
      "type": "object",
      "properties": {
        "clause_type": {
          "type": "string",
          "enum": ["Exclusivity", "Non-Compete"]
        },
        "extracted_text": {
          "type": "string"
        }
      },
      "required": ["clause_type", "extracted_text"],
      "additionalProperties": false
    }
  }
}
```

Reference: [RFT response-format schema](/rest/api/microsoft-foundry/azureopenai/fine-tuning#azurefinetunereinforcementmethod) and [structured outputs](../openai/how-to/structured-outputs.md).

Align the prompts, dataset fields, and grader with that output. Don't reuse an exact-text grader unchanged after switching to JSON.

::: zone-end

::: zone pivot="azd"

Keep the response format consistent with the grader in your YAML configuration. Use the matching dataset and grader files from the [RFT CLI samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/cli/finetuning/reinforcement).

::: zone-end
