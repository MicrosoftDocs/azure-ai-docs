---
title: "Agent optimizer cost and token usage overview"
description: "Understand how the agent optimizer estimates cost before a run and reports measured token usage after the run."
author: aahill
ms.author: aahi
ms.date: 08/07/2026
ms.topic: concept-article
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.custom: dev-focus, doc-kit-assisted
ai-usage: ai-assisted
# customer intent: As a developer, I want to understand optimization costs so that I can plan a run and review its measured usage.
---

# Agent optimizer cost and token usage overview

The agent optimizer in Foundry Agent Service provides a modeled cost estimate before you submit an optimization job. After the job finishes, its result can include measured token usage. Use the estimate for planning and the measured usage to understand the model activity that occurred during the run.

The pre-run estimate and post-run token usage serve different purposes. Neither value is a spending limit or a replacement for your Azure invoice.

> [!NOTE]
> In the Foundry portal, the pre-run cost estimate is currently available only for prompt-agent optimization runs. Hosted-agent optimization relies on Azure Developer CLI (`azd`) dependencies, so hosted-agent workflows don't currently show the estimate in the portal. Post-run token usage is available for both agent types.

## Pre-run cost estimate for prompt agents

Before you create a prompt-agent optimization job in the Foundry portal, the **Review** step shows a cost estimate for the requested settings. Hosted-agent optimization flows don't currently show this pre-run estimate.

The estimate predicts model calls and token charges. Requesting an estimate doesn't create an optimization job or call the models. The call counts are calculated from the job inputs. The currency values are modeled by applying static token assumptions and reference model prices to those call counts.

The portal shows three modeled currency values:

| Portal value | Meaning |
| --- | --- |
| **Minimum** | The modeled cost of the required full-dataset evaluations for the baseline and requested candidates. |
| **Estimated** | The expected modeled cost based on typical optimization behavior, including runs that finish before using the full call budget. |
| **Maximum** | A conservative modeled upper bound based on the optimization settings. It isn't an enforced spending limit. |

The summary identifies the candidate count, dataset row count, evaluator count, and reference-price date. Expand **Cost breakdown (estimated)** to review each phase.

> [!NOTE]
> The prices in the following screenshot are for **example only**. The pricing you view in the Foundry portal might be different based on your project setup.

:::image type="content" source="media/agent-optimizer-cost-estimate.png" alt-text="Screenshot of the prompt-agent optimization Review step showing Minimum, Estimated, and Maximum costs with the estimated cost breakdown expanded." lightbox="media/agent-optimizer-cost-estimate.png":::

## Inputs to the estimate

The optimizer calculates call-count ranges from the resolved job configuration. The calculation uses these inputs:

| Input | How it affects the estimate |
| --- | --- |
| Maximum candidates | The estimate includes the requested improved candidates and one additional baseline evaluation. |
| Evaluation dataset rows | Each full evaluation invokes the agent for every evaluation row. If you don't provide a separate validation dataset, the training dataset is used for evaluation. |
| Evaluators | Each agent response is scored by every selected evaluator. Adding evaluators increases evaluation-model calls. |
| Optimization behavior | Candidate generation, reflection, and early stopping affect how much of the modeled range the run uses. |
| Models | The agent, evaluation, and optimization model deployments determine which reference prices apply to each layer. |

For a referenced dataset, the service resolves its row count before it returns an estimate. If it can't resolve a nonempty row count, it doesn't create an estimate from an assumed dataset size.

For model-selection runs, the estimate doesn't separately price agent calls for every model in the search space. It uses the configured baseline agent model when available. If that model can't be resolved, it uses the evaluation model price for the agent layer.

## Static token assumptions

The estimate separates model activity into layers so that you can see which part of the run contributes to the total. It uses the following static `TokensPerCall` assumptions:

| API layer | Portal phase | Included activity | Prompt tokens per call | Completion tokens per call | Model used for pricing |
| --- | --- | --- | ---: | ---: | --- |
| `agent` | **Running your agent** | Invocations of the baseline agent and generated candidates against evaluation tasks. | 2,000 | 400 | Baseline agent model. If unavailable, the evaluation model. |
| `judge` | **Scoring responses** | Evaluation-model calls that score agent responses. The call count scales with the number of evaluators. | 3,000 | 120 | Evaluation model. |
| `reflection` | **Generating improvements** | Optimization-model calls that analyze results and generate candidate improvements. | 6,000 | 2,000 | Optimization model. |

These service-managed assumptions can change as the estimator is calibrated. For each layer, the optimizer multiplies the call-count range by the static prompt and completion token assumptions. It then applies dated reference prices per one million tokens:

`modeled layer cost = calls × ((prompt tokens × input price) + (completion tokens × output price)) / 1,000,000`

The total is the sum of the layers that can be priced. If a model price or token assumption isn't available for a layer, the estimate identifies the unpriced layer and excludes it from the total.

### What happens during an optimization run

To understand the cost layers, it helps to know how the optimizer uses each model behind the scenes. An optimization run follows this loop for both prompt agents and hosted agents:

1. **Evaluate the baseline (agent + judge).** The optimizer invokes your agent on every dataset row to collect responses. Then the eval model scores each response against each evaluator to establish baseline scores.
1. **Generate a candidate (reflection).** The optimization model receives the baseline scores, analyzes weaknesses, and produces an improved agent configuration. Depending on the agent type, the configuration can include rewritten instructions, refined skills, better tool descriptions, or a different model.
1. **Evaluate the candidate (agent + judge).** The optimizer runs the agent with the candidate configuration on the same dataset rows and scores the responses.
1. **Repeat.** Steps 2–3 repeat for each additional candidate. Each cycle adds another round of reflection and evaluation calls.

