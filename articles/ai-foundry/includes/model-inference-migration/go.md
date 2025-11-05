---
title: Include file
description: Include file
author: msakande
ms.reviewer: mopeakande
ms.author: mopeakande
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 10/28/2025
ms.custom: include
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

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go uses Azure SDK patterns.

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

---

With Microsoft Entra ID authentication:

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go supports Microsoft Entra ID through Azure SDK.

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

---

## Chat completions

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go uses Azure SDK patterns for chat completions.

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

---

### Streaming

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go supports streaming through Azure SDK patterns.

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

---

## Embeddings

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go uses Azure SDK patterns for embeddings.

# [OpenAI SDK](#tab/openai)

```go
package main

import (
    "context"
    "fmt"
    "log"
    "os"

    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/openai/openai-go/v2"
    "github.com/openai/openai-go/v2/azure"
    "github.com/openai/openai-go/v2/option"
)

func main() {
    token_credential, err := azidentity.NewDefaultAzureCredential(nil)
    if err != nil {
        fmt.Println("Error creating credential:", err)
        os.Exit(1)
    }
    // Create a client with Azure OpenAI endpoint and Entra ID credentials
    client := openai.NewClient(
        option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
        azure.WithTokenCredential(token_credential),
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
        log.Fatalf("Failed to get embedding: %v", err)
    }

    if len(resp.Data) == 0 {
        fmt.Println("No embedding data returned.")
        return
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

---

