---
title: 'Quickstart: Use Azure OpenAI in Azure AI Foundry Models with the JavaScript SDK and the completions API'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the Go SDK. 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mrbullwinkle
ms.author: mbullwin
ms.date: 08/30/2023
---

[Source code](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/ai/azopenai) | [Package (Go)](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai)| [Samples](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai#pkg-examples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- [Go 1.21.0](https://go.dev/dl/) or higher installed locally.
- An Azure OpenAI in Azure AI Foundry Models resource with the `gpt-35-turbo-instuct` model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

## Set up

[!INCLUDE [get-key-endpoint](get-key-endpoint.md)]

[!INCLUDE [environment-variables](environment-variables.md)]

## Create a sample application

 Create a new file named completions.go. Copy the following code into the completions.go file.

```go
package main

import (
	"context"
	"fmt"
	"os"

	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
)

func main() {
	azureOpenAIKey := os.Getenv("AZURE_OPENAI_API_KEY")
	modelDeploymentID := "gpt-35-turbo-instruct"

	azureOpenAIEndpoint := os.Getenv("AZURE_OPENAI_ENDPOINT")

	if azureOpenAIKey == "" || modelDeploymentID == "" || azureOpenAIEndpoint == "" {
		fmt.Fprintf(os.Stderr, "Skipping example, environment variables missing\n")
		return
	}

	keyCredential := azcore.NewKeyCredential(azureOpenAIKey)

	client, err := azopenai.NewClientWithKeyCredential(azureOpenAIEndpoint, keyCredential, nil)

	if err != nil {
		// TODO: handle error
	}

	resp, err := client.GetCompletions(context.TODO(), azopenai.CompletionsOptions{
		Prompt:         []string{"What is Azure OpenAI, in 20 words or less"},
		MaxTokens:      to.Ptr(int32(2048)),
		Temperature:    to.Ptr(float32(0.0)),
		DeploymentName: &modelDeploymentID,
	}, nil)

	if err != nil {
		// TODO: handle error
	}

	for _, choice := range resp.Choices {
		fmt.Fprintf(os.Stderr, "Result: %s\n", *choice.Text)
	}

}
```

> [!IMPORTANT]
> For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see this [security](../../../ai-services/security-features.md) article.

Now open a command prompt and run:

```cmd
go mod init completions.go
```

Next run:

```cmd
go mod tidy
```

```cmd
go run completions.go
```

## Output

```output
== Get completions Sample ==

Microsoft was founded on April 4, 1975.
```

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
