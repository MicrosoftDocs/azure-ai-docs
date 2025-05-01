---
title: How to use local inference with the Personalizer SDK
description: Learn how to use local inference to improve latency.
author: jcodella
ms.author: jacodel
manager: nitinme
ms.service: azure-ai-personalizer
ms.topic: how-to
ms.date: 01/19/2024
---

# Get started with the local inference SDK for Azure AI Personalizer

[!INCLUDE [Deprecation announcement](includes/deprecation.md)]

The Personalizer local inference SDK (Preview) downloads the Personalizer model locally, and thus significantly reduces the latency of Rank calls by eliminating network calls. Every minute the client will download the most recent model in the background and use it for inference.

In this guide, you'll learn how to use the Personalizer local inference SDK.

[!INCLUDE [Try local inference with C#](./includes/quickstart-local-inference-csharp.md)]
