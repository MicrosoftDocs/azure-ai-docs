---
title: include file
description: include file
author: sdgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 04/24/2025
ms.author: sgilley
ms.custom: include file, build-2024
---

1. Install azure-identity: `pip install azure-identity`. If in a notebook cell, use `%pip install azure-identity`.
1. Provide your subscription details:

    ```python
    from azure.identity import DefaultAzureCredential
    from azure.mgmt.cognitiveservices import CognitiveServicesManagementClient
    import os
    import json
    
    sub_id = 'your-sub'
    rgp = 'your-rgp'
    account_name = 'your-account'
    project_name = 'your-project'
    location = 'westus'
    storage_connection_name = 'your-storage-connection-name'
    ```
    

1. Get a handle to the subscription. All the Python code in this article uses `client`:

    ```python
    client = CognitiveServicesManagementClient(
        credential=DefaultAzureCredential(), 
        subscription_id=sub_id,
        api_version="2025-04-01-preview"
    )`
    ```

    
1. (Optional) If you have multiple accounts, add the tenant ID of the Microsoft Entra ID you wish to use into the `DefaultAzureCredential`. Find your tenant ID from the [Azure portal](https://portal.azure.com) under **Microsoft Entra ID, External Identities**.
        
    ```python
    DefaultAzureCredential(interactive_browser_tenant_id="<TENANT_ID>")
    ```
        
1. (Optional) If you're working on in the [Azure Government - US](/azure/azure-government/documentation-government-welcome) or [Azure China 21Vianet](https://azure.microsoft.com/global-infrastructure/services/?regions=china-east-2%2cchina-non-regional&products=all) regions, specify the region into which you want to authenticate. You can specify the region with `DefaultAzureCredential`. The following example authenticates to the Azure Government - US region:
        
    ```python
    from azure.identity import AzureAuthorityHosts
    DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
    ```
