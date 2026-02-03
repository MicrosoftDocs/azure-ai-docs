---
title: 'Quickstart: Use the OpenAI service image generation Go SDK'
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: Walkthrough on how to get started with Azure OpenAI image generation using the Go SDK. 
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 08/28/2023
---

Use this guide to get started generating images with the Azure OpenAI SDK for Go.

[Library source code](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/ai/azopenai) | [Package](https://pkg.go.dev/github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai) | [Samples](https://github.com/Azure/azure-sdk-for-go/tree/main/sdk/ai/azopenai)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- [Go 1.8+](https://go.dev/doc/install)
- An Azure OpenAI resource created in a supported region (see [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability)). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).


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

1. Create a new file named *quickstart.go*. Copy the following code into the *quickstart.go* file.

    ```go
	package main

    import (
    	"context"
    	"fmt"
    	"net/http"
    	"os"
    	"log"
    
    	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
    	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
    	"github.com/Azure/azure-sdk-for-go/sdk/azidentity"
    )
    
    func main() {
    	azureOpenAIEndpoint := os.Getenv("AZURE_OPENAI_ENDPOINT")
    	modelDeploymentID := "dall-e-3"
    
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
    
    	resp, err := client.GetImageGenerations(context.TODO(), azopenai.ImageGenerationOptions{
    		Prompt:         to.Ptr("A painting of a cat in the style of Dali."),
    		ResponseFormat: to.Ptr(azopenai.ImageGenerationResponseFormatURL),
    		DeploymentName: to.Ptr(modelDeploymentID),
    	}, nil)
    
    	if err != nil {
    		// Implement application specific error handling logic.
    		log.Printf("ERROR: %s", err)
    		return
    	}
    
    	for _, generatedImage := range resp.Data {
    		// The underlying type for the generatedImage is determined by the value of
    		// ImageGenerationOptions.ResponseFormat. 
    		// In this example we use `azopenai.ImageGenerationResponseFormatURL`,
    		// so the underlying type will be ImageLocation.
    
    		resp, err := http.Head(*generatedImage.URL)
    
    		if err != nil {
    			// Implement application specific error handling logic.
    			log.Printf("ERROR: %s", err)
    			return
    		}
    
    		fmt.Fprintf(os.Stderr, "Image generated, HEAD request on URL returned %d\nImage URL: %s\n", resp.StatusCode, *generatedImage.URL)
    	}
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

    ```go
    package main

    import (
    	"context"
    	"fmt"
    	"net/http"
    	"os"
    	"log"
    
    	"github.com/Azure/azure-sdk-for-go/sdk/ai/azopenai"
    	"github.com/Azure/azure-sdk-for-go/sdk/azcore"
    	"github.com/Azure/azure-sdk-for-go/sdk/azcore/to"
    )
    
    func main() {
    	azureOpenAIEndpoint := os.Getenv("AZURE_OPENAI_ENDPOINT")
    	modelDeploymentID := "dall-e-3"
    
    	azureOpenAIKey := os.Getenv("AZURE_OPENAI_API_KEY")
    	credential := azcore.NewKeyCredential(azureOpenAIKey)
    
    	client, err := azopenai.NewClientWithKeyCredential(
    		azureOpenAIEndpoint, credential, nil)
    	if err != nil {
    		log.Printf("ERROR: %s", err)
    		return
    	}
    
    	resp, err := client.GetImageGenerations(context.TODO(), azopenai.ImageGenerationOptions{
    		Prompt:         to.Ptr("A painting of a cat in the style of Dali."),
    		ResponseFormat: to.Ptr(azopenai.ImageGenerationResponseFormatURL),
    		DeploymentName: to.Ptr(modelDeploymentID),
    	}, nil)
    
    	if err != nil {
    		// Implement application specific error handling logic.
    		log.Printf("ERROR: %s", err)
    		return
    	}
    
    	for _, generatedImage := range resp.Data {
    		// The underlying type for the generatedImage is determined by the value of
    		// ImageGenerationOptions.ResponseFormat. 
    		// In this example we use `azopenai.ImageGenerationResponseFormatURL`,
    		// so the underlying type will be ImageLocation.
    
    		resp, err := http.Head(*generatedImage.URL)
    
    		if err != nil {
    			// Implement application specific error handling logic.
    			log.Printf("ERROR: %s", err)
    			return
    		}
    
    		fmt.Fprintf(os.Stderr, "Image generated, HEAD request on URL returned %d\nImage URL: %s\n", resp.StatusCode, *generatedImage.URL)
    	}
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

## Output

The URL of the generated image is printed to the console.

```console
Image generated, HEAD request on URL returned 200
Image URL: <SAS URL>
```
> [!NOTE]
> The Image APIs come with a content moderation filter. If the service recognizes your prompt as harmful content, it won't return a generated image. For more information, see the [content filter](../concepts/content-filter.md) article.

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* Explore the Image APIs in more depth with the [Image API how-to guide](../how-to/dall-e.md).
* For more examples check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai).
