---
title: 'Quickstart: Use GPT-4 Turbo with Vision on your images with the JavaScript SDK'
titleSuffix: Azure OpenAI
description: Get started using the OpenAI JavaScript SDK to deploy and use the GPT-4 Turbo with Vision model.
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.custom: references_regions
ms.date: 01/29/2026
ai-usage: ai-assisted
---

Use this article to get started using the OpenAI JavaScript SDK to deploy and use a vision-enabled chat model. 

This SDK is provided by OpenAI with Azure specific types provided by Azure. 

[Reference documentation](https://platform.openai.com/docs/api-reference/chat) | [Library source code](https://github.com/openai/openai-node?azure-portal=true) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI resource created in a supported region (see [Region availability](/azure/ai-foundry/openai/concepts/models#model-summary-table-and-region-availability)). For more information, see [Create a resource and deploy a model with Azure OpenAI](../how-to/create-resource.md).

> [!NOTE]
> This library is maintained by OpenAI. Refer to the [release history](https://github.com/openai/openai-node/releases) to track the latest updates to the library.

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up
 
1. Create a new folder `vision-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir vision-quickstart && cd vision-quickstart
    ```
    

1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```   

1. Install the OpenAI client library for JavaScript with:

    ```console
    npm install openai
    ```

1. For the **recommended** passwordless authentication:

    ```console
    npm install @azure/identity
    ```

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

> [!CAUTION]
> To use the recommended keyless authentication with the SDK, make sure that the `AZURE_OPENAI_API_KEY` environment variable isn't set. 

## Create a new JavaScript application for image prompts

Select an image from the [azure-samples/cognitive-services-sample-data-files](https://github.com/Azure-Samples/cognitive-services-sample-data-files/tree/master/ComputerVision/Images). Enter your publicly accessible image URL in the code below or set the `IMAGE_URL` environment variable to it.

> [!IMPORTANT]
> If you use a SAS URL to an image stored in Azure blob storage, you need to enable Managed Identity and assign the **Storage Blob Reader** role to your Azure OpenAI resource (do this in the Azure portal). This allows the model to access the image in blob storage.

> [!TIP]
> You can also use a base 64 encoded image data instead of a URL. For more information, see the [Vision chats how-to guide](../how-to/gpt-with-vision.md#use-a-local-image).

## [Microsoft Entra ID](#tab/keyless)

1. Create the `index.js` file with the following code:
    
    ```javascript
    const AzureOpenAI = require('openai').AzureOpenAI;
    const { 
        DefaultAzureCredential, 
        getBearerTokenProvider 
    } = require('@azure/identity');

    // You will need to set these environment variables or edit the following values
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const imageUrl = process.env.IMAGE_URL || "<image url>";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-07-01-preview";
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4-with-turbo";
    
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
    function createMessages() {
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
    async function printChoices(completion) {
      for (const choice of completion.choices) {
        console.log(choice.message);
      }
    }
    export async function main() {
      console.log("== Get Vision chats Sample ==");
    
      const client = getClient();
      const messages = createMessages();
      const completion = await client.chat.completions.create(messages);
      await printChoices(completion);
    }
    
    main().catch((err) => {
      console.error("Error occurred:", err);
    });
    ```

1. Sign in to Azure with the following command:

    ```shell
    az login
    ```

1. Run the JavaScript file.

    ```shell
    node index.js
    ```


## [API key](#tab/api-key)

1. Create the `index.js` file with the following code: 
    
    ```javascript
    const { AzureOpenAI } = require("openai");
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
    const imageUrl = process.env.IMAGE_URL || "<image url>";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-07-01-preview";
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4-with-turbo";
    
    function getClient() {
      return new AzureOpenAI({
        endpoint,
        apiKey,
        apiVersion,
        deployment: deploymentName,
      });
    }
    function createMessages() {
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
    async function printChoices(completion) {
      for (const choice of completion.choices) {
        console.log(choice.message);
      }
    }
    export async function main() {
      console.log("== Get Vision chats Sample ==");
    
      const client = getClient();
      const messages = createMessages();
      const completion = await client.chat.completions.create(messages);
      await printChoices(completion);
    }
    
    main().catch((err) => {
      console.error("Error occurred:", err);
    });
    ```

1. Run the JavaScript file.

    ```shell
    node index.js
    ```

---

<!--
## Troubleshooting

| Error | Cause | Solution |
|-------|-------|----------|
| `401 Unauthorized` | Invalid API key or token | Verify `AZURE_OPENAI_API_KEY` is set, or for keyless auth, run `az login` and check role assignment. |
| `404 Not Found` | Incorrect endpoint or deployment | Check `AZURE_OPENAI_ENDPOINT` and `AZURE_OPENAI_DEPLOYMENT_NAME` match your Azure resource. |
| `429 Too Many Requests` | Rate limit exceeded | Wait and retry, or request a quota increase in Azure portal. |
| Truncated response | `max_tokens` too low | Increase the `max_tokens` value in your request. |
| Content filtered response | Image triggered content filter | GPT-4 Turbo with Vision has mandatory content filtering that can't be disabled. |

--> 
## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource or resource group. Deleting the resource group also deletes any other resources associated with it.

- [Azure portal](../../../ai-services/multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../../ai-services/multi-service-resource.md?pivots=azcli#clean-up-resources)


