---
title: Java file for model inference SDK to OpenAI SDK migration
description: Include file
author: msakande
ms.author: mopeakande
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.topic: include
ms.date: 06/04/2026
ms.custom: include
ai-usage: ai-assisted
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
            "https://ai.azure.com/.default"
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
    .addUserMessage("How many languages are in the world?")
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
    new ChatRequestUserMessage("How many languages are in the world?")
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

## Responses

The Responses API is OpenAI's stateful interface that returns a structured `output` array containing message, tool call, and reasoning items.

# [OpenAI SDK](#tab/openai)

```java
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

Response response = client.responses().create(
    ResponseCreateParams.builder()
        .model("DeepSeek-V3.1") // Required: your deployment name
        .input("How many languages are in the world?")
        .maxOutputTokens(2000)
        .build()
);

System.out.println(response.outputText());
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

The Azure AI Inference SDK doesn't expose the Responses API. To call it, use the OpenAI SDK.

---

### Reasoning

> [!NOTE]
> This information on reasoning content doesn't apply to Azure OpenAI models. Azure OpenAI reasoning models use the [reasoning summaries feature](../../openai/how-to/reasoning.md#reasoning-summary).

Some reasoning models, like DeepSeek-R1, generate completions and include the reasoning behind them. The Responses API surfaces this as a structured `reasoning` output item whose `summary[].text` contains the model's thinking, alongside the final answer.

# [OpenAI SDK](#tab/openai)

```java
import com.openai.models.responses.Response;
import com.openai.models.responses.ResponseCreateParams;

Response response = client.responses().create(
    ResponseCreateParams.builder()
        .model("DeepSeek-R1-0528") // Required: your deployment name
        .input("How many languages are in the world?")
        .maxOutputTokens(2000)
        .build()
);

// Walk response.output() for items of type "reasoning" and join summary[].text.
StringBuilder sb = new StringBuilder();
response.output().stream()
    .flatMap(item -> item.reasoning().stream())
    .flatMap(reasoning -> reasoning.summary().stream())
    .forEach(summary -> {
        String text = summary.text();
        if (text != null && !text.isEmpty()) {
            if (sb.length() > 0) sb.append("\n");
            sb.append(text);
        }
    });

System.out.println("Thinking: " + sb.toString().trim());
```

**Output is as follows:**

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...
```

[!INCLUDE [reasoning-tokens-known-issue](reasoning-tokens-known-issue.md)]

# [Azure AI Inference SDK](#tab/azure-ai-inference)

The Azure AI Inference SDK doesn't expose the Responses API. To get reasoning content, call the chat completions API instead. The reasoning is included in the message content wrapped in `<think>` and `</think>` tags, which you can extract with a regex match.

```java
import com.azure.ai.inference.models.*;
import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

List<ChatRequestMessage> messages = List.of(
    new ChatRequestSystemMessage("You are a helpful assistant."),
    new ChatRequestUserMessage("How many languages are in the world?")
);

ChatCompletionsOptions options = new ChatCompletionsOptions(messages);
options.setModel("DeepSeek-R1-0528"); // Optional for single-model endpoints

ChatCompletions response = client.complete(options);
String content = response.getChoices().get(0).getMessage().getContent();

Pattern pattern = Pattern.compile("<think>(.*?)</think>(.*)", Pattern.DOTALL);
Matcher matcher = pattern.matcher(content);

if (matcher.find()) {
    System.out.println("Thinking: " + matcher.group(1).trim());
    System.out.println("Answer:   " + matcher.group(2).trim());
} else {
    System.out.println("Response: " + content);
}
```

**Output is as follows:**

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...
Answer:   There are approximately 7,000 languages spoken around the world today.
```

---

When you make multi-turn conversations, avoid sending the reasoning content in the chat history because reasoning tends to generate long explanations.

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