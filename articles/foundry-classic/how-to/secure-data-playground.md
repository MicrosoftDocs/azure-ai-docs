---
title: Securely use playground chat
titleSuffix: Microsoft Foundry
description: Learn how to securely use the Microsoft Foundry portal playground chat on your own data. 
ms.service: azure-ai-foundry
ms.custom:
  - hub-only
  - dev-focus
ms.topic: how-to
ms.date: 02/02/2026
ms.reviewer: meerakurup 
ms.author: jburchel 
author: jonburchel 
ai-usage: ai-assisted
# Customer intent: As an administrator, I want to make sure that my data is handled securely when used in the playground chat.
---

# Use your data securely with the Microsoft Foundry portal playground

[!INCLUDE [hub-only-alt](../includes/uses-hub-only-alt.md)]

Use this article to learn how to securely use [Microsoft Foundry](https://ai.azure.com/?cid=learnDocs)'s playground chat on your data. The following sections provide our recommended configuration to protect your data and resources by using Microsoft Entra ID role-based access control, a managed network, and private endpoints. Disable public network access for Azure OpenAI resources, Azure AI Search resources, and storage accounts. Using selected networks with IP rules isn't supported because the services' IP addresses are dynamic.

> [!NOTE]
> Foundry's managed virtual network settings apply only to Foundry's managed compute resources, not platform as a service (PaaS) services like Azure OpenAI or Azure AI Search. When you use PaaS services, there's no data exfiltration risk because Microsoft manages the services.

The following table summarizes the changes made in this article:

| Configurations | Default | Secure | Notes |
| ----- | ----- | ----- | ----- |
| Data sent between services | Sent over the public network | Sent through a private network | Data is sent encrypted by using HTTPS even over the public network. |
| Service authentication | API keys | Microsoft Entra ID | Anyone with the API key can authenticate to the service. Microsoft Entra ID provides more granular and robust authentication. |
| Service permissions | API Keys | Role-based access control | API keys provide full access to the service. Role-based access control provides granular access to the service. |
| Network access | Public | Private | Using a private network prevents entities outside the private network from accessing resources secured by it. |

## Prerequisites

### Account and roles

- **Azure Subscription**: You need an [Azure subscription](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn) to create resources.
- **Azure Roles**:
    - **Contributor** or **Owner** on the Resource Group to configure networking and resources.
    - **Cognitive Services OpenAI User** on the Azure OpenAI resource to run the verification code.
- **RBAC Knowledge**: Be familiar with using Microsoft Entra ID role-based access control to assign roles to resources and users. For more information, visit the [Role-based access control](/azure/role-based-access-control/overview) article.

### Foundry hub configuration

- **Foundry Hub**: Ensure that the Foundry hub is deployed with the **Identity-based access** setting for the Storage account. This configuration is required for the correct access control and security of your Foundry Hub. You can verify this configuration by using one of the following methods:
    - In the Azure portal, select the hub and then select **Settings**, **Properties**, and **Options**. At the bottom of the page, verify that **Storage account access type** is set to **Identity-based access**.
    - If deploying by using Azure Resource Manager or Bicep templates, include the `systemDatastoresAuthMode: 'identity'` property in your deployment template.

### Development environment

- **Python Environment**: To run the verification code, you need Python 3.8 or later with the following packages installed:
    - `openai` (version 1.0.0 or later)
    - `azure-identity`

### Network access

- **Network Access**: To run the verification code, you must have access to a machine within the virtual network (for example, an Azure VM) that has access to the private endpoints.

## Configure network isolated Foundry hub

If you're **creating a new Foundry hub**, use one of the following documents to create a hub with network isolation:

- [Create a secure Foundry hub in Azure portal](create-secure-ai-hub.md)
- [Create a secure Foundry hub using the Python SDK or Azure CLI](develop/create-hub-project-sdk.md)

If you have an **existing Foundry hub** that isn't configured to use a managed network, use the following steps to configure it to use one:

1. From the Azure portal, select the hub, then select **Settings**, **Networking**, **Public access**.
1. To disable public network access for the hub, set **Public network access** to **Disabled**. Select **Save** to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/hub-public-access-disable.png" alt-text="Screenshot of Foundry hub settings with public access disabled.":::

1. Select **Workspace managed outbound access** and then select either the **Allow Internet Outbound** or **Allow Only Approved Outbound** network isolation mode. Select **Save** to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/select-network-isolation-configuration.png" alt-text="Screenshot of the Foundry hub settings with allow internet outbound selected.":::

## Configure Foundry Tools resource

Depending on your configuration, you might use a Foundry Tools resource that also includes Azure OpenAI or a standalone Azure OpenAI resource. The steps in this section configure an AI services resource. The same steps apply to an Azure OpenAI resource.

1. If you don't have an existing Foundry Tools resource for your Foundry hub, [create one](/azure/ai-foundry/openai/how-to/create-resource?pivots=web-portal).
1. From the Azure portal, select the AI services resource, and then select **Resource Management**, **Identity**, and **System assigned**. 
1. To create a managed identity for the AI services resource, set the **Status** to **On**. Select **Save** to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-services-managed-identity.png" alt-text="Screenshot of setting the status of managed identity to on.":::

1. To disable public network access, select **Networking**, **Firewalls and virtual networks**, and then set **Allow access from** to **Disabled**. Under **Exceptions**, make sure that **Allow Azure services on the trusted services list** is enabled. Select **Save** to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-services-public-access-disable.png" alt-text="Screenshot of Foundry Tools with public network access disabled.":::

1. To create a private endpoint for the AI services resource, select **Networking**, **Private endpoint connections**, and then select **+ Private endpoint**. This private endpoint is used to allow clients in your Azure Virtual Network to securely communicate with the AI services resource. For more information on using private endpoints with Foundry Tools, visit the [Use private endpoints](/azure/ai-services/cognitive-services-virtual-networks#use-private-endpoints) article.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-services-private-endpoint.png" alt-text="Screenshot of the private endpoint section for Foundry Tools.":::

    1. From the **Basics** tab, enter a unique name for the private endpoint, network interface, and select the region to create the private endpoint in.
    1. From the **Resource** tab, accept the target subresource of **account**.
    1. From the **Virtual Network** tab, select the _Azure Virtual Network_ that the private endpoint connects to. This network should be the same one that your clients connect to, and that the Foundry hub has a private endpoint connection to.
    1. From the **DNS** tab, select the defaults for the DNS settings.
    1. Continue to the **Review + create** tab, and then select **Create** to create the private endpoint.

1. Currently, you can't disable local (shared key) authentication to Foundry Tools through the Azure portal. Instead, use the following [Azure PowerShell](/powershell/azure/what-is-azure-powershell) cmdlet:

    ```azurepowershell
    # Connect to Azure
    Connect-AzAccount

    # Set variables
    $resourceGroupName = "your-resource-group-name"
    $accountName = "your-ai-services-account-name"

    # Disable local authentication
    Set-AzCognitiveServicesAccount -ResourceGroupName $resourceGroupName -Name $accountName -DisableLocalAuth $true
    ```

    Reference: [Set-AzCognitiveServicesAccount](/powershell/module/az.cognitiveservices/set-azcognitiveservicesaccount)

    For more information, see the [Disable local authentication in Foundry Tools](/azure/ai-services/disable-local-auth) article.

## Configure Azure AI Search

Consider using an Azure AI Search index when you want to: 
 - Customize the index creation process. 
 - Reuse an index by ingesting data from other data sources. 

To use an existing index, it must have at least one searchable field. Ensure at least one valid vector column is mapped when using vector search. 

> [!IMPORTANT]
> The information in this section applies only to securing the Azure AI Search resource for use with Foundry. If you're using Azure AI Search for other purposes, you might need to configure other settings. For related information on configuring Azure AI Search, see the following articles:
>
> - [Configure network access and firewall rules](../../search/service-configure-firewall.md)
> - [Enable or disable role-based access control](/azure/search/search-security-enable-roles)
> - [Configure a search service to connect using a managed identity](/azure/search/search-howto-managed-identities-data-sources)

1. If you don't have an existing Azure AI Search resource for your Foundry hub, [create one](/azure/search/search-create-service-portal).
1. From the Azure portal, select the AI Search resource, and then select **Settings**, **Identity**, and **System assigned**.
1. To create a managed identity for the AI Search resource, set the **Status** to **On**. Select **Save** to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-search-managed-identity.png" alt-text="Screenshot of AI Search with a system-managed identity configuration.":::

1. To disable public network access, select **Settings**, **Networking**, and **Firewalls and virtual networks**. Set **Public network access** to **Disabled**. Under **Exceptions**, make sure that **Allow Azure services on the trusted services list** is enabled. Select **Save** to apply the changes.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-search-public-access-disable.png" alt-text="Screenshot of AI Search with public network access disabled.":::

1. To create a private endpoint for the AI Search resource, select **Networking**, **Private endpoint connections**, and then select **+ Create a private endpoint**.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/ai-search-private-endpoint.png" alt-text="Screenshot of the private endpoint section of AI Search.":::

    1. From the **Basics** tab, enter a unique name for the private endpoint, network interface, and select the region to create the private endpoint in.
    1. From the __Resource__ tab, select the __Subscription__ that contains the resource, set the __Resource type__ to __Microsoft.Search/searchServices__, and select the Azure AI Search resource. The only available subresource is __searchService__.
    1. From the **Virtual Network** tab, select the _Azure Virtual Network_ that the private endpoint connects to. This network should be the same one that your clients connect to, and that the Foundry hub has a private endpoint connection to.
    1. From the **DNS** tab, select the defaults for the DNS settings.
    1. Continue to the **Review + create** tab, and then select **Create** to create the private endpoint.

1. To enable API access based on role-based access controls, select __Settings__, __Keys__, and then set __API Access control__ to __Role-based access control__ or __Both__. Select __Yes__ to apply the changes.

    > [!NOTE]
    > Select __Both__ if you have other services that use a key to access the Azure AI Search. Select __Role-based access control__ to disable key-based access.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/search-api-access-control.png" alt-text="Screenshot of AI Search with API access set to both.":::

## Configure Azure Storage (ingestion-only)

If you use Azure Storage for the ingestion scenario with the Foundry portal playground, you need to configure your Azure Storage Account.

1. Create a Storage Account resource. 
1. From the Azure portal, select the Storage Account resource, and then select **Security + networking**, **Networking**, and **Firewalls and virtual networks**.
1. To disable public network access and allow access from trusted services, set **Public network access** to **Enabled from selected virtual networks and IP addresses**. Under **Exceptions**, make sure that **Allow Azure services on the trusted services list** is enabled.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/storage-account-public-access-disable.png" alt-text="Screenshot of storage account network configuration.":::

1. Set **Public network access** to **Disabled** and then select **Save** to apply the changes. The configuration to allow access from trusted services is still enabled.
1. To create a private endpoint for Azure Storage, select **Networking**, **Private endpoint connections**, and then select **+ Private endpoint**.

    :::image type="content" source="../media/how-to/secure-playground-on-your-data/storage-private-endpoint.png" alt-text="Screenshot of the private endpoint section for the storage account.":::

    1. From the **Basics** tab, enter a unique name for the private endpoint, network interface, and select the region to create the private endpoint in.
    1. From the **Resource** tab, set the **Target sub-resource** to **blob**.
    1. From the **Virtual Network** tab, select the _Azure Virtual Network_ that the private endpoint connects to. This network should be the same one that your clients connect to, and that the Foundry hub has a private endpoint connection to.
    1. From the **DNS** tab, select the defaults for the DNS settings.
    1. Continue to the **Review + create** tab, and then select **Create** to create the private endpoint.

1. Repeat the previous step to create a private endpoint, but set the **Target sub-resource** to **file**. The previous private endpoint allows secure communication to blob storage, and this private endpoint allows secure communication to file storage.
1. To disable local (shared key) authentication to storage, select **Configuration**, under **Settings**. Set **Allow storage account key access** to **Disabled**, and then select **Save** to apply the changes. For more information, see the [Prevent authorization with shared key](/azure/storage/common/shared-key-authorization-prevent) article. 

## Configure Azure Key Vault

Foundry uses Azure Key Vault to securely store and manage secrets. To grant access to the key vault from trusted services, use the following steps.

> [!NOTE]
> These steps assume that you already configured the key vault for network isolation when you created your Foundry Hub.

1. In the Azure portal, select the Key Vault resource, and then select **Settings**, **Networking**, and **Firewalls and virtual networks**.
1. In the **Exception** section of the page, make sure that **Allow trusted Microsoft services to bypass firewall** is **enabled**.

## Configure connections to use Microsoft Entra ID

Connections from Foundry to Foundry Tools and Azure AI Search should use Microsoft Entra ID for secure access. You create connections from [Foundry](https://ai.azure.com/?cid=learnDocs) instead of the Azure portal.

> [!IMPORTANT]
> Using Microsoft Entra ID with Azure AI Search is currently a preview feature. For more information on connections, visit the [Add connections](connections-add.md#create-a-new-connection) article.

1. From Foundry, select **Connections**. If you have existing connections to the resources, you can select the connection and then select the **pencil icon** in the **Access details** section to update the connection. Set the **Authentication** field to **Microsoft Entra ID**, and then select **Update**.
1. To create a new connection, select **+ New connection**, and then select the resource type. Browse for the resource or enter the required information, set **Authentication** to **Microsoft Entra ID**, and select **Add connection** to create the connection.

Repeat these steps for each resource that you want to connect to by using Microsoft Entra ID.

## Assign roles to resources and users

The services need to authorize each other to access the connected resources. The admin performing the configuration needs to have the __Owner__ role on these resources to add role assignments. The following table lists the required role assignments for each resource. The __Assignee__ column refers to the system-assigned managed identity of the listed resource. The __Resource__ column refers to the resource that the assignee needs to access. For example, the Azure AI Search has a system-assigned managed identity that needs to be assigned the __Storage Blob Data Contributor__ role for the Azure Storage Account.

For more information on assigning roles, see [Tutorial: Grant a user access to resources](/azure/role-based-access-control/quickstart-assign-role-user-portal).

| Resource | Role | Assignee | Description |
|----------|------|----------|-------------|
| Azure AI Search | Search Index Data Contributor | Foundry Tools/OpenAI | Read-write access to content in indexes. Import, refresh, or query the documents collection of an index. Only used for ingestion and inference scenarios. |
| Azure AI Search | Search Index Data Reader | Foundry Tools/OpenAI | Inference service queries the data from the index. Only used for inference scenarios. |
| Azure AI Search | Search Service Contributor | Foundry Tools/OpenAI | Read-write access to object definitions (indexes, aliases, synonym maps, indexers, data sources, and skillsets). Inference service queries the index schema for auto fields mapping. Data ingestion service creates index, data sources, skill set, indexer, and queries the indexer status. |
| Foundry Tools/OpenAI | Cognitive Services Contributor | Azure AI Search | Allow Search to create, read, and update AI Services resource. |
| Foundry Tools/OpenAI | Cognitive Services OpenAI Contributor | Azure AI Search | Allow Search the ability to fine-tune, deploy, and generate text |
| Azure Storage Account | Storage Blob Data Contributor | Azure AI Search | Reads blob and writes knowledge store. |
| Azure Storage Account | Storage Blob Data Contributor | Foundry Tools/OpenAI | Reads from the input container, and writes the preprocess result to the output container. |
| Azure Blob Storage private endpoint | Reader | Foundry project | For your Foundry project with managed network enabled to access Blob storage in a network restricted environment |
| Azure OpenAI Resource for chat model | Cognitive Services OpenAI User | Azure OpenAI resource for embedding model | [Optional] Required only if using two Azure OpenAI resources to communicate. |

> [!NOTE]
> The Cognitive Services OpenAI User role is only required if you're using two Azure OpenAI resources: one for your chat model and one for your embedding model. If this applies, enable Trusted Services AND ensure the Connection for your embedding model Azure OpenAI resource has EntraID enabled.  

### Assign roles to developers

To enable your developers to use these resources to build applications, assign the following roles to your developer's identity in Microsoft Entra ID. For example, assign the __Search Services Contributor__ role to the developer's Microsoft Entra ID for the Azure AI Search resource.

For more information on assigning roles, see [Tutorial: Grant a user access to resources](/azure/role-based-access-control/quickstart-assign-role-user-portal).

| Resource | Role | Assignee | Description |
|----------|------|----------|-------------|
| Azure AI Search | Search Services Contributor | Developer's Microsoft Entra ID | List API-Keys to list indexes from Foundry portal. |
| Azure AI Search | Search Index Data Contributor | Developer's Microsoft Entra ID | Required for the indexing scenario. |
| Foundry Tools/OpenAI | Cognitive Services OpenAI Contributor | Developer's Microsoft Entra ID | Call public ingestion API from Foundry portal. |
| Foundry Tools/OpenAI | Cognitive Services Contributor | Developer's Microsoft Entra ID | List API-Keys from Foundry portal. |
| Foundry Tools/OpenAI | Contributor | Developer's Microsoft Entra ID | Allows for calls to the control plane. |
| Azure Storage Account | Contributor | Developer's Microsoft Entra ID | List Account SAS to upload files from Foundry portal. |
| Azure Storage Account | Storage Blob Data Contributor | Developer's Microsoft Entra ID | Needed for developers to read and write to blob storage. |
| Azure Storage Account | Storage File Data Privileged Contributor | Developer's Microsoft Entra ID | Needed to Access File Share in Storage for Promptflow data. |
| The resource group or Azure subscription where the developer need to deploy the web app to | Contributor | Developer's Microsoft Entra ID | Deploy web app to the developer's Azure subscription. |

## Use your data in Foundry portal  

Now, the data you add to Foundry is secured to the isolated network provided by your Foundry hub and project. For an example of using data, visit the [build a question and answer copilot](../tutorials/copilot-sdk-build-rag.md) tutorial.

## Deploy web apps

For information on configuring web app deployments, visit the [Use Azure OpenAI on your data securely](/azure/ai-foundry/openai/how-to/on-your-data-configuration#web-app) article.

## Limitations

When using the Chat playground in Foundry portal, don't navigate to another tab within Studio. If you do navigate to another tab, when you return to the Chat tab you must remove your data and then add it back.

## Verify secure connection

To verify that your secure connection works, run the following Python script from a machine within your virtual network (for example, an Azure VM). This script uses your Microsoft Entra ID credentials to authenticate.

```python
import os
from azure.identity import DefaultAzureCredential
from openai import AzureOpenAI

# Set your Azure OpenAI details
endpoint = "https://<your-resource-name>.openai.azure.com/"
deployment_name = "<your-deployment-name>"

# Authenticate using DefaultAzureCredential
# This will use the identity of the VM or your local credentials if running locally
credential = DefaultAzureCredential()

# Initialize the Azure OpenAI client
client = AzureOpenAI(
    azure_endpoint=endpoint,
    azure_ad_token_provider=credential.get_token("https://cognitiveservices.azure.com/.default").token,
    api_version="2024-02-01" # Use a supported API version
)

# Test the connection with a simple chat completion
try:
    response = client.chat.completions.create(
        model=deployment_name,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello, can you confirm this connection is secure?"}
        ]
    )
    print("Connection successful!")
    print("Response:", response.choices[0].message.content)
except Exception as e:
    print("Connection failed.")
    print("Error:", e)
```

Reference: [AzureOpenAI](https://github.com/openai/openai-python) | [DefaultAzureCredential](/python/api/azure-identity/azure.identity.defaultazurecredential)

**Expected output:**

If your secure connection is configured correctly, you see output similar to:

```output
Connection successful!
Response: Yes, this connection is secure. Your request was processed...
```

If you see "Connection failed" with an error message, verify that your private endpoints are configured correctly and that you're running the script from within the virtual network.

## Related content

- [Tutorial: Deploy an enterprise chat web app](../tutorials/deploy-chat-web-app.md)
- [How to configure a managed network](configure-managed-network.md)
