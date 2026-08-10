---
title: Deploy a C# Search App to Azure Container Apps
description: Learn how to deploy a C# app with Azure AI Search to Azure Container Apps by using azd with managed identity or optional key-based authentication.
ms.reviewer: diberry
ms.service: azure-ai-search
ms.update-cycle: 180-days
ms.topic: tutorial
ms.date: 08/07/2026
ms.custom:
  - devx-track-csharp
  - devx-track-dotnet
  - ignite-2023
ms.devlang: csharp
ai-usage: ai-assisted
---

# Deploy a C# Azure AI Search app to Azure Container Apps

[!INCLUDE [search-fiq-banner](./includes/search-fiq-banner.md)]

Deploy the search-enabled website to Azure Container Apps by using the Azure Developer CLI (`azd`). This deployment includes the React client, the .NET API, Azure AI Search, managed identity, and supporting Azure resources.

The deployment uses managed identity as the default authentication method for Azure AI Search. You can opt in to key-based authentication by setting `USE_KEYLESS_AUTH` to `false` before deployment.

## Sign in to Azure

1. In Visual Studio Code, open a terminal at the repository root, such as `azure-search-static-web-app`.

1. Sign in to Azure by using `azd`.

    ```bash
    azd auth login
    ```

1. If prompted by your browser, complete the sign-in flow by using the Azure account that you're using for this tutorial.

## Create an azd environment

- Create an `azd` environment. Replace `YOUR-ENVIRONMENT-NAME` with a short name that identifies this tutorial deployment.

    ```bash
    azd env new YOUR-ENVIRONMENT-NAME
    ```

## (Optional) Configure key-based authentication

The default authentication method is managed identity, so most environments can skip this section. Complete this section only if your environment requires API keys.

Set `USE_KEYLESS_AUTH` to `false`.

  ```bash
  azd env set USE_KEYLESS_AUTH false
  ```

If you don't set `USE_KEYLESS_AUTH`, the deployment uses managed identity. The Bicep infrastructure grants the container app identity access to the Azure AI Search data plane.

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

    The deployment also created the Azure AI Search service and loaded the `good-books` index automatically through the `postprovision` hook in the sample repository.

## Use search in your Container Apps website

1. Open the client FQDN from the `azd up` output in a browser.

1. In the website search bar, enter a search query, such as `code`. The autocomplete feature suggests matching book titles.

1. Select a suggestion or continue entering your own query. Select **Enter** when you finish your search query.

1. Review the results, and then select a book to see more details.

## Troubleshooting

If the web app doesn't deploy or work, use the following list to determine and fix the issue:

- **Did `azd up` complete?**

  Review the `azd up` output for the first failed provisioning, build, or deploy step. If deployment stops during provisioning, check your subscription permissions and the selected region. If deployment stops during the container build or deploy steps, rerun `azd up` after you fix the reported issue.

- **Can you open the client endpoint?**

  Open the `AZURE_CLIENT_URL` value from the `azd up` output. If the page doesn't load, go to the Azure portal, open the client container app and review its revision status and logs.

- **Can the client call the server endpoint?**

  Open your browser developer tools and review the network calls from the client app. If calls to the API fail, confirm that the server container app is running and that the client app received the server FQDN during deployment.

- **Can the server query Azure AI Search?**

  If searches return errors, review the server container app logs. For managed identity, confirm that the identity has Azure AI Search data-plane access. For key-based authentication, confirm that you set `USE_KEYLESS_AUTH` to `false` before deployment and that the generated container environment contains the search service configuration.

## Clean up resources

Use `azd down --purge` to delete the Azure resources that this tutorial created. The `--purge` flag permanently removes resources that support soft-delete, instead of leaving them in a recoverable state for their retention period. Purging avoids naming conflicts if you redeploy this tutorial later.

1. From the repository root, run the clean-up command.

    ```bash
    azd down --purge
    ```

1. Review the resources that `azd` lists.

1. Confirm the deletion when prompted.

If you created an Azure AI Search service outside the `azd` deployment, go to your search service in the [Azure portal](https://portal.azure.com) and select **Delete** at the top of the page.

## Next step

> [!div class="nextstepaction"]
> [Explore the search integration code](tutorial-csharp-search-query-integration.md)
