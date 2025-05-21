---
title: How to run an evaluation in Azure DevOps
titleSuffix: Azure AI Foundry
description: How to run evaluation in Azure DevOps which enables offline evaluation of AI models within your CI/CD pipelines in Azure DevOps. 
manager: scottpolly
ms.service: azure-ai-foundry
ms.topic: how-to
ms.date: 05/19/2025
ms.reviewer: hanch
ms.author: lagayhar
author: lgayhardt
---

# How to run an evaluation in Azure DevOps (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Similar to the [Azure AI evaluation in GitHub Actions](evaluation-github-action.md), an Azure DevOps extension is also available in the Azure DevOps Marketplace. This extension enables offline evaluation of AI agents within your CI/CD pipelines.

[!INCLUDE [features](../includes/evaluation-github-action-azure-devops-features.md)]

## Prerequisites

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

- Install Azure AI evaluation extension.
  - Go to [Azure DevOps Marketplace](https://marketplace.visualstudio.com/azuredevops).
  - Search for Azure AI evaluation and install the extension into your Azure DevOps organization.

## Set up YAML configuration file

1. Create a new YAML file in your repository.
     You can use the sample YAML provided in the README or copy from the [GitHub repo](https://github.com/microsoft/ai-agent-evals?tab=readme-ov-file).
2.  Configure the following inputs:
    - Set up [Azure CLI](/azure/devops/pipelines/tasks/reference/azure-cli-v2) with [service connection](/azure/devops/pipelines/library/service-endpoints?view=azure-devops&preserve-view=true) and Azure Login.
    - Azure AI project connection string
    - Dataset and evaluators
      - Specify the evaluator names you want to use for this evaluation run.
      - Queries (required).
    - Agent IDs
      Retrieve agent identifiers from the AI Foundry portal.

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

```yml

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

## Set up a new pipeline and trigger an evaluation run

Commit and run the pipeline in Azure DevOps.

## View results

- Select the run and go to "Azure AI Evaluation" tab.
- The results are shown in this format:
  - The top section summarizes the overview of two AI agent variants. You can select it on the agent ID link, and it directs you to the agent setting page in Azure AI Foundry portal. You can also select the link for Evaluation Results, and it directs you to Azure AI Foundry portal to view individual result in detail.
  - The second section includes evaluation scores and comparison between different variants on statistical significance (for multiple agents) and confidence intervals (for single agent).

Evaluation results and comparisons from multiple AI agents:
:::image type="content" source="../media/evaluations/azure-devops-multi-agent-result.png" alt-text="Screenshot of multi agent evaluation result in Azure DevOps." lightbox="../media/evaluations/azure-devops-multi-agent-result.png":::

Single agent evaluation result:
:::image type="content" source="../media/evaluations/azure-devops-single-agent-result.png" alt-text="Screenshot of single agent evaluation result in Azure DevOps." lightbox="../media/evaluations/azure-devops-single-agent-result.png":::

## Related content

- [How to evaluate generative AI models and applications with Azure AI Foundry](./evaluate-generative-ai-app.md)
- [How to view evaluation results in Azure AI Foundry portal](./evaluate-results.md)
