---
title: Azure OpenAI Java support
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Azure OpenAI Java support
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/27/2025
---


[Source code](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai) | [Artifact (Maven)](https://central.sonatype.com/artifact/com.azure/azure-ai-openai/1.0.0-beta.12) | [API reference documentation](../../reference.md) | [Package reference documentation](/java/api/overview/azure/ai-openai-readme?view=azure-java-preview&preserve-view=true)   [Samples](https://github.com/Azure/azure-sdk-for-java/tree/main/sdk/openai/azure-ai-openai/src/samples)

## Azure OpenAI API version support

Unlike the Azure OpenAI client libraries for Python and JavaScript, to ensure compatibility the Azure OpenAI Java package is limited to targeting a specific subset of the Azure OpenAI API versions. Generally each Azure OpenAI Java package unlocks access to newer Azure OpenAI API release features. Having access to the latest API versions impacts feature availability.

Version selection is controlled by the [`OpenAIServiceVersion`](/java/api/com.azure.ai.openai.openaiserviceversion?view=azure-java-preview&preserve-view=true) enum.

The latest Azure OpenAI preview API supported is:

-`2025-01-01-preview`

The latest stable (GA) release supported is:

-`2024-06-01`

## Installation

### Package details

```XML
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-ai-openai</artifactId>
    <version>1.0.0-beta.16</version>
</dependency>
```

## Authentication

In order to interact with the Azure OpenAI in Azure AI Foundry Models you'll need to create an instance of client class, [`OpenAIAsyncClient`](https://github.com/Azure/azure-sdk-for-java/blob/azure-ai-openai_1.0.0-beta.12/sdk/openai/azure-ai-openai/src/main/java/com/azure/ai/openai/OpenAIAsyncClient.java) or [`OpenAIClient`](https://github.com/Azure/azure-sdk-for-java/blob/azure-ai-openai_1.0.0-beta.12/sdk/openai/azure-ai-openai/src/main/java/com/azure/ai/openai/OpenAIClient.java) by using [`OpenAIClientBuilder`](https://github.com/Azure/azure-sdk-for-java/blob/azure-ai-openai_1.0.0-beta.12/sdk/openai/azure-ai-openai/src/main/java/com/azure/ai/openai/OpenAIClientBuilder.java). To configure a client for use with Azure OpenAI, provide a valid endpoint URI to an Azure OpenAI resource along with a corresponding key credential, token credential, or Azure Identity credential that's authorized to use the Azure OpenAI resource.

# [Microsoft Entra ID](#tab/secure)

Authentication with Microsoft Entra ID requires some initial setup:

Add the Azure Identity package:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.13.3</version>
</dependency>
```

After setup, you can choose which type of credential from `azure.identity` to use. As an example, `DefaultAzureCredential` can be used to authenticate the client: Set the values of the client ID, tenant ID, and client secret of the Microsoft Entra ID application as environment variables: AZURE_CLIENT_ID, AZURE_TENANT_ID, AZURE_CLIENT_SECRET.

Authorization is easiest using DefaultAzureCredential. It finds the best credential to use in its running environment. 

```java
TokenCredential defaultCredential = new DefaultAzureCredentialBuilder().build();
OpenAIClient client = new OpenAIClientBuilder()
    .credential(defaultCredential)
    .endpoint("{endpoint}")
    .buildClient();
```

For more information about Azure OpenAI keyless authentication, see [Use Azure OpenAI without keys](/azure/developer/ai/keyless-connections?tabs=java%2Cazure-cli). 

# [API Key](#tab/api-key)

```java
OpenAIClient client = new OpenAIClientBuilder()
    .credential(new AzureKeyCredential("{key}"))
    .endpoint("{endpoint}")
    .buildClient();
```

Async

```java
OpenAIAsyncClient client = new OpenAIClientBuilder()
    .credential(new AzureKeyCredential("{key}"))
    .endpoint("{endpoint}")
    .buildAsyncClient();
```

---

## Audio

### client.getAudioTranscription

```java
String fileName = "{your-file-name}";
Path filePath = Paths.get("{your-file-path}" + fileName);

byte[] file = BinaryData.fromFile(filePath).toBytes();
AudioTranscriptionOptions transcriptionOptions = new AudioTranscriptionOptions(file)
    .setResponseFormat(AudioTranscriptionFormat.JSON);

AudioTranscription transcription = client.getAudioTranscription("{deploymentOrModelName}", fileName, transcriptionOptions);

System.out.println("Transcription: " + transcription.getText());
```

### client.generateSpeechFromText

**Text to speech (TTS)**

```java
String deploymentOrModelId = "{azure-open-ai-deployment-model-id}";
SpeechGenerationOptions options = new SpeechGenerationOptions(
        "Today is a wonderful day to build something people love!",
        SpeechVoice.ALLOY);
BinaryData speech = client.generateSpeechFromText(deploymentOrModelId, options);
// Checkout your generated speech in the file system.
Path path = Paths.get("{your-local-file-path}/speech.wav");
Files.write(path, speech.toBytes());
```

## Chat

### client.getChatCompletions

```java
List<ChatRequestMessage> chatMessages = new ArrayList<>();
chatMessages.add(new ChatRequestSystemMessage("You are a helpful assistant. You will talk like a pirate."));
chatMessages.add(new ChatRequestUserMessage("Can you help me?"));
chatMessages.add(new ChatRequestAssistantMessage("Of course, me hearty! What can I do for ye?"));
chatMessages.add(new ChatRequestUserMessage("What's the best way to train a parrot?"));

ChatCompletions chatCompletions = client.getChatCompletions("{deploymentOrModelName}",
    new ChatCompletionsOptions(chatMessages));

System.out.printf("Model ID=%s is created at %s.%n", chatCompletions.getId(), chatCompletions.getCreatedAt());
for (ChatChoice choice : chatCompletions.getChoices()) {
    ChatResponseMessage message = choice.getMessage();
    System.out.printf("Index: %d, Chat Role: %s.%n", choice.getIndex(), message.getRole());
    System.out.println("Message:");
    System.out.println(message.getContent());
}
```

### Streaming

```java
List<ChatRequestMessage> chatMessages = new ArrayList<>();
chatMessages.add(new ChatRequestSystemMessage("You are a helpful assistant. You will talk like a pirate."));
chatMessages.add(new ChatRequestUserMessage("Can you help me?"));
chatMessages.add(new ChatRequestAssistantMessage("Of course, me hearty! What can I do for ye?"));
chatMessages.add(new ChatRequestUserMessage("What's the best way to train a parrot?"));

ChatCompletions chatCompletions = client.getChatCompletions("{deploymentOrModelName}",
    new ChatCompletionsOptions(chatMessages));

System.out.printf("Model ID=%s is created at %s.%n", chatCompletions.getId(), chatCompletions.getCreatedAt());
for (ChatChoice choice : chatCompletions.getChoices()) {
    ChatResponseMessage message = choice.getMessage();
    System.out.printf("Index: %d, Chat Role: %s.%n", choice.getIndex(), message.getRole());
    System.out.println("Message:");
    System.out.println(message.getContent());
}
```

### Chat completions with images

```java
List<ChatRequestMessage> chatMessages = new ArrayList<>();
chatMessages.add(new ChatRequestSystemMessage("You are a helpful assistant that describes images"));
chatMessages.add(new ChatRequestUserMessage(Arrays.asList(
        new ChatMessageTextContentItem("Please describe this image"),
        new ChatMessageImageContentItem(
                new ChatMessageImageUrl("https://raw.githubusercontent.com/MicrosoftDocs/azure-ai-docs/main/articles/ai-services/openai/media/how-to/generated-seattle.png"))
)));

ChatCompletionsOptions chatCompletionsOptions = new ChatCompletionsOptions(chatMessages);
ChatCompletions chatCompletions = client.getChatCompletions("{deploymentOrModelName}", chatCompletionsOptions);

System.out.println("Chat completion: " + chatCompletions.getChoices().get(0).getMessage().getContent());
```

## Embeddings

### client.getEmbeddings

```java
EmbeddingsOptions embeddingsOptions = new EmbeddingsOptions(
    Arrays.asList("Your text string goes here"));

Embeddings embeddings = client.getEmbeddings("{deploymentOrModelName}", embeddingsOptions);

for (EmbeddingItem item : embeddings.getData()) {
    System.out.printf("Index: %d.%n", item.getPromptIndex());
    for (Float embedding : item.getEmbedding()) {
        System.out.printf("%f;", embedding);
    }
}
```

## Image generation

```java
ImageGenerationOptions imageGenerationOptions = new ImageGenerationOptions(
    "A drawing of the Seattle skyline in the style of Van Gogh");
ImageGenerations images = client.getImageGenerations("{deploymentOrModelName}", imageGenerationOptions);

for (ImageGenerationData imageGenerationData : images.getData()) {
    System.out.printf(
        "Image location URL that provides temporary access to download the generated image is %s.%n",
        imageGenerationData.getUrl());
}
```

## Handling errors

### Enable client logging

To troubleshoot issues with Azure OpenAI library, it's important to first enable logging to monitor the
behavior of the application. The errors and warnings in the logs generally provide useful insights into what went wrong
and sometimes include corrective actions to fix issues. The Azure client libraries for Java have two logging options:

* A built-in logging framework.
* Support for logging using the [SLF4J](https://www.slf4j.org/) interface.

Refer to the instructions in this reference document on how to [configure logging in Azure SDK for Java][logging_overview].

### Enable HTTP request/response logging

Reviewing the HTTP request sent or response received over the wire to/from the Azure OpenAI service can be
useful in troubleshooting issues. To enable logging the HTTP request and response payload, the [OpenAIClient][openai_client]
can be configured as shown below. If there's no SLF4J's `Logger` on the class path, set an environment variable
[AZURE_LOG_LEVEL][azure_log_level] in your machine to enable logging.

```java readme-sample-enablehttplogging
OpenAIClient openAIClient = new OpenAIClientBuilder()
        .endpoint("{endpoint}")
        .credential(new AzureKeyCredential("{key}"))
        .httpLogOptions(new HttpLogOptions().setLogLevel(HttpLogDetailLevel.BODY_AND_HEADERS))
        .buildClient();
// or
DefaultAzureCredential credential = new DefaultAzureCredentialBuilder().build();
OpenAIClient configurationClientAad = new OpenAIClientBuilder()
        .credential(credential)
        .endpoint("{endpoint}")
        .httpLogOptions(new HttpLogOptions().setLogLevel(HttpLogDetailLevel.BODY_AND_HEADERS))
        .buildClient();
```

Alternatively, you can configure logging HTTP requests and responses for your entire application by setting the
following environment variable. Note that this change will enable logging for every Azure client that supports logging
HTTP request/response.

Environment variable name: `AZURE_HTTP_LOG_DETAIL_LEVEL`

| Value            | Logging level                                                        |
|------------------|----------------------------------------------------------------------|
| none             | HTTP request/response logging is disabled                            |
| basic            | Logs only URLs, HTTP methods, and time to finish the request.        |
| headers          | Logs everything in BASIC, plus all the request and response headers. |
| body             | Logs everything in BASIC, plus all the request and response body.    |
| body_and_headers | Logs everything in HEADERS and BODY.                                 |

> [!NOTE]
> When logging the body of request and response, ensure that they don't contain confidential
information. When logging headers, the client library has a default set of headers that are considered safe to log
but this set can be updated by updating the log options in the builder as shown below.

```java
clientBuilder.httpLogOptions(new HttpLogOptions().addAllowedHeaderName("safe-to-log-header-name"))
```

### Troubleshooting exceptions
Azure OpenAI service methods throw a`[HttpResponseException` or its subclass on failure.
The `HttpResponseException` thrown by the OpenAI client library includes detailed response error object
that provides specific useful insights into what went wrong and includes corrective actions to fix common issues.
This error information can be found inside the message property of the `HttpResponseException` object.

Here's the example of how to catch it with synchronous client

```java readme-sample-troubleshootingExceptions
List<ChatRequestMessage> chatMessages = new ArrayList<>();
chatMessages.add(new ChatRequestSystemMessage("You are a helpful assistant. You will talk like a pirate."));
chatMessages.add(new ChatRequestUserMessage("Can you help me?"));
chatMessages.add(new ChatRequestAssistantMessage("Of course, me hearty! What can I do for ye?"));
chatMessages.add(new ChatRequestUserMessage("What's the best way to train a parrot?"));

try {
    ChatCompletions chatCompletions = client.getChatCompletions("{deploymentOrModelName}",
            new ChatCompletionsOptions(chatMessages));
} catch (HttpResponseException e) {
    System.out.println(e.getMessage());
    // Do something with the exception
}
```

With async clients, you can catch and handle exceptions in the error callbacks:

```java readme-sample-troubleshootingExceptions-async
asyncClient.getChatCompletions("{deploymentOrModelName}", new ChatCompletionsOptions(chatMessages))
        .doOnSuccess(ignored -> System.out.println("Success!"))
        .doOnError(
                error -> error instanceof ResourceNotFoundException,
                error -> System.out.println("Exception: 'getChatCompletions' could not be performed."));
```

### Authentication errors

Azure OpenAI supports Microsoft Entra ID authentication. `OpenAIClientBuilder`
has method to set the `credential`. To provide a valid credential, you can use `azure-identity` dependency. 


