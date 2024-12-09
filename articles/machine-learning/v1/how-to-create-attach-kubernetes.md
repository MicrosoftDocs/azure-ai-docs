---
title: Create and attach Azure Kubernetes Service
titleSuffix: Azure Machine Learning
description: 'Learn how to create a new Azure Kubernetes Service cluster through Azure Machine Learning, or how to attach an existing AKS cluster to your workspace.'
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: how-to
ms.custom: UpdateFrequency5, devx-track-azurecli, cliv1, sdkv1
ms.author: larryfr
author: Blackmist
ms.reviewer: bozhlin
ms.date: 04/21/2022
---

# Create and attach an Azure Kubernetes Service cluster with v1
[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]
[!INCLUDE [cli v1](../includes/machine-learning-cli-v1.md)]


> [!IMPORTANT]
> This article shows how to use the CLI and SDK v1 to create or attach an Azure Kubernetes Service cluster, which is considered as **legacy** feature now.  To attach Azure Kubernetes Service cluster using  the recommended approach for v2, see [Introduction to Kubernetes compute target in v2](../how-to-attach-kubernetes-anywhere.md).

Azure Machine Learning can deploy trained machine learning models to Azure Kubernetes Service. However, you must first either __create__ an Azure Kubernetes Service (AKS) cluster from your Azure Machine Learning workspace, or __attach__ an existing AKS cluster. This article provides information on both creating and attaching a cluster.

## Prerequisites
- An Azure Machine Learning workspace. For more information, see [Create an Azure Machine Learning workspace](../how-to-manage-workspace.md).

- The [Azure CLI extension (v1) for Machine Learning service](reference-azure-machine-learning-cli.md), [Azure Machine Learning Python SDK](/python/api/overview/azure/ml/intro), or the [Azure Machine Learning Visual Studio Code extension](../how-to-setup-vs-code.md).

    [!INCLUDE [cli v1 deprecation](../includes/machine-learning-cli-v1-deprecation.md)]

- If you plan on using an Azure Virtual Network to secure communication between your Azure Machine Learning workspace and the AKS cluster, your workspace and its associated resources (storage, key vault, Azure Container Registry) must have private endpoints or service endpoints in the same VNET as AKS cluster's VNET. Please follow tutorial [create a secure workspace](../tutorial-create-secure-workspace.md) to add those private endpoints or service endpoints to your VNET.

## Limitations

- An AKS can only be created or attached as a single compute target in Azure Machine Learning workspace. Multiple attachments for one AKS is not supported.
- If you need a **Standard Load Balancer(SLB)** deployed in your cluster instead of a Basic Load Balancer(BLB), create a cluster in the AKS portal/CLI/SDK and then **attach** it to the Azure Machine Learning workspace.

- If you have an Azure Policy that restricts the creation of Public IP addresses, then AKS cluster creation will fail. AKS requires a Public IP for [egress traffic](/azure/aks/limit-egress-traffic). The egress traffic article also provides guidance to lock down egress traffic from the cluster through the Public IP, except for a few fully qualified domain names. There are 2 ways to enable a Public IP:
    - The cluster can use the Public IP created by default with the BLB or SLB, Or
    - The cluster can be created without a Public IP and then a Public IP is configured with a firewall with a user defined route. For more information, see [Customize cluster egress with a user-defined-route](/azure/aks/egress-outboundtype).
    
    The Azure Machine Learning control plane does not talk to this Public IP. It talks to the AKS control plane for deployments. 

