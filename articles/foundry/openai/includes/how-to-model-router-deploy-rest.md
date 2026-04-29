---
title: Include file
description: Include file
author: PatrickFarley
ms.reviewer: sgilley
ms.author: pafarley
ms.service: microsoft-foundry
ms.topic: include
ms.date: 04/28/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

> [!TIP]
> The REST API deployment path targets the Microsoft Foundry account resource directly and doesn't require a Foundry project. This makes it a good option for existing customers who deploy and manage Foundry models without a project association.

Deploy model router programmatically with the Azure Management REST API. The following example deploys model router with a routing mode and a custom model subset in a single request.

> [!NOTE]
> The deployment request body uses `format`, `name`, and `version` for the model router itself and for each model in the routing subset. Find the correct values for each model in the [Supported models](#supported-models) table.

:::code language="bash" source="~/foundry-samples-main/samples/REST/model-router/deploy-model-router-all-configs.sh" id="deploy_model_router_all_configs":::

> [!TIP]
> For the full runnable sample and other deployment options (routing mode only, model subset only), see the [Model Router REST samples](https://github.com/microsoft-foundry/foundry-samples/tree/main/samples/REST/model-router) in the foundry-samples repository.
