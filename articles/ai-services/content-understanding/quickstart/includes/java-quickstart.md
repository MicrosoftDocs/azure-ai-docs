---
title: "Quickstart: Use the Content Understanding Java SDK"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-understanding
ms.topic: include
ms.date: 03/06/2026
ms.author: lahlouchu
ai-usage: ai-assisted
---

<!-- markdownlint-disable MD025 -->

[Client library](https://central.sonatype.com/artifact/com.azure/azure-ai-contentunderstanding) | [Samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding) | [SDK source](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding)

This quickstart shows you how to use the Content Understanding Java SDK to extract structured data using prebuilt analyzers from document, image, audio, and video files. To learn more about prebuilt analyzers and other features, see the documentation of [Prebuilt Analyzers](../concepts/prebuilt-analyzers.md).

## Prerequisites

* An active Azure subscription. If you don't have an Azure account, [create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).
* A [Microsoft Foundry resource](https://portal.azure.com/#create/Microsoft.CognitiveServicesAIFoundry) created in a [supported region](https://learn.microsoft.com/en-us/azure/ai-services/content-understanding/language-region-support).
* Your resource endpoint and API key (found under Keys and Endpoint in the Azure portal).
* Model deployment defaults configured for your resource. See [Models and deployments](../../concepts/models-deployments.md) for setup instructions.
* [Java Development Kit (JDK)](https://learn.microsoft.com/java/openjdk/download) version 8 or later.
* [Apache Maven](https://maven.apache.org/download.cgi).

## Set up

1. Create a new Maven project:

    ```console
    mvn archetype:generate -DgroupId=com.example \
        -DartifactId=content-understanding-quickstart \
        -DarchetypeArtifactId=maven-archetype-quickstart \
        -DinteractiveMode=false
    cd content-understanding-quickstart
    ```

1. Add the Content Understanding dependency to your **pom.xml** file in the `<dependencies>` section:

    ```xml
    <dependency>
        <groupId>com.azure</groupId>
        <artifactId>azure-ai-contentunderstanding</artifactId>
        <version>1.0.0-beta.1</version>
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
1) `CONTENTUNDERSTANDING_ENDPOINT` - the endpoint to your Content Understanding resource.
2) `CONTENTUNDERSTANDING_KEY` - your Content Understanding API key (optional if using [Microsoft Entra ID](../../concepts/secure-communications.md) DefaultAzureCredential).


# [Windows](#tab/windows)

```cmd
setx CONTENTUNDERSTANDING_ENDPOINT "your-endpoint"
setx CONTENTUNDERSTANDING_KEY "your-key"
```

# [Linux / macOS](#tab/linux)

```bash
export CONTENTUNDERSTANDING_ENDPOINT="your-endpoint"
export CONTENTUNDERSTANDING_KEY="your-key"
```

## Create a client

The `ContentUnderstandingClient` is the main entry point for interacting with the service. Create an instance by providing your endpoint and credential.

```java
import com.azure.core.credential.AzureKeyCredential;
import com.azure.ai.contentunderstanding.ContentUnderstandingClient;
import com.azure.ai.contentunderstanding.ContentUnderstandingClientBuilder;

String endpoint = System.getenv("CONTENTUNDERSTANDING_ENDPOINT");
String key = System.getenv("CONTENTUNDERSTANDING_KEY");

ContentUnderstandingClient client =
    new ContentUnderstandingClientBuilder()
        .endpoint(endpoint)
        .credential(new AzureKeyCredential(key))
        .buildClient();
```

## Get started with a prebuilt analyzer

Analyzers define how your content is processed and the insights that are extracted. We offer [prebuilt analyzers](../concepts/prebuilt-analyzers.md) for common use cases. You can [customize prebuilt analyzers](../concepts/prebuilt-analyzers.md) to better fit your specific needs and use cases.
This quickstart uses prebuilt invoice, image, audio, and video analyzers to help you get started.


# [Document](#tab/document)

This example uses the `prebuilt-invoice` analyzer to extract structured data from an invoice document.

```java
// TODO: Document (prebuilt-invoice) code snippet
```

This will produce the following output:
```bash
<!-- TODO: Document output -->
```

> [!NOTE]
> This code is based on the [Sample03_AnalyzeInvoice](https://github.com/Azure/azure-sdk-for-java/blob/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding/Sample03_AnalyzeInvoice.java) sample in the SDK repository.

# [Image](#tab/image)

This example uses the `prebuilt-imageSearch` analyzer to generate a description of the image.

```java
// TODO: Image code snippet
```

This will produce the following output:
```bash
<!-- TODO: Image output -->
```

# [Audio](#tab/audio)

This example uses the `prebuilt-audioSearch` analyzer to extract the audio transcript, generate a summary, and perform speaker labeling.

```java
// TODO: Audio code snippet
```

This will produce the following output:
```text
<!-- TODO: Audio output -->
```

# [Video](#tab/video)

This example uses the `prebuilt-videoSearch` analyzer to extract keyframes, transcript, and chapter segments from video.

```java
// TODO: Video code snippet
```

This will produce the following output:
```text
<!-- TODO: Video output -->
```


## Next steps

* Explore more [Java SDK samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/contentunderstanding/azure-ai-contentunderstanding/src/samples/java/com/azure/ai/contentunderstanding)
* [Create a custom analyzer](../../tutorial/create-custom-analyzer.md)
* [Prebuilt analyzers](../../concepts/prebuilt-analyzers.md)
* [Language and region support](../../language-region-support.md)
