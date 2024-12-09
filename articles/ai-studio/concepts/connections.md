---
title: Connections in Azure AI Foundry portal
titleSuffix: Azure AI Foundry
description: This article introduces connections in Azure AI Foundry portal.
manager: scottpolly
ms.service: azure-ai-studio
ms.custom:
  - ignite-2023
  - build-2024
  - ignite-2024
ms.topic: conceptual
ms.date: 11/21/2024
ms.reviewer: sgilley
ms.author: sgilley
author: sdgilley
---

# Connections in Azure AI Foundry portal

Connections in Azure AI Foundry portal are a way to authenticate and consume both Microsoft and non-Microsoft resources within your AI Foundry projects. For example, connections can be used for prompt flow, training data, and deployments. [Connections can be created](../how-to/connections-add.md) exclusively for one project or shared with all projects in the same hub. 

## Connections to Azure AI services

You can [create connections](../how-to/connections-add.md) to Azure AI services such as Azure OpenAI and Azure AI Content Safety. You can then use the connection in a prompt flow tool such as the LLM tool.

:::image type="content" source="../media/prompt-flow/llm-tool-connection.png" alt-text="Screenshot of a connection used by the LLM tool in prompt flow." lightbox="../media/prompt-flow/llm-tool-connection.png":::

As another example, you can [create a connection](../how-to/connections-add.md) to an Azure AI Search resource. The connection can then be used by prompt flow tools such as the Index Lookup tool.

:::image type="content" source="../media/prompt-flow/index-lookup-tool-connection.png" alt-text="Screenshot of a connection used by the Index Lookup tool in prompt flow." lightbox="../media/prompt-flow/index-lookup-tool-connection.png":::

## Connections to non-Microsoft services

Azure AI Foundry supports connections to non-Microsoft services, including the following:
- The [API key connection](../how-to/connections-add.md) handles authentication to your specified target on an individual basis. This is the most common non-Microsoft connection type.
- The [custom connection](../how-to/connections-add.md) allows you to securely store and access keys while storing related properties, such as targets and versions. Custom connections are useful when you have many targets that or cases where you wouldn't need a credential to access. LangChain scenarios are a good example where you would use custom service connections. Custom connections don't manage authentication, so you'll have to manage authentication on your own.

## Connections to datastores

> [!IMPORTANT]
> Data connections cannot be shared across projects. They are created exclusively in the context of one project. 

Creating a data connection allows you to access external data without copying it to your project. Instead, the connection provides a reference to the data source.

A data connection offers these benefits:

- A common, easy-to-use API that interacts with different storage types including Microsoft OneLake, Azure Blob, and Azure Data Lake Gen2.
- Easier discovery of useful connections in team operations.
- For credential-based access (service principal/SAS/key), AI Foundry connection secures credential information. This way, you won't need to place that information in your scripts.

When you create a connection with an existing Azure storage account, you can choose between two different authentication methods:

- **Credential-based**: Authenticate data access with a service principal, shared access signature (SAS) token, or account key. Users with *Reader* project permissions can access the credentials.
- **Identity-based**: Use your Microsoft Entra ID or managed identity to authenticate data access.

    > [!TIP]
    > When using an identity-based connection, Azure role-based access control (Azure RBAC) is used to determine who can access the connection. You must assign the correct Azure RBAC roles to your developers before they can use the connection. For more information, see [Scenario: Connections using Microsoft Entra ID](rbac-ai-studio.md#scenario-connections-using-microsoft-entra-id-authentication).


The following table shows the supported Azure cloud-based storage services and authentication methods:

Supported storage service | Credential-based authentication | Identity-based authentication
|---|:----:|:---:|
Azure Blob Container| ✓ | ✓|
Microsoft OneLake| ✓ | ✓|
Azure Data Lake Gen2| ✓ | ✓|

A Uniform Resource Identifier (URI) represents a storage location on your local computer, Azure storage, or a publicly available http or https location. These examples show URIs for different storage options:


| Storage location | URI examples |
|------------------|--------------|
| Azure AI Foundry connection | `azureml://datastores/<data_store_name>/paths/<folder1>/<folder2>/<folder3>/<file>.parquet` |
| Local files | `./home/username/data/my_data` |
| Public http or https server | `https://raw.githubusercontent.com/pandas-dev/pandas/main/doc/data/titanic.csv` |
| Blob storage | `wasbs://<containername>@<accountname>.blob.core.windows.net/<folder>/` |
| Azure Data Lake (gen2) | `abfss://<file_system>@<account_name>.dfs.core.windows.net/<folder>/<file>.csv` |
| Microsoft OneLake | `abfss://<file_system>@<account_name>.dfs.core.windows.net/<folder>/<file>.csv` `https://<accountname>.dfs.fabric.microsoft.com/<artifactname>` |

> [!NOTE]
> The Microsoft OneLake connection doesn't support OneLake tables.

## Key vaults and secrets

Connections allow you to securely store credentials, authenticate access, and consume data and information.  Secrets associated with connections are securely persisted in the corresponding Azure Key Vault, adhering to robust security and compliance standards. As an administrator, you can audit both shared and project-scoped connections on a hub level (link to connection rbac). 

Azure connections serve as key vault proxies, and interactions with connections are direct interactions with an Azure key vault. Azure AI Foundry connections store API keys securely, as secrets, in a key vault. The key vault [Azure role-based access control (Azure RBAC)](./rbac-ai-studio.md) controls access to these connection resources. A connection references the credentials from the key vault storage location for further use. You won't need to directly deal with the credentials after they're stored in the hub's key vault. You have the option to store the credentials in the YAML file. A CLI command or SDK can override them. We recommend that you avoid credential storage in a YAML file, because a security breach could lead to a credential leak.  


## Next steps

- [How to create a connection in Azure AI Foundry portal](../how-to/connections-add.md)
