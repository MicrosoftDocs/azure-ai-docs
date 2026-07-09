---
title: "Set Up Private Outbound Connectivity"
titleSuffix: Foundry IQ
description: Configure private outbound dependencies from Azure AI Search for private agentic retrieval with Foundry IQ.
manager: mcleans
ms.service: microsoft-foundry
ms.subservice: foundry-agent-service
ms.topic: tutorial
ms.date: 06/26/2026
author: haileytap
ms.author: haileytapia
ms.reviewer: magottei
ms.custom: doc-kit-assisted
ai-usage: ai-assisted
#customer intent: As a platform engineer, I want to configure outbound private connectivity from Azure AI Search to its dependencies so that Foundry IQ agentic retrieval works end-to-end over private network paths.
---

# Set up private outbound connectivity

> [!IMPORTANT]
> This tutorial series uses the 2026-05-01-preview REST API for agentic retrieval. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

This article is part two of a three-part tutorial series. In this part of the tutorial, you create outbound shared private links from Azure AI Search to Azure Blob Storage and Microsoft Foundry, approve the corresponding private endpoint connections, and grant the Azure AI Search managed identity the roles it needs to read blob content and call model endpoints. End-to-end validation of the full retrieval path occurs in part three.

## Prerequisites

- Completion of [Set up private inbound connectivity](foundry-iq-tutorial-private-inbound.md).

- Additional account access for part two actions:

  - `Contributor` or `Owner` on the Azure AI Search service to create shared private links.

  - `Contributor` or `Owner` on the Azure Storage account and Foundry resource to approve target-side private endpoint connections.
  
  - `Owner`, `User Access Administrator`, or `Role Based Access Control Administrator` at scopes where you create role assignments to grant runtime access to the search managed identity.

- [Role-based access control](/azure/search/search-security-enable-roles) and a [system-assigned managed identity](/azure/search/search-how-to-managed-identities) enabled on the Azure AI Search service.

## Create shared private links

Create shared private links on Azure AI Search so the search service can initiate the required outbound access to each target. In part three of the tutorial, you create a knowledge source that reads blob content from the Azure Storage account and calls an embedding model deployment on the Foundry resource to vectorize that content. The blob read uses the Azure Storage shared private link. The Foundry shared private link is still required for the target resource relationship, but the ingestion-time embedding call described in part three currently also relies on the Foundry resource's trusted-service bypass.

> [!TIP]
> For applicable commands in this article, replace the `<...-name>` placeholders and `<subscription-id>` with the resource names and subscription ID you recorded in part one.

To create the shared private links:

1. Review existing shared private links.

   ```azurecli
   az search shared-private-link-resource list \
     --service-name <search-service-name> \
     --resource-group rg-private-retrieval
   ```

1. Create the Azure Blob Storage shared private link.

   ```azurecli
   az search shared-private-link-resource create \
     --name spl-blob-private-retrieval \
     --service-name <search-service-name> \
     --resource-group rg-private-retrieval \
     --group-id blob \
     --resource-id "/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Storage/storageAccounts/<storage-account-name>" \
     --request-message "Approve private blob access for Azure AI Search"
   ```

1. Create the Foundry resource shared private link.

   ```azurecli
   az rest --method put \
     --uri "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Search/searchServices/<search-service-name>/sharedPrivateLinkResources/spl-foundry-private-retrieval?api-version=2025-05-01" \
     --body '{
       "properties": {
         "groupId": "openai_account",
         "privateLinkResourceId": "/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>",
        "requestMessage": "Approve private model access for Azure AI Search"
       }
     }'
   ```

   > [!NOTE]
   > - The `az search shared-private-link-resource create` command can reject `openai_account`, even when the search service accepts the resource through the Search Management REST API. Use the `az rest` approach shown here to avoid validation errors.
   >
   > - This shared private link uses `openai_account` because Azure AI Search reaches model inference on the Foundry resource through the Azure OpenAI endpoint type.

> [!IMPORTANT]
> Leave the Foundry resource's **Allow Azure services on the trusted services list** setting enabled for this tutorial. The `openai_account` shared private link doesn't currently carry the ingestion-time embedding call from Azure AI Search to Foundry. If you disable the trusted-service bypass (`networkAcls.bypass = AzureServices`), knowledge source ingestion can fail with `403 Public access is disabled`, even when the shared private link and private endpoints are approved.

## Approve private endpoint connections

Shared private links define intent, but target-side approvals establish the trust boundaries that allow traffic to flow. In this section, you approve each corresponding private endpoint connection on Azure Storage and Foundry to authorize outbound access.

To approve the private endpoint connection for each target resource:

1. List private endpoint connections on `<storage-account-name>`, and then copy the name of the `Pending` connection to use as `<storage-connection-name>` in the next step.

   ```azurecli
   az network private-endpoint-connection list \
     --id /subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Storage/storageAccounts/<storage-account-name> \
     --query "[].{name:name,status:properties.privateLinkServiceConnectionState.status}" \
     -o table
   ```

