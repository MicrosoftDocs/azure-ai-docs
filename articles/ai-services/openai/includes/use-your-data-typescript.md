---
#services: cognitive-services
manager: nitinme
author: glharper
ms.author: glharper
ms.service: azure-ai-openai
ms.topic: include
ms.date: 10/22/2024
---

[!INCLUDE [Set up required variables](./use-your-data-common-variables.md)]


## Initialize a Node.js application

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it. Then run the `npm init` command to create a node application with a _package.json_ file.

```console
npm init
```

## Install the client library

Install the Azure OpenAI client and Azure Identity libraries for JavaScript with npm:

```console
npm install openai @azure/identity @azure/openai 
```

The `@azure/openai/types` dependency is included to extend the Azure OpenAI model for the `data_sources` property. This import is only necessary for TypeScript.


Your app's _package.json_ file will be updated with the dependencies.

## Add the TypeScript code

#### [Microsoft Entra ID](#tab/typescript-keyless)

1. Open a command prompt where you want the new project, and create a new file named `ChatWithOwnData.ts`. Copy the following code into the `ChatWithOwnData.ts` file.
    
    ```typescript
    import { AzureOpenAI } from "openai";
    import { DefaultAzureCredential, getBearerTokenProvider } from "@azure/identity";
    import "@azure/openai/types";
    
    // Set the Azure and AI Search values from environment variables
    const endpoint = process.env["AZURE_OPENAI_ENDPOINT"];
    const searchEndpoint = process.env["AZURE_AI_SEARCH_ENDPOINT"];
    const searchIndex = process.env["AZURE_AI_SEARCH_INDEX"];
    
    // keyless authentication    
    const credential = new DefaultAzureCredential();
    const scope = "https://cognitiveservices.azure.com/.default";
    const azureADTokenProvider = getBearerTokenProvider(credential, scope);

    // Required Azure OpenAI deployment name and API version
    const deploymentName = "gpt-4";
    const apiVersion = "2024-07-01-preview";
    
    function getClient(): AzureOpenAI {
      return new AzureOpenAI({
        endpoint,
        azureADTokenProvider,
        deployment: deploymentName,
        apiVersion,
      });
    }
    
    async function main() {
      const client = getClient();
    
      const messages = [
        { role: "user", content: "What are my available health plans?" },
      ];
    
      console.log(`Message: ${messages.map((m) => m.content).join("\n")}`);
    
      const events = await client.chat.completions.create({
        stream: true,
        messages: [
          {
            role: "user",
            content:
              "What's the most common feedback we received from our customers about the product?",
          },
        ],
        max_tokens: 128,
        model: "",
        data_sources: [
          {
            type: "azure_search",
            parameters: {
              endpoint: searchEndpoint,
              index_name: searchIndex,
              authentication: {
                type: "api_key",
                key: searchKey,
              },
            },
          },
        ],
      });
    
      let response = "";
      for await (const event of events) {
        for (const choice of event.choices) {
          const newText = choice.delta?.content;
          if (newText) {
            response += newText;
            // To see streaming results as they arrive, uncomment line below
            // console.log(newText);
          }
        }
      }
      console.log(response);
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    ```

1. Build the application with the following command:

    ```console
    tsc
    ```

1. Run the application with the following command:

    ```console
    node ChatWithOwnData.js
    ```


#### [API key](#tab/typescript-key)

1. Open a command prompt where you want the new project, and create a new file named `ChatWithOwnData.ts`. Copy the following code into the `ChatWithOwnData.ts` file.
    
    ```typescript
    import { AzureOpenAI } from "openai";
    import "@azure/openai/types";
    
    // Set the Azure and AI Search values from environment variables
    const endpoint = process.env["AZURE_OPENAI_ENDPOINT"];
    const apiKey = process.env["AZURE_OPENAI_API_KEY"];
    const searchEndpoint = process.env["AZURE_AI_SEARCH_ENDPOINT"];
    const searchKey = process.env["AZURE_AI_SEARCH_API_KEY"];
    const searchIndex = process.env["AZURE_AI_SEARCH_INDEX"];
    
    // Required Azure OpenAI deployment name and API version
    const deploymentName = "gpt-4";
    const apiVersion = "2024-07-01-preview";
    
    function getClient(): AzureOpenAI {
      return new AzureOpenAI({
        endpoint,
        apiKey,
        deployment: deploymentName,
        apiVersion,
      });
    }
    
    async function main() {
      const client = getClient();
    
      const messages = [
        { role: "user", content: "What are my available health plans?" },
      ];
    
      console.log(`Message: ${messages.map((m) => m.content).join("\n")}`);
    
      const events = await client.chat.completions.create({
        stream: true,
        messages: [
          {
            role: "user",
            content:
              "What's the most common feedback we received from our customers about the product?",
          },
        ],
        max_tokens: 128,
        model: "",
        data_sources: [
          {
            type: "azure_search",
            parameters: {
              endpoint: searchEndpoint,
              index_name: searchIndex,
              authentication: {
                type: "api_key",
                key: searchKey,
              },
            },
          },
        ],
      });
    
      let response = "";
      for await (const event of events) {
        for (const choice of event.choices) {
          const newText = choice.delta?.content;
          if (newText) {
            response += newText;
            // To see streaming results as they arrive, uncomment line below
            // console.log(newText);
          }
        }
      }
      console.log(response);
    }
    
    main().catch((err) => {
      console.error("The sample encountered an error:", err);
    });
    ```

1. Build the application with the following command:

    ```console
    tsc
    ```

1. Run the application with the following command:

    ```console
    node ChatWithOwnData.js
    ```


---


> [!IMPORTANT]
> For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see the Azure AI services [security](../../security-features.md) article.


## Output

```output
Message: What are my available health plans?
The available health plans in the Contoso Electronics plan and benefit packages are the Northwind Health Plus and Northwind Standard plans.

```

