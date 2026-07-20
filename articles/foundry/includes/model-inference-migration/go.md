---
title: Go file for model inference SDK to OpenAI SDK migration
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

Install the OpenAI SDK:

```bash
go get github.com/openai/openai-go/v3
```

For Microsoft Entra ID authentication, also install:

```bash
go get -u github.com/Azure/azure-sdk-for-go/sdk/azidentity
```

## Client configuration

With API key authentication:

# [OpenAI SDK](#tab/openai)

```go
import (
    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v3/option"
)

client := openai.NewClient(
    option.WithBaseURL("https://<resource>.openai.azure.com/openai/v1/"),
    option.WithAPIKey(os.Getenv("AZURE_OPENAI_API_KEY")),
)
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go uses Azure SDK patterns.

---

With Microsoft Entra ID authentication:

# [OpenAI SDK](#tab/openai)

```go
import (
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v3/azure"
    "github.com/openai/openai-go/v3/option"
)

tokenCredential, err := azidentity.NewDefaultAzureCredential(nil)
if err != nil {
    panic(err)
}

client := openai.NewClient(
    option.WithBaseURL("https://<resource>.openai.azure.com/openai/v1/"),
    azure.WithTokenCredential(tokenCredential),
)
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go supports Microsoft Entra ID through Azure SDK.

---

## Chat completions

# [OpenAI SDK](#tab/openai)

```go
import (
    "context"
    "fmt"
    "github.com/openai/openai-go/v3"
)

chatCompletion, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
    Messages: []openai.ChatCompletionMessageParamUnion{
        openai.SystemMessage("You are a helpful assistant."),
        openai.UserMessage("What is Azure AI?"),
    },
    Model: "DeepSeek-V3.1", // Required: your deployment name
})

if err != nil {
    panic(err.Error())
}

fmt.Println(chatCompletion.Choices[0].Message.Content)
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go uses Azure SDK patterns for chat completions.

---


### Streaming

# [OpenAI SDK](#tab/openai)

```go
import (
    "context"
    "fmt"
    "github.com/openai/openai-go/v3"
)

stream := client.Chat.Completions.NewStreaming(context.TODO(), openai.ChatCompletionNewParams{
    Messages: []openai.ChatCompletionMessageParamUnion{
        openai.SystemMessage("You are a helpful assistant."),
        openai.UserMessage("Write a poem about Azure."),
    },
    Model: "DeepSeek-V3.1", // Required: your deployment name
})

for stream.Next() {
    chunk := stream.Current()
    if len(chunk.Choices) > 0 && chunk.Choices[0].Delta.Content != "" {
        fmt.Print(chunk.Choices[0].Delta.Content)
    }
}

if err := stream.Err(); err != nil {
    panic(err.Error())
}
```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go supports streaming through Azure SDK patterns.

---

## Responses

The Responses API is OpenAI's stateful interface that returns a structured `output` array containing message, tool call, and reasoning items.

# [OpenAI SDK](#tab/openai)

```go
import (
    "context"
    "fmt"

    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v3/responses"
)

resp, err := client.Responses.New(context.TODO(), responses.ResponseNewParams{
    Model: "DeepSeek-V3.1", // Required: your deployment name
    Input: responses.ResponseNewParamsInputUnion{
        OfString: openai.String("How many languages are in the world?"),
    },
    MaxOutputTokens: openai.Int(2000),
})
if err != nil {
    panic(err.Error())
}

fmt.Println(resp.OutputText())
```


# [Azure AI Inference SDK](#tab/azure-ai-inference)

The Azure AI Inference SDK doesn't expose the Responses API. To call it, use the OpenAI SDK.

---

### Reasoning

> [!NOTE]
> This information on reasoning content doesn't apply to Azure OpenAI models. Azure OpenAI reasoning models use the [reasoning summaries feature](../../openai/how-to/reasoning.md#reasoning-summary).

Some reasoning models, like DeepSeek-R1, generate completions and include the reasoning behind them. The Responses API surfaces this as a structured `reasoning` output item whose `summary[].text` contains the model's thinking, alongside the final answer.

# [OpenAI SDK](#tab/openai)

```go
import (
    "context"
    "fmt"
    "strings"

    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v3/responses"
)

resp, err := client.Responses.New(context.TODO(), responses.ResponseNewParams{
    Model: "DeepSeek-R1-0528", // Required: your deployment name
    Input: responses.ResponseNewParamsInputUnion{
        OfString: openai.String("How many languages are in the world?"),
    },
    MaxOutputTokens: openai.Int(2000),
})
if err != nil {
    panic(err.Error())
}

// Walk resp.Output for items of type "reasoning" and join summary[].text.
var parts []string
for _, item := range resp.Output {
    if item.Type != "reasoning" {
        continue
    }
    for _, s := range item.Summary {
        if s.Text != "" {
            parts = append(parts, s.Text)
        }
    }
}
reasoningSummary := strings.TrimSpace(strings.Join(parts, "\n"))

fmt.Println("Thinking:", reasoningSummary)
fmt.Println("Answer:  ", resp.OutputText())
```

**Output is as follows:**

```console
Thinking: Okay, the user is asking how many languages exist in the world. I need to provide a clear and accurate answer...
Answer:   There are approximately 7,000 languages spoken around the world today.
```

[!INCLUDE [reasoning-tokens-known-issue](reasoning-tokens-known-issue.md)]

# [Azure AI Inference SDK](#tab/azure-ai-inference)

The Azure AI Inference SDK for Go doesn't expose the Responses API. To get reasoning content, call the chat completions API instead. The reasoning is included in the message content wrapped in `<think>` and `</think>` tags, which you can extract with a regex match.

---

When you make multi-turn conversations, avoid sending the reasoning content in the chat history because reasoning tends to generate long explanations.

## Embeddings

# [OpenAI SDK](#tab/openai)

```go
package main

import (
    "context"
    "fmt"
    "log"

    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v3/azure"
    "github.com/openai/openai-go/v3/option"
)

func main() {
    tokenCredential, err := azidentity.NewDefaultAzureCredential(nil)
    if err != nil {
        log.Fatalf("Error creating credential:%s", err)
    }
    // Create a client with Azure OpenAI endpoint and Entra ID credentials
    client := openai.NewClient(
        option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
        azure.WithTokenCredential(tokenCredential),
    )

    inputText := "The quick brown fox jumped over the lazy dog"

    // Make the embedding request synchronously
    resp, err := client.Embeddings.New(context.Background(), openai.EmbeddingNewParams{
        Model: openai.EmbeddingModel("text-embedding-3-large"), // Use your deployed model name on Azure
        Input: openai.EmbeddingNewParamsInputUnion{
            OfArrayOfStrings: []string{inputText},
        },
    })
    if err != nil {
        log.Fatalf("Failed to get embedding: %s", err)
    }

    if len(resp.Data) == 0 {
        log.Fatalf("No embedding data returned.")
    }

    // Print embedding information
    embedding := resp.Data[0].Embedding
    fmt.Printf("Embedding Length: %d\n", len(embedding))
    fmt.Println("Embedding Values:")
    for _, value := range embedding {
        fmt.Printf("%f, ", value)
    }
    fmt.Println()
}

```

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go uses Azure SDK patterns for embeddings.

---

