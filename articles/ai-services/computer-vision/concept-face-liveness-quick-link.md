---
title: "Face liveness quick link - Face"
titleSuffix: Azure AI services
description: This article explains the concept of Face liveness quick link, its usage flow, and related concepts. 
author: JinyuID
manager: nitinme

ms.service: azure-ai-vision
ms.subservice: azure-ai-face
ms.custom:
ms.topic: conceptual
ms.date: 05/15/2025
ms.author: pafarley
feedback_help_link_url: https://learn.microsoft.com/answers/tags/156/azure-face
---

# Face Liveness Quick Link (Preview)

This article explains the concept of Face liveness quick link, its usage flow, and related concepts.

## Introduction

Azure Liveness Quick Link is an optional integration path for [Face liveness detection](concept-face-liveness-detection.md). It exchanges a liveness session’s session-authorization-token for a single use URL that hosts the capture experience on an Azure operated page. After finishing the operation, the service returns to a developer supplied callback endpoint. 
Azure Liveness Quick Link provides multiple benefits to customers: 
- No need to embed the liveness client SDK. Easier integration in application side.
- No need to keep track of liveness client SDK updates. Azure operated websites always use the latest and greatest version of liveness detection.

## How it works

You can utilize the liveness quick link website liveness.face.azure.com to turn a liveness session into a shareable, single use link:

:::image type="content" source="media/liveness/liveness-quick-link-diagram.png" alt-text="A diagram illustrates liveness quick link work flow":::

1.	Start a session server side. Your backend asks Face API for a new liveness session and receives a short lived authorization token that represents that session.
2.	Swap the token for a link. Your backend sends the token to the Quick Link service, which creates a one time URL tied to the session.
3.	Send the link to the user. You can redirect the browser, show a button, or display a QR code—anything that gets the user to open the link on a camera enabled device.
4.	Azure hosts the capture. When the link opens, the Azure operated page guides the user through the liveness check sequence using the latest Liveness Web Client.
5.	Get the outcome callback. As soon as the check finishes—or if the user abandons or times out—Quick Link notify to your callback endpoint so your application can decide what happens next.
