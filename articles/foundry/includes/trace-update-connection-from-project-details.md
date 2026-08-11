---
title: Include file
description: Include file
author: lgayhardt
ms.reviewer: anksing
ms.author: lagayhar
ms.service: microsoft-foundry
ms.topic: include
ms.date: 07/29/2026
ms.custom: include
ai-usage: ai-assisted
---

If your project already has a connection to Application Insights and you want to convert it to use Microsoft Entra authentication, follow these steps. If you don't have an existing connection, skip to [Create a new connection](#create-a-new-connection).

1. Select **Manage** in the upper-right navigation, and then select **Project details**.
   :::image type="content" source="../media/observability/tracing/project-details-connection-update.png" alt-text="Screenshot of the project name menu showing the Project details option highlighted." lightbox="../media/observability/tracing/project-details-connection-update.png":::
1. Select the existing Application Insights connection, and then select **Edit authentication**.
   :::image type="content" source="../media/observability/tracing/project-details-connection-update-authentication.png" alt-text="Screenshot of an Application Insights connection with the Edit authentication option highlighted." lightbox="../media/observability/tracing/project-details-connection-update-authentication.png":::
1. Select **Project managed identity**, and then select **Save**.
   :::image type="content" source="../media/observability/tracing/project-details-connection-update-authentication-identity.png" alt-text="Screenshot of the Edit authentication pane with Project managed identity selected and the Save button highlighted." lightbox="../media/observability/tracing/project-details-connection-update-authentication-identity.png":::
