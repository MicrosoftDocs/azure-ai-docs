---
title: Gather required parameters
author: aahill
manager: nitinme
description: The parameters for all Azure AI containers.
ms.service: azure-ai-services
ms.topic: include 
ms.date: 04/01/2020
ms.author: aahi
ms.custom: sfi-image-nochange
---

## Gather required parameters

Three primary parameters for all Azure AI containers are required. The Microsoft Software License Terms must be present with a value of **accept**. An Endpoint URI and API key are also needed.

### Endpoint URI

The `{ENDPOINT_URI}` value is available on the Azure portal **Overview** page of the corresponding Foundry Tools resource. Go to the **Overview** page, hover over the endpoint, and a **Copy to clipboard** <span class="docon docon-edit-copy x-hidden-focus"></span> icon appears. Copy and use the endpoint where needed.

![Screenshot that shows gathering the endpoint URI for later use.](../media/overview-endpoint-uri.png)

### Keys

The `{API_KEY}` value is used to start the container and is available on the Azure portal's **Keys** page of the corresponding Foundry Tools resource. Go to the **Keys** page, and select the **Copy to clipboard** <span class="docon docon-edit-copy x-hidden-focus"></span> icon.

![Screenshot that shows getting one of the two keys for later use.](../media/keys-copy-api-key.png)

> [!IMPORTANT]
> These subscription keys are used to access your Foundry Tools API. Don't share your keys. Store them securely. For example, use Azure Key Vault. We also recommend that you regenerate these keys regularly. Only one key is necessary to make an API call. When you regenerate the first key, you can use the second key for continued access to the service.
