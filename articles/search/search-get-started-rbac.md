---
title: 'Quickstart: Keyless Connection'
titleSuffix: Azure AI Search
description: Learn how to use role-based access control (RBAC) to connect to an Azure AI Search service.
author: haileytap
ms.author: haileytapia
ms.service: azure-ai-search
ms.topic: quickstart
ms.date: 07/08/2025
zone_pivot_groups: search-get-started-rbac
---

# Quickstart: Connect to a search service

::: zone pivot="python"

[!INCLUDE [Python quickstart](includes/quickstarts/search-get-started-rbac-python.md)]

::: zone-end

::: zone pivot="rest"

[!INCLUDE [REST quickstart](includes/quickstarts/search-get-started-rbac-rest.md)]

::: zone-end

## Related content

+ [Configure a system- or user-assigned managed identity](search-howto-managed-identities-data-sources.md) for your search service.

+ [Use role assignments](keyless-connections.md) to authorize access to other Azure resources.

+ [Set inbound rules](service-configure-firewall.md) to accept or reject Azure AI Search requests based on IP address.