- To attach an AKS cluster, the service principal/user performing the operation must be assigned the __Owner or contributor__ Azure role-based access control (Azure RBAC) role on the Azure resource group that contains the cluster. The service principal/user must also be assigned [Azure Kubernetes Service Cluster Admin Role](/azure/role-based-access-control/built-in-roles#azure-kubernetes-service-cluster-admin-role) on the cluster.

- If you **attach** an AKS cluster, which has an [Authorized IP range enabled to access the API server](/azure/aks/api-server-authorized-ip-ranges), enable the Azure Machine Learning control plane IP ranges for the AKS cluster. The Azure Machine Learning control plane is deployed across paired regions and deploys inference pods on the AKS cluster. Without access to the API server, the inference pods cannot be deployed. Use the [IP ranges](https://www.microsoft.com/download/confirmation.aspx?id=56519) for both the [paired regions](/azure/reliability/cross-region-replication-azure) when enabling the IP ranges in an AKS cluster.

    Authorized IP ranges only works with Standard Load Balancer.

- If you want to use a private AKS cluster (using Azure Private Link), you must create the cluster first, and then **attach** it to the workspace. For more information, see [Create a private Azure Kubernetes Service cluster](/azure/aks/private-clusters).

- Using a [public fully qualified domain name (FQDN) with a private AKS cluster](/azure/aks/private-clusters) is __not supported__ with Azure Machine Learning. 

- The compute name for the AKS cluster MUST be unique within your Azure Machine Learning workspace. It can include letters, digits and dashes. It must start with a letter, end with a letter or digit, and be between 3 and 24 characters in length.
 
 - If you want to deploy models to **GPU** nodes or **FPGA** nodes (or any specific SKU), then you must create a cluster with the specific SKU. There is no support for creating a secondary node pool in an existing cluster and deploying models in the secondary node pool.
 
- When creating or attaching a cluster, you can select whether to create the cluster for __dev-test__ or __production__. If you want to create an AKS cluster for __development__, __validation__, and __testing__ instead of production, set the __cluster purpose__ to __dev-test__. If you do not specify the cluster purpose, a __production__ cluster is created. 

    > [!IMPORTANT]
    > A __dev-test__ cluster is not suitable for production level traffic and may increase inference times. Dev/test clusters also do not guarantee fault tolerance.

- When creating or attaching a cluster, if the cluster will be used for __production__, then it must contain at least __3 nodes__. For a __dev-test__ cluster, it must contain at least 1 node.

- The Azure Machine Learning SDK does not provide support scaling an AKS cluster. To scale the nodes in the cluster, use the UI for your AKS cluster in the Azure Machine Learning studio. You can only change the node count, not the VM size of the cluster. For more information on scaling the nodes in an AKS cluster, see the following articles:

    - [Manually scale the node count in an AKS cluster](/azure/aks/scale-cluster)
    - [Set up cluster autoscaler in AKS](/azure/aks/cluster-autoscaler)

- __Do not directly update the cluster by using a YAML configuration__. While Azure Kubernetes Services supports updates via YAML configuration, Azure Machine Learning deployments will override your changes. The only two YAML fields that will not overwritten are __request limits__ and __cpu and memory__.

- Creating an AKS cluster using the Azure Machine Learning studio UI, SDK, or CLI extension is __not__ idempotent. Attempting to create the resource again will result in an error that a cluster with the same name already exists.
    
    - Using an Azure Resource Manager template and the [Microsoft.MachineLearningServices/workspaces/computes](/azure/templates/microsoft.machinelearningservices/2019-11-01/workspaces/computes) resource to create an AKS cluster is also __not__ idempotent. If you attempt to use the template again to update an already existing resource, you will receive the same error.

## Azure Kubernetes Service version

Azure Kubernetes Service allows you to create a cluster using a variety of Kubernetes versions. For more information on available versions, see [supported Kubernetes versions in Azure Kubernetes Service](/azure/aks/supported-kubernetes-versions).

When **creating** an Azure Kubernetes Service cluster using one of the following methods, you *do not have a choice in the version* of the cluster that is created:

* Azure Machine Learning studio, or the Azure Machine Learning section of the Azure portal.
* Machine Learning extension for Azure CLI.
* Azure Machine Learning SDK.

These methods of creating an AKS cluster use the __default__ version of the cluster. *The default version changes over time* as new Kubernetes versions become available.

When **attaching** an existing AKS cluster, we support all currently supported AKS versions.

> [!IMPORTANT]
> Azure Kubernetes Service uses [Blobfuse FlexVolume driver](https://github.com/Azure/kubernetes-volume-drivers/blob/master/flexvolume/blobfuse/README.md) for the versions <=1.16 and [Blob CSI driver](https://github.com/kubernetes-sigs/blob-csi-driver/blob/master/README.md) for the versions >=1.17. 
> Therefore, it is important to re-deploy or [update the web service](../how-to-deploy-update-web-service.md) after cluster upgrade in order to deploy to correct blobfuse method for the cluster version.

> [!NOTE]
> There may be edge cases where you have an older cluster that is no longer supported. In this case, the attach operation will return an error and list the currently supported versions.
>
> You can attach **preview** versions. Preview functionality is provided without a service level agreement, and it's not recommended for production workloads. Certain features might not be supported or might have constrained capabilities. Support for using preview versions may be limited. For more information, see [Supplemental Terms of Use for Microsoft Azure Previews](https://azure.microsoft.com/support/legal/preview-supplemental-terms/).

### Available and default versions

To find the available and default AKS versions, use the [Azure CLI](/cli/azure/install-azure-cli) command [az aks get-versions](/cli/azure/aks#az-aks-get-versions). For example, the following command returns the versions available in the West US region:

```azurecli-interactive
az aks get-versions -l westus -o table
```

The output of this command is similar to the following text:

```text
KubernetesVersion    Upgrades
-------------------  ----------------------------------------
1.18.6(preview)      None available
1.18.4(preview)      1.18.6(preview)
1.17.9               1.18.4(preview), 1.18.6(preview)
1.17.7               1.17.9, 1.18.4(preview), 1.18.6(preview)
1.16.13              1.17.7, 1.17.9
1.16.10              1.16.13, 1.17.7, 1.17.9
1.15.12              1.16.10, 1.16.13
1.15.11              1.15.12, 1.16.10, 1.16.13
```

To find the default version that is used when **creating** a cluster through Azure Machine Learning, you can use the `--query` parameter to select the default version:

```azurecli-interactive
az aks get-versions -l westus --query "orchestrators[?default == `true`].orchestratorVersion" -o table
```

The output of this command is similar to the following text:

```text
Result
--------
1.16.13
```

If you'd like to **programmatically check the available versions**, use the Container Service Client - List Orchestrators REST API. To find the available versions, look at the entries where `orchestratorType` is `Kubernetes`. The associated `orchestrationVersion` entries contain the available versions that can be **attached** to your workspace.

To find the default version that is used when **creating** a cluster through Azure Machine Learning, find the entry where `orchestratorType` is `Kubernetes` and `default` is `true`. The associated `orchestratorVersion` value is the default version. The following JSON snippet shows an example entry:

```json
...
 {
        "orchestratorType": "Kubernetes",
        "orchestratorVersion": "1.16.13",
        "default": true,
        "upgrades": [
          {
            "orchestratorType": "",
            "orchestratorVersion": "1.17.7",
            "isPreview": false
          }
        ]
      },
...
```

## Create a new AKS cluster

**Time estimate**: Approximately 10 minutes.

Creating or attaching an AKS cluster is a one time process for your workspace. You can reuse this cluster for multiple deployments. If you delete the cluster or the resource group that contains it, you must create a new cluster the next time you need to deploy. You can have multiple AKS clusters attached to your workspace.

The following example demonstrates how to create a new AKS cluster using the SDK and CLI:

# [Python SDK](#tab/python)

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

```python
from azureml.core.compute import AksCompute, ComputeTarget

# Use the default configuration (you can also provide parameters to customize this).
# For example, to create a dev/test cluster, use:
# prov_config = AksCompute.provisioning_configuration(cluster_purpose = AksCompute.ClusterPurpose.DEV_TEST)
prov_config = AksCompute.provisioning_configuration()

# Example configuration to use an existing virtual network
# prov_config.vnet_name = "mynetwork"
# prov_config.vnet_resourcegroup_name = "mygroup"
# prov_config.subnet_name = "default"
# prov_config.service_cidr = "10.0.0.0/16"
# prov_config.dns_service_ip = "10.0.0.10"
# prov_config.docker_bridge_cidr = "172.17.0.1/16"

aks_name = 'myaks'
# Create the cluster
aks_target = ComputeTarget.create(workspace = ws,
                                    name = aks_name,
                                    provisioning_configuration = prov_config)

# Wait for the create process to complete
aks_target.wait_for_completion(show_output = True)
```

For more information on the classes, methods, and parameters used in this example, see the following reference documents:

* [AksCompute.ClusterPurpose](/python/api/azureml-core/azureml.core.compute.aks.akscompute.clusterpurpose)
* [AksCompute.provisioning_configuration](/python/api/azureml-core/azureml.core.compute.akscompute#provisioning-configuration-agent-count-none--vm-size-none--ssl-cname-none--ssl-cert-pem-file-none--ssl-key-pem-file-none--location-none--vnet-resourcegroup-name-none--vnet-name-none--subnet-name-none--service-cidr-none--dns-service-ip-none--docker-bridge-cidr-none--cluster-purpose-none--load-balancer-type-none--load-balancer-subnet-none-)
* [ComputeTarget.create](/python/api/azureml-core/azureml.core.compute.computetarget#create-workspace--name--provisioning-configuration-)
* [ComputeTarget.wait_for_completion](/python/api/azureml-core/azureml.core.compute.computetarget#wait-for-completion-show-output-false-)

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v1](../includes/machine-learning-cli-v1.md)]

```azurecli
az ml computetarget create aks -n myaks
```

For more information, see the [az ml computetarget create aks](/cli/azure/ml(v1)/computetarget/create#az-ml-computetarget-create-aks) reference.

# [Studio](#tab/azure-studio)

For information on creating an AKS cluster in the portal, see [Create compute targets in Azure Machine Learning studio](../how-to-create-attach-compute-studio.md#other-compute-targets).

---

## Attach an existing AKS cluster

**Time estimate:** Approximately 5 minutes.

If you already have AKS cluster in your Azure subscription, you can use it with your workspace.

> [!TIP]
> The existing AKS cluster can be in a Azure region other than your Azure Machine Learning workspace.


> [!WARNING]
> **Do not** create multiple, simultaneous attachments to the same AKS cluster. For example, attaching one AKS cluster to a workspace using two different names, or attaching one AKS cluster to different workspace. Each new attachment will break the previous existing attachment(s), and cause unpredictable error.
>
> If you want to re-attach an AKS cluster, for example to change TLS or other cluster configuration setting, you must first remove the existing attachment by using [AksCompute.detach()](/python/api/azureml-core/azureml.core.compute.akscompute#detach--).

For more information on creating an AKS cluster using the Azure CLI or portal, see the following articles:

* [Create an AKS cluster (CLI)](/cli/azure/aks?bc=/azure/bread/toc.json&toc=/azure/aks/TOC.json#az-aks-create)
* [Create an AKS cluster (portal)](/azure/aks/learn/quick-kubernetes-deploy-portal)
* [Create an AKS cluster (ARM Template on Azure Quickstart Templates)](https://github.com/Azure/azure-quickstart-templates/tree/master/quickstarts/microsoft.containerinstance/aks-azml-targetcompute)

The following example demonstrates how to attach an existing AKS cluster to your workspace:

# [Python SDK](#tab/python)

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

```python
from azureml.core.compute import AksCompute, ComputeTarget
# Set the resource group that contains the AKS cluster and the cluster name
resource_group = 'myresourcegroup'
cluster_name = 'myexistingcluster'

# Attach the cluster to your workgroup. If the cluster has less than 12 virtual CPUs, use the following instead:
# attach_config = AksCompute.attach_configuration(resource_group = resource_group,
#                                         cluster_name = cluster_name,
#                                         cluster_purpose = AksCompute.ClusterPurpose.DEV_TEST)
attach_config = AksCompute.attach_configuration(resource_group = resource_group,
                                         cluster_name = cluster_name)
aks_target = ComputeTarget.attach(ws, 'myaks', attach_config)

# Wait for the attach process to complete
aks_target.wait_for_completion(show_output = True)
```

For more information on the classes, methods, and parameters used in this example, see the following reference documents:

* [AksCompute.attach_configuration()](/python/api/azureml-core/azureml.core.compute.akscompute#attach-configuration-resource-group-none--cluster-name-none--resource-id-none--cluster-purpose-none-)
* [AksCompute.ClusterPurpose](/python/api/azureml-core/azureml.core.compute.aks.akscompute.clusterpurpose)
* [AksCompute.attach](/python/api/azureml-core/azureml.core.compute.computetarget#attach-workspace--name--attach-configuration-)

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v1](../includes/machine-learning-cli-v1.md)]

To attach an existing cluster using the CLI, you need to get the resource ID of the existing cluster. To get this value, use the following command. Replace `myexistingcluster` with the name of your AKS cluster. Replace `myresourcegroup` with the resource group that contains the cluster:

```azurecli
az aks show -n myexistingcluster -g myresourcegroup --query id
```

This command returns a value similar to the following text:

```text
/subscriptions/{GUID}/resourcegroups/{myresourcegroup}/providers/Microsoft.ContainerService/managedClusters/{myexistingcluster}
```

To attach the existing cluster to your workspace, use the following command. Replace `aksresourceid` with the value returned by the previous command. Replace `myresourcegroup` with the resource group that contains your workspace. Replace `myworkspace` with your workspace name.

```azurecli
az ml computetarget attach aks -n myaks -i aksresourceid -g myresourcegroup -w myworkspace
```

For more information, see the [az ml computetarget attach aks](/cli/azure/ml(v1)/computetarget/attach#az-ml-computetarget-attach-aks) reference.

# [Studio](#tab/azure-studio)

For information on attaching an AKS cluster in the studio, see [Create compute targets in Azure Machine Learning studio](../how-to-create-attach-compute-studio.md#other-compute-targets).

---

## Create or attach an AKS cluster with TLS termination
When you [create or attach an AKS cluster](how-to-create-attach-kubernetes.md), you can enable TLS termination with **[AksCompute.provisioning_configuration()](/python/api/azureml-core/azureml.core.compute.akscompute#provisioning-configuration-agent-count-none--vm-size-none--ssl-cname-none--ssl-cert-pem-file-none--ssl-key-pem-file-none--location-none--vnet-resourcegroup-name-none--vnet-name-none--subnet-name-none--service-cidr-none--dns-service-ip-none--docker-bridge-cidr-none--cluster-purpose-none--load-balancer-type-none--load-balancer-subnet-none-)** and **[AksCompute.attach_configuration()](/python/api/azureml-core/azureml.core.compute.akscompute#attach-configuration-resource-group-none--cluster-name-none--resource-id-none--cluster-purpose-none-)** configuration objects. Both methods return a configuration object that has an **enable_ssl** method, and you can use **enable_ssl** method to enable TLS.

Following example shows how to enable TLS termination with automatic TLS certificate generation and configuration by using Microsoft certificate under the hood.

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

```python
   from azureml.core.compute import AksCompute, ComputeTarget
   
   # Enable TLS termination when you create an AKS cluster by using provisioning_config object enable_ssl method

   # Leaf domain label generates a name using the formula
   # "<leaf-domain-label>######.<azure-region>.cloudapp.azure.com"
   # where "######" is a random series of characters
   provisioning_config.enable_ssl(leaf_domain_label = "contoso")
   
   # Enable TLS termination when you attach an AKS cluster by using attach_config object enable_ssl method

   # Leaf domain label generates a name using the formula
   # "<leaf-domain-label>######.<azure-region>.cloudapp.azure.com"
   # where "######" is a random series of characters
   attach_config.enable_ssl(leaf_domain_label = "contoso")


```
Following example shows how to enable TLS termination with custom certificate and custom domain name. With custom domain and certificate, you must update your DNS record to point to the IP address of scoring endpoint, please see [Update your DNS](../how-to-secure-web-service.md#update-your-dns)

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

```python
   from azureml.core.compute import AksCompute, ComputeTarget

   # Enable TLS termination with custom certificate and custom domain when creating an AKS cluster
   
   provisioning_config.enable_ssl(ssl_cert_pem_file="cert.pem",
                                        ssl_key_pem_file="key.pem", ssl_cname="www.contoso.com")
    
   # Enable TLS termination with custom certificate and custom domain when attaching an AKS cluster

   attach_config.enable_ssl(ssl_cert_pem_file="cert.pem",
                                        ssl_key_pem_file="key.pem", ssl_cname="www.contoso.com")


```
>[!NOTE]
> For more information about how to secure model deployment on AKS cluster, please see [use TLS to secure a web service through Azure Machine Learning](../how-to-secure-web-service.md)

## Create or attach an AKS cluster to use Internal Load Balancer with private IP

When you create or attach an AKS cluster, you can configure the cluster to use an Internal Load Balancer. With an Internal Load Balancer, scoring endpoints for your deployments to AKS will use a private IP within the virtual network. Following code snippets show how to configure an Internal Load Balancer for an AKS cluster.

# [Create](#tab/akscreate)

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

To create an AKS cluster that uses an Internal Load Balancer, use the `load_balancer_type` and `load_balancer_subnet` parameters:

```python
from azureml.core.compute.aks import AksUpdateConfiguration
from azureml.core.compute import AksCompute, ComputeTarget

# When you create an AKS cluster, you can specify Internal Load Balancer to be created with provisioning_config object
provisioning_config = AksCompute.provisioning_configuration(load_balancer_type = 'InternalLoadBalancer')

# Create the cluster
aks_target = ComputeTarget.create(workspace = ws,
                                name = aks_name,
                                provisioning_configuration = provisioning_config)

# Wait for the create process to complete
aks_target.wait_for_completion(show_output = True)
```

# [Attach](#tab/aksattach)

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

To attach an AKS cluster and use an internal load balancer (no public IP for the cluster), use the `load_balancer_type` and `load_balancer_subnet` parameters:

```python
from azureml.core.compute import AksCompute, ComputeTarget
# Set the resource group that contains the AKS cluster and the cluster name
resource_group = 'myresourcegroup'
cluster_name = 'myexistingcluster'
# Change to the name of the subnet that contains AKS
subnet_name = "default"

# Attach the cluster to your workgroup. If the cluster has less than 12 virtual CPUs, use the following instead:
# attach_config = AksCompute.attach_configuration(resource_group = resource_group,
#                                         cluster_name = cluster_name,
#                                         cluster_purpose = AksCompute.ClusterPurpose.DEV_TEST)
attach_config = AksCompute.attach_configuration(resource_group = resource_group,
                                         cluster_name = cluster_name,
                                         load_balancer_type = 'InternalLoadBalancer', 
                                         load_balancer_subnet = subnet_name)
aks_target = ComputeTarget.attach(ws, 'myaks', attach_config)

# Wait for the attach process to complete
aks_target.wait_for_completion(show_output = True)
```

---

>[!IMPORTANT]
> If your AKS cluster is configured with an Internal Load Balancer, using a Microsoft provided certificate is not supported and you must use [custom certificate to enable TLS](../how-to-secure-web-service.md#deploy-on-azure-kubernetes-service). 

>[!NOTE]
> For more information about how to secure inferencing environment, please see [Secure an Azure Machine Learning Inferencing Environment](how-to-secure-inferencing-vnet.md)

## Detach an AKS cluster

To detach a cluster from your workspace, use one of the following methods:

> [!WARNING]
> Using the Azure Machine Learning studio, SDK, or the Azure CLI extension for machine learning to detach an AKS cluster **does not delete the AKS cluster**. To delete the cluster, see [Use the Azure CLI with AKS](/azure/aks/learn/quick-kubernetes-deploy-cli#delete-the-cluster).

# [Python SDK](#tab/python)

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

```python
aks_target.detach()
```

# [Azure CLI](#tab/azure-cli)

[!INCLUDE [cli v1](../includes/machine-learning-cli-v1.md)]

To detach the existing cluster to your workspace, use the following command. Replace `myaks` with the name that the AKS cluster is attached to your workspace as. Replace `myresourcegroup` with the resource group that contains your workspace. Replace `myworkspace` with your workspace name.

```azurecli
az ml computetarget detach -n myaks -g myresourcegroup -w myworkspace
```

# [Studio](#tab/azure-studio)

In Azure Machine Learning studio, select __Compute__, __Inference clusters__, and the cluster you wish to remove. Use the __Detach__ link to detach the cluster.

---

## Troubleshooting
### Update the cluster

Updates to Azure Machine Learning components installed in an Azure Kubernetes Service cluster must be manually applied. 

You can apply these updates by detaching the cluster from the Azure Machine Learning workspace and reattaching the cluster to the workspace. 

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

```python
compute_target = ComputeTarget(workspace=ws, name=clusterWorkspaceName)
compute_target.detach()
compute_target.wait_for_completion(show_output=True)
```

Before you can re-attach the cluster to your workspace, you need to first delete any `azureml-fe` related resources. If there is no active service in the cluster, you can delete your `azureml-fe` related resources with the following code. 

```shell
kubectl delete sa azureml-fe
kubectl delete clusterrole azureml-fe-role
kubectl delete clusterrolebinding azureml-fe-binding
kubectl delete svc azureml-fe
kubectl delete svc azureml-fe-int-http
kubectl delete deploy azureml-fe
kubectl delete secret azuremlfessl
kubectl delete cm azuremlfeconfig
```

If TLS is enabled in the cluster, you will need to supply the TLS/SSL certificate and private key when reattaching the cluster.

[!INCLUDE [sdk v1](../includes/machine-learning-sdk-v1.md)]

```python
attach_config = AksCompute.attach_configuration(resource_group=resourceGroup, cluster_name=kubernetesClusterName)

# If SSL is enabled.
attach_config.enable_ssl(
    ssl_cert_pem_file="cert.pem",
    ssl_key_pem_file="key.pem",
    ssl_cname=sslCname)

attach_config.validate_configuration()

compute_target = ComputeTarget.attach(workspace=ws, name=args.clusterWorkspaceName, attach_configuration=attach_config)
compute_target.wait_for_completion(show_output=True)
```

If you no longer have the TLS/SSL certificate and private key, or you are using a certificate generated by Azure Machine Learning, you can retrieve the files prior to detaching the cluster by connecting to the cluster using `kubectl` and retrieving the secret `azuremlfessl`.

```bash
kubectl get secret/azuremlfessl -o yaml
```

> [!NOTE]
> Kubernetes stores the secrets in Base64-encoded format. You will need to Base64-decode the `cert.pem` and `key.pem` components of the secrets prior to providing them to `attach_config.enable_ssl`. 

### Webservice failures

Many webservice failures in AKS can be debugged by connecting to the cluster using `kubectl`. You can get the `kubeconfig.json` for an AKS cluster by running

[!INCLUDE [cli v1](../includes/machine-learning-cli-v1.md)]

```azurecli-interactive
az aks get-credentials -g <rg> -n <aks cluster name>
```

### Delete azureml-fe related resources

After detaching cluster, if there is none active service in cluster, please delete the `azureml-fe` related resources before attaching again:

```shell
kubectl delete sa azureml-fe
kubectl delete clusterrole azureml-fe-role
kubectl delete clusterrolebinding azureml-fe-binding
kubectl delete svc azureml-fe
kubectl delete svc azureml-fe-int-http
kubectl delete deploy azureml-fe
kubectl delete secret azuremlfessl
kubectl delete cm azuremlfeconfig
```

### Load balancers should not have public IPs

When trying to create or attach an AKS cluster, you may receive a message that the request has been denied because "Load Balancers should not have public IPs". This message is returned when an administrator has applied a policy that prevents using an AKS cluster with a public IP address.

To resolve this problem, create/attach the cluster by using the `load_balancer_type` and `load_balancer_subnet` parameters. For more information, see  [Internal Load Balancer (private IP)](#create-or-attach-an-aks-cluster-to-use-internal-load-balancer-with-private-ip).

## Next steps

* [Use Azure RBAC for Kubernetes authorization](/azure/aks/manage-azure-rbac)
* [How and where to deploy a model](how-to-deploy-and-where.md)
