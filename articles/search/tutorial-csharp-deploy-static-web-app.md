---
title: Deploy a .NET search app to Azure Container Apps
description: Deploy a search-enabled .NET website to Azure Container Apps with azd and managed identity.
ms.reviewer: diberry
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: tutorial
ms.date: 07/24/2026
ms.custom:
  - devx-track-csharp
  - devx-track-dotnet
  - ignite-2023
ms.devlang: csharp
ai-usage: ai-assisted
---

# Step 3 - Deploy the search-enabled .NET website

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

Deploy the search-enabled website to Azure Container Apps with the Azure Developer CLI (`azd`). This deployment includes the React client, the .NET API, Azure AI Search, managed identity, and supporting Azure resources.

The deployment uses managed identity as the default authentication method for Azure AI Search. You can opt in to key authentication by setting `SEARCH_USE_KEY_AUTH` before deployment.

## Sign in to Azure

1. In Visual Studio Code, open a terminal at the repository root, for example, `azure-search-static-web-app`.

1. Sign in to Azure with `azd`.

    ```bash
    azd auth login
    ```

1. If your browser prompts you, complete the sign-in flow with the Azure account you use for this tutorial.

## Configure the deployment environment

1. Create an `azd` environment. Replace `YOUR-ENVIRONMENT-NAME` with a short name that identifies this tutorial deployment.

    ```bash
    azd env new YOUR-ENVIRONMENT-NAME
    ```

1. Set key authentication only if your deployment requires API keys instead of managed identity.

    ```bash
    azd env set SEARCH_USE_KEY_AUTH true
    ```

    If you don't set `SEARCH_USE_KEY_AUTH`, the deployment uses managed identity. The Bicep infrastructure grants the container app identity access to the Azure AI Search data plane.

## Deploy with azd up

1. From the repository root, run `azd up`.

    ```bash
    azd up
    ```

1. When prompted, select the Azure subscription and location for the resources.

1. Wait for `azd` to provision the infrastructure, build the containers, push the images, and deploy the services to Azure Container Apps.

1. Review the output after deployment. The output includes the client and server fully qualified domain names (FQDNs) for the Azure Container Apps deployment.

    ```output
    AZURE_CLIENT_URL: <client-container-app-fqdn>
    AZURE_SERVER_URL: <server-container-app-fqdn>
    SEARCH_SERVICE_NAME: <search-service-name>
    ```

    Use the `AZURE_CLIENT_URL` value to open the website. The client app calls the server app through the endpoint configured during deployment.

## Use search in your Container Apps website

1. Open the client FQDN from the `azd up` output in a browser.

1. In the website search bar, enter a search query such as `code`, so the suggest feature suggests book titles.

1. Select a suggestion, or continue entering your own query. Press Enter when you finish your search query.

1. Review the results, and then select one of the books to see more details.

## Troubleshooting

If the web app didn't deploy or work, use the following list to determine and fix the issue.

- **Did `azd up` complete?**

  Review the `azd up` output for the first failed provisioning, build, or deploy step. If deployment stops during provisioning, check your subscription permissions and the selected region. If deployment stops during the container build or deploy steps, rerun `azd up` after you fix the reported issue.

- **Can you open the client endpoint?**

  Open the `AZURE_CLIENT_URL` value from the `azd up` output. If the page doesn't load, go to the Azure portal, open the client container app, and review its revision status and logs.

- **Can the client call the server endpoint?**

  Open your browser developer tools and review the network calls from the client app. If calls to the API fail, confirm that the server container app is running and that the client app received the server FQDN during deployment.

- **Can the server query Azure AI Search?**

  If searches return errors, review the server container app logs. For managed identity, confirm that the identity has Azure AI Search data-plane access. For key authentication, confirm that you set `SEARCH_USE_KEY_AUTH` before deployment and that the generated container environment contains the search service configuration.

## Clean up resources

Use `azd down` to delete the Azure resources created by this tutorial.

1. From the repository root, run the clean-up command.

    ```bash
    azd down
    ```

1. Review the resources that `azd` lists.

1. Confirm the deletion when prompted.

If you created an Azure AI Search service outside the `azd` deployment, go to your search service in the [Azure portal](https://portal.azure.com), and select **Delete** at the top of the page.

## Next steps

* [Understand Search integration for the search-enabled website](tutorial-csharp-search-query-integration.md)
