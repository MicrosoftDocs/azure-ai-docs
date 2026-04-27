---
title: "How-to: Copy custom analyzers using the Content Understanding Java SDK"
author: PatrickFarley
manager: nitinme
description: Learn to copy custom analyzers with Content Understanding using the Java SDK.
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 04/14/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

This guide shows you how to use the Content Understanding Java SDK to copy custom analyzers within a resource and across Foundry resources.

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](../../language-region-support.md).
* Your resource endpoint and API key.
* [Java Development Kit (JDK)](/java/openjdk/download) version 8 or later.
* [Apache Maven](https://maven.apache.org/download.cgi).
* An existing custom analyzer in your resource. See [Create a custom analyzer](../../tutorial/create-custom-analyzer.md) if you need to create one.

## Set up

1. Add the Content Understanding dependency to your **pom.xml** file in the `<dependencies>` section:

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-ai-contentunderstanding</artifactId>
        <version>1.0.0</version>
    </dependency>
    ```

1. Optionally, add the Azure Identity library for Microsoft Entra authentication:

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-identity</artifactId>
        <version>1.14.2</version>
    </dependency>
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

```java
import com.azure.core.credential.AzureKeyCredential;
import com.azure.core.util.polling.SyncPoller;
import com.azure.ai.contentunderstanding.ContentUnderstandingClient;
import com.azure.ai.contentunderstanding.ContentUnderstandingClientBuilder;
import com.azure.ai.contentunderstanding.models.ContentAnalyzer;
import com.azure.ai.contentunderstanding.models.ContentAnalyzerOperationStatus;
import com.azure.ai.contentunderstanding.models.CopyAuthorization;
import com.azure.identity.DefaultAzureCredentialBuilder;

String endpoint = System.getenv("CONTENTUNDERSTANDING_ENDPOINT");
String key = System.getenv("CONTENTUNDERSTANDING_KEY");

ContentUnderstandingClientBuilder builder =
    new ContentUnderstandingClientBuilder()
        .endpoint(endpoint);

ContentUnderstandingClient client;
if (key != null && !key.trim().isEmpty()) {
    client = builder.credential(
        new AzureKeyCredential(key)).buildClient();
} else {
    client = builder.credential(
        new DefaultAzureCredentialBuilder()
            .build()).buildClient();
}
```

## Copy within a Foundry resource

To copy an analyzer within the same resource, call the `beginCopyAnalyzer` method with the target and source analyzer IDs.

```java
String sourceAnalyzerId = "my-source-analyzer";
String targetAnalyzerId = "my-target-analyzer";

SyncPoller<ContentAnalyzerOperationStatus, ContentAnalyzer>
    copyPoller = client.beginCopyAnalyzer(
        targetAnalyzerId, sourceAnalyzerId);
ContentAnalyzer copiedAnalyzer =
    copyPoller.getFinalResult();

System.out.println(
    "Analyzer copied to '"
    + targetAnalyzerId + "' successfully!");
```

> [!TIP]
> This code is based on the [copy analyzer sample](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample14_CopyAnalyzer.java) in the SDK repository.

## Copy across Foundry resources

Copying an analyzer across Foundry resources is a multi-step process:

1. Grant copy authorization on the source resource.
1. Use the authorization to call the copy API on the target resource.

> [!IMPORTANT]
> Both the source and target resources require the **Cognitive Services User** role to be granted to the credential used to run the code. This role is required for cross-resource copying operations.

Example resource ID format:
`/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.CognitiveServices/accounts/{name}`

```java
String sourceEndpoint =
    System.getenv("CONTENTUNDERSTANDING_ENDPOINT");
String sourceKey =
    System.getenv("CONTENTUNDERSTANDING_KEY");
String sourceResourceId =
    System.getenv(
        "CONTENTUNDERSTANDING_SOURCE_RESOURCE_ID");
String sourceRegion =
    System.getenv(
        "CONTENTUNDERSTANDING_SOURCE_REGION");
String targetEndpoint =
    System.getenv(
        "CONTENTUNDERSTANDING_TARGET_ENDPOINT");
String targetKey =
    System.getenv("CONTENTUNDERSTANDING_TARGET_KEY");
String targetResourceId =
    System.getenv(
        "CONTENTUNDERSTANDING_TARGET_RESOURCE_ID");
String targetRegion =
    System.getenv(
        "CONTENTUNDERSTANDING_TARGET_REGION");

String sourceAnalyzerId = "my-source-analyzer";
String targetAnalyzerId = "my-target-analyzer";

// Build source client
ContentUnderstandingClientBuilder sourceBuilder =
    new ContentUnderstandingClientBuilder()
        .endpoint(sourceEndpoint);
ContentUnderstandingClient sourceClient;
if (sourceKey != null
    && !sourceKey.trim().isEmpty()) {
    sourceClient = sourceBuilder.credential(
        new AzureKeyCredential(sourceKey))
        .buildClient();
} else {
    sourceClient = sourceBuilder.credential(
        new DefaultAzureCredentialBuilder()
            .build()).buildClient();
}

// Build target client
ContentUnderstandingClientBuilder targetBuilder =
    new ContentUnderstandingClientBuilder()
        .endpoint(targetEndpoint);
ContentUnderstandingClient targetClient;
if (targetKey != null
    && !targetKey.trim().isEmpty()) {
    targetClient = targetBuilder.credential(
        new AzureKeyCredential(targetKey))
        .buildClient();
} else {
    targetClient = targetBuilder.credential(
        new DefaultAzureCredentialBuilder()
            .build()).buildClient();
}

// Step 1: Grant copy authorization on source client
CopyAuthorization copyAuth =
    sourceClient.grantCopyAuthorization(
        sourceAnalyzerId,
        targetResourceId,
        targetRegion);

System.out.println(
    "Copy authorization granted successfully!");
System.out.println(
    "  Target Azure Resource ID: "
    + copyAuth.getTargetAzureResourceId());
System.out.println(
    "  Expires at: " + copyAuth.getExpiresAt());

// Step 2: Copy analyzer to target resource
SyncPoller<ContentAnalyzerOperationStatus,
    ContentAnalyzer> copyPoller =
    targetClient.beginCopyAnalyzer(
        targetAnalyzerId,
        sourceAnalyzerId,
        false,
        sourceResourceId,
        sourceRegion);

ContentAnalyzer targetResult =
    copyPoller.getFinalResult();
System.out.println(
    "Target analyzer '"
    + targetAnalyzerId + "' copied successfully!");
System.out.println(
    "  Description: "
    + targetResult.getDescription());
```

> [!TIP]
> This code is based on the [grant copy auth sample](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/samples/Sample15_GrantCopyAuth.java) in the SDK repository.

> [!NOTE]
>
> Analyzers now support classification/segmentation and analysis of each of the identified classes and segments in a single request. When copying an analyzer that uses this feature, you need to copy any referenced analyzers as well.

## Verify the copy

Validate that the analyzer was copied by retrieving it from the target resource.

```java
ContentAnalyzer analyzer =
    targetClient.getAnalyzer(targetAnalyzerId);

System.out.println(
    "Analyzer '" + targetAnalyzerId + "' found.");
if (analyzer.getDescription() != null) {
    System.out.println(
        "  Description: "
        + analyzer.getDescription());
}
```
