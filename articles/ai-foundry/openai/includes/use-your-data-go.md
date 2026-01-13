---
manager: nitinme
author: travisw
ms.author: travisw
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 01/17/2025
---

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up
 
1. Create a new folder `dall-e-quickstart` and go to the quickstart folder with the following command:

	```shell
	mkdir dall-e-quickstart && cd dall-e-quickstart
	```

1. For the **recommended** keyless authentication with Microsoft Entra ID, sign in to Azure with the following command:

	```console
	az login
	```

[!INCLUDE [Set up required variables](./use-your-data-common-variables.md)]

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

1. Create a new file named *quickstart.go*. Copy the following code into the *quickstart.go* file.

   ```golang
   package main

   import (
   	"context"
   	"fmt"
   	"log"
   	"os"
   
   	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
   	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
   	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
   )
   
   func main() {
    azureOpenAIEndpoint := os.Getenv("AZURE_OPENAI_ENDPOINT")
    credential, err := azidentity.NewDefaultAzureCredential(nil)
    client, err := azopenai.NewClient(azureOpenAIEndpoint, credential, nil)

   	modelDeploymentID := os.Getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
   
   	// Azure AI Search configuration
   	searchIndex := os.Getenv("AZURE_AI_SEARCH_INDEX")
   	searchEndpoint := os.Getenv("AZURE_AI_SEARCH_ENDPOINT")
   	searchAPIKey := os.Getenv("AZURE_AI_SEARCH_API_KEY")
   
   	if modelDeploymentID == "" || azureOpenAIEndpoint == "" || searchIndex == "" || searchEndpoint == "" || searchAPIKey == "" {
   		fmt.Fprintf(os.Stderr, "Skipping example, environment variables missing\n")
   		return
   	}
    
   	client, err := azopenai.NewClientWithKeyCredential(azureOpenAIEndpoint, credential, nil)
   
   	if err != nil {
		// Implement application specific error handling logic.
		log.Printf("ERROR: %s", err)
		return
	}
   
   	resp, err := client.GetChatCompletions(context.TODO(), azopenai.ChatCompletionsOptions{
   		Messages: []azopenai.ChatRequestMessageClassification{
   			&azopenai.ChatRequestUserMessage{Content: azopenai.NewChatRequestUserMessageContent("What are my available health plans?")},
   		},
   		MaxTokens: to.Ptr[int32](512),
   		AzureExtensionsOptions: []azopenai.AzureChatExtensionConfigurationClassification{
   			&azopenai.AzureSearchChatExtensionConfiguration{
   				// This allows Azure OpenAI to use an Azure AI Search index.
   				// Answers are based on the model's pretrained knowledge
   				// and the latest information available in the designated data source. 
   				Parameters: &azopenai.AzureSearchChatExtensionParameters{
   					Endpoint:  &searchEndpoint,
   					IndexName: &searchIndex,
   					Authentication: &azopenai.OnYourDataAPIKeyAuthenticationOptions{
   						Key: &searchAPIKey,
   					},
   				},
   			},
   		},
   		DeploymentName: &modelDeploymentID,
   	}, nil)
   
   	if err != nil {
		// Implement application specific error handling logic.
		log.Printf("ERROR: %s", err)
		return
	}
   
   	fmt.Fprintf(os.Stderr, "Extensions Context Role: %s\nExtensions Context (length): %d\n",
   		*resp.Choices[0].Message.Role,
   		len(*resp.Choices[0].Message.Content))
   
   	fmt.Fprintf(os.Stderr, "ChatRole: %s\nChat content: %s\n",
   		*resp.Choices[0].Message.Role,
   		*resp.Choices[0].Message.Content,
   	)
   }
   ```

1. Run the following command to create a new Go module:

	```shell
	go mod init quickstart.go
	```

1. Run `go mod tidy` to install the required dependencies:

	```cmd
	go mod tidy
	```

1. Run the following command to run the sample:

	```shell
	go run quickstart.go
	```

#### [API key](#tab/api-key)

To run the sample:

1. Create a new file named *quickstart.go*. Copy the following code into the *quickstart.go* file.

   ```golang
   package main

   import (
   	"context"
   	"fmt"
   	"log"
   	"os"
   
   	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
   	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
   	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
   )
   
   func main() {
   	azureOpenAIEndpoint := os.Getenv("AZURE_OPENAI_ENDPOINT")
   	azureOpenAIKey := os.Getenv("AZURE_OPENAI_API_KEY")
   	modelDeploymentID := os.Getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
   
   	// Azure AI Search configuration
   	searchIndex := os.Getenv("AZURE_AI_SEARCH_INDEX")
   	searchEndpoint := os.Getenv("AZURE_AI_SEARCH_ENDPOINT")
   	searchAPIKey := os.Getenv("AZURE_AI_SEARCH_API_KEY")
   
   	if azureOpenAIKey == "" || modelDeploymentID == "" || azureOpenAIEndpoint == "" || searchIndex == "" || searchEndpoint == "" || searchAPIKey == "" {
   		fmt.Fprintf(os.Stderr, "Skipping example, environment variables missing\n")
   		return
   	}
   
   	credential := azcore.NewKeyCredential(azureOpenAIKey)
   
   	client, err := azopenai.NewClientWithKeyCredential(azureOpenAIEndpoint, credential, nil)
   
   	   	if err != nil {
		// Implement application specific error handling logic.
		log.Printf("ERROR: %s", err)
		return
	}
   
   	resp, err := client.GetChatCompletions(context.TODO(), azopenai.ChatCompletionsOptions{
   		Messages: []azopenai.ChatRequestMessageClassification{
   			&azopenai.ChatRequestUserMessage{Content: azopenai.NewChatRequestUserMessageContent("What are my available health plans?")},
   		},
   		MaxTokens: to.Ptr[int32](512),
   		AzureExtensionsOptions: []azopenai.AzureChatExtensionConfigurationClassification{
   			&azopenai.AzureSearchChatExtensionConfiguration{
   				// This allows Azure OpenAI to use an Azure AI Search index.
   				// Answers are based on the model's pretrained knowledge
   				// and the latest information available in the designated data source. 
   				Parameters: &azopenai.AzureSearchChatExtensionParameters{
   					Endpoint:  &searchEndpoint,
   					IndexName: &searchIndex,
   					Authentication: &azopenai.OnYourDataAPIKeyAuthenticationOptions{
   						Key: &searchAPIKey,
   					},
   				},
   			},
   		},
   		DeploymentName: &modelDeploymentID,
   	}, nil)
   
   	if err != nil {
		// Implement application specific error handling logic.
		log.Printf("ERROR: %s", err)
		return
	}
   
   	fmt.Fprintf(os.Stderr, "Extensions Context Role: %s\nExtensions Context (length): %d\n",
   		*resp.Choices[0].Message.Role,
   		len(*resp.Choices[0].Message.Content))
   
   	fmt.Fprintf(os.Stderr, "ChatRole: %s\nChat content: %s\n",
   		*resp.Choices[0].Message.Role,
   		*resp.Choices[0].Message.Content,
   	)
   }
   ```

1. Run the following command to create a new Go module:

	```shell
	go mod init quickstart.go
	```

1. Run `go mod tidy` to install the required dependencies:

    ```cmd
    go mod tidy
    ```

1. Run the following command to run the sample:

	```shell
	go run quickstart.go
	```

---

The application prints the response including both answers to your query and citations from your uploaded files.
