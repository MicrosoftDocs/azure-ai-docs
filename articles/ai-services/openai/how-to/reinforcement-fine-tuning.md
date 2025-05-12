---
title: 'Customize o4-mini model with Azure OpenAI and reinforcement fine-tuning'
description: Learn how to use reinforcement fine-tuning with Azure OpenAI
manager: nitinme
ms.service: azure-ai-openai
ms.custom: 
ms.topic: how-to
ms.date: 05/11/2025
author: mrbullwinkle
ms.author: mbullwin
---

# Reinforcement fine-tuning (RFT) with Azure OpenAI o4-mini

Reinforcement fine-tuning (RFT) is a technique for improving reasoning models like o4-mini by training them through a reward-based process, rather than relying only on labeled data. By using feedback or "rewards" to guide learning, RFT helps models develop better reasoning and problem-solving skills, especially in cases where labeled examples are limited or complex behaviors are desired.

## Process

The process of Reinforcement fine-tuning (RFT) is similar to Supervised fine-tuning (SFT) with some notable differences:

- **Data preparation** system messages aren't supported, and instead of an `assistant` message, the final message in your training data is a reference answer.
- **Model selection:** only o4-mini supports RFT.
- **Grader definition:** RFT requires the use of **graders** to score the quality of your fine-tuned model and guide learning. You can use string check, text similarity, or model-based graders – or combine them with a multi-grader.
- **Training:** includes additional parameters: `eval_samples`, `eval_interval`, `reasoning_effort`, and `compute_multiplier`. You also have the option to pause and resume jobs, allowing you to pause training, inspect checkpoints, and only continue if further training is needed.
- **Evaluation**: In addition to accuracy and loss, RFT returns mean reward and parse error, and mean tokens.

Throughout the training process, the platform iterates over the dataset, generating multiple responses for each prompt. These responses are then evaluated by the grader, and policy-gradient updates are applied based on the received scores. This cycle repeats until the training data is fully processed or the job is halted at a specified checkpoint, ultimately resulting in a model fine-tuned for your desired metric.

However, despite these differences, there are many commonalities between SFT and RFT: data preparation is key; serverless training jobs can be initiated through the Foundry UI; and we support standard and global standard deployments.

## Training & evaluation file formation requirements

Both training and validation files are required to run o4-mini RFT. o4 -mini uses a new format of data for reinforcement fine-tuning. These should be jsonl files, like what is used for supervised fine tuning (SFT).

Each line of the file should contain the messages field, with some differences to SFT:

- System messages aren't supported
- The final message must be from the user, not the assistant (as is the case for SFT)
- `Tools`, `functions`, `response_formats`, are supported
- Images / multimodal data aren't supported

Each line must include a new field called reference answer

- `Reference_answer` contains the data used by your grader to determine the correctness of the answer.
- This value must be a valid JSON object (for example, dictionary, or list; the specific type and structure is dependent on your selected grader).

We currently support a maximum of 50,000 reference examples for training.

### Example training data

```jsonl
{"messages": [{"role": "user", "content": "Your task is to calculate the results for this math problem based on BODMAS rules. Please analyze the following math problem:  36453-1238 + 25*5"}], "reference_answer": {“Result”: 35090}}
```

Expanding the above text from a single line, you can see the expected fields: messages, role, content, and reference answer:

```json
{
  "messages": [
    {
      "role": "user",
      "content": "Your task is to calculate the results for this math problem based on BODMAS rules. Please analyze the following math problem:  36453-1238 + 25*5"
    }
  ],
  "reference_answer": {
    "Result": 35090
  }
}
```

### Dataset size for RFT

Begin with a small dataset, comprising several dozen to a few hundred examples, to evaluate the efficacy of RFT prior to committing to a larger dataset. For safety reasons, the training set must undergo an automated screening process, which initiates when a fine-tuning job is started, rather than upon file upload. Once a file has successfully passed screening, it can be utilized repeatedly without delay.

High-quality examples are essential, even in limited quantities. Following screening, an increased volume of data is advantageous, provided it maintains high quality. Larger datasets permit the use of higher batch sizes, which generally enhance training stability.

Training files may contain a maximum of 50,000 examples, while test datasets may include up to 1,000 examples. Both types of datasets are subject to automated screening  

## Creating fine tuning jobs

You can create training jobs for o4-mini RFT in the Azure AI Foundry the same way you would fine tune any other model: Select **fine-tuning** in a supported region and select o4-mini as your base model.

