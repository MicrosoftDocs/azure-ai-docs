---
title: Rotate keys in Foundry Tools
titleSuffix: Foundry Tools
description: "Learn how to rotate API keys for better security, without interrupting service"
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-services
ms.custom:
  - ignite-2023
ms.topic: how-to
ms.date: 10/02/2025
ms.author: pafarley
---

# Rotate API keys

Each resource has two API keys to enable secret rotation. This is a security precaution that lets you regularly change the keys that can be used to access your service, protecting the privacy of your resource if a key gets leaked.

## How to rotate keys

You can rotate keys using the following procedure:
 
1. If you're using both keys in production, change your code so that only one key is in use. In this guide, assume it's key 1.

   This is a necessary step because once a key is regenerated, the older version of that key stops working immediately. This would cause clients using the older key to get `401 access denied` errors.
1. Once you have only key 1 in use, you can regenerate key 2. Go to your resource's page on the Azure portal, select the **Keys and Endpoint** tab, and select the **Regenerate Key 2** button at the top of the page.
1. Next, update your code to use the newly generated key 2.

   It helps to have logs or availability to check that users of the key have successfully swapped from using key 1 to key 2 before you proceed.
1. Now you can regenerate key 1 using the same process.
1. Finally, update your code to use the new key 1. 

## See also

* [Configure key-less authentication](../ai-foundry/foundry-models/how-to/configure-entra-id.md)
