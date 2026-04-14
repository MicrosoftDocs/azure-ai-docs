---
title: "How-to: Copy custom analyzers using the Content Understanding .NET SDK"
author: PatrickFarley
manager: nitinme
description: Learn to copy custom analyzers with Content Understanding using the .NET SDK.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 04/14/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

This guide shows you how to use the Content Understanding .NET SDK to copy custom analyzers within a resource and across Foundry resources.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* Your resource endpoint and API key.
* The current version of [.NET](https://dotnet.microsoft.com/download/dotnet).
* An existing custom analyzer in your resource. See [Create a custom analyzer](../../tutorial/create-custom-analyzer.md) if you need to create one.

## Set up

1. Create a new .NET console application:

    ```console
    dotnet new console -n CopyAnalyzerExample
    cd CopyAnalyzerExample
    ```

1. Install the Content Understanding client library for .NET:

    ```console
    dotnet add package Azure.AI.ContentUnderstanding
    ```

1. Optionally, install the Azure Identity library for Microsoft Entra authentication:

    ```console
    dotnet add package Azure.Identity
    ```

## Set up environment variables

To authenticate with the Content Understanding service, set the environment variables with your own values before running the sample:
- `CONTENTUNDERSTANDING_ENDPOINT` - the endpoint to your Content Understanding resource.
- `CONTENTUNDERSTANDING_KEY` - your Content Understanding API key (optional if using [Microsoft Entra ID](../../concepts/secure-communications.md) DefaultAzureCredential).

### Windows

```cmd
setx CONTENTUNDERSTANDING_ENDPOINT "your-endpoint"
setx CONTENTUNDERSTANDING_KEY "your-key"
```

### Linux / macOS

```bash
export CONTENTUNDERSTANDING_ENDPOINT="your-endpoint"
export CONTENTUNDERSTANDING_KEY="your-key"
```

## Create the client

```csharp
using Azure;
using Azure.AI.ContentUnderstanding;
using Azure.Identity;

string endpoint = "<endpoint>";
string apiKey = "<apiKey>";
var client = new ContentUnderstandingClient(
    new Uri(endpoint),
    new AzureKeyCredential(apiKey));
```

## Copy within a Foundry resource

To copy an analyzer within the same resource, call the `CopyAnalyzerAsync` method with the target and source analyzer IDs.

```csharp
string sourceAnalyzerId = "my-source-analyzer";
string targetAnalyzerId = "my-target-analyzer";

await client.CopyAnalyzerAsync(
    WaitUntil.Completed,
    targetAnalyzerId,
    sourceAnalyzerId);
```

> [!TIP]
> This code is based on the [copy analyzer sample](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples/Sample14_CopyAnalyzer.md) in the SDK repository.

## Copy across Foundry resources

Copying an analyzer across Foundry resources is a multi-step process:

1. Grant copy authorization on the source resource.
1. Use the authorization to call the copy API on the target resource.

> [!IMPORTANT]
> Both the source and target resources require the **Cognitive Services User** role to be granted to the credential used to run the code. This role is required for cross-resource copying operations.

```csharp
// Get source endpoint from configuration
string sourceEndpoint =
    "https://source-resource.services.ai.azure.com/";

// Create source client using DefaultAzureCredential
ContentUnderstandingClient sourceClient =
    new ContentUnderstandingClient(
        new Uri(sourceEndpoint),
        new DefaultAzureCredential());

// Source analyzer ID (must already exist in the source resource)
string sourceAnalyzerId =
    "my_source_analyzer";
// Target analyzer ID (will be created during copy)
string targetAnalyzerId =
    "my_target_analyzer";

// Get source and target resource information
string sourceResourceId =
    "/subscriptions/{subscriptionId}"
    + "/resourceGroups/{resourceGroupName}"
    + "/providers/Microsoft.CognitiveServices"
    + "/accounts/{name}";
string sourceRegion = "eastus";
string targetEndpoint =
    "https://target-resource.services.ai.azure.com/";
string targetResourceId =
    "/subscriptions/{subscriptionId}"
    + "/resourceGroups/{resourceGroupName}"
    + "/providers/Microsoft.CognitiveServices"
    + "/accounts/{name}";
string targetRegion = "westus";

// Create target client using DefaultAzureCredential
ContentUnderstandingClient targetClient =
    new ContentUnderstandingClient(
        new Uri(targetEndpoint),
        new DefaultAzureCredential());

// Step 1: Grant copy authorization
var copyAuth = await
    sourceClient.GrantCopyAuthorizationAsync(
        sourceAnalyzerId,
        targetResourceId,
        targetRegion);

Console.WriteLine("Copy authorization granted successfully!");
Console.WriteLine(
    $"  Target Azure Resource ID: "
    + $"{copyAuth.Value.TargetAzureResourceId}");
Console.WriteLine(
    $"  Expires at: {copyAuth.Value.ExpiresAt}");

// Step 2: Copy analyzer to target resource
var copyOperation = await
    targetClient.CopyAnalyzerAsync(
        WaitUntil.Completed,
        targetAnalyzerId,
        sourceAnalyzerId,
        sourceResourceId,
        sourceRegion);

var targetResult = copyOperation.Value;
Console.WriteLine(
    $"Target analyzer '{targetAnalyzerId}' "
    + "copied successfully to target resource!");
Console.WriteLine(
    $"Target analyzer description: "
    + $"{targetResult.Description}");
```

> [!TIP]
> This code is based on the [grant copy auth sample](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/contentunderstanding/Azure.AI.ContentUnderstanding/samples/Sample15_GrantCopyAuth.md) in the SDK repository.

> [!NOTE]
>
> Analyzers now support classification/segmentation and analysis of each of the identified classes and segments in a single request. When copying an analyzer that uses this feature, you need to copy any referenced analyzers as well.

## Verify the copy

Validate that the analyzer was copied by retrieving it from the target resource.

```csharp
var analyzerDetails = await
    targetClient.GetAnalyzerAsync(targetAnalyzerId);
var result = analyzerDetails.Value;

Console.WriteLine(
    $"Analyzer '{targetAnalyzerId}' found.");
if (result.Description != null)
{
    Console.WriteLine(
        $"  Description: {result.Description}");
}
```