:::image type="content" source="../media/how-to/reinforcement-fine-tuning/model.png" alt-text="Screenshot of o4-mini model selection in the Azure AI Foundry portal." lightbox="../media/how-to/reinforcement-fine-tuning/model.png":::

:::image type="content" source="../media/how-to/reinforcement-fine-tuning/model.png" alt-text="Screenshot of the reinforcement fine-tuning menu in the Azure AI Foundry portal." lightbox="../media/how-to/reinforcement-fine-tuning/reinforcement.png":::

### Hyperparameter selection

The hyperparameters section of the **reinforcement** method supports all of the regular training hyperparameters (for example, learning rate, number of epochs, and batch size), as well as three new hyperparameters:

| Hyperparameter name | Value | Description |
|----|----|----|
|`Eval_samples`: |1-10 | The number of samples to use during evaluation. Validation split reward metrics will be averaged across the different samples for each datapoint. Default is 5.|
|`Eval_interval` |1-25 | The number of training steps between evaluations over a provided validation file. Default is 1.|
|`Compute-multiplier` |0.125 -8.0 | The multiplier on amount of compute use for exploring search space during training. Increasing will result in greater number of samples being rolled per instance. Too low likely to underfit, too high would be prone to overfit. Default is 10.|
|`Reasoning_effort`|Low, Medium, High | The amount of effort the model should put into reasoning. Defaults to medium effort. If performance is poor, consider increasing the reasoning effort. |

> [!NOTE]
> If a method is provided, the top level hyperparameters field will be ignored. If you want to set both regular and reinforcement training params, set both in the reinforcement hyperparameters section.

> [!TIP]
> All these values are optional, and we recommend users to start your first job with default values before adjusting the hyperparameters.

## Graders

RFT is unique because it uses graders to assess the quality of a model’s response to teach the model to reason. Unlike SFT, the final message isn't from the assistant – instead we sample the model and use a grader on each sample to score its quality. We then train based on those scores to improve model performance.

Effectively, graders are functions that compare the reference_answer from your training file with the sampled response.

**Graders:**

- Return floating point numbers between 0 and 1. It can be helpful to give the model partial credit for answers, rather than binary 0/1.
- Graders are specified as JSON (see below)
- We only support simple comparisons at this time (for example, between strings or JSON objects).

### Supported graders

We support three types of graders: String check, Text similarity, Model graders. There's also an option on Multi-graders to use graders in combinations.

### String-check-grader 

Use these basic string operations to return a `0` or `1`.

**Specification:**

```json
{
    "type": "string_check",
    "name": string,
    "operation": "eq" | "ne" | "like" | "ilike",
    "input": string,
    "reference": string,
}
```

**Supported operations:**

- `eq`: Returns 1 if the input matches the reference (case-sensitive), 0 otherwise
- `neq`: Returns 1 if the input doesn't match the reference (case-sensitive), 0 otherwise
- `like`: Returns 1 if the input contains the reference (case-sensitive), 0 otherwise
- `ilike`: Returns 1 if the input contains the reference (not case-sensitive), 0 otherwise

### Text similarity

To evaluate how close the model-generated output is to the reference, scored with various evaluation metrics.

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

***Supported operations:***

- `bleu` – computes bleu score between strings
- `Fuzzy_match` – fuzzy string match, using rapidfuzz
- `gleu` – computes google BLEU score between strings
- `meteor` – computes METEOR score between strings
- `rouge-*` - as defined by the rouge python library

### Score Model

This is Model Grader where you can use LLM to grade the training output.

Models which we're supporting as grader models are:

- `gpt-4o-2024-08-06`
- `o3-mini-2025-01-31`

```json
{
    "type": "score_model",
    "name": string,
    "input": Message[],
    "model": string,
    "pass_threshold": number,
    "range": number[],
    "sampling_parameters": {
        "seed": number,
        "top_p": number,
        "temperature": number,
        "max_completion_tokens": number,
        "reasoning_effort": "low" | "medium" | "high"
    }
}
```

To use a score model grader, the input is a list of chat messages, each containing a role, and content. The output of the grader will be truncated to the given range, and default to 0 for all non-numeric outputs.

### Multi Grader

A multigrader object combines the output of multiple graders to produce a single score.	

```json
{  
"type": "multi",
 "graders": dict[str, Grader],
 "calculate_output": string, 
"invalid_grade": float
}
```

