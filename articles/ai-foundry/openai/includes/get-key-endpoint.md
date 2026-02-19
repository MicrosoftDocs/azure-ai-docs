---
title: 'Get the key and endpoint'
titleSuffix: Azure OpenAI in Microsoft Foundry Models
description: To successfully make a call against Azure OpenAI, you need an endpoint and a key.
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: include
ms.date: 08/28/2023
---



### Retrieve key and endpoint

To successfully make a call against Azure OpenAI, you need an **endpoint** and a **key**.

|Variable name | Value |
|--------------------------|-------------|
| `ENDPOINT`    | The service endpoint can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. Alternatively, you can find the endpoint via the **Deployments** page in Microsoft Foundry portal. An example endpoint is: `https://docs-test-001.openai.azure.com/`. |
| `API-KEY` | This value can be found in the **Keys & Endpoint** section when examining your resource from the Azure portal. You can use either `KEY1` or `KEY2`.|

Go to your resource in the Azure portal. The **Keys & Endpoint** section can be found in the **Resource Management** section. Copy your endpoint and access key as you'll need both for authenticating your API calls. You can use either `KEY1` or `KEY2`. Always having two keys allows you to securely rotate and regenerate keys without causing a service disruption.

:::image type="content" source="../media/quickstarts/endpoint.png" alt-text="Screenshot of the overview UI for an Azure OpenAI resource in the Azure portal with the endpoint and access keys location circled in red." lightbox="../media/quickstarts/endpoint.png":::