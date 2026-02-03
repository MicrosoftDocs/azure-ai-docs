---
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: include
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: devx-track-js
ai-usage: ai-assisted
---
[Reference documentation](/javascript/api/overview/azure/ai-language-text-readme?view=azure-node-latest&preserve-view=true) | [More samples](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/cognitivelanguage/ai-language-text/samples/v1) | [Package (npm)](https://www.npmjs.com/package/@azure/ai-language-text) | [Library source code](https://github.com/Azure/azure-sdk-for-js/tree/main/sdk/cognitivelanguage/ai-language-text)

Use this quickstart to create a language detection application with the client library for Node.js. In the following example, you create a JavaScript application that can identify the language a text sample was written in.


## Prerequisites

* Azure subscription - [Create one for free](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn)
* [Node.js](https://nodejs.org/) v14 LTS or later


## Setting up

[!INCLUDE [Create an Azure resource](../../../includes/create-resource.md)]



[!INCLUDE [Get your key and endpoint](../../../includes/get-key-endpoint.md)]



[!INCLUDE [Create environment variables](../../../includes/environment-variables.md)]


### Create a new Node.js application

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it. 

```console
mkdir myapp 

cd myapp
```

Run the `npm init` command to create a node application with a `package.json` file. 

```console
npm init
```

### Install the client library

Install the npm package:

```console
npm install @azure/ai-language-text
```


## Code example

Open the file and copy the below code. Then run the code. 

```javascript
"use strict";

const { AzureKeyCredential, TextAnalysisClient } = require("@azure/ai-language-text");

// This example requires environment variables named "LANGUAGE_KEY" and "LANGUAGE_ENDPOINT"
const key = process.env.LANGUAGE_KEY;
const endpoint = process.env.LANGUAGE_ENDPOINT;

if (!key || !endpoint) {
  throw new Error(
    "Missing LANGUAGE_KEY or LANGUAGE_ENDPOINT environment variables."
  );
}

//Example sentences in different languages to be analyzed
const documents = [
    "This document is written in English.",
    "这是一个用中文写的文件",
];

//Example of how to use the client library to detect language
async function main() {
    console.log("== Language detection sample ==");
  
    const client = new TextAnalysisClient(endpoint, new AzureKeyCredential(key));
  
    const result = await client.analyze("LanguageDetection", documents);
  
    for (const doc of result) {
      if (!doc.error) {
        console.log(
          `ID ${doc.id} - Primary language: ${doc.primaryLanguage.name} (iso6391 name: ${doc.primaryLanguage.iso6391Name})`
        );
      }
    }
}

main().catch((err) => {
    console.error("The sample encountered an error:", err);
});
```



### Output

```console
== Language detection sample ==
ID 0 - Primary language: English (iso6391 name: en)
ID 1 - Primary language: Chinese_Simplified (iso6391 name: zh_chs)
```