**Supported operations:**

*Operators:*
- `+` (addition)
- `-` (subtraction)
- `*` (multiplication)
- `/` (division)
- `^` (power)

*Functions:*
- `min`
- `max`
- `abs`
- `floor`
- `ceil`
- `exp`
- `sqrt`
- `log`

When using the UX you're able to write a prompt and generate a valid grader and response format in json as needed.

> [!IMPORTANT]
> Generating correct grader schema requires careful prompt authoring. You may find that your first few attempts generate invalid schemas or don't create a schema that will properly handle your training data. Grader is a mandatory field that must be entered while submitting a fine-tuning job. Response format is optional.

:::image type="content" source="../media/how-to/reinforcement-fine-tuning/grader-schema.png" alt-text="Screenshot of the reinforcement fine-tuning grader schema generation experience." lightbox="../media/how-to/reinforcement-fine-tuning/grader-schema.png":::

Here's an example grader for each category:

**string-check-grader** - use simple string operations to return a 0 or 1.

**Example:**

```json
{
"name": "simpleadd_ans_grader",
 "type": "string_check", 
"input": "{{item.reference_answer}}",
 "reference": "{{sample.output_text}}", 
"operation": "eq"
}
```

**Text similarity** - Evaluate how close the model-generated output is to the reference, scored with various evaluation metrics.

```json
{
"name": "text_similarity_sample_grader",
 "type": "text_similarity",
 "input": "{{item.reference_answer}}",
 "reference": "{{sample.output_text}}", "evaluation_metric":"fuzzy_match"
}
```

**Score Model** - This is Model Grader where you can use LLM to grade the training output.

Models which we're supporting as grader models are `gpt-4o-2024-08-06`and `o3-mini-2025-01-31`.

```json
0.5 if one is the same, and 0.0 if neither are the same. Return just a floating point score\n\n Reference answer: {\u0022donors\u0022: {{item.reference_answer.donors}}, \u0022acceptors\u0022: {{item.reference_answer.acceptors}}}\n\n Model answer: {{sample.output_text}}"
          }
        ],
        "model": "gpt-4o",
        "sampling_params": {
          "seed": 1,
          "temperature": 1,
          "max_completions_tokens": 1000,
          "top_p": 1
        },
        "name": "grader-test"
```

**Multi Grader** - A multigrader object combines the output of multiple graders to produce a single score.

```json
{
"name":"clause_match_grader",
"type":"multi",
"graders":{"ext_text_similarity":{"name":"ext_text_similarity",
"type":"text_similarity",
"input":"{{sample.output_json.ext_text}}",
"reference":"{{item.reference_answer.ext_text}}",
"evaluation_metric":"fuzzy_match"},

"clause_string_check":{"name":"clause_string_check",
"type":"string_check",
"input":"{{sample.output_json.clause_type}}",
"operation":"eq",
"reference":"{{item.reference_answer.clause_type}}"}},

"calculate_output":"0.5 * ext_text_similarity + 0.5 * clause_string_check"

}
```

## Training progress and results

RFT jobs are typically long running, and may take up to 24 hours depending on your parameter selection. You can track progress in both fine-tuning views of the AI Foundry portal. You'll see your job go through the same statuses as normal fine tuning jobs (queued, running, succeeded).

You can also review the results files while training runs, to get a peak at the progress and whether or not your training is proceeding as expected.

**New feature: pause and resume**

During the training you can view the logs and RFT metrics and pause the job as needed (if metrics aren't converging or if you feel model isn't learning at the right pace, incorrect grader chosen, etc.).

:::image type="content" source="../media/how-to/reinforcement-fine-tuning/pause.png" alt-text="Screenshot of the reinforcement fine-tuning with a running job." lightbox="../media/how-to/reinforcement-fine-tuning/pause.png":::


Once the training job is paused, a deployable checkpoint will be created and available for you to infer or resume the job further to completion. Pause operation is only applicable for jobs which have been trained for at least one step and are in *Running* state.

## Interpreting training results

For reinforcement fine-tuning jobs, the primary metrics are the per-step reward metrics. These metrics indicate how well your model is performing on the training data. They're calculated by the graders you defined in your job configuration.

### Reward Metrics

These are two separate top-level reward metrics:

 - `train_reward_mean`: The average reward across the samples taken from all datapoints in the current step. Because the specific datapoints in a batch change with each step, train_reward_mean values across different steps aren't directly comparable and the specific values can fluctuate drastically from step to step.
 
