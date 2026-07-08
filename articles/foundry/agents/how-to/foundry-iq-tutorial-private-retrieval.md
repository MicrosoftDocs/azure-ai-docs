---
title: "Validate End-to-End Private Agentic Retrieval"
titleSuffix: Foundry IQ
description: Validate end-to-end private agentic retrieval with Foundry IQ by creating retrieval objects and confirming grounded, citation-backed responses.
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
#customer intent: As a platform engineer, I want to validate the final retrieval path from private content to grounded answers so that I can confirm the full private scenario before production rollout.
---

# Validate end-to-end private agentic retrieval

> [!IMPORTANT]
> These features and functionality are part of the 2026-05-01-preview REST API. The 2026-05-01-preview is licensed to you as part of your Azure subscription and is subject to the terms applicable to "Previews" in the [Microsoft Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage), the [Microsoft Products and Services Data Protection Addendum](https://www.microsoft.com/licensing/docs/view/Microsoft-Products-and-Services-Data-Protection-Addendum-DPA) ("DPA"), and the [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).
>
> The 2026-05-01-preview supports connections to other Microsoft services and third-party services. Use of these services is subject to their respective terms and might result in data processing or storage outside of the Azure compliance boundary, as well as data flowing into the Azure compliance boundary.
>
> The 2026-05-01-preview can't modify access permissions that were set outside of the 2026-05-01-preview. If you use the 2026-05-01-preview with access- or permission-restricted content, a timing lag occurs before the 2026-05-01-preview recognizes changes to those access or permission restrictions.
>
> It's your responsibility to manage whether your data flows outside of your organization's compliance and geographic boundaries and any related implications, and that appropriate permissions, boundaries, and approvals are provisioned.
>
> MCP implementations are susceptible to risks, such as attacks, cascading failures, and loss of human oversight. You can mitigate these risks by vetting MCP servers for security and reliability, following [Microsoft's recommended practices](/azure/api-management/secure-mcp-servers) and [industry best practices](https://modelcontextprotocol.io/specification/draft/basic/security_best_practices), and implementing approval mechanisms and monitoring cascading behaviors.
>
> You're responsible for carefully reviewing and testing applications you build in the context of your specific use cases and making all appropriate decisions and customizations. This responsibility includes implementing your own responsible AI mitigations, such as metaprompts, content filters, or other safety systems, and ensuring your applications meet appropriate quality, reliability, security, and trustworthiness standards. For more information, see the [Azure AI Search Transparency Note](/azure/foundry/responsible-ai/search/transparency-note).

This article is part three of a three-part tutorial series. In this part of the tutorial, you create a knowledge source and knowledge base, register the MCP endpoint as a project connection, and run a validation prompt through an agent to confirm grounded, cited responses from private content. At this point, the network, identity, and retrieval layers come together in the same runtime path.

## Prerequisites

- Completion of [Set up private inbound connectivity](foundry-iq-tutorial-private-inbound.md) and [Set up private outbound connectivity](foundry-iq-tutorial-private-outbound.md).

- `Owner`, `User Access Administrator`, or `Role Based Access Control Administrator` at scopes where you assign roles to your user account.

- Foundry model deployments for `text-embedding-3-large` and `gpt-4.1`. The template used in part one deploys `gpt-4.1`, but it doesn't deploy `text-embedding-3-large`. Deploy `text-embedding-3-large`, and then verify both deployments before you continue. For deployment instructions, see [Deploy Microsoft Foundry Models in the Foundry portal](/azure/foundry/foundry-models/how-to/deploy-foundry-models).

- [Visual Studio Code](https://code.visualstudio.com/download) with the [REST Client extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client).

- The same in-VNet client you used in part one, such as a jumpbox, VM, dev box, or Azure Bastion-connected workstation, connected to the private network path in your deployment and able to reach your private endpoints.

- The Foundry resource's **Allow Azure services on the trusted services list** setting remains enabled. Part two explains why knowledge source ingestion still depends on this bypass for the embedding call.

## Verify model deployments

Verify that your Foundry resource includes the deployments used later in this article.

1. List the model deployments on the Foundry resource.

   ```azurecli
   az cognitiveservices account deployment list \
      --name <foundry-resource-name> \
      --resource-group rg-private-retrieval \
      --query "[].{deployment:name,model:properties.model.name,status:properties.provisioningState}" \
      -o table
   ```

1. Confirm that `text-embedding-3-large` and `gpt-4.1` both appear with a `Succeeded` status.

   If `gpt-4.1` isn't deployed yet, deploy it before you create the agent later in this article.

## Assign user account roles

Part two of the tutorial grants runtime access to Azure AI Search. In this section, you grant your user account the permissions needed to upload sample content, create agentic retrieval objects, configure the project connection, and run agent operations.

> [!TIP]
> For applicable commands in this article, replace the `<...-name>` placeholders and `<subscription-id>` with the resource names and subscription ID you recorded in part one.

To assign the roles to your user account:

1. Get your account object ID to use as `<principal-object-id>` in the following commands.

    ```azurecli
    az ad signed-in-user show --query id -o tsv
    ```

1. Assign a role on the Azure Storage account scope.

   `Storage Blob Data Contributor` is required to create the blob container and upload the sample content in the next section.

    ```azurecli
    az role assignment create \
       --assignee-object-id <principal-object-id> \
       --assignee-principal-type User \
       --role "Storage Blob Data Contributor" \
       --scope "/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Storage/storageAccounts/<storage-account-name>"
    ```

1. Assign roles on the Azure AI Search service scope.

   `Search Service Contributor` is required to manage the knowledge source and knowledge base. `Search Index Data Contributor` is required for knowledge base retrieval during validation.

    ```azurecli
    az role assignment create \
       --assignee-object-id <principal-object-id> \
       --assignee-principal-type User \
       --role "Search Service Contributor" \
       --scope "/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Search/searchServices/<search-service-name>"

    az role assignment create \
       --assignee-object-id <principal-object-id> \
       --assignee-principal-type User \
       --role "Search Index Data Contributor" \
       --scope "/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Search/searchServices/<search-service-name>"
    ```

1. Assign roles on the Foundry resource scope.

   `Foundry Project Manager` is required to create the project connection. `Foundry User` is required to create the agent and run the validation conversation in the Foundry project.

    [!INCLUDE [role-rename-note](../../includes/role-rename-note.md)]

    ```azurecli
    az role assignment create \
       --assignee-object-id <principal-object-id> \
       --assignee-principal-type User \
       --role "Foundry Project Manager" \
       --scope "/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>"

    az role assignment create \
       --assignee-object-id <principal-object-id> \
       --assignee-principal-type User \
       --role "Foundry User" \
       --scope "/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>"
    ```

1. Verify role assignments.

    ```azurecli
    az role assignment list \
       --assignee-object-id <principal-object-id> \
       --query "[].{role:roleDefinitionName,scope:scope}" \
       -o table
    ```

    You should see `Search Service Contributor`, `Search Index Data Contributor`, `Foundry Project Manager`, `Foundry User`, and `Storage Blob Data Contributor` at the expected scopes.

## Upload sample content

Upload sample JSON documents to a container in Azure Blob Storage. The validation prompt later in this article grounds its answers in this blob content, so the documents must be in place before the knowledge source ingests them.

> [!IMPORTANT]
> Run the commands and REST calls in the rest of this article from your in-VNet client. Several steps reach private endpoints on Azure Blob Storage, Azure AI Search, and Foundry, including the upload commands in this section. Because part one disables public network access on these services, these steps succeed only over the private network path.

To upload the sample content:

1. Download the [sample JSON documents](https://github.com/Azure-Samples/azure-search-sample-data/tree/main/nasa-e-book/earth-at-night-json) to your in-VNet client.

    ```bash
    git clone --depth 1 https://github.com/Azure-Samples/azure-search-sample-data.git
    ```

1. Create the `earth-at-night-json` blob container.

    ```azurecli
    az storage container create \
       --name earth-at-night-json \
       --account-name <storage-account-name> \
       --auth-mode login
    ```

1. Split the sample file into one blob per record.

   The downloaded sample stores all records in one `documents.json` file. Uploading that file as a single blob can delay or stall ingestion, so split it before you upload.

   ```bash
   mkdir -p earth-at-night-split
   python - <<'PY'
   import json
   from pathlib import Path

   source = Path("azure-search-sample-data/nasa-e-book/earth-at-night-json/documents.json")
   target = Path("earth-at-night-split")
   target.mkdir(exist_ok=True)

   for doc in json.loads(source.read_text()):
       (target / f"{doc['id']}.json").write_text(json.dumps(doc))
   PY
   ```

   If Python isn't available on your in-VNet client, use another JSON-aware tool to create one blob per record before you continue.

1. Upload the split sample documents to the container.

    ```azurecli
    az storage blob upload-batch \
       --destination earth-at-night-json \
       --source earth-at-night-split \
       --account-name <storage-account-name> \
       --auth-mode login
    ```

1. Verify that the documents uploaded successfully.

    ```azurecli
    az storage blob list \
       --container-name earth-at-night-json \
       --account-name <storage-account-name> \
       --auth-mode login \
       --query "[].name" -o tsv
    ```

    The output lists the JSON files from the Earth at Night sample set. These per-record blobs become the private content that the knowledge source ingests in the next section.

## Create a knowledge source and knowledge base

In Azure AI Search, agentic retrieval involves two objects: a knowledge source and a knowledge base. This section creates a blob knowledge source, which generates an ingestion pipeline that chunks your private blob content, uses your deployed `text-embedding-3-large` model for vectorization, and stores the enriched content in a search index. The knowledge base then orchestrates retrieval from the knowledge source and exposes results through an MCP endpoint, which becomes the target that the agent calls in a later section.

To create the knowledge source and knowledge base:

1. Get an Azure AI Search bearer token to use as `<search-access-token>` in the following requests.

   ```azurecli
   az account get-access-token --scope https://search.azure.com/.default --query accessToken -o tsv
   ```

1. Open Visual Studio Code and create a file named `private-agentic-retrieval.rest`.

1. Create a blob knowledge source.

    ```http
   PUT https://<search-service-name>.search.windows.net/knowledgesources/ks-private-retrieval?api-version=2026-05-01-preview
    Authorization: Bearer <search-access-token>
    Content-Type: application/json

    {
      "name": "ks-private-retrieval",
       "kind": "azureBlob",
       "description": "Private blob-backed knowledge source for tutorial content.",
       "azureBlobParameters": {
          "connectionString": "ResourceId=/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.Storage/storageAccounts/<storage-account-name>;",
          "containerName": "earth-at-night-json",
          "isADLSGen2": false,
          "ingestionParameters": {
             "embeddingModel": {
                "kind": "azureOpenAI",
                "azureOpenAIParameters": {
                   "resourceUri": "https://<foundry-resource-name>.openai.azure.com/",
                   "deploymentId": "text-embedding-3-large",
                   "modelName": "text-embedding-3-large"
                }
             },
             "contentExtractionMode": "minimal",
             "disableImageVerbalization": true
          }
       }
    }
    ```

1. Create a knowledge base that references the knowledge source.

    ```http
   PUT https://<search-service-name>.search.windows.net/knowledgebases/kb-private-retrieval?api-version=2026-05-01-preview
    Authorization: Bearer <search-access-token>
    Content-Type: application/json

    {
      "name": "kb-private-retrieval",
       "description": "Knowledge base grounded in private blob tutorial content.",
       "knowledgeSources": [
          {
             "name": "ks-private-retrieval"
          }
       ],
       "outputMode": "extractiveData",
       "retrievalReasoningEffort": {
          "kind": "minimal"
       }
    }
    ```

1. Confirm the knowledge source was created successfully.

   ```http
   GET https://<search-service-name>.search.windows.net/knowledgesources/ks-private-retrieval?api-version=2026-05-01-preview
   Authorization: Bearer <search-access-token>
   ```

   This request should return HTTP 200. The response payload should include `"name": "ks-private-retrieval"`.

1. Confirm the knowledge base was created successfully.

   ```http
   GET https://<search-service-name>.search.windows.net/knowledgebases/kb-private-retrieval?api-version=2026-05-01-preview
   Authorization: Bearer <search-access-token>
   ```

   This request should return HTTP 200. The response payload should include `"name": "kb-private-retrieval"` and list `"name": "ks-private-retrieval"` under `knowledgeSources`.

    > [!NOTE]
    > Creating the knowledge source starts asynchronous ingestion of your blob content. First-time ingestion can take several minutes to complete. Re-run the knowledge source and knowledge base `GET` requests in this section before you create the agent, and confirm they still return HTTP 200. If you run the validation prompt too early, the response can fail before citations appear. Wait 30 to 60 seconds, and then retry. If ingestion stalls, verify that you uploaded split per-record blobs instead of a single large `documents.json` file, and confirm that the Foundry trusted-service bypass described in part two is still enabled.
    
## Create a project connection

Register the knowledge base MCP endpoint as a project connection in Foundry. This connection lets the agent call the MCP endpoint by using the project managed identity instead of embedded secrets. When you finish this section, you have a reusable connection name that the agent definition references.

To create the project connection:

1. Get an Azure Resource Manager token to use as `<management-access-token>` in the following requests.

    ```azurecli
    az account get-access-token --scope https://management.azure.com/.default --query accessToken -o tsv
    ```

1. Get your project resource ID to use as `<project-resource-id>` in the following requests.

    ```azurecli
    az rest --method get \
      --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>/projects?api-version=2025-10-01-preview" \
      --query "value[0].id" -o tsv
    ```

1. Create the project connection by using Azure Resource Manager.

    ```http
   PUT https://management.azure.com/<project-resource-id>/connections/conn-kb-private-retrieval?api-version=2025-10-01-preview
    Authorization: Bearer <management-access-token>
    Content-Type: application/json

    {
      "name": "conn-kb-private-retrieval",
       "type": "Microsoft.MachineLearningServices/workspaces/connections",
       "properties": {
          "authType": "ProjectManagedIdentity",
          "category": "RemoteTool",
          "target": "https://<search-service-name>.search.windows.net/knowledgebases/kb-private-retrieval/mcp?api-version=2026-05-01-preview",
          "isSharedToAll": true,
          "audience": "https://search.azure.com/",
          "metadata": {
             "ApiType": "Azure"
          }
       }
    }
    ```

1. Confirm the connection was created.

    ```http
   GET https://management.azure.com/<project-resource-id>/connections/conn-kb-private-retrieval?api-version=2025-10-01-preview
    Authorization: Bearer <management-access-token>
    ```

   This request returns HTTP 200. Verify `authType` is `ProjectManagedIdentity`, `target` matches your knowledge base MCP URL, and `name` is `conn-kb-private-retrieval`. You must grant `ProjectManagedIdentity` authorization access to your Azure AI Search service using the "Search Index Data Reader" (and "Search Index Data Contributor" if write access is needed) roles. For help, see [Create a project connection](/azure/foundry/agents/how-to/foundry-iq-connect#create-a-project-connection).

## Create an agent and validate citations

Create an agent that uses the project connection to call the knowledge base MCP tool, and then run a validation prompt through a conversation. The goal is to confirm end-to-end retrieval behavior: the agent answers from private content and returns grounded citations instead of relying on general model knowledge.

To create the agent and validate citations:

1. Get a Foundry access token to use as `<foundry-access-token>` in the following requests.

    ```azurecli
    az account get-access-token --scope https://ai.azure.com/.default --query accessToken -o tsv
    ```

1. Get your project endpoint to use as `<project-endpoint>` in the following requests.

    ```azurecli
    az rest --method get \
      --url "https://management.azure.com/subscriptions/<subscription-id>/resourceGroups/rg-private-retrieval/providers/Microsoft.CognitiveServices/accounts/<foundry-resource-name>/projects?api-version=2025-10-01-preview" \
      --query "value[0].properties.endpoints.* | [0]" -o tsv
    ```

1. Create a prompt agent that uses your MCP connection.

    ```http
    POST <project-endpoint>/agents?api-version=v1
    Authorization: Bearer <foundry-access-token>
    Content-Type: application/json

    {
      "name": "agent-private-retrieval",
       "definition": {
          "model": "gpt-4.1",
          "instructions": "Use the knowledge base for every answer. Return grounded citations. If the answer is not in the knowledge base, say that you do not know.",
          "tools": [
             {
                "type": "mcp",
                "server_label": "knowledge-base",
                "server_url": "https://<search-service-name>.search.windows.net/knowledgebases/kb-private-retrieval/mcp?api-version=2026-05-01-preview",
                "project_connection_id": "conn-kb-private-retrieval",
                "require_approval": "never",
                "allowed_tools": ["knowledge_base_retrieve"]
             }
          ],
          "kind": "prompt"
       }
    }
    ```

1. Create a conversation, and then copy the `id` value from the response to use as `<conversation-id>` in the next step.

    ```http
    POST <project-endpoint>/openai/v1/conversations
    Authorization: Bearer <foundry-access-token>
    Content-Type: application/json

    {}
    ```

1. Run a validation prompt through the agent.

    ```http
    POST <project-endpoint>/openai/v1/responses
    Authorization: Bearer <foundry-access-token>
    Content-Type: application/json

    {
       "conversation": "<conversation-id>",
       "input": "Summarize the key findings from the Earth at Night sample documents and cite the source content.",
       "agent_reference": {
          "type": "agent_reference",
          "name": "agent-private-retrieval"
       }
    }
    ```

   Expected result:

	- The agent returns an answer that's grounded in your uploaded blob content.
   - The response includes citations that reference the Earth at Night source content.
   - The request succeeds from your private network client by using the same private path configured in parts one and two.

## Troubleshooting

Use the following table to isolate failures in the retrieval-validation flow.

| Check or symptom | Likely issue | What to do next |
| --- | --- | --- |
| `403` when creating the knowledge source or knowledge base | Azure AI Search authorization (caller or dependent resources) | Verify your caller has `Search Service Contributor` on the search service scope. Then verify Azure AI Search can reach Azure Blob Storage and Foundry endpoints over private links, and verify managed identity role assignments from part two. |
| `401` with `Failed to create or update Knowledge Source` and `Unable to retrieve blob container ... using your managed identity` | Azure AI Search runtime dependencies from part two are incomplete | Verify both shared private links show `Approved`, and verify the Azure AI Search managed identity has `Storage Blob Data Reader` on the storage account and `Cognitive Services User` on the Foundry resource. |
| `400` when creating the knowledge source or knowledge base | Invalid embedding model configuration | Verify the `resourceUri`, `deploymentId`, and `modelName` values for the `text-embedding-3-large` embedding model. |
| `403 Public access is disabled` during ingestion | The Foundry trusted-service bypass is disabled | Re-enable **Allow Azure services on the trusted services list** on the Foundry resource, and then retry ingestion. The `openai_account` shared private link doesn't currently replace this ingestion-time dependency. |
| `404` on the MCP endpoint URL | Incorrect knowledge base endpoint | Verify the MCP target is `https://<search-service-name>.search.windows.net/knowledgebases/kb-private-retrieval/mcp?api-version=2026-05-01-preview`. |
| `401` or `403` when creating the project connection | Azure Resource Manager authorization or token scope | Verify your caller identity can manage project connections on `<project-resource-id>`. Also verify you requested the token with `--scope https://management.azure.com/.default`. |
| `401` or `403` when the agent calls the MCP tool | Project managed identity doesn't have the required Search data-plane access, or the role assignment hasn't propagated yet | Verify the project managed identity for the connection has the required Search data-plane role on the Azure AI Search service, and then wait briefly for role propagation before you retry the validation prompt. |
| Agent returns an answer without citations | Agent tool wiring, instructions, or retrieval data availability | Verify the agent includes the MCP tool, `allowed_tools` contains `knowledge_base_retrieve`, and your instructions require grounded citations. Also verify the knowledge base contains retrievable content from `earth-at-night-json`. |

## Clean up resources

When you work in your own subscription, it's a good idea to finish a project by removing the resources you no longer need. Resources that are left running can cost you money.

This tutorial used a dedicated resource group named `rg-private-retrieval`. If you no longer need the resource group, delete it:

```bash
az group delete \
   --name rg-private-retrieval \
   --yes \
   --no-wait
```

## Learn more

For more information about the topics covered in this part of the tutorial, see the following articles:

- [Assign Azure roles using Azure CLI](/azure/role-based-access-control/role-assignments-cli)
- [Create a blob knowledge source from Azure Blob Storage or ADLS Gen2](/azure/search/agentic-knowledge-source-how-to-blob)
- [Create a knowledge base](/azure/search/agentic-retrieval-how-to-create-knowledge-base)
- [Add a new connection to your project](/azure/foundry/how-to/connections-add)
- [Quickstart: Create a prompt agent](/azure/foundry/agents/quickstarts/prompt-agent)
- [Connect a Foundry IQ knowledge base to Foundry Agent Service](/azure/foundry/agents/how-to/foundry-iq-connect)
