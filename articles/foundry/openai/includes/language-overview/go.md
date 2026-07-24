---
title: Azure OpenAI Go support
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Azure OpenAI Go support.
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

[Source code](https://github.com/openai/openai-go) | [Package](https://pkg.go.dev/github.com/openai/openai-go/v3) | [REST API reference](https://ai.azure.com/api-reference/) | [Go API reference](https://github.com/openai/openai-go/blob/main/api.md)

The examples require Go 1.25 or later. They were tested with `github.com/openai/openai-go/v3` 3.44.0 and `azidentity` 1.14.0.

## Install the modules

Install the OpenAI and Azure Identity modules:

```bash
go get github.com/openai/openai-go/v3
go get github.com/Azure/azure-sdk-for-go/sdk/azidentity
```

The `/v3` suffix is required because it identifies the current major version of the Go module.

## Create a response with Microsoft Entra ID

Use `DefaultAzureCredential` and the Azure authentication option to authenticate without storing an API key.

```go
package main

import (
	"context"
	"fmt"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/azure"
	"github.com/openai/openai-go/v3/option"
	"github.com/openai/openai-go/v3/responses"
)

func main() {
	credential, err := azidentity.NewDefaultAzureCredential(nil)
	if err != nil { panic(err) }
	endpoint := "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
	openaiClient := openai.NewClient(
		option.WithBaseURL(endpoint),
		azure.WithTokenCredential(credential, azure.WithTokenCredentialScopes(
			[]string{"https://ai.azure.com/.default"})))
	response, err := openaiClient.Responses.New(context.Background(), responses.ResponseNewParams{
		Model: openai.ChatModel("gpt-5-mini"),
		Input: responses.ResponseNewParamsInputUnion{OfString: openai.String(
			"Explain the purpose of an API in one sentence.")},
	})
	if err != nil { panic(err) }
	fmt.Println(response.OutputText())
}
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`ResponseService.New`](https://github.com/openai/openai-go/blob/main/examples/responses/main.go) and [`WithTokenCredentialScopes`](https://github.com/openai/openai-go/blob/main/azure/azure.go)

## Create a response with an API key

API keys aren't recommended for production use. Store the key in the `AZURE_OPENAI_API_KEY` environment variable instead of placing it in source code.

```bash
export AZURE_OPENAI_API_KEY="<your-api-key>"
```

Then create the client and request:

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/option"
	"github.com/openai/openai-go/v3/responses"
)

func main() {
	apiKey := os.Getenv("AZURE_OPENAI_API_KEY")
	if apiKey == "" { panic("AZURE_OPENAI_API_KEY is required") }
	endpoint := "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
	openaiClient := openai.NewClient(
		option.WithBaseURL(endpoint),
		option.WithAPIKey(apiKey))
	response, err := openaiClient.Responses.New(context.Background(), responses.ResponseNewParams{
		Model: openai.ChatModel("gpt-5-mini"),
		Input: responses.ResponseNewParamsInputUnion{OfString: openai.String(
			"Explain the purpose of an API in one sentence.")},
	})
	if err != nil { panic(err) }
	fmt.Println(response.OutputText())
}
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`Responses.New`](https://github.com/openai/openai-go/blob/main/examples/azure/main.go)

## Use Chat Completions

For new applications, use the Responses API. Use Chat Completions when you need its message-based interface or are maintaining an existing application.

```go
package main

import (
	"context"
	"fmt"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/azure"
	"github.com/openai/openai-go/v3/option"
)

func main() {
	credential, err := azidentity.NewDefaultAzureCredential(nil)
	if err != nil { panic(err) }
	endpoint := "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
	openaiClient := openai.NewClient(
		option.WithBaseURL(endpoint),
		azure.WithTokenCredential(credential, azure.WithTokenCredentialScopes(
			[]string{"https://ai.azure.com/.default"})))
	completion, err := openaiClient.Chat.Completions.New(context.Background(),
		openai.ChatCompletionNewParams{
			Model: openai.ChatModel("gpt-5-mini"),
			Messages: []openai.ChatCompletionMessageParamUnion{
				openai.DeveloperMessage("You are a helpful assistant."),
				openai.UserMessage("Explain the purpose of an API.")}})
	if err != nil { panic(err) }
	fmt.Println(completion.Choices[0].Message.Content)
}
```

The following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`Chat.Completions.New`](https://github.com/openai/openai-go/blob/main/README.md#chat-completions-api)

## Stream a response

Call `Responses.NewStreaming`, and process text delta events as the model generates them:

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/option"
	"github.com/openai/openai-go/v3/responses"
)

func main() {
	endpoint := "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
	openaiClient := openai.NewClient(option.WithBaseURL(endpoint),
		option.WithAPIKey(os.Getenv("AZURE_OPENAI_API_KEY")))
	// Stream text as the model generates it.
	stream := openaiClient.Responses.NewStreaming(context.Background(), responses.ResponseNewParams{
		Model: openai.ChatModel("gpt-5-mini"),
		Input: responses.ResponseNewParamsInputUnion{OfString: openai.String(
			"Explain the purpose of an API in one sentence.")},
	})
	for stream.Next() { fmt.Print(stream.Current().Delta) }
	if err := stream.Err(); err != nil { panic(err) }
}
```

The following streamed output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [`Responses.NewStreaming`](https://github.com/openai/openai-go/blob/main/examples/responses-streaming/main.go)

## Handle errors and retries

The SDK retries connection errors and HTTP 408, 409, 429, and 5xx responses twice with exponential backoff. Use `option.WithMaxRetries` to change the default. Check the returned `error` before reading a response, and use `errors.As` to inspect an `openai.Error`.

```go
package main

import (
	"context"
	"errors"
	"fmt"
	"os"

	"github.com/openai/openai-go/v3"
	"github.com/openai/openai-go/v3/option"
	"github.com/openai/openai-go/v3/responses"
)

func main() {
	endpoint := "https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"
	openaiClient := openai.NewClient(option.WithBaseURL(endpoint),
		option.WithAPIKey(os.Getenv("AZURE_OPENAI_API_KEY")), option.WithMaxRetries(4))
	// Send the request and inspect structured service errors.
	result, err := openaiClient.Responses.New(context.Background(), responses.ResponseNewParams{
		Model: openai.ChatModel("gpt-5-mini"),
		Input: responses.ResponseNewParamsInputUnion{OfString: openai.String("Explain an API.")},
	})
	if err != nil {
		var apiError *openai.Error
		if errors.As(err, &apiError) { fmt.Printf("Status: %d; Request ID: %s\n",
			apiError.StatusCode, apiError.Response.Header.Get("x-request-id")) }
		panic(err)
	}
	fmt.Println(result.OutputText())
}
```

For a successful request, the following output is representative. The exact wording might vary:

```output
An API allows software applications to communicate and exchange data through a defined set of rules.
```

Reference: [Errors and retries](https://github.com/openai/openai-go#errors)

## More SDK examples

- [Use the Responses API](../../how-to/responses.md)
- [Generate embeddings](../../how-to/embeddings.md)
- [Analyze images](../../how-to/gpt-with-vision.md)
- [Fine-tune a model](../../how-to/fine-tuning.md)
