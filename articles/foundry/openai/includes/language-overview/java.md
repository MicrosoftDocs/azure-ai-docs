---
title: Azure OpenAI Java support
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI Java support.
author: alvinashcraft
manager: mcleans
ms.author: aashcraft
ms.service: microsoft-foundry
ms.subservice: foundry-openai
ms.topic: include
ms.date: 07/20/2026
ms.custom: include, classic-and-new, doc-kit-assisted
ai-usage: ai-assisted
---

[Source code](https://github.com/openai/openai-java) | [Package](https://central.sonatype.com/artifact/com.openai/openai-java) | [REST API reference](https://ai.azure.com/api-reference/) | [Java API reference](https://javadoc.io/doc/com.openai/openai-java/latest/index.html)

The examples require Java 8 or later. They were tested with `openai-java` 4.43.0 and `azure-identity` 1.18.4.

## Install the packages

### Maven

Add the OpenAI and Azure Identity dependencies to your Maven project:

```xml
<dependencies>
  <dependency>
    <groupId>com.openai</groupId>
    <artifactId>openai-java</artifactId>
                <version>4.43.0</version>
  </dependency>
  <dependency>
    <groupId>com.azure</groupId>
    <artifactId>azure-identity</artifactId>
    <version>1.18.4</version>
  </dependency>
</dependencies>
```

Maven resolves the packages and their transitive dependencies when you build the project.

### Gradle

Add the same packages to the `dependencies` block in your Gradle build file:

```gradle
dependencies {
        implementation("com.openai:openai-java:4.43.0")
        implementation("com.azure:azure-identity:1.18.4")
}
```

Gradle resolves the packages when you build the project.

## Create a response with Microsoft Entra ID

Use `DefaultAzureCredential` and `BearerTokenCredential` to authenticate without storing an API key.

```java
import com.azure.identity.AuthenticationUtil;
import com.azure.identity.DefaultAzureCredentialBuilder;
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.credential.BearerTokenCredential;
import com.openai.models.responses.ResponseCreateParams;

public class ResponsesExample {
    public static void main(String[] args) {
        String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
        OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
                .baseUrl(endpoint)
                .credential(BearerTokenCredential.create(
                        AuthenticationUtil.getBearerTokenSupplier(
                                new DefaultAzureCredentialBuilder().build(),
                                "https://ai.azure.com/.default")))
                .build();
        ResponseCreateParams params = ResponseCreateParams.builder()
                .model("gpt-5-mini")
                .input("Explain the purpose of an API in one sentence.")
                .build();
        openAIClient.responses().create(params).output().stream()
                .flatMap(item -> item.message().stream())
                .flatMap(message -> message.content().stream())
                .flatMap(content -> content.outputText().stream())
                .forEach(output -> System.out.println(output.text()));
    }
}
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`AzureEntraIdExample`](https://github.com/openai/openai-java/blob/main/openai-java-example/src/main/java/com/openai/example/AzureEntraIdExample.java) and [`ResponsesExample`](https://github.com/openai/openai-java/blob/main/openai-java-example/src/main/java/com/openai/example/ResponsesExample.java)

## Create a response with an API key

Don't use API keys for production. Store the key in the `AZURE_OPENAI_API_KEY` environment variable instead of placing it in source code.

```bash
export AZURE_OPENAI_API_KEY="<your-api-key>"
```

Then create the client and request:

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.responses.ResponseCreateParams;

public class ApiKeyResponsesExample {
    public static void main(String[] args) {
        String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
        String apiKey = System.getenv("AZURE_OPENAI_API_KEY");
        if (apiKey == null) throw new IllegalStateException(
                "AZURE_OPENAI_API_KEY is required.");
        OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
                .baseUrl(endpoint).apiKey(apiKey).build();
        ResponseCreateParams params = ResponseCreateParams.builder()
                .model("gpt-5-mini")
                .input("Explain the purpose of an API in one sentence.")
                .build();
        openAIClient.responses().create(params).output().stream()
                .flatMap(item -> item.message().stream())
                .flatMap(message -> message.content().stream())
                .flatMap(content -> content.outputText().stream())
                .forEach(output -> System.out.println(output.text()));
    }
}
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`OpenAIOkHttpClient`](https://github.com/openai/openai-java#client-configuration)

## Use Chat Completions

For new applications, use the Responses API. Use Chat Completions when you need its message-based interface or are maintaining an existing application.

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.models.chat.completions.ChatCompletionCreateParams;

public class ChatExample {
    public static void main(String[] args) {
        String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
        String apiKey = System.getenv("AZURE_OPENAI_API_KEY");
        if (apiKey == null) throw new IllegalStateException(
                "AZURE_OPENAI_API_KEY is required.");
        OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
                .baseUrl(endpoint).apiKey(apiKey).build();
        ChatCompletionCreateParams params = ChatCompletionCreateParams.builder()
                .model("gpt-5-mini")
                .addDeveloperMessage("You are a helpful assistant.")
                .addUserMessage("Explain the purpose of an API.")
                .build();
        openAIClient.chat().completions().create(params).choices().stream()
                .flatMap(choice -> choice.message().content().stream())
                .forEach(System.out::println);
    }
}
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`ChatCompletionCreateParams`](https://github.com/openai/openai-java/blob/main/openai-java-example/src/main/java/com/openai/example/CompletionsExample.java)

## Stream a response

Call `createStreaming`, and process text delta events as the model generates them:

```java
import com.openai.client.OpenAIClient;
import com.openai.client.okhttp.OpenAIOkHttpClient;
import com.openai.core.http.StreamResponse;
import com.openai.models.responses.ResponseCreateParams;
import com.openai.models.responses.ResponseStreamEvent;

public class StreamingExample {
    public static void main(String[] args) {
        String endpoint = "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/";
        String apiKey = System.getenv("AZURE_OPENAI_API_KEY");
        if (apiKey == null) throw new IllegalStateException(
                "AZURE_OPENAI_API_KEY is required.");
        OpenAIClient openAIClient = OpenAIOkHttpClient.builder()
                .baseUrl(endpoint).apiKey(apiKey).build();
        // Stream text as the model generates it.
        ResponseCreateParams params = ResponseCreateParams.builder()
                .model("gpt-5-mini")
                .input("Explain the purpose of an API in one sentence.")
                .build();
        try (StreamResponse<ResponseStreamEvent> stream =
                openAIClient.responses().createStreaming(params)) {
            stream.stream().flatMap(event -> event.outputTextDelta().stream())
                    .forEach(delta -> System.out.print(delta.delta()));
        }
    }
}
```

The following streamed output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`responses.createStreaming`](https://github.com/openai/openai-java/blob/main/openai-java-example/src/main/java/com/openai/example/ResponsesStreamingExample.java)

## Handle errors and retries

The SDK retries connection errors and HTTP 408, 409, 429, and 5xx responses twice with exponential backoff. Catch `OpenAIServiceException` to inspect the HTTP status and error details for a service response, and catch `OpenAIException` for other SDK failures.

Call `maxRetries` on `OpenAIOkHttpClient.builder()` to change the default. Preserve the service exception so that your application can log its status and request metadata.

Reference: [Error handling](https://github.com/openai/openai-java#error-handling) and [retries](https://github.com/openai/openai-java#retries)

## More SDK examples

- [Use the Responses API](../../how-to/responses.md)
- [Generate embeddings](../../how-to/embeddings.md)
- [Analyze images](../../how-to/gpt-with-vision.md)
- [Fine-tune a model](../../how-to/fine-tuning.md)
