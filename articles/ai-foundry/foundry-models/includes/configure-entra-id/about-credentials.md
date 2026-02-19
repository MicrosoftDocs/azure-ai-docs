---
manager: nitinme
author: santiagxf
ms.author: fasantia 
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-model-inference
ms.date: 01/22/2026
ms.topic: include
---

### Options for credential when using Microsoft Entra ID

`DefaultAzureCredential` is an opinionated, ordered sequence of mechanisms for authenticating to Microsoft Entra ID. Each authentication mechanism is a class that's derived from the `TokenCredential` class and is known as a credential. At runtime, `DefaultAzureCredential` attempts to authenticate using the first credential. If that credential fails to acquire an access token, the next credential in the sequence is attempted, and so on, until an access token is obtained. In this way, your app can use different credentials in different environments without writing environment-specific code.

When the preceding code runs on your local development workstation, it looks in the environment variables for an application service principal or at locally installed developer tools, like Visual Studio, for a set of developer credentials. You can use either approach to authenticate the app to Azure resources during local development.

When deployed to Azure, this same code can also authenticate your app to other Azure resources. `DefaultAzureCredential` can retrieve environment settings and managed identity configurations to authenticate to other services automatically.

### Best practices

* Use deterministic credentials in production environments: Strongly consider moving from `DefaultAzureCredential` to one of the following deterministic solutions in production environments:

  * A specific `TokenCredential` implementation, like `ManagedIdentityCredential`. See the [Derived list for options](/dotnet/api/azure.core.tokencredential#definition).
  * A pared-down `ChainedTokenCredential` implementation that's optimized for the Azure environment in which your app runs. `ChainedTokenCredential` essentially creates a specific allowlist of acceptable credential options, like `ManagedIdentity` for production and `VisualStudioCredential` for development.

* Configure system-assigned or user-assigned managed identities to the Azure resources where your code runs, if possible. Configure Microsoft Entra ID access to those specific identities. 