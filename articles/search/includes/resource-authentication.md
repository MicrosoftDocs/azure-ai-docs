---
title: Include File
description: Include file for Azure AI Search authentication and role-based access configuration.
author: haileytap 
ms.author: haileytapia 
ms.service: azure-ai-search
ms.topic: include
ms.date: 02/02/2026
# Use this file to describe authentication for search-only, non-integrated scenarios. For managed identities, use resource-authentication-identity.md.
---

Before you begin, make sure you have permissions to access content and operations in Azure AI Search. This quickstart uses Microsoft Entra ID for authentication and role-based access for authorization. You must be an **Owner** or **User Access Administrator** to assign roles. If roles aren't feasible, use [key-based authentication](../search-security-api-keys.md) instead.

To configure the recommended role-based access:

1. [Enable role-based access](../search-security-enable-roles.md) for your search service.

1. [Assign the following roles](../search-security-rbac.md) to your user account.

    + **Search Service Contributor**

    + **Search Index Data Contributor**

    + **Search Index Data Reader**
