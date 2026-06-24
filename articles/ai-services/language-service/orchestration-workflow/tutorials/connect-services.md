---
title: Integrate custom question answering and conversational language understanding with orchestration workflow
description: Learn how to connect different projects with orchestration workflow. 
keywords: conversational language understanding, bot framework, bot, language understanding, nlu
author: laujan
ms.author: lajanuar
manager: mcleans
ms.reviewer: cahann, hazemelh
ms.service: azure-ai-language
ms.topic: tutorial
ms.date: 11/18/2025
---
<!-- markdownlint-disable MD025 -->

# Integrate custom question answering and conversational language understanding with orchestration workflow

Orchestration workflow lets you connect conversational language understanding and custom question answering projects in one orchestration project. You can then use that project for predictions through a single endpoint, with requests automatically routed to the appropriate downstream task.

This tutorial shows how to prepare the prerequisite projects in Microsoft Foundry and then call the orchestration project using the .NET SDK sample.

## Prerequisites

* Create a [Foundry resource](../../../multi-service-resource.md) or [Language resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesTextAnalytics).
* Complete the [custom question answering quickstart](../../question-answering/quickstart/sdk.md) in Microsoft Foundry.
* Complete the [conversational language understanding quickstart](../../conversational-language-understanding/quickstart.md) in Microsoft Foundry.
* Download the **OrchestrationWorkflowSample** [sample](https://aka.ms/orchestration-sample).

## Prepare the prerequisite projects

Use the Foundry quickstarts to create the projects that the orchestration workflow connects:

1. Create a custom question answering project and deploy it.
1. Create a conversational language understanding project and deploy it.
1. Create an orchestration workflow project and link those tasks.

If you need step-by-step guidance, follow the orchestration workflow [quickstart](../../orchestration-workflow/quickstart.md).

## Call the orchestration project with the Conversations SDK

1. In the downloaded sample, open OrchestrationWorkflowSample.sln in Visual Studio.

1. In the OrchestrationWorkflowSample solution, make sure to install all the required packages. In Visual Studio, go to _Tools_, _NuGet Package Manager_ and select _Package Manager Console_ and run the following command.

```powershell
dotnet add package Azure.AI.Language.Conversations
```

Alternatively, you can search for "Azure.AI.Language.Conversations" in the NuGet package manager and install the latest release.

1. In `Program.cs`, replace `{api-key}` and the `{endpoint}` variables. Use the key and endpoint for the Azure AI resource you created earlier. You can find them in the **Keys and Endpoint** tab in your resource.

```csharp
Uri endpoint = new Uri("{endpoint}");
AzureKeyCredential credential = new AzureKeyCredential("{api-key}");
```

1. Replace the project and deployment parameters with the names you used in Foundry.

```csharp
string projectName = "Orchestrator";
string deploymentName = "Testing";
```

1. Run the project or press F5 in Visual Studio.
1. Input a query such as "read the email from matt" or "hello how are you." You should see different responses for each, with one routed to conversational language understanding and the other routed to custom question answering.

## Next steps

* Learn more about [conversational language understanding](./../../conversational-language-understanding/overview.md).
* Learn more about [custom question answering](./../../question-answering/overview.md).
