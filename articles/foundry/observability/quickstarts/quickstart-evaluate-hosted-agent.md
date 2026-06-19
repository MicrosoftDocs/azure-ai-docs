---
title: "Quickstart: Evaluate your hosted agent"
description: "Evaluate a deployed hosted agent in Foundry Agent Service by using the Azure Developer CLI or the Microsoft Foundry portal to generate a test suite, run an evaluation, and review the results."
author: lgayhardt
ms.author: lagayhar
ms.date: 06/16/2026
ms.manager: mcleans
ms.topic: quickstart
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: mode-other, dev-focus, doc-kit-assisted
ai-usage: ai-assisted
---

# Quickstart: Evaluate your hosted agent

> [!NOTE]
> Hosted agents and the Azure Developer CLI evaluation experience are currently in preview.

In this quickstart, you evaluate the hosted agent you deployed in [Deploy your first hosted agent](../../agents/quickstarts/quickstart-hosted-agent.md). You provide a test dataset, choose evaluators, run an evaluation against the deployed agent, and review the scores. Each step shows two ways to do the same task: the Azure Developer CLI (`azd`) and the Microsoft Foundry portal.

Evaluation establishes a quality baseline for your agent and lets you set acceptance thresholds, such as a task adherence passing rate, before you release changes to users.

## Prerequisites

Before you begin, you need:

