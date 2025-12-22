---
title: Java file for model inference SDK to OpenAI SDK migration
description: Include file
author: msakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.topic: include
ms.date: 11/05/2025
ms.custom: include
---

## Setup

Add the OpenAI SDK to your project. Check the [OpenAI Java GitHub repository](https://github.com/openai/openai-java) for the latest version and installation instructions.

For Microsoft Entra ID authentication, also add:

```xml
<dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.18.0</version>
</dependency>
```

## Client configuration

With API key authentication:

# [OpenAI SDK](#tab/openai)

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;

OpenAIClient client = OpenAIOkHttpClient.builder()
    .baseUrl("https://<resource>.openai.azure.com/openai/v1/")
    .apiKey(System.getenv("AZURE_OPENAI_API_KEY"))
    .build();
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```java
import com.azure.ai.inference.ChatCompletionsClient;
import com.azure.ai.inference.ChatCompletionsClientBuilder;
import com.azure.core.credential.AzureKeyCredential;

ChatCompletionsClient client = new ChatCompletionsClientBuilder()
    .credential(new AzureKeyCredential(System.getenv("AZURE_INFERENCE_CREDENTIAL")))
    .endpoint("https://<resource>.services.ai.azure.com/models")
    .buildClient();
```

---

With Microsoft Entra ID authentication:

# [OpenAI SDK](#tab/openai)

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;

DefaultAzureCredential tokenCredential = new DefaultAzureCredentialBuilder().build();

OpenAIClient client = OpenAIOkHttpClient.builder()
    .baseUrl("https://<resource>.openai.azure.com/openai/v1/")
    .credential(BearerTokenCredential.create(
        AuthenticationUtil.getBearerTokenSupplier(
            tokenCredential, 
            "https://cognitiveservices.azure.com/.default"
        )
    ))
    .build();
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```java
import com.azure.ai.inference.ChatCompletionsClient;
import com.azure.ai.inference.ChatCompletionsClientBuilder;
import com.azure.identity.DefaultAzureCredential;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.azure.core.credential.TokenCredential;

TokenCredential credential = new DefaultAzureCredentialBuilder().build();
ChatCompletionsClient client = new ChatCompletionsClientBuilder()
    .credential(credential)
    .endpoint("https://<resource>.services.ai.azure.com/models")
    .buildClient();
```

---

## Chat completions

# [OpenAI SDK](#tab/openai)

```java
import com.openai.models.chat.completions.*;

ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
    .addSystemMessage("You are a helpful assistant.")
    .addUserMessage("What is Azure AI?")
    .model("DeepSeek-V3.1") // Required: your deployment name
    .build();

ChatCompletion completion = client.chat().completions().create(params);
System.out.println(completion.choices().get(0).message().content());
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```java
import com.azure.ai.inference.models.*;
import java.util.List;

List<ChatRequestMessage> messages = List.of(
    new ChatRequestSystemMessage("You are a helpful assistant."),
    new ChatRequestUserMessage("What is Azure AI?")
);

ChatCompletionsOptions options = new ChatCompletionsOptions(messages);
options.setModel("DeepSeek-V3.1"); // Optional for single-model endpoints

ChatCompletions response = client.complete(options);
System.out.println(response.getChoices().get(0).getMessage().getContent());
```

---

### Streaming

# [OpenAI SDK](#tab/openai)

```java
import com.openai.models.chat.completions.*;
import java.util.stream.Stream;

ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
    .addSystemMessage("You are a helpful assistant.")
    .addUserMessage("Write a poem about Azure.")
    .model("DeepSeek-V3.1") // Required: your deployment name
    .build();

Stream<ChatCompletionChunk> stream = client.chat().completions().createStreaming(params);

stream.forEach(chunk -> {
    if (chunk.choices() != null && !chunk.choices().isEmpty()) {
        String content = chunk.choices().get(0).delta().content();
        if (content != null) {
            System.out.print(content);
        }
    }
});
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```java
import com.azure.ai.inference.models.*;

List<ChatRequestMessage> messages = List.of(
    new ChatRequestSystemMessage("You are a helpful assistant."),
    new ChatRequestUserMessage("Write a poem about Azure.")
);

ChatCompletionsOptions options = new ChatCompletionsOptions(messages);
options.setModel("DeepSeek-V3.1");

IterableStream<ChatCompletions> response = client.completeStream(options);

response.forEach(update -> {
    if (update.getChoices() != null && !update.getChoices().isEmpty()) {
        String content = update.getChoices().get(0).getDelta().getContent();
        if (content != null) {
            System.out.print(content);
        }
    }
});
```

---

## Embeddings

# [OpenAI SDK](#tab/openai)

```java
package com.openai.example;

import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.embeddings.EmbeddingCreateParams;
import com.openai.models.embeddings.EmbeddingModel;

public final class EmbeddingsExample {
    private EmbeddingsExample() {}

    public static void main(String[] args) {
        // Configures using one of:
        // - The `OPENAI_API_KEY` environment variable
        // - The `OPENAI_BASE_URL` and `AZURE_OPENAI_KEY` environment variables
        OpenAIClient client = OpenAIOkHttpClient.fromEnv();

        EmbeddingCreateParams createParams = EmbeddingCreateParams.builder()
                .input("The quick brown fox jumped over the lazy dog")
                .model(EmbeddingModel.TEXT_EMBEDDING_3_SMALL)
                .build();

        System.out.println(client.embeddings().create(createParams));
    }
}
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

```java
import com.azure.ai.inference.EmbeddingsClient;
import com.azure.ai.inference.EmbeddingsClientBuilder;
import com.azure.core.credential.AzureKeyCredential;

EmbeddingsClient client = new EmbeddingsClientBuilder()
    .credential(new AzureKeyCredential(System.getenv("AZURE_INFERENCE_CREDENTIAL")))
    .endpoint("https://<resource>.services.ai.azure.com/models")
    .buildClient();

EmbeddingsOptions embeddingsOptions = new EmbeddingsOptions(
    List.of("Your text string goes here")
);
embeddingsOptions.setModel("text-embedding-3-small");

EmbeddingsResult response = client.embed(embeddingsOptions);
List<Float> embedding = response.getData().get(0).getEmbedding();
```

---