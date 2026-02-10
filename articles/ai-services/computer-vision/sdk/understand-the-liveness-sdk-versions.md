---
title: Understand liveness client-side SDK versions 
titleSuffix: Foundry Tools
description: Explains the importance of updating the Liveness SDK for security and reliability, detailing versioning and update policies
author: PatrickFarley
ms.author: pafarley
manager: qingflin
ms.service: azure-ai-vision
ms.date: 09/26/2025
ms.topic: concept-article
---

# Understand the liveness versions

Microsoft regularly updates the liveness detection client SDK and service to improve security, reliability, and user convenience. It's important to stay current with these updates because the liveness detection field faces active and sophisticated attacks.

## Client-side SDK version numbers

Liveness detection client-side SDKs use `major.minor.patch` format to indicate the software version.
- A patch version update is an optional reliability fix to the client SDK that doesn't affect compatibility with the service.
- A minor version update is an important security and reliability improvement. We try to extend support for a minor update as long as possible, and Azure announces the retirement of a minor update six months in advance.
- A major version update is a critical security or breaking API update. Customers should update their application as soon as possible. Azure service will block the previous major version after six months.

## Azure Face API version development pattern

The Face liveness detection feature is generally available from version `1.2`. Face API follows the Azure development cycle in which newer API versions add new features during the preview release before becoming generally available. A newer service version might require a newer minimal client SDK version. The requirement is announced when a new service version is available.

## Service model version

In the **Create Liveness Session** operation, customers can specify a liveness model version to use within the session. Azure Face service continually adds or updates models. We strongly recommend customers always use the latest model version, which entails leaving the `model-version` parameter empty in API calls.
- The latest model version (default) remains compatible with all supported client versions.
- Azure announces the retirement of a service model six months in advance, giving customers time to update their backend service.
