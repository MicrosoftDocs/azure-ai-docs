---
title: 'Quickstart: Use Azure OpenAI in Azure AI Foundry Models with the JavaScript SDK and the completions API'
titleSuffix: Azure OpenAI
description: Walkthrough on how to get started with Azure OpenAI and make your first completions call with the JavaScript SDK. 
manager: nitinme
ms.service: azure-ai-openai
ms.topic: include
author: mrbullwinkle
ms.author: mbullwin
ms.date: 10/22/2024
---

[Source code](https://github.com/openai/openai-node) | [Package (npm)](https://www.npmjs.com/package/openai) | [Samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples)

> [!NOTE]
> This guide uses the [latest OpenAI npm package](https://www.npmjs.com/package/openai) which now fully supports Azure OpenAI. If you're looking for code examples for the legacy Azure OpenAI JavaScript SDK, they're currently still [available in this repo](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/openai/openai/samples/v2-beta/javascript).

## Prerequisites


- An Azure subscription - [Create one for free](https://azure.microsoft.com/free/cognitive-services?azure-portal=true)
- [LTS versions of Node.js](https://github.com/nodejs/release#release-schedule)
- [Azure CLI](/cli/azure/install-azure-cli) used for passwordless authentication in a local development environment, create the necessary context by signing in with the Azure CLI.
- An Azure OpenAI in Azure AI Foundry Models resource with the `gpt-35-turbo-instruct` model deployed. For more information about model deployment, see the [resource deployment guide](../how-to/create-resource.md).

## Retrieve resource information

[!INCLUDE [resource authentication](resource-authentication.md)]

> [!CAUTION]
> To use the recommended keyless authentication with the SDK, make sure that the `AZURE_OPENAI_API_KEY` environment variable isn't set. 

## Install the client library

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it.

Install the required packages for JavaScript with npm from within the context of your new directory:

```console
npm install openai @azure/identity
```

Your app's _package.json_ file is updated with the dependencies.


## Create a sample application

Open a command prompt where you created the new project, and create a new file named Completion.js. Copy the following code into the Completion.js file.


## [Microsoft Entra ID](#tab/keyless)

```javascript
const { AzureOpenAI } = require("openai");
const { 
  DefaultAzureCredential, 
  getBearerTokenProvider 
} = require("@azure/identity");

// You will need to set these environment variables or edit the following values
const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
const apiVersion = process.env.OPENAI_API_VERSION || "2024-04-01-preview";
const deployment = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-35-turbo-instruct"; //The deployment name for your completions API model. The instruct model is the only new model that supports the legacy API.

// keyless authentication    
const credential = new DefaultAzureCredential();
const scope = "https://cognitiveservices.azure.com/.default";
const azureADTokenProvider = getBearerTokenProvider(credential, scope);

const prompt = ["When was Microsoft founded?"];

async function main() {
  console.log("== Get completions Sample ==");

  const client = new AzureOpenAI({ endpoint, azureADTokenProvider, apiVersion, deployment });  

  const result = await client.completions.create({ prompt, model: deployment, max_tokens: 128 });

  for (const choice of result.choices) {
    console.log(choice.text);
  }
}

main().catch((err) => {
  console.error("Error occurred:", err);
});

module.exports = { main };
```

Run the script with the following command:

```cmd
node.exe Completion.js
```


## [API key](#tab/api-key)

```javascript
const { AzureOpenAI } = require("openai");

// You will need to set these environment variables or edit the following values
const endpoint = process.env.AZURE_OPENAI_ENDPOINT || "Your endpoint";
const apiKey = process.env.AZURE_OPENAI_API_KEY || "Your API key";
const apiVersion = process.env.OPENAI_API_VERSION || "2024-04-01-preview";
const deployment = process.env.AZURE_OPENAI_DEPLOYMENT_NAME || "gpt-35-turbo-instruct"; //The deployment name for your completions API model. The instruct model is the only new model that supports the legacy API.

const prompt = ["When was Microsoft founded?"];

async function main() {
  console.log("== Get completions Sample ==");

  const client = new AzureOpenAI({ endpoint, apiKey, apiVersion, deployment });  

  const result = await client.completions.create({ prompt, model: deployment, max_tokens: 128 });

  for (const choice of result.choices) {
    console.log(choice.text);
  }
}

main().catch((err) => {
  console.error("Error occurred:", err);
});

module.exports = { main };
```

Run the script with the following command:

```cmd
node.exe Completion.js
```

---

## Output

```output
== Get completions Sample ==

Microsoft was founded on April 4, 1975.
```

> [!NOTE]
> If your receive the error: *Error occurred: OpenAIError: The `apiKey` and `azureADTokenProvider` arguments are mutually exclusive; only one can be passed at a time.* You might need to remove a preexisting environment variable for the API key from your system. Even though the Microsoft Entra ID code sample isn't explicitly referencing the API key environment variable, if one is present on the system executing this sample, this error is still generated.


## Clean up resources

If you want to clean up and remove an Azure OpenAI resource, you can delete the resource. Before deleting the resource, you must first delete any deployed models.

- [Azure portal](../../multi-service-resource.md?pivots=azportal#clean-up-resources)
- [Azure CLI](../../multi-service-resource.md?pivots=azcli#clean-up-resources)

## Next steps

* [Azure OpenAI Overview](../overview.md)
* For more examples, check out the [Azure OpenAI Samples GitHub repository](https://github.com/Azure-Samples/openai)
