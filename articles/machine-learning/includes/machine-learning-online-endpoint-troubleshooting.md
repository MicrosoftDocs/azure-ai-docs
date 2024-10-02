---
author: larryfr
ms.service: azure-machine-learning
ms.custom: devx-track-azurecli
ms.topic: include
ms.date: 09/17/2024
ms.author: larryfr
---

### Online endpoint creation fails with a V1LegacyMode == true message

You can configure the Azure Machine Learning workspace for `v1_legacy_mode`, which disables v2 APIs. Managed online endpoints are a feature of the v2 API platform, and don't work if `v1_legacy_mode` is enabled for the workspace. 

To disable `v1_legacy_mode`, see [Network isolation with v2](../how-to-configure-network-isolation-with-v2.md).

> [!IMPORTANT]
> Check with your network security team before you disable `v1_legacy_mode`, because they might have enabled it for a reason.

### Online endpoint creation with key-based authentication fails

Use the following command to list the network rules of the Azure key vault for your workspace. Replace `<keyvault-name>` with the name of your key vault:

```azurecli
az keyvault network-rule list -n <keyvault-name>
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

If the value of `bypass` isn't `AzureServices`, use the guidance in the [Configure key vault network settings](/azure/key-vault/general/how-to-azure-key-vault-network-security?tabs=azure-cli) to set it to `AzureServices`.

### Online deployments fail with an image download error

> [!NOTE]
> This issue applies when you use the [legacy network isolation method for managed online endpoints](../concept-secure-online-endpoint.md#secure-outbound-access-with-legacy-network-isolation-method), in which Azure Machine Learning creates a managed virtual network for each deployment under an endpoint.

1. Check if the `egress-public-network-access` flag is `disabled` for the deployment. If this flag is enabled, and the visibility of the container registry is private, this failure is expected.
1. Use the following command to check the status of the private endpoint connection. Replace `<registry-name>` with the name of the Azure container registry for your workspace:

   ```azurecli
   az acr private-endpoint-connection list -r <registry-name> --query "[?privateLinkServiceConnectionState.description=='Egress for Microsoft.MachineLearningServices/workspaces/onlineEndpoints'].{Name:name, status:privateLinkServiceConnectionState.status}"
   ```

   In the response code, verify that the `status` field is set to `Approved`. If not, use the following command to approve it. Replace `<private-endpoint-name>` with the name returned from the preceding command.

   ```azurecli
   az network private-endpoint-connection approve -n <private-endpoint-name>
   ```

### Scoring endpoint can't be resolved

1. Verify that the client issuing the scoring request is a virtual network that can access the Azure Machine Learning workspace.
1. Use the `nslookup` command on the endpoint hostname to retrieve the IP address information, for example:

   ```bash
   nslookup endpointname.westcentralus.inference.ml.azure.com
   ```

   The response contains an address that should be in the range provided by the virtual network.
   
   > [!NOTE]
   > - For Kubernetes online endpoint, the endpoint hostname should be the **CName** (domain name) that's specified in your Kubernetes cluster. 
   > - If the endpoint is HTTP, the IP address is contained in the endpoint URI, which you can get from the studio UI.
   > - You can find more ways to get the IP address of the endpoint in [Secure Kubernetes online endpoint](../how-to-secure-Kubernetes-online-endpoint.md#update-your-dns-with-an-fqdn).

1. If the `nslookup` command doesn't resolve the host name, take the following actions:

#### Managed online endpoints

1. Use the following command to check whether an A record exists in the private Domain Name Server (DNS) zone for the virtual network.

   ```azurecli
   az network private-dns record-set list -z privatelink.api.azureml.ms -o tsv --query [].name
   ```

   The results should contain an entry similar to `*.<GUID>.inference.<region>`.

1. If no inference value returns, delete the private endpoint for the workspace and then recreate it. For more information, see [How to configure a private endpoint](/azure/container-registry/container-registry-private-link).

1. If the workspace with a private endpoint [uses a custom DNS server](../how-to-custom-dns.md), run the following command to verify that the resolution from custom DNS works correctly.

```bash
dig endpointname.westcentralus.inference.ml.azure.com
```

#### Kubernetes online endpoints

1. Check the DNS configuration in the Kubernetes cluster.
1. Also check if the [azureml-fe](../how-to-kubernetes-inference-routing-azureml-fe.md) works as expected, by using the following command:

   ```bash
   kubectl exec -it deploy/azureml-fe -- /bin/bash
   (Run in azureml-fe pod)
   
   curl -vi -k https://localhost:<port>/api/v1/endpoint/<endpoint-name>/swagger.json
   "Swagger not found"
   ```

   For HTTP, use the following command:

   ```bash
    curl https://localhost:<port>/api/v1/endpoint/<endpoint-name>/swagger.json
   "Swagger not found"
   ```

1. If curl HTTPs fails or times out but HTTP works, check whether the certificate is valid.

1. If the preceding process fails to resolve to the A record, verify if the resolution works from Azure DNS (168.63.129.16).

   ```bash
   dig @168.63.129.16 endpointname.westcentralus.inference.ml.azure.com
   ```

1. If the preceding command succeeds, troubleshoot the conditional forwarder for private link on custom DNS.

### Online deployments can't be scored

1. Run the following command to see if the deployment was successful:

   ```azurecli
   az ml online-deployment show -e <endpointname> -n <deploymentname> --query '{name:name,state:provisioning_state}' 
   ```

   If the deployment completed successfully, the value of `state` is `Succeeded`.

1. If the deployment was successful, use the following command to check that traffic is assigned to the deployment. Replace `<endpointname>` with the name of your endpoint.

   ```azurecli
   az ml online-endpoint show -n <endpointname>  --query traffic
   ```

   The response from this command should list the percentage of traffic assigned to deployments.


   > [!TIP]
   > This step isn't necessary if you use the `azureml-model-deployment` header in your request to target this deployment.

1. If the traffic assignments or deployment header are set correctly, use the following command to get the logs for the endpoint. Replace `<endpointname>` with the name of the endpoint, and `<deploymentname>` with the deployment.

   ```azurecli
   az ml online-deployment get-logs  -e <endpointname> -n <deploymentname> 
   ```

1. Review the logs to see if there's a problem running the scoring code when you submit a request to the deployment.
