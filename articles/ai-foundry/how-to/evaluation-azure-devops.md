---
title: How to run an evaluation in Azure DevOps
titleSuffix: Microsoft Foundry
description: How to run evaluation in Azure DevOps, which enables offline evaluation of AI models within your CI/CD pipelines in Azure DevOps. 
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 01/16/2026
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
monikerRange: 'foundry-classic || foundry'
ai-usage: ai-assisted
---

# How to run an evaluation in Azure DevOps (preview)

[!INCLUDE [version-banner](../includes/version-banner.md)]

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

::: moniker range="foundry-classic"

Similar to the [Azure AI evaluation in GitHub Actions](evaluation-github-action.md), an Azure DevOps extension is also available in the Azure DevOps Marketplace. By using this extension, you can evaluate AI agents offline within your CI/CD pipelines.

::: moniker-end

::: moniker range="foundry"

This [Azure DevOps extension](https://marketplace.visualstudio.com/items?itemName=ms-azure-exp-external.microsoft-extension-ai-agent-evaluation) enables offline evaluation of [Microsoft Foundry Agents](../agents/overview.md) within your CI/CD pipelines. It streamlines the offline evaluation process, so you can identify potential problems and make improvements before releasing an update to production.

To use this extension, provide a data set with test queries and a list of evaluators. This task invokes your agents with the queries, evaluates them, and generates a summary report.

::: moniker-end

[!INCLUDE [features](../includes/evaluation-github-action-azure-devops-features.md)]

## Prerequisites

::: moniker range="foundry-classic"

- Foundry project or Hubs based project. To learn more, see [Create a project](create-projects.md).
- Install Azure AI evaluation extension.
  - Go to [Azure DevOps Marketplace](https://marketplace.visualstudio.com/azuredevops).
  - Search for Azure AI evaluation and install the extension into your Azure DevOps organization.

::: moniker-end
  
::: moniker range="foundry"

- A project. To learn more, see [Create a project](create-projects.md).
- Install the [AI Agent AI evaluation extension](https://marketplace.visualstudio.com/items?itemName=ms-azure-exp-external.microsoft-extension-ai-agent-evaluation).

::: moniker-end

::: moniker range="foundry-classic"

## Set up YAML configuration file

1. Create a new YAML file in your repository.
     You can use the sample YAML provided in the README or copy from the [GitHub repo](https://github.com/microsoft/ai-agent-evals?tab=readme-ov-file).
2.  Configure the following inputs:
    - Set up [Azure CLI](/azure/devops/pipelines/tasks/reference/azure-cli-v2) with [service connection](/azure/devops/pipelines/library/service-endpoints?view=azure-devops&preserve-view=true) and Azure Login.
    - Foundry project connection string
    - Dataset and evaluators
      - Specify the evaluator names you want to use for this evaluation run.
      - Queries (required).
    - Agent IDs  Retrieve agent identifiers from Foundry.

  See the following sample dataset:

  ```JSON
  { 
    "name": "MyTestData", 
    "evaluators": [ 
      "FluencyEvaluator", 
      "ViolenceEvaluator" 
    ], 
    "data": [ 
  
      { 
        "query": "Tell me about Tokyo?", 
      }, 
      { 
        "query": "Where is Italy?", 
      } 
    ] 
  } 
  ```

A sample YAML file:

# [Foundry project](#tab/foundry-project)

```yaml

trigger: 
- main 
pool: 

  vmImage: 'windows-latest'  

steps: 

- task: AzureCLI@2 
  inputs: 
    addSpnToEnvironment: true 
    azureSubscription: ${{vars.Service_Connection_Name}}
    scriptType: bash 
    scriptLocation: inlineScript     

    inlineScript: | 
      echo "##vso[task.setvariable variable=ARM_CLIENT_ID]$servicePrincipalId"  
      echo "##vso[task.setvariable variable=ARM_ID_TOEKN]$idToken" 
      echo "##vso[task.setvariable variable=ARM_TENANT_ID]$tenantId" 

- bash: | 

   az login --service-principal -u $(ARM_CLIENT_ID) --tenant $(ARM_TENANT_ID) --allow-no-subscriptions --federated-token $(ARM_ID_TOEKN) 

  displayName: 'Login Azure' 
 
- task: UsePythonVersion@0 
  inputs: 
    versionSpec: '3.11' 
- task: AIAgentEvaluation@0 
  inputs: 
    azure-ai-project-endpoint: "<your-ai-project-endpoint>"
    deployment-name: "gpt-4o-mini" 
    data-path: $(Build.SourcesDirectory)\tests\data\golden-dataset-medium.json 
agent-ids: "<your-ai-agent-ids> 

```

# [Hub-based project](#tab/hub-project)

```yaml

trigger: 
- main 
pool: 

  vmImage: 'windows-latest'  

steps: 

- task: AzureCLI@2 
  inputs: 
    addSpnToEnvironment: true 
    azureSubscription: ${{vars.Service_Connection_Name}}
    scriptType: bash 
    scriptLocation: inlineScript     

    inlineScript: | 
      echo "##vso[task.setvariable variable=ARM_CLIENT_ID]$servicePrincipalId"  
      echo "##vso[task.setvariable variable=ARM_ID_TOEKN]$idToken" 
      echo "##vso[task.setvariable variable=ARM_TENANT_ID]$tenantId" 

- bash: | 

   az login --service-principal -u $(ARM_CLIENT_ID) --tenant $(ARM_TENANT_ID) --allow-no-subscriptions --federated-token $(ARM_ID_TOEKN) 

  displayName: 'Login Azure' 
 
- task: UsePythonVersion@0 
  inputs: 
    versionSpec: '3.11' 
- task: AIAgentEvaluation@0 
  inputs: 
    azure-aiproject-connection-string: 'azure-ai-project-connection-string-sample' 
    deployment-name: "gpt-4o-mini" 
    data-path: $(Build.SourcesDirectory)\tests\data\golden-dataset-medium.json 
agent-ids: "<your-ai-agent-ids> 

```

---

## Set up a new pipeline and trigger an evaluation run

Commit and run the pipeline in Azure DevOps.

## View results

- Select the run and go to the **Azure AI Evaluation** tab.
- The results are shown in this format:
  - The top section summarizes the overview of two AI agent variants. You can select it on the agent ID link, and it directs you to the agent setting page in Microsoft Foundry portal. You can also select the link for **Evaluation Results**, and it directs you to Foundry portal to view individual result in detail.
  - The second section includes evaluation scores and comparison between different variants on statistical significance (for multiple agents) and confidence intervals (for single agent).

Evaluation results and comparisons from multiple AI agents:
:::image type="content" source="../media/evaluations/azure-devops-multi-agent-result.png" alt-text="Screenshot of multi agent evaluation result in Azure DevOps." lightbox="../media/evaluations/azure-devops-multi-agent-result.png":::

Single agent evaluation result:
:::image type="content" source="../media/evaluations/azure-devops-single-agent-result.png" alt-text="Screenshot of single agent evaluation result in Azure DevOps." lightbox="../media/evaluations/azure-devops-single-agent-result.png":::

::: moniker-end

::: moniker range="foundry"

## Inputs

### Parameters

| Name | Required? | Description |
| - | - | - |
| azure-ai-project-endpoint | Yes | Endpoint of your Microsoft Foundry Project. |
| deployment-name | Yes | The name of the Azure AI model deployment to use for evaluation. |
| data-path | Yes | Path to the data file that contains the evaluators and input queries for evaluations. |
| agent-IDs | Yes | ID of one or more agents to evaluate in format `agent-name:version` (for example, `my-agent:1` or `my-agent:1,my-agent:2`). Multiple agents are comma-separated and compared with statistical test results. |
| baseline-agent-id | No | ID of the baseline agent to compare against when evaluating multiple agents. If not provided, the first agent is used. |

### Data file

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

```json

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



## Sample pipeline

To use this Azure DevOps extension, add the task to your Azure Pipeline and configure authentication to access your Microsoft Foundry project.

```yaml
steps:
  - task: AIAgentEvaluation@2
    displayName: "Evaluate AI Agents"
    inputs:
      azure-ai-project-endpoint: "$(AzureAIProjectEndpoint)"
      deployment-name: "$(DeploymentName)"
      data-path: "$(System.DefaultWorkingDirectory)/path/to/your/dataset.json"
      agent-ids: "$(AgentIds)"
```

## Evaluation results and outputs

Evaluation results appear in the Azure DevOps pipeline summary with detailed metrics and comparisons between agents when multiple are evaluated.

Evaluation results output to the summary section for each AI Evaluation task run in your Azure DevOps pipeline.

The following screenshot is a sample report for comparing two agents.

:::image type="content" source="../default/media/observability/github-action-agent-output.png" alt-text="Screenshot of agent evaluation result." lightbox="../default/media/observability/github-action-agent-output.png":::

::: moniker-end


## Related content

- [How to evaluate generative AI models and applications with Foundry](./evaluate-generative-ai-app.md)
- [How to view evaluation results in Foundry portal](./evaluate-results.md)
