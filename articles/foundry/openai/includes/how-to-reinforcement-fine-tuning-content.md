---
title: Include file
description: Prepare reinforcement data, choose and test graders, and configure text or structured responses.
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 10/05/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

## Prepare your data

Start with the [MedMCQ sample datasets on GitHub](https://github.com/microsoft-foundry/fine-tuning/tree/main/Sample_Datasets/Reinforcement_Fine_Tuning/MedMCQ), or prepare your own data.

Save separate `training.jsonl` and `validation.jsonl` files with one example per line. Each example needs a `messages` array ending in a `user` message, plus any fields your grader uses.

For the exact-answer MedMCQ task, each example supplies a prompt and a `reference_answer`:

```jsonl
{"messages": [{"role": "user", "content": "Chronic urethral obstruction due to benign prismatic hyperplasia can lead to the following change in kidney parenchyma\n- A. Hyperplasia\n- B. Hyperophy\n- C. Atrophy\n- D. Dyplasia"}], "reference_answer": "C"}
```

Reference: [RFT dataset samples](https://github.com/microsoft-foundry/fine-tuning/tree/main/Sample_Datasets/Reinforcement_Fine_Tuning).

Keep validation and final test examples out of the training set.

## Understand how graders work

A grader is the reward function for your RFT job. During training, the model generates responses to your prompts. The grader scores those responses, and the training service uses the scores to update the model.

Define the behavior you want to reward before choosing a grader. Use a reliable reference answer, an objective check, or a clear scoring rubric. Submit one grader configuration per job; use a multigrader to combine several checks into one reward.

### Choose a grader type

The OpenAI RFT workflow supports the following grader types. Check availability for your selected base model before using them with another model family.

| Grader type | How it scores a response | When to use it |
| --- | --- | --- |
| `string_check` | Applies `eq`, `ne`, `like`, or `ilike` to return `0` or `1`. | Exact answers, labels, or substring checks. |
| `text_similarity` | Compares generated text with a reference using a metric such as BLEU, ROUGE, or fuzzy matching. | Responses that should resemble a known reference. |
| `score_model` | Gives a grading model a prompt and rubric to produce a numeric score. | Answers that require judgment beyond an exact match. |
| `python` | Runs a Python `grade(sample, item)` function that returns a numeric score. | Task-specific calculations or checks implemented in code. |
| `multi` | Combines named graders through a `calculate_output` arithmetic expression. | Tasks with more than one scoring criterion. |

Python graders run in a constrained environment without network access. Keep calculations within the runtime and resource limits. For an example, use the [Countdown Python grader workflow](https://github.com/microsoft-foundry/fine-tuning/blob/main/Demos/RFT_Countdown/demo_with_python_grader.ipynb).

Endpoint graders call an HTTP endpoint to score responses. They're available in private preview; use the instructions provided for your approved access rather than assuming the standard grader configuration applies.

### Reference model output and dataset fields

Templated graders resolve variables when they score each response:

| Reference | Content |
| --- | --- |
| `{{sample.output_text}}` | The generated response as text. |
| `{{sample.output_json}}` | The generated structured response as JSON. |
| `{{item.reference_answer}}` | The `reference_answer` field from the current dataset record. |
| `{{item.ground_truth.date}}` | A nested field in a dataset record's `ground_truth` object. |

Put reference information in extra dataset fields, separate from the prompt's `messages` array. Match each grader reference to an actual field in your data. Python graders receive `sample` and `item` as function arguments instead of using template substitution.

### Model grader deployments

A model grader uses a grading model, which can differ from the model you're fine-tuning. The deployment requirement depends on the **base model you're fine-tuning**, not just the grader type.

| Base model for the RFT job | Grader deployment |
| --- | --- |
| OpenAI or MAI model | Foundry provides a hosted model deployment for grading. You don't provision a separate grader deployment. |
| Other models supporting RFT | Provision your own grader model deployment in Foundry before training, then configure the model grader to use that deployment. |

For a user-provisioned grader deployment, confirm access, capacity, and the grading budget before creating the job. Use a grader model supported by the selected RFT workflow; don't assume every model in the catalog is compatible.

For OpenAI RFT, documented grading models include `gpt-4o-2024-08-06` and `o3-mini-2025-01-31`. Build the grader prompt around the response, your reference fields, and an explicit rubric. The [ClauseMatching model grader](https://github.com/microsoft-foundry/fine-tuning/blob/main/Sample_Datasets/Reinforcement_Fine_Tuning/ClauseMatching/model_grader.json) shows an example.

In an OpenAI `score_model` configuration, `model` selects the grading model and `input` supplies its prompt. Use `range` to define score bounds and `sampling_params` for grading-model settings. Those settings are separate from the training hyperparameters.

Model grading can vary between runs. Test the rubric on responses with known scores, and inspect failed examples when scores don't match your intended behavior.

## Configure and test the grader

Save the following configuration as `grader.json` for the exact-answer dataset above. Configure your prompts to request only the answer label:

```json
{
  "name": "medmcqa_ans_grader",
  "type": "string_check",
  "input": "{{item.reference_answer}}",
  "reference": "{{sample.output_text}}",
  "operation": "eq"
}
```

Reference: [MedMCQ grader](https://github.com/microsoft-foundry/fine-tuning/blob/main/Sample_Datasets/Reinforcement_Fine_Tuning/MedMCQ/stringcheck_grader.json).

This configuration returns `1` for an exact match and `0` otherwise. Test it on correct, incorrect, and malformed responses before training.

For tasks that allow multiple valid answers, use a task-appropriate configuration from the [grader samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/cli/finetuning/reinforcement). For combined scoring, start with the [ClauseMatching multigrader](https://github.com/microsoft-foundry/fine-tuning/blob/main/Sample_Datasets/Reinforcement_Fine_Tuning/ClauseMatching/multi_grader.json).

Check that correct answers receive higher scores than incorrect answers. Test malformed output and responses that meet superficial criteria without solving the task. If your grader rewards those responses, revise it before training.

## Choose a response format

The response format controls the output generated during training. For the OpenAI examples in this guide, choose plain text or structured JSON:

| Format | Configuration | Grader reference |
| --- | --- | --- |
| Text, the default | Leave `response_format` unset. | Use `{{sample.output_text}}`. |
| Structured JSON | Supply a JSON schema in `method.reinforcement.response_format`. | Use `{{sample.output_json}}` or its fields. |

Keep text output for the MedMCQ exact-answer example. A JSON answer wouldn't equal the plain answer label expected by its string-check grader.

For structured output, the following configuration wraps the [ClauseMatching sample schema](https://github.com/microsoft-foundry/fine-tuning/blob/main/Sample_Datasets/Reinforcement_Fine_Tuning/ClauseMatching/schema.json) for the v1 API. Save it as `response-format.json` only when using the matching ClauseMatching dataset and grader.

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

Reference: [v1 RFT response-format schema](/rest/api/microsoft-foundry/azureopenai/fine-tuning#azurefinetunereinforcementmethod) and [structured outputs](../how-to/structured-outputs.md).

The schema requires both fields, restricts `clause_type` to two labels, and rejects additional properties. Align the prompts, dataset fields, and grader with that output. Don't reuse an exact-text grader unchanged after switching to JSON.