- `valid_reward_mean`: The average reward across the samples taken from all datapoints in the validation set, which is a more stable metric.

> [!TIP]
> You should always test inferencing with your model. If you’ve selected an inappropriate grader, it’s possible that the mean reward doesn't reflect the model’s performance. Review sample outputs from the model to ensure they're formatted correctly and make sense. Check if the model's predictions align with the ground truth and if the descriptive analysis provides a reasonable explanation.

### Reasoning tokens

The `train_reasoning_tokens_mean` and `valid_reasoning_tokens_mean` metrics to see how the model is changing its behavior over time. These metrics are the average number of reasoning tokens used by the model to respond to a prompt in the training and validation datasets, respectively. You can also view the mean reasoning token count in the fine-tuning dashboard.

> [!TIP]
> Often, during training, the model will drastically change the average number of reasoning tokens it uses to respond to a prompt. This is a sign that the model is changing its behavior in response to the reward signal. The model may learn to use fewer reasoning tokens to achieve the same reward, or it may learn to use more reasoning tokens to achieve a higher reward.

## Evaluate the results

By the time your fine-tuning job finishes, you should have a decent idea of how well the model is performing based on the mean reward value on the validation set. However, it's possible that the model has either overfit to the training data or has learned to reward hack your grader, which allows it to produce high scores without actually being correct. Before deploying your model, inspect its behavior on a representative set of prompts to ensure it behaves how you expect.

Understanding the model's behavior can be done quickly by inspecting the evals associated with the fine-tuning job. Specifically, pay close attention to the run made for the final training step to see the end model's behavior. You can also use the evals product to compare the final run to earlier runs and see how the model's behavior has changed over the course of training.

## Deploying and using your o4-mini RFT model

Your fine tuned model can be deployed via the UI or REST API, just like any other fine tuned model.

You can deploy the fine tuning job which is completed or any intermittent checkpoints created automatically or manually by triggering pause operation. To know more about model deployment and test with Chat Playground refer, see [fine-tuning deployment](./fine-tuning-deploy.md).

When using your model, make sure to use the same instructions and structure as used during training. This keeps the model in distribution, and ensures that you see the same performance on your problems during inference as you achieved during training.

## Best practices

### Grader selection

Your graders are used for reinforcement learning: choosing the wrong grader means that your rewards will be invalid, and your fine tuning won't produce the expected results.

Some basic rules for grader selection:

- If you have **short, specific answers** like numbers, Boolean responses, or multiple choice then choose a **string matching grader**.

- If you have **complex responses that can be scored on multiple criteria, use multi graders**. This allows you to score different aspects of the response and combine it into an aggregate.

- **Guard against reward hacking**. This happens when the model finds a shortcut that earns high scores without real skill. Make it hard to loophole your grading system.

- **Consider breaking the grader down into multiple steps**, and giving partial credit, to nudge the models reasoning in the right direction, grading is stable and aligned with preference. Provide few-shot examples of great, fair, and poor answers in the prompt.

- **Use an LLM as a-judge when code falls short**. For rich, open ended answers, ask another language model to grade. When building LLM graders, run multiple candidate responses and ground truths through your LLM judge to ensure

### Test your graders

All of the graders available in RFT are supported in [Azure OpenAI evaluation](./evaluations.md). Before initiating a training run, test a vanilla o4-mini model against your validation data with the same grader you intend to use for training. If the grader scores don't match your expectations – then you need to select a different grader.

We also provide a grader check API that you can use to check the validity of your configuration.

### Data preparation

Aim for a few hundred examples initially and consider scaling up to around 1,000 examples if necessary. The dataset should be balanced, in terms of classes predicted, to avoid bias and ensure generalization.

For the prompts, make sure to provide clear and detailed instructions, including specifying the response format and any constraints on the outputs (e.g. minimum length for explanations, only respond with true/false etc.)

## RFT spending limits

As RFT job can lead to high training costs, we're capping the pricing for per training job billing which means this will be the maximum amount that a job can cost before we end the job, even if weʼre not done processing the entire dataset. The training will be paused and a deployable checkpoint will be created.

Users can validate the training job, metrics, logs and then decide to resume the job to complete further. If the user decides to resume the job, billing will continue for the job and subsequently no further price limits would be placed on the training job.