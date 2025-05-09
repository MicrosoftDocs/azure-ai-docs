---
title: How to run evaluation in Azure DevOps
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

# How to run evaluation in Azure DevOps (preview)

[!INCLUDE [feature-preview](../includes/feature-preview.md)]

Similar to Azure AI evaluation in GitHub Action, an Azure DevOps extension is also provided in Azure DevOps marketplace which enables offline evaluation of AI models within your CI/CD pipelines in Azure DevOps. The supported feature or evaluators can be found, [GitHub Action](evaluation-github-action.md)

[!INCLUDE [features](../includes/evaluation-github-action-azure-devops-features.md)]

## Prerequisites

[!INCLUDE [hub-only-prereq](../includes/hub-only-prereq.md)]

- Install Azure AI evaluation extension.
  - Go to [Azure DevOps Marketplace](https://marketplace.visualstudio.com/azuredevops).
  - Search for Azure AI evaluation and install the extension into your Azure DevOps organization.

## Set up YAML configuration file

1. Create a new YAML file in your repository.
     You can use the sample YAML provided in the README or clone from the [GitHub repo](https://github.com/microsoft/ai-agent-evals?tab=readme-ov-file).
2.  Configure the following inputs:
    - Set up [Azure CLI](/azure/devops/pipelines/tasks/reference/azure-cli-v2) with [service connection](/azure/devops/pipelines/library/service-endpoints?view=azure-devops&preserve-view=true) and Azure Login.
    - Azure AI project connection string
    - Dataset and evaluators
      - Specify the evaluator names you want to use for this evaluation run.
      - Queries (required) and Ground Truth (optional).

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
          "ground_truth": "Tokyo is the capital of Japan and the largest city in the country. It is located on the eastern coast of Honshu, the largest of Japan's four main islands. Tokyo is the political, economic, and cultural center of Japan and is one of the world's most populous cities. It is also one of the world's most important financial centers and is home to the Tokyo Stock Exchange." 
        }, 
        { 
          "query": "Where is Italy?", 
          "ground_truth": "Italy is a country in southern Europe, located on the Italian Peninsula and the two largest islands in the Mediterranean Sea, Sicily and Sardinia. It is a unitary parliamentary republic with its capital in Rome, the largest city in Italy. Other major cities include Milan, Naples, Turin, and Palermo." 
        } 
      ] 
    } 
    ```

   - Agent IDs
      Retrieve agent identifiers from the AI Foundry portal.

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
    azureSubscription: 'az-dev-gh-aprilk-test-connection' 
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
    api-version: "2024-08-01-preview" 
    data-path: $(Build.SourcesDirectory)\tests\data\golden-dataset-medium.json 
agent-ids: 'agent-id1, agent-id2' 

```

## Set up a new pipeline and trigger an evaluation run

Commit and run the pipeline in Azure DevOps.

## View results

- Select the run and go to "Azure AI Evaluation" tab.
- The results are shown in the same format as GitHub Action results.
  - The top section summarizes the overview of two AI agent variants. You can select it on the agent ID link, and it directs you to the agent setting page in Azure AI Foundry portal. You can also select the link for Evaluation Results, and it directs you to Azure AI Foundry portal to view individual result in detail.
  - The second section includes evaluation scores and comparison between different variants on statistical significance (for multiple agents) and confidence intervals (for single agent).

Multi agent evaluation result:
:::image type="content" source="../media/evaluations/azure-devops-multi-agent-result.png" alt-text="Screenshot of multi agent evaluation result in Azure DevOps." lightbox="../media/evaluations/azure-devops-multi-agent-result.png":::

Single agent evaluation result:
:::image type="content" source="../media/evaluations/azure-devops-single-agent-result.png" alt-text="Screenshot of single agent evaluation result in Azure DevOps." lightbox="../media/evaluations/azure-devops-single-agent-result.png":::

## Related content

- [How to evaluate generative AI models and applications with Azure AI Foundry](./evaluate-generative-ai-app.md)
- [How to view evaluation results in Azure AI Foundry portal](./evaluate-results.md)
