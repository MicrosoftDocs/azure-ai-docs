---
manager: nitinme
author: glharper
ms.author: glharper
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 01/10/2025
---

[!INCLUDE [Set up required variables](./use-your-data-common-variables.md)]

## Set up
 
1. Create a new folder `use-data-quickstart` and go to the quickstart folder with the following command:

    ```shell
    mkdir use-data-quickstart && cd use-data-quickstart
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

## Add the JavaScript code

#### [Microsoft Entra ID](#tab/keyless)

1. Create the `index.js` file with the following code: 
    
    ```javascript
    const { DefaultAzureCredential, getBearerTokenProvider } = require("@azure/identity");
    const { AzureOpenAI } = require("openai");
    
    // Set the Azure and AI Search values from environment variables
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const searchEndpoint = process.env.AZURE_AI_SEARCH_ENDPOINT || "Your search endpoint";
    const searchIndex = process.env.AZURE_AI_SEARCH_INDEX || "Your search index";

    // keyless authentication    
    const credential = new DefaultAzureCredential();
    const scope = "https://cognitiveservices.azure.com/.default";
    const azureADTokenProvider = getBearerTokenProvider(credential, scope);

    // Required Azure OpenAI deployment name and API version
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4";
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-10-21";
    
    function getClient() {
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
    
    // Set the Azure and AI Search values from environment variables
    const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
    const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
    const searchEndpoint = process.env.AZURE_AI_SEARCH_ENDPOINT || "Your search endpoint";
    const searchKey = process.env.AZURE_AI_SEARCH_API_KEY || "Your search key";
    const searchIndex = process.env.AZURE_AI_SEARCH_INDEX || "Your search index";
    
    // Required Azure OpenAI deployment name and API version
    const deploymentName = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-4";
    const apiVersion = process.env.OPENAI_API_VERSION || "2024-10-21";
    
    function getClient() {
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

1. Run the JavaScript file.

    ```shell
    node index.js
    ```

---


## Output

```output
Message: What are my available health plans?
The available health plans in the Contoso Electronics plan and benefit packages are the Northwind Health Plus and Northwind Standard plans.

```

