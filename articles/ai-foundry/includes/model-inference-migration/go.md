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

# [OpenAI v1 SDK](#tab/openai)

```go
import (
    "github.com/openai/openai-go/v3"
    "github.com/openai/openai-go/v2/option"
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

# [OpenAI v1 SDK](#tab/openai)

```go
import (
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/openai/openai-go/v2"
    "github.com/openai/openai-go/v3/azure"
    "github.com/openai/openai-go/v2/option"
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

## Responses API

Responses API supports only Azure OpenAI in Foundry Models. For Azure OpenAI models, use the Responses API for chat completions:

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support the Responses API. Use chat completions instead.

# [OpenAI v1 SDK](#tab/openai)

```go
import (
    "context"
    "fmt"
    "github.com/openai/openai-go/v2"
    "github.com/openai/openai-go/v2/responses"
)

question := "This is a test"

resp, err := client.Responses.New(context.Background(), responses.ResponseNewParams{
    Input: responses.ResponseNewParamsInputUnion{OfString: openai.String(question)},
    Model: "gpt-4o-mini", // Your deployment name
})

if err != nil {
    panic(err.Error())
}

println(resp.OutputText())
```

---

## Chat completions

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go uses Azure SDK patterns for chat completions.

# [OpenAI v1 SDK](#tab/openai)

```go
import (
    "context"
    "fmt"
    "github.com/openai/openai-go/v2"
)

chatCompletion, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
    Messages: []openai.ChatCompletionMessageParamUnion{
        openai.SystemMessage("You are a helpful assistant."),
        openai.UserMessage("What is Azure AI?"),
    },
    Model: "gpt-4o-mini", // Required: your deployment name
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

# [OpenAI v1 SDK](#tab/openai)

```go
import (
    "context"
    "fmt"
    "github.com/openai/openai-go/v2"
)

stream := client.Chat.Completions.NewStreaming(context.TODO(), openai.ChatCompletionNewParams{
    Messages: []openai.ChatCompletionMessageParamUnion{
        openai.SystemMessage("You are a helpful assistant."),
        openai.UserMessage("Write a poem about Azure."),
    },
    Model: "gpt-4o-mini",
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

# [OpenAI v1 SDK](#tab/openai)

OpenAI v1 SDK doesn't support embeddings models.


---

## Image generation

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support image generation models.

# [OpenAI v1 SDK](#tab/openai)

OpenAI v1 SDK doesn't support image generation models.

---

