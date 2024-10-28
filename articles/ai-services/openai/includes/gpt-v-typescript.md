---
title: 'Quickstart: Use GPT-4 Turbo with Vision on your images and videos with the JavaScript SDK'
titleSuffix: Azure OpenAI
description: Get started using the OpenAI JavaScript SDK to deploy and use the GPT-4 Turbo with Vision model.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
ms.custom: references_regions
ms.date: 10/23/2024
---

Use this article to get started using the OpenAI JavaScript SDK to deploy and use the GPT-4 Turbo with Vision model. 

This SDK is provided by OpenAI with Azure specific types provided by Azure. 

[Reference documentation](https://platform.openai.com/docs/api-reference/chat) | [Library source code](https://github.com/openai/openai-node?azure-portal=true) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [TypeScript](https://www.typescriptlang.org/download/)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI resource created in a supported region (see [Region availability](/azure/ai-services/openai/concepts/models#model-summary-table-and-region-availability)). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).


> [!NOTE]
> This library is maintained by OpenAI. Refer to the [release history](https://github.com/openai/openai-node/releases) to track the latest updates to the library.

[!INCLUDE [get-key-endpoint](get-key-endpoint.md)]

[!INCLUDE [environment-variables](environment-variables.md)]


## Create a Node application

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it. Then run the `npm init` command to create a node application with a _package.json_ file.

```console
npm init
```

## Install the client library

Install the client libraries with:

```console
npm install openai @azure/identity
```

Your app's _package.json_ file will be updated with the dependencies.

## Create a new JavaScript application for image prompts

Select an image from the [azure-samples/cognitive-services-sample-data-files](https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/ComputerVision/Images) and set the URL for an image in the environment variables.


## [Microsoft Entra ID](#tab/typescript-keyless)

1. Create a _quickstart.ts_ and paste in the following code. 
    
    ```typescript
    import "dotenv/config";
    import { AzureOpenAI } from "openai";
    import { 
        DefaultAzureCredential, 
        getBearerTokenProvider 
    } from "@azure/identity";
    import type {
      ChatCompletion,
      ChatCompletionCreateParamsNonStreaming,
    } from "openai/resources/index";
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env["AZURE_OPENAI_ENDPOINT"] || "<endpoint>";
    const imageUrl = process.env["IMAGE_URL"] || "<image url>";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = "2024-07-01-preview";
    const deploymentName = "gpt-4-with-turbo";
    
    // keyless authentication    
    const credential = new DefaultAzureCredential();
    const scope = "https://cognitiveservices.azure.com/.default";
    const azureADTokenProvider = getBearerTokenProvider(credential, scope);

    function getClient(): AzureOpenAI {
      return new AzureOpenAI({
        endpoint,
        azureADTokenProvider,
        apiVersion,
        deployment: deploymentName,
      });
    }
    function createMessages(): ChatCompletionCreateParamsNonStreaming {
      return {
        messages: [
          { role: "system", content: "You are a helpful assistant." },
          {
            role: "user",
            content: [
              {
                type: "text",
                text: "Describe this picture:",
              },
              {
                type: "image_url",
                image_url: {
                  url: imageUrl,
                },
              },
            ],
          },
        ],
        model: "",
        max_tokens: 2000,
      };
    }
    async function printChoices(completion: ChatCompletion): Promise<void> {
      for (const choice of completion.choices) {
        console.log(choice.message);
      }
    }
    export async function main() {
      console.log("== Get GPT-4 Turbo with vision Sample ==");
    
      const client = getClient();
      const messages = createMessages();
      const completion = await client.chat.completions.create(messages);
      await printChoices(completion);
    }
    
    main().catch((err) => {
      console.error("Error occurred:", err);
    });
    ```
1. Make the following changes:
    1. Enter the name of your GPT-4 Turbo with Vision deployment in the appropriate field.
    1. Change the value of the `"url"` field to the URL of your image.
        > [!TIP]
        > You can also use a base 64 encoded image data instead of a URL. For more information, see the [GPT-4 Turbo with Vision how-to guide](../how-to/gpt-with-vision.md#use-a-local-image).

1. Build the application with the following command:

    ```console
    tsc
    ```

1. Run the application with the following command:

    ```console
    node quickstart.js
    ```



## [API key](#tab/typescript-key)

1. Create a _quickstart.ts_ and paste in the following code. 
    
    ```typescript
    import "dotenv/config";
    import { AzureOpenAI } from "openai";
    import type {
      ChatCompletion,
      ChatCompletionCreateParamsNonStreaming,
    } from "openai/resources/index";
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env["AZURE_OPENAI_ENDPOINT"] || "<endpoint>";
    const apiKey = process.env["AZURE_OPENAI_API_KEY"] || "<api key>";
    const imageUrl = process.env["IMAGE_URL"] || "<image url>";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = "2024-07-01-preview";
    const deploymentName = "gpt-4-with-turbo";
    
    function getClient(): AzureOpenAI {
      return new AzureOpenAI({
        endpoint,
        apiKey,
        apiVersion,
        deployment: deploymentName,
      });
    }
    function createMessages(): ChatCompletionCreateParamsNonStreaming {
      return {
        messages: [
          { role: "system", content: "You are a helpful assistant." },
          {
            role: "user",
            content: [
              {
                type: "text",
                text: "Describe this picture:",
              },
              {
                type: "image_url",
                image_url: {
                  url: imageUrl,
                },
              },
            ],
          },
        ],
        model: "",
        max_tokens: 2000,
      };
    }
    async function printChoices(completion: ChatCompletion): Promise<void> {
      for (const choice of completion.choices) {
        console.log(choice.message);
      }
    }
    export async function main() {
      console.log("== Get GPT-4 Turbo with vision Sample ==");
    
      const client = getClient();
      const messages = createMessages();
      const completion = await client.chat.completions.create(messages);
      await printChoices(completion);
    }
    
    main().catch((err) => {
      console.error("Error occurred:", err);
    });
    ```
1. Make the following changes:
    1. Enter the name of your GPT-4 Turbo with Vision deployment in the appropriate field.
    1. Change the value of the `"url"` field to the URL of your image.
        > [!TIP]
        > You can also use a base 64 encoded image data instead of a URL. For more information, see the [GPT-4 Turbo with Vision how-to guide](../how-to/gpt-with-vision.md#use-a-local-image).

1. Build the application with the following command:

    ```console
    tsc
    ```

1. Run the application with the following command:

    ```console
    node quickstart.js
    ```



---

## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)


