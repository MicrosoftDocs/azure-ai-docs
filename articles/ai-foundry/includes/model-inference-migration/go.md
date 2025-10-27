## Benefits of migrating

Migrating to the OpenAI v1 SDK provides several advantages:

- **Unified API**: Use the same SDK for both OpenAI and Azure OpenAI endpoints
- **Latest features**: Access to the newest OpenAI features without waiting for Azure-specific updates
- **Simplified authentication**: Built-in support for both API key and Microsoft Entra ID authentication
- **No API versioning**: The v1 API eliminates the need to frequently update `api-version` parameters
- **Broader model support**: Works with Azure OpenAI in Foundry Models and other Foundry Models from providers like DeepSeek and Grok

## Setup

Install the OpenAI SDK:

```bash
go get github.com/openai/openai-go/v2
```

For Microsoft Entra ID authentication, also install:

```bash
go get -u github.com/Azure/azure-sdk-for-go/sdk/azidentity
```

## Client configuration

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go uses Azure SDK patterns.

# [OpenAI v1 SDK](#tab/openai)

```go
import (
    "github.com/openai/openai-go/v2"
    "github.com/openai/openai-go/v2/option"
)

client := openai.NewClient(
    option.WithBaseURL("https://<resource>.openai.azure.com/openai/v1/"),
    option.WithAPIKey(os.Getenv("AZURE_OPENAI_API_KEY")),
)
```

---

With Microsoft Entra ID:

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go supports Microsoft Entra ID through Azure SDK.

# [OpenAI v1 SDK](#tab/openai)

```go
import (
    "github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    "github.com/openai/openai-go/v2"
    "github.com/openai/openai-go/v2/azure"
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

For Azure OpenAI models, use the Responses API for chat completions:

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

```go
import (
    "context"
    "fmt"
    "github.com/openai/openai-go/v2"
)

embedding, err := client.Embeddings.New(context.TODO(), openai.EmbeddingNewParams{
    Input: openai.F[openai.EmbeddingNewParamsInputUnion](
        openai.EmbeddingNewParamsInputArrayOfStrings([]string{
            "Your text string goes here",
        }),
    ),
    Model: "text-embedding-3-small", // Your deployment name
})

if err != nil {
    panic(err.Error())
}

fmt.Printf("Embedding: %v\n", embedding.Data[0].Embedding)
```

---

## Image generation

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK doesn't support image generation. Use OpenAI SDK instead.

# [OpenAI v1 SDK](#tab/openai)

```go
import (
    "context"
    "fmt"
    "github.com/openai/openai-go/v2"
)

image, err := client.Images.Generate(context.TODO(), openai.ImageGenerateParams{
    Prompt: openai.F("a happy monkey eating a banana, in watercolor"),
    Model:  openai.F("dall-e-3"), // Your deployment name
    N:      openai.F(int64(1)),
    Size:   openai.F(openai.ImageGenerateParamsSize1024x1024),
    Quality: openai.F(openai.ImageGenerateParamsQualityStandard),
})

if err != nil {
    panic(err.Error())
}

fmt.Printf("Generated image available at: %s\n", image.Data[0].URL)
```

---

## Error handling

# [Azure AI Inference SDK](#tab/azure-ai-inference)

Azure AI Inference SDK for Go uses standard Go error handling with Azure SDK patterns.

# [OpenAI v1 SDK](#tab/openai)

```go
import (
    "context"
    "errors"
    "fmt"
    "github.com/openai/openai-go/v2"
)

chatCompletion, err := client.Chat.Completions.New(context.TODO(), params)
if err != nil {
    var apiErr *openai.Error
    if errors.As(err, &apiErr) {
        fmt.Printf("API error: %s (code: %s)\n", apiErr.Message, apiErr.Code)
    } else {
        fmt.Printf("Error: %v\n", err)
    }
    return
}
```

---
