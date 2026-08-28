---
title: Evaluation datasets in Microsoft Foundry
description: Learn how evaluation datasets are structured, how to prepare them, and how Microsoft Foundry uses them in evaluation runs.
author: lgayhardt
ms.author: lagayhar
ms.reviewer: fishah
ms.date: 08/26/2026
ms.service: microsoft-foundry
ms.subservice: foundry-observability
ms.topic: concept-article
ai-usage: ai-assisted
---

# Evaluation datasets in Microsoft Foundry

An evaluation dataset is a reusable collection of test cases for measuring
model or agent quality. Evaluation datasets typically use JSONL, with one JSON
object per line. This article explains when to use a reusable dataset, how
evaluation data is organized, and the available ways to prepare it.

## Do you need an evaluation dataset?

Create a dataset when you want a stable test set that you can rerun against
different model, prompt, or agent versions. Reusable datasets work well for
regression testing, CI/CD quality gates, and comparisons across evaluation
runs.

You don't always need a dataset. If your Foundry agent already has
responses or your application emits traces to Application Insights, you can
evaluate that data where it exists. See
[Evaluate interactions by response ID](cloud-evaluation-deployed-interactions.md#evaluate-interactions-by-response-id)
and [Evaluate traces](cloud-evaluation-deployed-interactions.md#evaluate-traces-preview).

## How Foundry uses evaluation data

In a JSONL dataset, the `messages` field represents model or agent
interactions. Each message identifies a role and its content.

If your dataset contains completed responses, Foundry evaluates those
responses directly. If you run the evaluation against a model or agent,
Foundry generates a new response for each input and evaluates that response.
Any response already stored in the dataset is ignored.

For example, consider a user who can't sign in. The agent asks which error
appears, the user says their password is rejected, and the agent recommends a
password reset. Turn-level evaluation scores an individual agent response,
such as the password-reset guidance, by using preceding messages as context.
Conversation-level evaluation scores the complete interaction.

The `evaluation_level` setting on the run controls the scoring granularity.
The dataset and selected evaluators must support that level. For details, see
[Choose an evaluation level](cloud-evaluation-conversations.md#choose-an-evaluation-level).
For standard columns and examples, see
[Evaluation dataset schema](evaluation-dataset-schema.md).

## Choose how to prepare evaluation data

| Situation | Recommended approach |
|---|---|
| **You have curated evaluation data** | Upload it as a versioned Foundry dataset or provide a small dataset inline. See [Prepare input data](cloud-evaluation-datasets.md#prepare-input-data). |
| **You want to review and reuse generated test cases before running an evaluation** | [Generate a synthetic evaluation dataset](evaluation-dataset-synthetic.md) from an agent definition, inline prompt, or reference file. |
| **You want a reusable dataset based on production traffic** | [Convert traces into a dataset](traces-to-dataset.md). |
| **You want to test simulated multi-turn scenarios** | [Generate a simulation seed dataset](evaluation-dataset-synthetic.md#generate-a-simulation-seed-dataset-sdk) or author test case scenarios as JSONL, and then [simulate conversations](cloud-evaluation-synthetic-data.md#simulate-conversations-preview). |
| **You have Foundry response IDs** | [Evaluate interactions by response ID](cloud-evaluation-deployed-interactions.md#evaluate-interactions-by-response-id) without creating a dataset. |
| **You want to evaluate existing Application Insights traces** | [Evaluate traces](cloud-evaluation-deployed-interactions.md#evaluate-traces-preview) without creating a dataset. |
| **You want to generate queries, invoke a target, and evaluate its responses in one workflow** | [Generate synthetic queries](cloud-evaluation-synthetic-data.md#generate-synthetic-queries) during the evaluation run. Foundry saves the generated queries as a dataset for reuse. |

## Next step

> [!div class="nextstepaction"]
> [Review the evaluation dataset schema](evaluation-dataset-schema.md)

## Related content

- [Run evaluations from the SDK](cloud-evaluation.md)
- [Generate a synthetic evaluation dataset](evaluation-dataset-synthetic.md)
- [Convert agent traces into evaluation datasets](traces-to-dataset.md)
- [Evaluate your agent](evaluate-agent.md)
