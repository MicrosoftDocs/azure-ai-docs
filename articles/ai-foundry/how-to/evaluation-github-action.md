---
title: How to run an evaluation in GitHub Action 
titleSuffix: Microsoft Foundry
description: How to run evaluation in GitHub Action to streamline the evaluation process, allowing you to assess model performance and make informed decisions before deploying to production.
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/12/2026
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
ai-usage: ai-assisted
monikerRange: 'foundry-classic || foundry'
---

# How to run an evaluation in GitHub Action (preview)

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

::: moniker range="foundry-classic"

This GitHub Action enables offline evaluation of AI models and agents within your CI/CD pipelines. It streamlines the evaluation process, so you can assess model performance and make informed decisions before deploying to production.

Offline evaluation involves testing AI models and agents by using test datasets to measure their performance on various quality and safety metrics such as fluency, coherence, and appropriateness. After you select a model in the [Foundry model catalog](https://azure.microsoft.com/products/ai-model-catalog?msockid=1f44c87dd9fa6d1e257fdd6dd8406c42) or [GitHub Model marketplace](https://github.com/marketplace/models), perform offline pre-production evaluation to validate the AI application during integration testing. This process allows developers to identify potential problems and make improvements before deploying the model or application to production, such as when creating and updating agents.

::: moniker-end

::: moniker range="foundry"

This [GitHub Action](https://github.com/microsoft/ai-agent-evals) enables offline evaluation of [Microsoft Foundry Agents](../agents/overview.md) within your CI/CD pipelines. It's designed to streamline the offline evaluation process, so you can identify potential problems and make improvements before releasing an update to production.

To use this action, provide a data set with test queries and a list of evaluators. This action invokes your agents with the queries, runs the evaluations, and generates a summary report.

::: moniker-end

[!INCLUDE [features](../includes/evaluation-github-action-azure-devops-features.md)]

::: moniker range="foundry-classic"

- **Seamless Integration**: Easily integrate with existing GitHub workflows to run evaluation based on rules that you specify in your workflows (for examples, when changes are committed to agent versions, prompt templates, or feature flag configuration).
- **Statistical Analysis**: Evaluation results include confidence intervals and test for statistical significance to determine if changes are meaningful and not due to random variation.
- **Out-of-box operation metrics**: Automatically generates operational metrics for each evaluation run (client run duration, server run duration, completion tokens, and prompt tokens).

::: moniker-end

## Prerequisites

- A project. To learn more, see [Create a project](create-projects.md).
- A [Foundry agent](../agents/overview.md).

> [!TIP]
> The recommended way to authenticate is by using Microsoft Entra ID, which allows you to securely connect to your Azure resources. You can automate the authentication process by using the [Azure Login GitHub action](/azure/developer/github/connect-from-azure). To learn more, see [Azure Login action with OpenID Connect](/azure/developer/github/connect-from-azure-openid-connect).

::: moniker range="foundry-classic"

Two GitHub Actions are available for evaluating AI applications: **ai-agent-evals** and **genai-evals**.

- If your application already uses Foundry agents, **ai-agent-evals** is a good choice because it offers a simplified setup process and direct integration with agent-based workflows.
- **genai-evals** is designed for evaluating generative AI models outside of the agent framework.

> [!NOTE]
> The **ai-agent-evals** interface is more straightforward to configure. In contrast, **genai-evals** requires you to prepare structured evaluation input data. Code samples are provided to help with setup.

::: moniker-end

## How to set up AI agent evaluations

### AI agent evaluations input

::: moniker range="foundry-classic"

The input of ai-agent-evals includes:

**Required:**

# [Foundry project](#tab/foundry-project)

- `azure-ai-project-endpoint`: The endpoint of the Foundry project. Use this endpoint to connect to your AI project, simulate conversations with each agent, and connect to the Azure AI evaluation SDK to perform the evaluation.

# [Hub-based project](#tab/hub-project)

- `azure-aiproject-connection-string`: The connection string of the Foundry project. Use this string to connect to your AI project, simulate conversations with each agent, and connect to the Azure AI evaluation SDK to perform the evaluation.

---

- `deployment-name`: The deployed model name for evaluation judgment.
- `data-path`: Path to the input data file containing the conversation starters. Each conversation starter is sent to each agent for a pairwise comparison of evaluation results.
  - `evaluators`: Built-in evaluator names.
  - `data`: A set of conversation starters or queries.
  - Only single agent turn is supported.
- `agent-ids`: A unique identifier for the agent and a comma-separated list of agent IDs to evaluate.
  - When you specify only one `agent-id`, the evaluation results include the absolute values for each metric along with the corresponding confidence intervals.
  - When you specify multiple `agent-ids`, the results include absolute values for each agent and a statistical comparison against the designated baseline agent ID.

**Optional:**

- `api-version`: The API version of deployed model.
- `baseline-agent-id`: Agent ID of the baseline agent to compare against. By default, the first agent is used.  
- `evaluation-result-view`: Specifies the format of evaluation results. Defaults to "default" (boolean scores such as passing and defect rates) if omitted. Options are "default", "all-scores" (includes all evaluation scores), and "raw-scores-only" (non-boolean scores only).

Here's a sample of the dataset:

```JSON
{ 
  "name": "MyTestData", 
  "evaluators": [ 
    "RelevanceEvaluator", 
    "ViolenceEvaluator", 
    "HateUnfairnessEvaluator",
  ], 
  "data": [ 
    { 
      "query": "Tell me about Tokyo?", 
    }, 
    { 
      "query": "Where is Italy?", 
    } 
  ] 
} 

```

::: moniker-end

::: moniker range="foundry"

#### Parameters

| Name | Required? | Description |
| - | - | - |
| azure-ai-project-endpoint | Yes | Endpoint of your Microsoft Foundry Project. |
| deployment-name | Yes | The name of the Azure AI model deployment to use for evaluation. |
| data-path | Yes | Path to the data file that contains the evaluators and input queries for evaluations. |
| agent-IDs | Yes | ID of one or more agents to evaluate in format `agent-name:version` (for example, `my-agent:1` or `my-agent:1,my-agent:2`). Multiple agents are comma-separated and compared with statistical test results. |
| baseline-agent-id | No | ID of the baseline agent to compare against when evaluating multiple agents. If not provided, the first agent is used. |

#### Data file

The input data file should be a JSON file with the following structure:

| Field | Type | Required? | Description |
| - | - | - |
| name | string | Yes | Name of the evaluation dataset. |
| evaluators | string[] | Yes | List of evaluator names to use. Check out the list of available evaluators in your project's evaluator catalog in Foundry portal: **Build > Evaluations > Evaluator catalog**. |
| data | object[] | Yes | Array of input objects with `query` and optional evaluator fields like `ground_truth`, `context`. Automapped to evaluators; use `data_mapping` to override. |
| openai_graders | object | No | Configuration for OpenAI-based evaluators (label_model, score_model, string_check, etc.). |
| evaluator_parameters | object | No | Evaluator-specific initialization parameters (for example, thresholds, custom settings). |
| data_mapping | object | No | Custom data field mappings (autogenerated from data if not provided). |

#### Basic sample data file

```JSON
{
  "name": "test-data",
  "evaluators": [
    "builtin.fluency",
    "builtin.task_adherence",
    "builtin.violence",
  ],
  "data": [
    {
      "query": "Tell me about Tokyo disneyland"
    },
    {
      "query": "How do I install Python?"
    }
  ]
}

```

#### Additional sample data files

| Filename | Description |
| - | - |
| [dataset-tiny.json](https://github.com/microsoft/ai-agent-evals/blob/main/samples/data/dataset-tiny.json) | Dataset with small number of test queries and evaluators. |
| [dataset.json](https://github.com/microsoft/ai-agent-evals/blob/main/samples/data/dataset.json) | Dataset with all supported evaluator types and enough queries for confidence interval calculation and statistical test. |
| [dataset-builtin-evaluators.json](https://github.com/microsoft/ai-agent-evals/blob/main/samples/data/dataset-builtin-evaluators.json) | Built-in Foundry evaluators example (for example, coherence, fluency, relevance, groundedness, metrics). |
| [dataset-openai-graders.json](https://github.com/microsoft/ai-agent-evals/blob/main/samples/data/dataset-openai-graders.json) | OpenAI-based graders example (label models, score models, text similarity, string checks). |
| [dataset-custom-evaluators.json](https://github.com/microsoft/ai-agent-evals/blob/main/samples/data/dataset-custom-evaluators.json) | Custom evaluators example with evaluator parameters. |
| [dataset-data-mapping.json](https://github.com/microsoft/ai-agent-evals/blob/main/samples/data/dataset-data-mapping.json) | Data mapping example showing how to override automatic field mappings with custom data column names. |

::: moniker-end

### AI agent evaluations workflow

To use the GitHub Action, add the GitHub Action to your CI/CD workflows. Specify the trigger criteria, such as on commit, and the file paths to trigger your automated workflows.

> [!TIP]
> To minimize costs, don't run evaluation on every commit.  

This example shows how you can run Azure Agent AI Evaluation when you compare different agents by using agent IDs.

::: moniker range="foundry-classic"

# [Foundry project](#tab/foundry-project)

```YAML
name: "AI Agent Evaluation"

on:
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  run-action:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Azure login using Federated Credentials
        uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - name: Run Evaluation
        uses: microsoft/ai-agent-evals@v2-beta
        with:
          # Replace placeholders with values for your Azure AI Project
          azure-ai-project-endpoint: "<your-ai-project-endpoint>"
          deployment-name: "<your-deployment-name>"
          agent-ids: "<your-ai-agent-ids>"
          data-path: ${{ github.workspace }}/path/to/your/data-file

```

# [Hub-based project](#tab/hub-project)

```YAML
name: "AI Agent Evaluation"

on:
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  run-action:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Azure login using Federated Credentials
        uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - name: Run Evaluation
        uses: microsoft/ai-agent-evals@v1-beta
        with:
          # Replace placeholders with values for your Azure AI Project
          azure-aiproject-connection-string: "<your-ai-project-conn-str>"
          deployment-name: "<your-deployment-name>"
          agent-ids: "<your-ai-agent-ids>"
          data-path: ${{ github.workspace }}/path/to/your/data-file

```

---

::: moniker-end

::: moniker range="foundry"

```yaml
name: "AI Agent Evaluation"

on:
  workflow_dispatch:
  push:
    branches:
      - main

permissions:
  id-token: write
  contents: read

jobs:
  run-action:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Azure login using Federated Credentials
        uses: azure/login@v2
        with:
          client-id: ${{ vars.AZURE_CLIENT_ID }}
          tenant-id: ${{ vars.AZURE_TENANT_ID }}
          subscription-id: ${{ vars.AZURE_SUBSCRIPTION_ID }}

      - name: Run Evaluation
        uses: microsoft/ai-agent-evals@v3-beta
        with:
          # Replace placeholders with values for your Foundry Project
          azure-ai-project-endpoint: "<your-ai-project-endpoint>"
          deployment-name: "<your-deployment-name>"
          agent-ids: "<your-ai-agent-ids>"
          data-path: ${{ github.workspace }}/path/to/your/data-file
```

::: moniker-end

### AI agent evaluations output

::: moniker range="foundry-classic"

The evaluation process outputs results to the summary section for each AI evaluation GitHub Action run. You can view these results under **Actions** in GitHub.com.

The result includes two main parts:

- The top section summarizes the overview of your AI agent variants. You can select it on the agent ID link, and it directs you to the agent setting page in Foundry portal. You can also select the link for Evaluation Results, and it directs you to Foundry portal to view individual result in detail.

- The second section includes evaluation scores and comparison between different variants on statistical significance (for multiple agents) and confidence intervals (for single agent).

Multi agent evaluation result:

:::image type="content" source="../media/evaluations/github-action-multi-agent-result.png" alt-text="Screenshot of multi agent evaluation result in GitHub Action." lightbox="../media/evaluations/github-action-multi-agent-result.png":::

Single agent evaluation result:

:::image type="content" source="../media/evaluations/github-action-single-agent-output.png" alt-text="Screenshot of single agent evaluation result in GitHub Action." lightbox="../media/evaluations/github-action-single-agent-output.png":::

::: moniker-end

::: moniker range="foundry"

Evaluation results are output to the summary section for each AI Evaluation GitHub Action run under Actions in GitHub.

The following is a sample report for comparing two agents.

:::image type="content" source="../default/media/observability/github-action-agent-output.png" alt-text="Screenshot of agent evaluation result in GitHub Action." lightbox="../default/media/observability/github-action-agent-output.png":::

::: moniker-end

::: moniker range="foundry-classic"

## How to set up genAI evaluations

### GenAI evaluations input

The input for genai-evals includes the following items. Some items are optional depending on the evaluator you use:

Evaluation configuration file:

- `data`: a set of queries and ground truth. Ground-truth is optional and only required for a subset of evaluators. (See which [evaluator requires ground-truth](./develop/evaluate-sdk.md#data-requirements-for-built-in-evaluators)).

    Here's a sample of the dataset:

    ```json
    [ 
        { 
            "query": "Tell me about Tokyo?", 
            "ground-truth": "Tokyo is the capital of Japan and the largest city in the country. It is located on the eastern coast of Honshu, the largest of Japan's four main islands. Tokyo is the political, economic, and cultural center of Japan and is one of the world's most populous cities. It is also one of the world's most important financial centers and is home to the Tokyo Stock Exchange." 
        }, 
        { 
            "query": "Where is Italy?", 
            "ground-truth": "Italy is a country in southern Europe, located on the Italian Peninsula and the two largest islands in the Mediterranean Sea, Sicily and Sardinia. It is a unitary parliamentary republic with its capital in Rome, the largest city in Italy. Other major cities include Milan, Naples, Turin, and Palermo." 
        }, 
    
        { 
            "query": "Where is Papua New Guinea?", 
            "ground-truth": "Papua New Guinea is an island country that lies in the south-western Pacific. It includes the eastern half of New Guinea and many small offshore islands. Its neighbours include Indonesia to the west, Australia to the south and Solomon Islands to the south-east." 
        } 
    ] 
    
    ```

- `evaluators`: Built-in evaluator names.
- `ai_model_configuration`: includes type, `azure_endpoint`, `azure_deployment`, and `api_version`.

### GenAI evaluations workflow

This example shows how to run Azure AI Evaluation when you commit changes to specific files in your repo.

> [!NOTE]
> Update `GENAI_EVALS_DATA_PATH` to point to the correct directory in your repo.

```yml
name: Sample Evaluate Action 
on: 
  workflow_call: 
  workflow_dispatch: 

permissions: 
  id-token: write 
  contents: read 

jobs: 
  evaluate: 
    runs-on: ubuntu-latest 
    env: 
      GENAI_EVALS_CONFIG_PATH: ${{ github.workspace }}/evaluate-config.json 
      GENAI_EVALS_DATA_PATH: ${{ github.workspace }}/.github/.test_files/eval-input.jsonl 
    steps: 
      - uses: actions/checkout@v4 
      - uses: azure/login@v2 
        with: 
          client-id: ${{ secrets.OIDC_AZURE_CLIENT_ID }} 
          tenant-id: ${{ secrets.OIDC_AZURE_TENANT_ID }} 
          subscription-id: ${{ secrets.OIDC_AZURE_SUBSCRIPTION_ID }} 
      - name: Write evaluate config 
        run: | 
          cat > ${{ env.GENAI_EVALS_CONFIG_PATH }} <<EOF 
          { 
            "data": "${{ env.GENAI_EVALS_DATA_PATH }}", 
            "evaluators": { 
              "coherence": "CoherenceEvaluator", 
              "fluency": "FluencyEvaluator" 
            }, 
            "ai_model_configuration": { 
              "type": "azure_openai", 
              "azure_endpoint": "${{ secrets.AZURE_OPENAI_ENDPOINT }}", 
              "azure_deployment": "${{ secrets.AZURE_OPENAI_CHAT_DEPLOYMENT }}", 
              "api_key": "${{ secrets.AZURE_OPENAI_API_KEY }}", 
              "api_version": "${{ secrets.AZURE_OPENAI_API_VERSION }}" 
            } 
          } 
          EOF 
      - name: Run AI Evaluation 
        id: run-ai-evaluation 
        uses: microsoft/genai-evals@main 
        with: 
          evaluate-configuration: ${{ env.GENAI_EVALS_CONFIG_PATH }} 
```

### GenAI evaluations output

The evaluation process outputs results to the summary section for each AI evaluation GitHub Action run. You can view these results under **Actions** in GitHub.com.

The results include three parts:

- Test Variants: a summary of variant names and system prompts.
- Average scores: the average score of each evaluator for each variant.
- Individual test scores: detailed result for each individual test case.

:::image type="content" source="../media/evaluations/github-action-output-results.png" alt-text="Screenshot of result output including test variants, average score, and individual test in GitHub Action." lightbox="../media/evaluations/github-action-output-results.png":::

::: moniker-end

## Related content

- [How to evaluate generative AI models and applications with Microsoft Foundry](./evaluate-generative-ai-app.md)
- [How to view evaluation results in Foundry portal](./evaluate-results.md)
