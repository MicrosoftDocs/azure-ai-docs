---
author: larryfr
ms.service: azure-machine-learning
ms.custom: devx-track-azurecli
ms.topic: include
ms.date: 12/02/2024
ms.author: larryfr
---

### Scoring endpoint can't be resolved

1. Verify that the client issuing the scoring request is a virtual network that can access the Azure Machine Learning workspace.
1. Use the `nslookup` command on the endpoint host name to retrieve the IP address information:

   ```bash
   nslookup <endpoint-name>.<endpoint-region>.inference.ml.azure.com
   ```

   For example, your command might look similar to the following one:

   ```bash
   nslookup endpointname.westcentralus.inference.ml.azure.com
   ```

   The response contains an address that should be in the range provided by the virtual network.
   
   > [!NOTE]
   > - For a Kubernetes online endpoint, the endpoint host name should be the **CName** (domain name) that's specified in your Kubernetes cluster.
   > - If the endpoint uses HTTP, the IP address is contained in the endpoint URI, which you can get from the studio UI.
   > - For more ways to get the IP address of the endpoint, see [Update your DNS with an FQDN](../how-to-secure-Kubernetes-online-endpoint.md#update-your-dns-with-an-fqdn).

1. If the `nslookup` command doesn't resolve the host name, take the actions in one of the following sections.

#### Managed online endpoints

1. Use the following command to check whether an A record exists in the private Domain Name System (DNS) zone for the virtual network:

   ```azurecli
   az network private-dns record-set list -z privatelink.api.azureml.ms -o tsv --query [].name
   ```

   The results should contain an entry similar to `*.<GUID>.inference.<region>`.

1. If no inference value is returned, delete the private endpoint for the workspace and then re-create it. For more information, see [How to configure a private endpoint](/azure/container-registry/container-registry-private-link).

1. If the workspace with a private endpoint [uses a custom DNS server](../how-to-custom-dns.md), run the following command to verify that the resolution from the custom DNS server works correctly:

   ```bash
   dig <endpoint-name>.<endpoint-region>.inference.ml.azure.com
   ```

#### Kubernetes online endpoints

1. Check the DNS configuration in the Kubernetes cluster.
1. Check whether the [Azure Machine Learning inference router, `azureml-fe`,](../how-to-kubernetes-inference-routing-azureml-fe.md) works as expected. To perform this check, take the following steps:
   1. Run the following command in the `azureml-fe` pod:

      ```bash
      kubectl exec -it deploy/azureml-fe -- /bin/bash
      ```

   1. Run one of the following commands:
   
      ```bash
      curl -vi -k https://localhost:<port>/api/v1/endpoint/<endpoint-name>/swagger.json
      "Swagger not found"
      ```

      For HTTP, use the following command:

      ```bash
      curl https://localhost:<port>/api/v1/endpoint/<endpoint-name>/swagger.json
      "Swagger not found"
      ```

1. If the curl HTTPS command fails or times out but the HTTP command works, check whether the certificate is valid.

1. If the preceding process fails to resolve to the A record, use the following command to verify whether the resolution works from the Azure DNS virtual public IP address, 168.63.129.16:

   ```bash
   dig @168.63.129.16 <endpoint-name>.<endpoint-region>.inference.ml.azure.com
   ```

1. If the preceding command succeeds, troubleshoot the conditional forwarder for Azure Private Link on a custom DNS.