The three cost layers map directly to this loop:

- **Running your agent** — every time the agent is invoked against a dataset row (baseline and each candidate).
- **Scoring responses** — every time the eval model judges a response against an evaluator.
- **Generating improvements** — every time the optimization model reflects on results and produces a new candidate.

### Worked example: 2-max-candidate run

The following example shows how the formula applies to a concrete job configuration. All prices are for illustration only.

**Job settings:**

| Setting | Value |
| --- | --- |
| Maximum candidates | 2 |
| Dataset rows | 20 |
| Evaluators | 2 |
| Agent model | gpt-4.1 |
| Eval model | gpt-4.1-mini |
| Optimization model | gpt-5 |

**Estimated call counts:**

The optimizer derives call counts from the job configuration:

| Layer | Calculation | Estimated calls |
| --- | --- | ---: |
| Agent | (1 baseline + 2 candidates) × 20 rows | 60 |
| Judge | (1 baseline + 2 candidates) × 20 rows × 2 evaluators | 120 |
| Reflection | Determined by optimization algorithm for 2 candidates | 12 |

**Apply the formula to each layer:**

The optimizer looks up the dated reference input and output prices for each model and applies the formula. For example, the agent layer calculation is:

`60 × ((2,000 × <input price>) + (400 × <output price>)) / 1,000,000`

The same pattern applies to the judge and reflection layers, each using the token assumptions and reference prices for its respective model. The portal then sums all layers to produce the **Minimum**, **Estimated**, and **Maximum** values shown on the **Review** step.

In a typical 2-candidate run, the reflection layer (optimization model) accounts for the largest share of the estimated cost because it uses a more capable model with higher per-token rates. The judge layer is usually the least expensive because it uses a smaller eval model with low token assumptions per call.

> [!NOTE]
> The call counts in this example are for illustration. Actual reflection call counts and early-stopping behavior vary by configuration and are determined by the service at estimate time. The portal resolves reference prices automatically. Select **View pricing** on the **Review** step to see the pricing source, or see [Azure OpenAI Service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/).

## Estimation assumptions and limitations

The estimate is a planning value rather than a final charge because it combines an algorithmic call budget with modeled token use.

- Token assumptions are averages for each cost layer. Actual prompt, response, reasoning, and cached-token counts vary by model and request.
- An optimization job can stop early after it finds no further improvement. Early stopping can reduce actual usage below the **Estimated** or **Maximum** value.
- Agent usage varies with instructions, conversation turns, response length, tool calls, and tool output.
- Reference model prices are dated and might differ from prices for your subscription, region, deployment type, or agreement.
- The estimate doesn't include charges from external APIs, databases, search services, or other tools that your agent calls.
- The **Maximum** value isn't a spending limit.

## Post-run measured token usage

When an optimization job finishes, its result can include measured token usage for each phase of the run. The **Token usage** view can be available for both prompt-agent and hosted-agent runs.

For hosted agents, **Running your agent** usage is available only when the agent's evaluation sample or trace includes token usage information. If the hosted agent doesn't report usage, the portal omits the agent phase rather than reporting it as zero. The portal captures **Scoring responses** and **Generating improvements** usage separately when those model calls report usage.

The view can contain multiple rows for **Running your agent** when the optimizer evaluates multiple agent models.

> [!NOTE]
> The prices in the following screenshot are for **example only**. The pricing you view in the Foundry portal might be different based on your project setup.

:::image type="content" source="media/agent-optimizer-token-usage.png"alt-text="Screenshot of the Token usage view showing input, output, total tokens, and estimated cost grouped by optimization phase and model." lightbox="media/agent-optimizer-token-usage.png":::

| Portal column | Meaning |
| --- | --- |
| **Phase** | **Running your agent**, **Scoring responses**, or **Generating improvements**. |
| **Model** | Model associated with the measured usage. The portal shows `--` when usage can't be attributed to a model. |
| **Input** | Measured prompt or input tokens. |
| **Output** | Measured completion or output tokens. |
| **Total** | Sum of measured input and output tokens for the row. The final row totals measured usage across all phases. |
| **Est. cost** | Estimated cost calculated from measured token usage and reference model prices. |

The portal calculates an estimated cost from measured token usage and reference model prices. Select **View pricing** to review the pricing source. The estimate isn't the final billed amount.

A missing phase or token value means that usage wasn't measured. It doesn't mean that the phase used zero tokens or incurred no charge. Some hosted agents and older optimization jobs might not provide agent usage.

The underlying job result can contain more cached-token and reasoning-token details. Cached tokens are a subset of input tokens, and reasoning tokens are a subset of output tokens. Don't add these subset values to the input or output totals.

## Calculate model cost from measured usage

Measured token usage is more representative than the pre-run assumptions, but it reports token counts rather than the final billed amount. Apply the pricing for each model row to approximate the model cost:

`approximate model cost = ((input tokens × input price) + (output tokens × output price)) / 1,000,000`

If detailed usage provides a cached-token count and the model has a separate cached-input rate, subtract cached tokens from the input total and price the cached and noncached portions separately.

Calculate each phase and model row separately, and then add the results. If a row doesn't identify a model, you can't reliably apply a deployment-specific price to that usage.

Use the rates that apply to your subscription, region, deployment type, and billing agreement. For published rates, see [Azure OpenAI Service pricing](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/). The result still excludes charges from external tools and services.

## Related content

- [Agent optimizer overview](agent-optimizer-overview.md)
- [Quickstart: Optimize a prompt agent](../quickstarts/quickstart-optimize-prompt-agent.md)
- [Quickstart: Optimize a hosted agent](../quickstarts/quickstart-optimize-hosted-agent.md)