1. Approve the Azure Blob Storage private endpoint connection.

   ```azurecli
   az network private-endpoint-connection approve \
     --id /subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Storage/storageAccounts/<storage-account-name>/privateEndpointConnections/<storage-connection-name>
   ```

1. List private endpoint connections on `<foundry-resource-name>`, and then copy the name of the `Pending` connection to use as `<foundry-connection-name>` in the next step.

    This connection can take a minute or two to appear after you create the shared private link, so if the list is empty, wait briefly, and then run the command again.

   ```azurecli
   az network private-endpoint-connection list \
     --id /subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name> \
     --query "[].{name:name,status:properties.privateLinkServiceConnectionState.status}" \
     -o table
   ```

1. Approve the Foundry resource private endpoint connection.

    If the connection name is returned in the `<foundry-resource-name>/<connection-name>` format, use only the portion after the slash as `<foundry-connection-name>`.

   ```azurecli
   az network private-endpoint-connection approve \
     --id /subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>/privateEndpointConnections/<foundry-connection-name>
   ```

1. Verify that the specific shared private links you created on Azure AI Search have an `Approved` state.

   ```azurecli
   az search shared-private-link-resource list \
     --service-name <search-service-name> \
     --resource-group rg-private-retrieval \
     --query "[].{name:name,status:properties.status}" \
     -o table
   ```

    The rows for `spl-blob-private-retrieval` and `spl-foundry-private-retrieval` should show `Approved`.

## Assign managed identity roles

After you approve private links, assign RBAC roles to the Azure AI Search managed identity so runtime calls in part three of the tutorial can access blob content and model endpoints. Private networking controls path access, while RBAC controls data and model authorization.

To assign roles to the Azure AI Search managed identity:

1. Get the Azure AI Search managed identity's object ID to use as `<search-mi-object-id>` in the following commands.

   ```azurecli
   az search service show \
     --name <search-service-name> \
     --resource-group rg-private-retrieval \
     --query identity.principalId \
     -o tsv
   ```

1. Assign the `Storage Blob Data Reader` role to the Azure AI Search managed identity at the storage account scope.

   This role is required so Azure AI Search can read blob content during ingestion and retrieval.

   ```azurecli
   az role assignment create \
     --assignee-object-id <search-mi-object-id> \
     --assignee-principal-type ServicePrincipal \
     --role "Storage Blob Data Reader" \
     --scope "/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Storage/storageAccounts/<storage-account-name>"
   ```

1. Assign the `Cognitive Services User` role to the Azure AI Search managed identity at the Foundry resource scope.

   This role is required so Azure AI Search can call model inference endpoints on the Foundry resource.

   ```azurecli
   az role assignment create \
     --assignee-object-id <search-mi-object-id> \
     --assignee-principal-type ServicePrincipal \
     --role "Cognitive Services User" \
     --scope "/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>"
   ```

1. Verify that both role assignments were created successfully.

   ```azurecli
   az role assignment list \
     --assignee-object-id <search-mi-object-id> \
     --query "[].{role:roleDefinitionName,scope:scope}" \
     -o table
   ```

   You should see the `Storage Blob Data Reader` and `Cognitive Services User` roles listed.

## Troubleshooting

Outbound private retrieval works only when shared private link creation, target approval, and RBAC authorization align. Use the following table to isolate which control layer is failing so you can correct the specific dependency boundary before end-to-end validation.

| Check or symptom | Likely issue | What to do next |
| --- | --- | --- |
| Shared private link status stays `Pending` | The private endpoint connection isn't approved on the target resource. | Approve the connection on Azure Storage or the Foundry resource, and then recheck the shared private link status. |
| Shared private link creation fails | Incorrect resource ID, group ID, or API version. | Recheck the resource ID and group ID. For the Foundry link, confirm the `openai_account` group ID and the `2025-05-01` API version. |
| `az role assignment create` fails with an authorization error | Your account lacks permission to create role assignments at the target scope. | Verify your account has `Owner`, `User Access Administrator`, or `Role Based Access Control Administrator` at the Azure Storage account and Foundry resource scopes. |

## Learn more

For more information about the topics covered in this part of the tutorial, see the following articles:

- [Make outbound connections through a shared private link](/azure/search/search-indexer-howto-access-private)
- [Manage Azure private endpoints](/azure/private-link/manage-private-endpoint)
- [Configure a search service to use managed identities](/azure/search/search-how-to-managed-identities)
- [Connect to Azure AI Search using Azure roles](/azure/search/search-security-rbac)
- [Assign Azure roles using Azure CLI](/azure/role-based-access-control/role-assignments-cli)

## Next step

> [!div class="nextstepaction"]
> [Validate end-to-end private agentic retrieval](foundry-iq-tutorial-private-retrieval.md)
