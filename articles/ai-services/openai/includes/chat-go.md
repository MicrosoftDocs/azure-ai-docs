---
title: 'Quickstart: Use Azure OpenAI in Azure AI Foundry Models with the JavaScript SDK and the completions API'
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the Go SDK.
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mrbullwinkle
ms.author: mbullwin
ms.date: 3/21/2025
---

[Source code](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/ai/azopenai) | [Package (Go)](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai)| [Samples](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai#pkg-examples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- [Go 1.21.0](https://go.dev/dl/) or higher installed locally.
- An Azure OpenAI in Azure AI Foundry Models resource with the `gpt-4` model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up
 
1. Create a new folder `chat-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir chat-quickstart && cd chat-quickstart
    ```

1. For the **recommended** keyless authentication with Microsoft Entra ID, sign in to Azure with the following command:

    ```console
    az login
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

## Run the quickstart

The sample code in this quickstart uses Microsoft Entra ID for the recommended keyless authentication. If you prefer to use an API key, you can replace the `NewDefaultAzureCredential` implementation with `NewKeyCredential`. 

#### [Microsoft Entra ID](#tab/keyless)

```go
azureOpenAIEndpoint := os.Getenv("AZURE_OPENAI_ENDPOINT")
credential, err := azidentity.NewDefaultAzureCredential(nil)
client, err := azopenai.NewClient(azureOpenAIEndpoint, credential, nil)
```

#### [API key](#tab/api-key)

```go
azureOpenAIEndpoint := os.Getenv("AZURE_OPENAI_ENDPOINT")
azureOpenAIKey := os.Getenv("AZURE_OPENAI_API_KEY")
credential := azcore.NewKeyCredential(azureOpenAIKey)
client, err := azopenai.NewClientWithKeyCredential(azureOpenAIEndpoint, credential, nil)
```
---

#### [Microsoft Entra ID](#tab/keyless)

To run the sample:

1. Create a new file named *chat_completions_keyless.go*. Copy the following code into the *chat_completions_keyless.go* file.

    ```go
    package main

    import (
    	"context"
    	"fmt"
    	"log"
    	"os"
    
    	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
    	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    )
    
    func main() {
    	azureOpenAIEndpoint := os.Getenv("AZURE_OPENAI_ENDPOINT")
    	modelDeploymentID := "gpt-4o"
        maxTokens:= int32(400)
    
    	credential, err := azidentity.NewDefaultAzureCredential(nil)
    	if err != nil {
    		log.Printf("ERROR: %s", err)
    		return
    	}
    
    	client, err := azopenai.NewClient(
    		azureOpenAIEndpoint, credential, nil)
    	if err != nil {
    		log.Printf("ERROR: %s", err)
    		return
    	}
    
    	// This is a conversation in progress.
    	// All messages, regardless of role, count against token usage for this API.
    	messages := []azopenai.ChatRequestMessageClassification{
    		// System message sets the tone and rules of the conversation.
    		&azopenai.ChatRequestSystemMessage{
    			Content: azopenai.NewChatRequestSystemMessageContent(
    				"You are a helpful assistant."),
    		},
    
    		// The user asks a question
    		&azopenai.ChatRequestUserMessage{
    			Content: azopenai.NewChatRequestUserMessageContent(
    				"Can I use honey as a substitute for sugar?"),
    		},
    
    		// The reply would come back from the model. You
    		// add it to the conversation so we can maintain context.
    		&azopenai.ChatRequestAssistantMessage{
    			Content: azopenai.NewChatRequestAssistantMessageContent(
    				"Yes, you can use use honey as a substitute for sugar."),
    		},
    
    		// The user answers the question based on the latest reply.
    		&azopenai.ChatRequestUserMessage{
    			Content: azopenai.NewChatRequestUserMessageContent(
    				"What other ingredients can I use as a substitute for sugar?"),
    		},
    
    		// From here you can keep iterating, sending responses back from the chat model.
    	}
    
    	gotReply := false
    
    	resp, err := client.GetChatCompletions(context.TODO(), azopenai.ChatCompletionsOptions{
    		// This is a conversation in progress.
    		// All messages count against token usage for this API.
    		Messages: messages,
    		DeploymentName: &modelDeploymentID,
    		MaxTokens: &maxTokens,
    	}, nil)
    
    	if err != nil {
    		// Implement application specific error handling logic.
    		log.Printf("ERROR: %s", err)
    		return
    	}
    
    	for _, choice := range resp.Choices {
    		gotReply = true
    
    		if choice.ContentFilterResults != nil {
    			fmt.Fprintf(os.Stderr, "Content filter results\n")
    
    			if choice.ContentFilterResults.Error != nil {
    				fmt.Fprintf(os.Stderr, "  Error:%v\n", choice.ContentFilterResults.Error)
    			}
    
    			fmt.Fprintf(os.Stderr, "  Hate: sev: %v, filtered: %v\n", *choice.ContentFilterResults.Hate.Severity, *choice.ContentFilterResults.Hate.Filtered)
    			fmt.Fprintf(os.Stderr, "  SelfHarm: sev: %v, filtered: %v\n", *choice.ContentFilterResults.SelfHarm.Severity, *choice.ContentFilterResults.SelfHarm.Filtered)
    			fmt.Fprintf(os.Stderr, "  Sexual: sev: %v, filtered: %v\n", *choice.ContentFilterResults.Sexual.Severity, *choice.ContentFilterResults.Sexual.Filtered)
    			fmt.Fprintf(os.Stderr, "  Violence: sev: %v, filtered: %v\n", *choice.ContentFilterResults.Violence.Severity, *choice.ContentFilterResults.Violence.Filtered)
    		}
    
    		if choice.Message != nil && choice.Message.Content != nil {
    			fmt.Fprintf(os.Stderr, "Content[%d]: %s\n", *choice.Index, *choice.Message.Content)
    		}
    
    		if choice.FinishReason != nil {
    			// The conversation for this choice is complete.
    			fmt.Fprintf(os.Stderr, "Finish reason[%d]: %s\n", *choice.Index, *choice.FinishReason)
    		}
    	}
    
    	if gotReply {
    		fmt.Fprintf(os.Stderr, "Received chat completions reply\n")
    	}
    
    }
    ```
    
1. Run the following command to create a new Go module:

	```shell
	go mod init chat_completions_keyless.go
	```

1. Run `go mod tidy` to install the required dependencies:

    ```cmd
    go mod tidy
    ```

1. Run the following command to run the sample:

	```shell
	go run chat_completions_keyless.go
	```

#### [API key](#tab/api-key)

To run the sample:

1. Create a new file named *chat_completions_api-key.go*. Copy the following code into the *chat_completions_api-key.go* file.

    ```go
    package main

    import (
    	"context"
    	"fmt"
    	"log"
    	"os"
    
    	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
    	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
    )
    
    func main() {
    	azureOpenAIEndpoint := os.Getenv("AZURE_OPENAI_ENDPOINT")
    	modelDeploymentID := "gpt-4o"
        maxTokens:= int32(400)
    
    	azureOpenAIKey := os.Getenv("AZURE_OPENAI_API_KEY")
    	credential := azcore.NewKeyCredential(azureOpenAIKey)
    
    	client, err := azopenai.NewClientWithKeyCredential(
    		azureOpenAIEndpoint, credential, nil)
    	if err != nil {
    		log.Printf("ERROR: %s", err)
    		return
    	}
    
    	// This is a conversation in progress.
    	// All messages, regardless of role, count against token usage for this API.
    	messages := []azopenai.ChatRequestMessageClassification{
    		// System message sets the tone and rules of the conversation.
    		&azopenai.ChatRequestSystemMessage{
    			Content: azopenai.NewChatRequestSystemMessageContent(
    				"You are a helpful assistant."),
    		},
    
    		// The user asks a question
    		&azopenai.ChatRequestUserMessage{
    			Content: azopenai.NewChatRequestUserMessageContent(
    				"Can I use honey as a substitute for sugar?"),
    		},
    
    		// The reply would come back from the model. You
    		// add it to the conversation so we can maintain context.
    		&azopenai.ChatRequestAssistantMessage{
    			Content: azopenai.NewChatRequestAssistantMessageContent(
    				"Yes, you can use use honey as a substitute for sugar."),
    		},
    
    		// The user answers the question based on the latest reply.
    		&azopenai.ChatRequestUserMessage{
    			Content: azopenai.NewChatRequestUserMessageContent(
    				"What other ingredients can I use as a substitute for sugar?"),
    		},
    
    		// From here you can keep iterating, sending responses back from the chat model.
    	}
    
    	gotReply := false
    
    	resp, err := client.GetChatCompletions(context.TODO(), azopenai.ChatCompletionsOptions{
    		// This is a conversation in progress.
    		// All messages count against token usage for this API.
    		Messages: messages,
    		DeploymentName: &modelDeploymentID,
    		MaxTokens: &maxTokens,
    	}, nil)
    
    	if err != nil {
    		// Implement application specific error handling logic.
    		log.Printf("ERROR: %s", err)
    		return
    	}
    
    	for _, choice := range resp.Choices {
    		gotReply = true
    
    		if choice.ContentFilterResults != nil {
    			fmt.Fprintf(os.Stderr, "Content filter results\n")
    
    			if choice.ContentFilterResults.Error != nil {
    				fmt.Fprintf(os.Stderr, "  Error:%v\n", choice.ContentFilterResults.Error)
    			}
    
    			fmt.Fprintf(os.Stderr, "  Hate: sev: %v, filtered: %v\n", *choice.ContentFilterResults.Hate.Severity, *choice.ContentFilterResults.Hate.Filtered)
    			fmt.Fprintf(os.Stderr, "  SelfHarm: sev: %v, filtered: %v\n", *choice.ContentFilterResults.SelfHarm.Severity, *choice.ContentFilterResults.SelfHarm.Filtered)
    			fmt.Fprintf(os.Stderr, "  Sexual: sev: %v, filtered: %v\n", *choice.ContentFilterResults.Sexual.Severity, *choice.ContentFilterResults.Sexual.Filtered)
    			fmt.Fprintf(os.Stderr, "  Violence: sev: %v, filtered: %v\n", *choice.ContentFilterResults.Violence.Severity, *choice.ContentFilterResults.Violence.Filtered)
    		}
    
    		if choice.Message != nil && choice.Message.Content != nil {
    			fmt.Fprintf(os.Stderr, "Content[%d]: %s\n", *choice.Index, *choice.Message.Content)
    		}
    
    		if choice.FinishReason != nil {
    			// The conversation for this choice is complete.
    			fmt.Fprintf(os.Stderr, "Finish reason[%d]: %s\n", *choice.Index, *choice.FinishReason)
    		}
    	}
    
    	if gotReply {
    		fmt.Fprintf(os.Stderr, "Received chat completions reply\n")
    	}
    
    }
    ```
    
1. Run the following command to create a new Go module:

	```shell
	go mod init chat_completions_api-key.go
	```

1. Run `go mod tidy` to install the required dependencies:

    ```cmd
    go mod tidy
    ```

1. Run the following command to run the sample:

	```shell
	go run chat_completions_api-key.go
	```

---

## Output

The output of the sample code looks similar to the following:

```output
Content filter results
  Hate: sev: safe, filtered: false
  SelfHarm: sev: safe, filtered: false
  Sexual: sev: safe, filtered: false
  Violence: sev: safe, filtered: false
Content[0]: There are many alternatives to sugar that you can use, depending on the type of recipe you’re making and your dietary needs or taste preferences. Here are some popular sugar substitutes:

---

### **Natural Sweeteners**  
1. **Honey**
   - Sweeter than sugar and adds moisture, with a distinct flavor.
   - Substitution: Use ¾ cup honey for 1 cup sugar, and reduce the liquid in your recipe by 2 tablespoons. Lower the baking temperature by 25°F to prevent over-browning.

2. **Maple Syrup**
   - Adds a rich, earthy sweetness with a hint of maple flavor.
   - Substitution: Use ¾ cup syrup for 1 cup sugar. Reduce liquids by 3 tablespoons.

3. **Agave Nectar**
   - Sweeter and milder than honey, it dissolves well in cold liquids.
   - Substitution: Use ⅔ cup agave for 1 cup sugar. Reduce liquids in the recipe slightly.

4. **Molasses**
   - A byproduct of sugar production with a robust, slightly bitter flavor.
   - Substitution: Use 1 cup of molasses for 1 cup sugar. Reduce liquid by ¼ cup and consider combining it with other sweeteners due to its strong flavor.

5. **Coconut Sugar**
   - Made from the sap of coconut palms, it has a rich, caramel-like flavor.
   - Substitution: Use it in a 1:1 ratio for sugar.

6. **Date Sugar** (or Medjool Dates)
   - Made from ground, dried dates, or blended into a puree, offering a rich, caramel taste.
   - Substitution: Use 1:1 for sugar. Adjust liquid in recipes if needed.

---

### **Calorie-Free or Reduced-Calorie Sweeteners**
1. **Stevia**
   - A natural sweetener derived from stevia leaves, hundreds of
Finish reason[0]: length
Received chat completions reply
```

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
