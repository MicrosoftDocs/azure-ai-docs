---
title: Azure OpenAI Go support
titleSuffix: Azure OpenAI in Azure AI Foundry Models
description: Azure OpenAI Go support
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.date: 03/27/2025
---

[Source code](https://github.com/openai/openai-go) | [Package (pkg.go.dev)](https://pkg.go.dev/github.com/openai/openai-go/v2) | [REST API reference documentation](../../latest.md) | [Package reference documentation](https://pkg.go.dev/github.com/openai/openai-go/v2#section-documentation) 

## Azure OpenAI API version support

- v1 Generally Available (GA) API now allows access to both GA and Preview operations. To learn more, see the [API version lifecycle guide](../../api-version-lifecycle.md).

## Installation

Install the `openai` and `azidentity` modules with go get:

```
go get -u 'github.com/openai/openai-go@v2.1.1'

# optional
go get github.com/Azure/azure-sdk-for-go/sdk/azidentity
```

## Authentication

# [Microsoft Entra ID](#tab/secure)

The [azidentity](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/azidentity) module is used for Microsoft Entra ID authentication with Azure OpenAI.

```go
package main

import (
	"context"
	"fmt"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/openai/openai-go/v2"
	"github.com/openai/openai-go/v2/azure"
	"github.com/openai/openai-go/v2/option"
)

func main() {
	// Create an Azure credential
	tokenCredential, err := azidentity.NewDefaultAzureCredential(nil)
	if err != nil {
		panic(fmt.Sprintf("Failed to create credential: %v", err))
	}

	// Create a client with Azure OpenAI endpoint and token credential
	client := openai.NewClient(
		option.WithBaseURL("https://YOUR-RESOURCE_NAME.openai.azure.com/openai/v1/"),
		azure.WithTokenCredential(tokenCredential),
	)

	// Make a completion request
	chatCompletion, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
		Messages: []openai.ChatCompletionMessageParamUnion{
			openai.UserMessage("Explain what the bitter lesson is?"),
		},
		Model: "o4-mini", // Use your deployed model name on Azure
	})
	if err != nil {
		panic(err.Error())
	}

	fmt.Println(chatCompletion.Choices[0].Message.Content)
}
```

For more information about Azure OpenAI keyless authentication, see [Use Azure OpenAI without keys](/azure/developer/ai/keyless-connections?tabs=go%2Cazure-cli). 

# [API Key](#tab/api-key)

```go
package main

import (
	"context"
	"fmt"

	"github.com/openai/openai-go/v2"
	"github.com/openai/openai-go/v2/option"
)

func main() {
	// Create a client with Azure OpenAI endpoint and API key
	client := openai.NewClient(
		option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
		option.WithAPIKey("API-KEY-HERE"),
	)

	// Make a completion request
	chatCompletion, err := client.Chat.Completions.New(context.TODO(), openai.ChatCompletionNewParams{
		Messages: []openai.ChatCompletionMessageParamUnion{
			openai.UserMessage("Tell me about the bitter lesson"),
		},
		Model: "o4-mini", // Use your deployed model name on Azure
	})
	if err != nil {
		panic(err.Error())
	}

	fmt.Println(chatCompletion.Choices[0].Message.Content)
}
```

---

## Responses

```go
package main

import (
	"context"

	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
	"github.com/openai/openai-go/v2"
	"github.com/openai/openai-go/v2/azure"
	"github.com/openai/openai-go/v2/option"
	"github.com/openai/openai-go/v2/responses"
)

func main() {
	// Create Azure token credential
	tokenCredential, err := azidentity.NewDefaultAzureCredential(nil)
	if err != nil {
		panic(err)
	}

	// Create client with Azure endpoint and token credential
	client := openai.NewClient(
		option.WithBaseURL("https://YOUR-RESOURCE-NAME.openai.azure.com/openai/v1/"),
		azure.WithTokenCredential(tokenCredential),
	)

	ctx := context.Background()
	question := "Tell me about the attention is all you need paper"

	resp, err := client.Responses.New(ctx, responses.ResponseNewParams{
		Input: responses.ResponseNewParamsInputUnion{OfString: openai.String(question)},
		Model: "o4-mini",
	})

	if err != nil {
		panic(err)
	}

	println(resp.OutputText())
}
```

