---
title: include file
description: include file
author: sdgilley
ms.service: azure-ai-foundry
ms.topic: include
ms.date: 5/21/2024
ms.author: sgilley
ms.custom: include file, build-2024
---

1. Install packages.  (If in a notebook cell, use `%pip install` instead.)

    ```bash
    pip install azure-ai-ml
    pip install azure-identity
    ```

1. Provide your subscription details:

    [!notebook-python[](~/azureml-examples-main/sdk/python/resources/workspace/workspace.ipynb?name=subscription_id)]

1. Get a handle to the subscription. All the Python code in this article uses `ml_client`:

    [!notebook-python[](~/azureml-examples-main/sdk/python/resources/workspace/workspace.ipynb?name=ml_client)]
    
1. (Optional) If you have multiple accounts, add the tenant ID of the Microsoft Entra ID you wish to use into the `DefaultAzureCredential`. Find your tenant ID from the [Azure portal](https://portal.azure.com) under **Microsoft Entra ID, External Identities**.
        
    ```python
    DefaultAzureCredential(interactive_browser_tenant_id="<TENANT_ID>")
    ```
        
1. (Optional) If you're working on in the [Azure Government - US](/azure/azure-government/documentation-government-welcome) or [Azure China 21Vianet](https://azure.microsoft.com/global-infrastructure/services/?regions=china-east-2%2cchina-non-regional&products=all) regions, specify the region into which you want to authenticate. You can specify the region with `DefaultAzureCredential`. The following example authenticates to the Azure Government - US region:
        
    ```python
    from azure.identity import AzureAuthorityHosts
    DefaultAzureCredential(authority=AzureAuthorityHosts.AZURE_GOVERNMENT)
    ```
1. Verify the connection.
    
    ```python
    for hub in ml_client.workspaces.list():
        print(f"  - {hub.name}")
    ```

If you receive an authentication error, ensure your Azure credentials are configured (run `az login` or set up your credentials via the Azure Identity SDK). If you receive a permission error, check that you have the Contributor role on the subscription or resource group.

**References**: [`MLClient`](/python/api/azure-ai-ml/azure.ai.ml.mlclient), [`DefaultAzureCredential`](/python/api/azure-identity/azure.identity.defaultazurecredential)
