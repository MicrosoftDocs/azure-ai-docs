---
#services: cognitive-services
manager: nitinme
author: glharper
ms.author: glharper
ms.service: azure-ai-openai
ms.topic: include
ms.date: 09/06/2024
---

[!INCLUDE [Set up required variables](./use-your-data-common-variables.md)]


## Create a Node application

In a console window (such as cmd, PowerShell, or Bash), create a new directory for your app, and navigate to it. Then run the `npm init` command to create a node application with a _package.json_ file.

```console
npm init
```

## Install the client library

Install the Azure OpenAI client and Azure Identity libraries for JavaScript with npm:

#### [TypeScript](#tab/typescript)

```console
npm install openai @azure/identity @azure/openai 
```

#### [JavaScript](#tab/javascript)

```console
npm install @azure/openai @azure/identity
```

---

Your app's _package.json_ file will be updated with the dependencies.

## Create a sample application

#### [TypeScript](#tab/typescript)

1. Open a command prompt where you want the new project, and create a new file named `ChatWithOwnData.ts`. Copy the following code into the `ChatWithOwnData.ts` file.

```typescript
```

1. Build the application with the following command:

    ```console
    tsc
    ```

1. Run the application with the following command:

    ```console
    node ChatWithOwnData.js
    ```

#### [JavaScript](#tab/javascript)

1. Open a command prompt where you want the new project, and create a new file named `ChatWithOwnData.js`. Copy the following code into the `ChatWithOwnData.js` file.

```javascript
```

1. Run the application with the following command:

    ```console
    node ChatWithOwnData.js
    ```

```

> [!IMPORTANT]
> For production, use a secure way of storing and accessing your credentials like [Azure Key Vault](/azure/key-vault/general/overview). For more information about credential security, see the Azure AI services [security](../../security-features.md) article.


## Output

```output
Message: What are my available health plans?
The available health plans in the Contoso Electronics plan and benefit packages are the Northwind Health Plus and Northwind Standard plans.

```

> [!div class="nextstepaction"]
> [I ran into an issue when running the code sample.](https://microsoft.qualtrics.com/jfe/form/SV_0Cl5zkG3CnDjq6O?PLanguage=JAVASCRIPT&Pillar=AOAI&Product=ownData&Page=quickstart&Section=Create-application)
