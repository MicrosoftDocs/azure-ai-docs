---
title: 'Quickstart: Use Azure OpenAI Service with the JavaScript SDK'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first chat completions call with the JavaScript SDK. 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mrbullwinkle
ms.author: mbullwin
ms.date: 10/22
---

[Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

> [!NOTE]
> This guide uses the [latest OpenAI npm package](https://www.npmjs.com/package/openai) which now fully supports Azure OpenAI. If you're looking for code examples for the legacy Azure OpenAI JavaScript SDK, they're currently still [available in this repo](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples/v2-beta/javascript).

## Prerequisites

- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [TypeScript](https://www.typescriptlang.org/download/)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI Service resource with a `gpt-4` series model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

### Microsoft Entra ID prerequisites

For the recommended keyless authentication with Microsoft Entra ID, you need to:
- Install the [Azure CLI](/cli/azure/install-azure-cli) used for keyless authentication with Microsoft Entra ID.
- Assign the `Cognitive Services User` role to your user account. You can assign roles in the Azure portal under **Access control (IAM)** > **Add role assignment**.

## Set up

1. Create a new folder `chat-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir chat-quickstart && cd chat-quickstart
    ```
    
1. Create the `package.json` with the following command:

    ```shell
    npm init -y
    ```

1. Update the `package.json` to ECMAScript with the following command: 

    ```shell
    npm pkg set type=module
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

## Create a sample application

## [Microsoft Entra ID](#tab/typescript-keyless)
   
1. Create the `index.ts` file with the following code:
 
    ```typescript
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
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-08-01-preview";
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4o-mini"; //This must match your deployment name.
    
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
            content: "Does Azure OpenAI support customer managed keys?",
          },
          {
            role: "assistant",
            content: "Yes, customer managed keys are supported by Azure OpenAI?",
          },
          { role: "user", content: "Do other Azure AI services support this too?" },
        ],
        model: "",
      };
    }
    async function printChoices(completion: ChatCompletion): Promise<void> {
      for (const choice of completion.choices) {
        console.log(choice.message);
      }
    }
    export async function main() {
      const client = getClient();
      const messages = createMessages();
      const result = await client.chat.completions.create(messages);
      await printChoices(result);
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    ```

1. Create the `tsconfig.json` file to transpile the TypeScript code and copy the following code for ECMAScript.

    ```json
    {
        "compilerOptions": {
          "module": "NodeNext",
          "target": "ES2022", // Supports top-level await
          "moduleResolution": "NodeNext",
          "skipLibCheck": true, // Avoid type errors from node_modules
          "strict": true // Enable strict type-checking options
        },
        "include": ["*.ts"]
    }
    ```

1. Transpile from TypeScript to JavaScript.

    ```shell
    tsc
    ```
    
1. Run the code with the following command:

    ```shell
    node index.js
    ```

## [API Key](#tab/typescript-key)

1. Create the `index.ts` file with the following code:
    
    ```typescript
    import { AzureOpenAI } from "openai";
    import type {
      ChatCompletion,
      ChatCompletionCreateParamsNonStreaming,
    } from "openai/resources/index";
    
    // You will need to set these environment variables or edit the following values
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
    
    // Required Azure OpenAI deployment name and API version
    const apiVersion = process.env.OPENAI_API_KEY || "2024-08-01-preview";
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4o-mini"; //This must match your deployment name.
    
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
            content: "Does Azure OpenAI support customer managed keys?",
          },
          {
            role: "assistant",
            content: "Yes, customer managed keys are supported by Azure OpenAI?",
          },
          { role: "user", content: "Do other Azure AI services support this too?" },
        ],
        model: "",
      };
    }
    async function printChoices(completion: ChatCompletion): Promise<void> {
      for (const choice of completion.choices) {
        console.log(choice.message);
      }
    }
    export async function main() {
      const client = getClient();
      const messages = createMessages();
      const result = await client.chat.completions.create(messages);
      await printChoices(result);
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    ```

1. Create the `tsconfig.json` file to transpile the TypeScript code and copy the following code for ECMAScript.

    ```json
    {
        "compilerOptions": {
          "module": "NodeNext",
          "target": "ES2022", // Supports top-level await
          "moduleResolution": "NodeNext",
          "skipLibCheck": true, // Avoid type errors from node_modules
          "strict": true // Enable strict type-checking options
        },
        "include": ["*.ts"]
    }
    ```

1. Transpile from TypeScript to JavaScript.

    ```shell
    tsc
    ```

1. Run the code with the following command:

    ```shell
    node index.js
    ```

---

## Output

```output
== Chat Completions Sample ==
{
  content: 'Yes, several other Azure AI services also support customer managed keys for enhanced security and control over encryption keys.',
  role: 'assistant'
}
```

---

> [!NOTE]
> If your receive the error: *Error occurred: OpenAIError: The `apiKey` and `azureADTokenProvider` arguments are mutually exclusive; only one can be passed at a time.* You might need to remove a preexisting environment variable for the API key from your system. Even though the Microsoft Entra ID code sample isn't explicitly referencing the API key environment variable, if one is present on the system executing this sample, this error is still generated.


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* [Azure OpenAI Overview](../overview.md)
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
