---
title: Understand Liveness Client-side SDK versions 
titleSuffix: Azure AI services
description: Explains the importance of updating the Liveness SDK for security and reliability, detailing versioning and update policies
author: JinyuID
ms.author: lijiny
manager: qingflin
ms.service: azure-ai-vision
ms.date: 01/15/2025
ms.topic: reference
---

# Understand the Liveness Client-side SDK versions

Microsoft regularly upgrades the liveness detection client SDK and service to improve security, reliability, and user convenience. Staying current with these updates is crucial because the liveness detection field faces active and sophisticated attacks.

## Client-side SDK Versions

Liveness detection client-side SDK uses major.minor.patch format to indicate software version.   
- A patch version update is an optional reliability fix on the client SDK that doesn't affect compatibility with the service.
- A minor version update is important security and reliability improvement. We'll try to extend support for  a minor update as long as possible, Azure service might announce retirement of minor update after six months
- A major version update is critical security or breaking API updates. Customers should make client update as soon as possible. Azure service will block the previous major version after six months.    

## Azure Face API Service Version

Face liveness detection feature is generally available from version 1.2. Face API follows the Azure development cycle where newer API versions add new features during the preview release before becoming generally available. A newer service version might require a newer minimal client SDK version. The requirement is announced when new service version is available.

## Service Model Version

In the "Create Liveness Session" operation, customers can specify a liveness model version to classify the session. Azure service is also progressively updating  new models. We strongly recommend customers always use the latest model version, which means simply leaving the model version parameter empty.
- The latest model version (default version) remains compatible with all supported client versions.
- Azure announces the retirement of a service model six months in advance, giving customers buffer time to update their backend service.
