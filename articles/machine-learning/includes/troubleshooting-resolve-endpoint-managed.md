---
author: larryfr
ms.service: azure-machine-learning
ms.custom: devx-track-azurecli
ms.topic: include
ms.date: 11/26/2024
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
   > 
   > If the endpoint uses HTTP, the IP address is contained in the endpoint URI, which you can get from the studio UI.

1. If the `nslookup` command doesn't resolve the host name, use the following command to check whether an A record exists in the private Domain Name System (DNS) zone for the virtual network:

   ```azurecli
   az network private-dns record-set list -z privatelink.api.azureml.ms -o tsv --query [].name
   ```

   The results should contain an entry similar to `*.<GUID>.inference.<region>`.

1. If no inference value is returned, delete the private endpoint for the workspace and then re-create it. For more information, see [How to configure a private endpoint](/azure/container-registry/container-registry-private-link).

1. If the workspace with a private endpoint [uses a custom DNS server](../how-to-custom-dns.md), run the following command to verify that the resolution from the custom DNS server works correctly:

   ```bash
   dig <endpoint-name>.<endpoint-region>.inference.ml.azure.com
   ```