* A deployed, invokable hosted agent from [Deploy your first hosted agent](../../agents/quickstarts/quickstart-hosted-agent.md), and the `azd` project directory you created in that quickstart.
* The **Foundry User** role on the Foundry resource.
* To use the UI path, access to the [Foundry portal](https://ai.azure.com). For the azd path, see the next requirements.
* The `azd ai agent` extension (`azure.ai.agents`), version 0.1.40-preview or later, which provides the `azd ai agent eval` commands. This extension is included in the `microsoft.foundry` extension you installed in the previous quickstart. Verify the installed version with `azd ext list`. If you need to install or upgrade it, run `azd ext install microsoft.foundry` or `azd ext upgrade microsoft.foundry`.
* An authenticated `azd` session. Check your status with `azd auth status`, and run `azd auth login` if you're not signed in.

  [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

* A chat-completion model deployment in the same Foundry project to use as the judge model that scores responses. You can reuse the model deployment your agent already uses, including the one from the previous quickstart, so you don't need a separate deployment.

## Step 1: Confirm your deployed agent

Evaluation runs against a deployed, invokable agent. Confirm your agent responds before you set up the evaluation.

### [Azure Developer CLI](#tab/azd)

From your `azd` project directory, verify the agent is deployed and invokable:

```
azd ai agent show
```

Send a test prompt:

```
azd ai agent invoke "Write a haiku about deploying cloud applications."
```

You should see a response within a few seconds.

### [Foundry portal](#tab/portal)

1. Open the [Foundry portal](https://ai.azure.com) and go to your project.
1. Select your agent, and then select the **Playground** tab.
1. Send a test prompt, such as `Write a haiku about deploying cloud applications.`

You should see a response within a few seconds.

---

## Step 2: Generate the evaluation suite

Provide a test dataset and choose the built-in evaluators that define what to measure.

### [Azure Developer CLI](#tab/azd)

First, create a JSONL file of test queries for your agent. Each line is a JSON object with a `query` field. Save it as `tests/queries.jsonl` in your agent project folder:

```json
{"query": "What's the weather in Seattle?"}
{"query": "Book a flight to Paris"}
{"query": "Tell me a joke"}
```

Generate the evaluation suite from your dataset and a set of built-in evaluators:

```
azd ai agent eval generate \
  --dataset ./tests/queries.jsonl \
  --evaluator builtin.intent_resolution \
  --evaluator builtin.task_adherence \
  --eval-model <your-chat-completion-deployment>
```

Replace `<your-chat-completion-deployment>` with a chat-completion deployment in your project; you can reuse the one your agent already uses. The command creates `eval.yaml` in the agent project root and registers the dataset and evaluators in your project. The `--eval-model` value is the judge model that scores responses.

Open `eval.yaml` to review the agent target, dataset reference, and evaluators that the run uses. It looks similar to this:

```yaml
name: <eval-suite-name>
agent:
  name: <your-agent-name>
  kind: hosted
dataset:
  local_uri: tests/queries.jsonl
evaluators:
  - builtin.intent_resolution
  - builtin.task_adherence
options:
  eval_model: <your-chat-completion-deployment>
max_samples: 15
```

The suite name and some values are generated. Your file might also include a generated evaluator in addition to the built-in ones you selected.

### [Foundry portal](#tab/portal)

1. In the [Foundry portal](https://ai.azure.com), open your agent and select the **Evaluation** tab, then select **Create**.
1. For **Select evaluation target**, select **Agent**.
1. For **Select evaluation scope**, select **Individual turns**.
1. For **Select data source**, select **Existing dataset** and choose a CSV or JSONL file of test queries from your project's data assets.
1. If the **Configure agents** step appears, review the agent and accept the default user prompt, `{{item.query}}`. Adjust it only if your agent expects a different input format.
1. For **Select testing criteria**, select one or more agent evaluators, such as **Task Adherence** and **Intent Resolution**.

Keep the wizard open. You submit the evaluation in the next step.

---

## Step 3: Run the evaluation

Run the suite against your deployed agent. The service sends each test query to the agent, captures the response, and scores it with your selected evaluators.

> [!NOTE]
> Target-based evaluation invokes your hosted agent directly. It works with agents that use the responses or invocations protocol with synchronous, non-streaming execution. To evaluate agents that use the A2A or Activity protocol, or other execution patterns such as long-running or streaming, evaluate the traces your agent emits instead. See [Trace evaluation](../../how-to/develop/cloud-evaluation.md#trace-evaluation-preview).

### [Azure Developer CLI](#tab/azd)

From the agent project folder, run the evaluation:

```
azd ai agent eval run
```

The command runs `eval.yaml` from the agent project root, sends each query to your agent, scores the responses, and prints a summary when it finishes:

```output
Eval run started
   Eval: eval_b36748dede424e4ba3f8e6c99ca2cf27
   Run:  evalrun_5f72ef189ad24790a32128e6f230b131
   (✓) Done  Eval run  (4m 9s)

Results:    8 total, 8 passed, 0 failed, 0 errored

Per-criteria results:
  intent_resolution: 8 passed, 0 failed, 0 errored
  task_adherence: 8 passed, 0 failed, 0 errored
```

### [Foundry portal](#tab/portal)

1. On the **Review and submit** step, enter a **name** for the evaluation.
1. Review the target, scope, data source, and selected evaluators.
1. Select **Submit** to start the run.

---

## Step 4: Review the results

Evaluations typically complete in a few minutes, depending on the number of queries.

### [Azure Developer CLI](#tab/azd)

List recent evaluations:

```
azd ai agent eval list
```

```output
    Eval ID                                Name        Status of last run  Runs
    -------                                ----        ------------------  ----
*   eval_b36748dede424e4ba3f8e6c99ca2cf27  agent-core  Completed           1

* = active eval in current environment
```

Show the most recent evaluation and its runs:

```
azd ai agent eval show
```

```output
Eval:   eval_b36748dede424e4ba3f8e6c99ca2cf27
Name:   agent-core
Agent:  <your-agent-name>
Runs:   1

Recent runs:
  Run ID                                    Status     Passed  Failed  Created
  ------                                    ------     ------  ------  -------
  evalrun_5f72ef189ad24790a32128e6f230b131  Completed  8/8     0       2026-06-17 14:52 UTC
```

Use the results to confirm which agent version was evaluated and which evaluator scores were produced. To see per-evaluator details and a link to the report in the Foundry portal, run `azd ai agent eval show <eval-id> --eval-run-id <run-id>`.

### [Foundry portal](#tab/portal)

1. In the left pane, select **Evaluation**.
1. Select your run from the list to open its details. The details page shows the target, dataset, status, token usage, and an aggregate score for each evaluator.
1. Select the run name to view row-level results: each query, the agent response, the evaluator score, and the score explanation.

---

## Clean up resources

The evaluation registers a dataset, evaluators, and run history in your Foundry project. These assets incur little or no ongoing cost. To remove everything you created across this and the previous quickstart, run `azd down` from your agent project directory.

> [!WARNING]
> `azd down` permanently deletes every resource in the resource group, including the Foundry project, model deployments, and the hosted agent.

## Troubleshooting

| Issue | Solution |
| ----- | -------- |
| `azd ai agent eval` command not found or fails | Run `azd ext list` and verify the `azd ai agent` extension is 0.1.40-preview or later. Upgrade with `azd ext upgrade microsoft.foundry` |
| Evaluation target not found or agent not invokable | Confirm the agent is deployed and invokable with `azd ai agent show`. Redeploy with `azd deploy` if needed. |
| Many errored rows or unexpectedly low scores | Open the run report and check whether rows failed with agent response or evaluator errors. Fix the underlying errors, then rerun the evaluation. |
| `AuthenticationError` or `DefaultAzureCredential` failure | Refresh credentials with `azd auth logout` and then `azd auth login`. |
| Eval model deployment not found | Verify the chat-completion deployment name exists in your project under **Build** > **Deployments**. |

## What you learned

In this quickstart, you:

* Created a test dataset and chose evaluators for your hosted agent.
* Ran an evaluation against the deployed agent.
* Reviewed aggregated and row-level results.
* Completed each task with both the Azure Developer CLI and the Foundry portal.

## Next steps

> [!div class="nextstepaction"]
> [Optimize a hosted agent](../../agents/quickstarts/quickstart-optimize-hosted-agent.md)

## Related content

* [Evaluate your AI agents](../how-to/evaluate-agent.md)
* [Run agent evaluations with the azd CLI](../how-to/azure-developer-cli-evaluation.md)
* [Troubleshoot evaluation and observability issues](../how-to/troubleshooting.md)
* [Agent evaluators reference](../../concepts/evaluation-evaluators/agent-evaluators.md)
* [What are hosted agents?](../../agents/concepts/hosted-agents.md)
