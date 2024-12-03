---
author: larryfr
ms.service: azure-machine-learning
ms.custom: devx-track-azurecli
ms.topic: include
ms.date: 12/02/2024
ms.author: larryfr
---

### Online endpoint creation fails with a message about v1 legacy mode

Managed online endpoints are a feature of the Azure Machine Learning v2 API platform. If your Azure Machine Learning workspace is configured for v1 legacy mode, the managed online endpoints don't work. Specifically, if the `v1_legacy_mode` workspace setting is set to `true`, v1 legacy mode is turned on, and there's no support for v2 APIs.

To see how to turn off v1 legacy mode, see [Network isolation change with our new API platform on Azure Resource Manager](../how-to-configure-network-isolation-with-v2.md).

> [!IMPORTANT]
> Check with your network security team before you set `v1_legacy_mode` to `false`, because v1 legacy mode might be turned on for a reason.

### Online endpoint creation with key-based authentication fails

Use the following command to list the network rules of the Azure key vault for your workspace. Replace `<key-vault-name>` with the name of your key vault.

```azurecli
az keyvault network-rule list -n <key-vault-name>
```

The response for this command is similar to the following JSON code:

```json
{
    "bypass": "AzureServices",
    "defaultAction": "Deny",
    "ipRules": [],
    "virtualNetworkRules": []
}
```

If the value of `bypass` isn't `AzureServices`, use the guidance in [Configure Azure Key Vault networking settings](/azure/key-vault/general/how-to-azure-key-vault-network-security?tabs=azure-cli) to set it to `AzureServices`.

### Online deployments fail with an image download error

> [!NOTE]
> This issue applies when you use the [legacy network isolation method for managed online endpoints](../concept-secure-online-endpoint.md#secure-outbound-access-with-legacy-network-isolation-method). In this method, Azure Machine Learning creates a managed virtual network for each deployment under an endpoint.

1. Check whether the `egress-public-network-access` flag has a value of `disabled` for the deployment. If this flag is enabled, and the visibility of the container registry is private, this failure is expected.
1. Use the following command to check the status of the private endpoint connection. Replace `<registry-name>` with the name of the Azure container registry for your workspace:

   ```azurecli
   az acr private-endpoint-connection list -r <registry-name> --query "[?privateLinkServiceConnectionState.description=='Egress for Microsoft.MachineLearningServices/workspaces/onlineEndpoints'].{ID:id, status:privateLinkServiceConnectionState.status}"
   ```

   In the response code, verify that the `status` field is set to `Approved`. If the value isn't `Approved`, use the following command to approve the connection. Replace `<private-endpoint-connection-ID>` with the ID that the preceding command returns.

   ```azurecli
   az network private-endpoint-connection approve --id <private-endpoint-connection-ID> --description "Approved"
   ```

### Online deployments can't be scored

1. Run the following command to see the status of a deployment that can't be scored:

   ```azurecli
   az ml online-deployment show -e <endpoint-name> -n <deployment-name> --query '{name:name,state:provisioning_state}' 
   ```

   A value of `Succeeded` for the `state` field indicates a successful deployment.

1. For a successful deployment, use the following command to check that traffic is assigned to the deployment:

   ```azurecli
   az ml online-endpoint show -n <endpoint-name>  --query traffic
   ```

   The response from this command should list the percentage of traffic that's assigned to each deployment.

   > [!TIP]
   > This step isn't necessary if you use the `azureml-model-deployment` header in your request to target this deployment.

1. If the traffic assignments or deployment header are set correctly, use the following command to get the logs for the endpoint:

   ```azurecli
   az ml online-deployment get-logs  -e <endpoint-name> -n <deployment-name> 
   ```

1. Review the logs to see whether there's a problem running the scoring code when you submit a request to the deployment.
