---
title: Deploy Azure Machine Learning extension on Kubernetes cluster
description: Learn about the Azure Machine Learning extension, available configuration settings, and different deployment scenarios, and verify and managed Azure Machine Learning extension
titleSuffix: Azure Machine Learning
author: s-polly
ms.author: scottpolly
ms.reviewer: bozhlin
ms.service: azure-machine-learning
ms.subservice: core
ms.date: 01/28/2026
ms.topic: how-to
ms.custom: cliv2, sdkv2, devx-track-azurecli, dev-focus
ai-usage: ai-assisted
---

# Deploy Azure Machine Learning extension on Azure Kubernetes Service (AKS) or Azure Arc-enabled Kubernetes cluster

To enable your Azure Kubernetes Service (AKS) or Azure Arc-enabled Kubernetes cluster to run training jobs or inference workloads, first deploy the Azure Machine Learning extension. The Azure Machine Learning extension is a [Standard cluster extension for AKS](/azure/aks/cluster-extensions) and [cluster extension for Azure Arc-enabled Kubernetes](/azure/azure-arc/kubernetes/conceptual-extensions). You can manage its lifecycle by using Azure CLI [k8s-extension](/cli/azure/k8s-extension).

In this article, you learn about:
> [!div class="checklist"]
> * Prerequisites
> * Limitations
> * Review Azure Machine Learning extension config settings 
> * Azure Machine Learning extension deployment scenarios
> * Verify Azure Machine Learning extension deployment
> * Review Azure Machine Learning extension components
> * Manage Azure Machine Learning extension

## Prerequisites

* An AKS cluster running in Azure. If you didn't previously use cluster extensions, you need to [register the KubernetesConfiguration service provider](/azure/aks/dapr#register-the-kubernetesconfiguration-resource-provider).
* Or an Azure Arc-enabled Kubernetes cluster that's up and running. Follow instructions in [connect existing Kubernetes cluster to Azure Arc](/azure/azure-arc/kubernetes/quickstart-connect-cluster).
  * If the cluster is an Azure RedHat OpenShift (ARO) Service cluster or OpenShift Container Platform (OCP) cluster, you must satisfy other prerequisite steps as documented in the [Reference for configuring Kubernetes cluster](./reference-kubernetes.md#prerequisites-for-aro-or-ocp-clusters) article.
* For production purposes, the Kubernetes cluster must have a minimum of **4 vCPU cores and 14-GB memory**. For more information on resource detail and cluster size recommendations, see [Recommended resource planning](./reference-kubernetes.md).
* A cluster running behind an **outbound proxy server** or **firewall** needs extra [network configurations](./how-to-access-azureml-behind-firewall.md#scenario-use-kubernetes-compute).
* Install or upgrade Azure CLI to version 2.51.0 or higher.
* Install or upgrade Azure CLI extension `k8s-extension` to version 1.2.3 or higher.
  

## Limitations

- Azure Machine Learning **doesn't support** [using a service principal with AKS](/azure/aks/kubernetes-service-principal). The AKS cluster must use a **managed identity** instead. Both **system-assigned managed identity** and **user-assigned managed identity** are supported. For more information, see [Use a managed identity in Azure Kubernetes Service](/azure/aks/use-managed-identity).
    - When you convert your AKS cluster from using a service principal to using managed identity, you need to delete and recreate all node pools before installing the extension. You can't directly update the node pools.
- Azure Machine Learning **doesn't support** [disabling local accounts](/azure/aks/local-accounts#disable-local-accounts) for AKS. When you deploy the AKS cluster, local accounts are enabled by default.
- If your AKS cluster has an [Authorized IP range enabled to access the API server](/azure/aks/api-server-authorized-ip-ranges), you must enable the Azure Machine Learning control plane IP ranges for the AKS cluster. The Azure Machine Learning control plane is deployed across paired regions. Without access to the API server, the machine learning pods can't be deployed. Use the [IP ranges](https://www.microsoft.com/en-us/download/details.aspx?id=56519) for both the [paired regions](/azure/reliability/cross-region-replication-azure) when enabling the IP ranges in an AKS cluster.
- Azure Machine Learning doesn't support attaching an AKS cluster cross subscription. If you have an AKS cluster in a different subscription, you must first [connect it to Azure Arc](/azure/azure-arc/kubernetes/quickstart-connect-cluster) and specify in the same subscription as your Azure Machine Learning workspace.
- Azure Machine Learning doesn't guarantee support for all preview stage features in AKS. For example, [Microsoft Entra pod-managed identity](/azure/aks/use-azure-ad-pod-identity) (deprecated) isn't supported. Use [Microsoft Entra Workload ID](/azure/aks/workload-identity-overview) instead.
- If you followed the steps in the [Azure Machine Learning AKS v1 document](v1/how-to-create-attach-kubernetes.md) to create or attach your AKS as an inference cluster, use the following link to [clean up the legacy azureml-fe related resources](v1/how-to-create-attach-kubernetes.md#delete-azureml-fe-related-resources) before you continue the next step.


## Review Azure Machine Learning extension configuration settings

Use the Azure CLI command `az k8s-extension create` to deploy the Azure Machine Learning extension. The `az k8s-extension create` command accepts configuration settings as space-separated `key=value` pairs through the `--config` or `--config-protected` parameter. The following table lists the available configuration settings you can specify during deployment.

|Configuration Setting Key Name  |Description  |Training |Inference |Training and Inference
   |--|--|--|--|--|
   |`enableTraining` |`True` or `False`, default `False`. **Must** be set to `True` for Azure Machine Learning extension deployment with Machine Learning model training and batch scoring support.  |  **&check;**| N/A |  **&check;** |
   | `enableInference` |`True` or `False`, default `False`.  **Must** be set to `True` for Azure Machine Learning extension deployment with Machine Learning inference support. |N/A| **&check;** |  **&check;** |
   | `allowInsecureConnections` |`True` or `False`, default `False`. **Can** be set to `True` to use inference HTTP endpoints for development or test purposes. |N/A| Optional |  Optional |
   | `inferenceRouterServiceType` |`loadBalancer`, `nodePort`, or `clusterIP`. **Required** if `enableInference=True`. | N/A| **&check;** |   **&check;** |
   | `internalLoadBalancerProvider` | This config is only applicable for Azure Kubernetes Service(AKS) cluster now. Set to `azure` to allow the inference router using internal load balancer.  | N/A| Optional |  Optional |
   |`sslSecret`| The name of the Kubernetes secret in the `azureml` namespace. This config is used to store `cert.pem` (PEM-encoded TLS/SSL cert) and `key.pem` (PEM-encoded TLS/SSL key), which are required for inference HTTPS endpoint support when ``allowInsecureConnections`` is set to `False`. For a sample YAML definition of `sslSecret`, see [Configure sslSecret](./how-to-secure-kubernetes-online-endpoint.md). Use this config or a combination of `sslCertPemFile` and `sslKeyPemFile` protected config settings. |N/A| Optional |  Optional |
   |`sslCname` |An TLS/SSL CNAME is used by inference HTTPS endpoint. **Required** if `allowInsecureConnections=False`  |  N/A | Optional | Optional|
   | `inferenceRouterHA` |`True` or `False`, default `True`. By default, Azure Machine Learning extension deploys three inference router replicas for high availability, which requires at least three worker nodes in a cluster. Set to `False` if your cluster has fewer than three worker nodes, in this case only one inference router service is deployed. | N/A| Optional |  Optional |
   |`nodeSelector` | By default, the deployed kubernetes resources and your machine learning workloads are randomly deployed to one or more nodes of the cluster, and DaemonSet resources are deployed to ALL nodes. If you want to restrict the extension deployment and your training/inference workloads to specific nodes with label `key1=value1` and `key2=value2`, use `nodeSelector.key1=value1`, `nodeSelector.key2=value2` correspondingly. | Optional| Optional |  Optional |
   |`installNvidiaDevicePlugin`  | `True` or `False`, default `False`. [NVIDIA Device Plugin](https://github.com/NVIDIA/k8s-device-plugin#nvidia-device-plugin-for-kubernetes) is required for ML workloads on NVIDIA GPU hardware. By default, Azure Machine Learning extension deployment won't install NVIDIA Device Plugin regardless Kubernetes cluster has GPU hardware or not. User can specify this setting to `True`, to install it, but make sure to fulfill [Prerequisites](https://github.com/NVIDIA/k8s-device-plugin#prerequisites). | Optional |Optional |Optional |
   |`installPromOp`|`True` or `False`, default `True`. Azure Machine Learning extension needs prometheus operator to manage prometheus. Set to `False` to reuse the existing prometheus operator. For more information about reusing the existing  prometheus operator, see [reusing the prometheus operator](./how-to-troubleshoot-kubernetes-extension.md#prometheus-operator)| Optional| Optional |  Optional |
   |`installVolcano`| `True` or `False`, default `True`. Azure Machine Learning extension needs volcano scheduler to schedule the job. Set to `False` to reuse existing volcano scheduler. For more information about reusing the existing volcano scheduler, see [reusing volcano scheduler](./how-to-troubleshoot-kubernetes-extension.md#volcano-scheduler)   | Optional| N/A |  Optional |
   |`installDcgmExporter`  |`True` or `False`, default `False`. Dcgm-exporter can expose GPU metrics for Azure Machine Learning workloads, which can be monitored in Azure portal. Set `installDcgmExporter`  to `True` to install dcgm-exporter. But if you want to utilize your own dcgm-exporter, see [DCGM exporter](./how-to-troubleshoot-kubernetes-extension.md#dcgm-exporter) |Optional |Optional |Optional |


   |Configuration Protected Setting Key Name  |Description  |Training |Inference |Training and Inference
   |--|--|--|--|--|
   | `sslCertPemFile`, `sslKeyPemFile` |Path to TLS/SSL certificate and key file (PEM-encoded), required for Azure Machine Learning extension deployment with inference HTTPS endpoint support, when  ``allowInsecureConnections`` is set to False. **Note** PEM file with pass phrase protected isn't supported | N/A| Optional |  Optional |

As you can see from the configuration settings table, the combinations of different configuration settings allow you to deploy Azure Machine Learning extension for different ML workload scenarios:

  * For training job and batch inference workload, specify `enableTraining=True`
  * For inference workload only, specify `enableInference=True`
  * For all kinds of ML workload, specify both `enableTraining=True` and `enableInference=True`

If you plan to deploy Azure Machine Learning extension for real-time inference workload and want to specify `enableInference=True`, pay attention to following configuration settings related to real-time inference workload:

  * `azureml-fe` router service is required for real-time inference support and you need to specify `inferenceRouterServiceType` config setting for `azureml-fe`. `azureml-fe` can be deployed with one of following `inferenceRouterServiceType`:
      * Type `loadBalancer`. Exposes `azureml-fe` externally using a cloud provider's load balancer. To specify this value, ensure that your cluster supports load balancer provisioning. Note most on-premises Kubernetes clusters might not support external load balancer.
      * Type `nodePort`. Exposes `azureml-fe` on each Node's IP at a static port. You can contact `azureml-fe`, from outside of cluster, by requesting `<NodeIP>:<NodePort>`. Using `nodePort` also allows you to set up your own load balancing solution and TLS/SSL termination for `azureml-fe`. For more information on how to set up your own ingress, see [Integrate other ingress controller with Azure Machine Learning extension over HTTP or HTTPS](./reference-kubernetes.md#integrate-other-ingress-controller-with-azure-machine-learning-extension-over-http-or-https).
      * Type `clusterIP`. Exposes `azureml-fe` on a cluster-internal IP, and it makes `azureml-fe` only reachable from within the cluster. For `azureml-fe` to serve inference requests coming outside of cluster, it requires you to set up your own load balancing solution and TLS/SSL termination for `azureml-fe`. For more information on how to set up your own ingress, see [Integrate other ingress controller with Azure Machine Learning extension over HTTP or HTTPS](./reference-kubernetes.md#integrate-other-ingress-controller-with-azure-machine-learning-extension-over-http-or-https).
   * To ensure high availability of `azureml-fe` routing service, Azure Machine Learning extension deployment by default creates three replicas of `azureml-fe` for clusters having three nodes or more. If your cluster has **less than 3 nodes**, set `inferenceRouterHA=False`.
   * You also want to consider using **HTTPS** to restrict access to model endpoints and secure the data that clients submit. For this purpose, you need to specify either `sslSecret` config setting or combination of `sslKeyPemFile` and `sslCertPemFile` config-protected settings. 
   * By default, Azure Machine Learning extension deployment expects config settings for **HTTPS** support. For development or testing purposes, **HTTP** support is conveniently provided through config setting `allowInsecureConnections=True`.

## Azure Machine Learning extension deployment - CLI examples and Azure portal

### [Azure CLI](#tab/deploy-extension-with-cli)
To deploy the Azure Machine Learning extension by using CLI, use the `az k8s-extension create` command and provide values for the mandatory parameters.

The following list describes four typical extension deployment scenarios. To deploy the extension for your production usage, carefully read the complete list of [configuration settings](#review-azure-machine-learning-extension-configuration-settings).

- **Use AKS cluster in Azure for a quick proof of concept to run all kinds of ML workload, for example, to run training jobs or to deploy models as online/batch endpoints**

   For Azure Machine Learning extension deployment on AKS cluster, specify `managedClusters` value for `--cluster-type` parameter. Run the following Azure CLI command to deploy Azure Machine Learning extension:
   ```azurecli
   az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True enableInference=True inferenceRouterServiceType=loadBalancer allowInsecureConnections=True inferenceRouterHA=False --cluster-type managedClusters --cluster-name <your-AKS-cluster-name> --resource-group <your-RG-name> --scope cluster
   ```

- **Use an Azure Arc-enabled Kubernetes cluster outside of Azure for a quick proof of concept, to run training jobs only**

   For Azure Machine Learning extension deployment on an [Azure Arc-enabled Kubernetes](/azure/azure-arc/kubernetes/overview) cluster, specify `connectedClusters` value for `--cluster-type` parameter. Run the following Azure CLI command to deploy Azure Machine Learning extension:
   ```azurecli
   az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <your-RG-name> --scope cluster
   ```

- **Enable an AKS cluster in Azure for production training and inference workload**
   For Azure Machine Learning extension deployment on AKS, specify `managedClusters` value for `--cluster-type` parameter. Assuming your cluster has more than three nodes, and you use an Azure public load balancer and HTTPS for inference workload support. Run the following Azure CLI command to deploy Azure Machine Learning extension:
   ```azurecli
   az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True enableInference=True inferenceRouterServiceType=loadBalancer sslCname=<ssl cname> --config-protected sslCertPemFile=<file-path-to-cert-PEM> sslKeyPemFile=<file-path-to-cert-KEY> --cluster-type managedClusters --cluster-name <your-AKS-cluster-name> --resource-group <your-RG-name> --scope cluster
   ```
- **Enable an [Azure Arc-enabled Kubernetes](/azure/azure-arc/kubernetes/overview) cluster anywhere for production training and inference workload using NVIDIA GPUs**

   For Azure Machine Learning extension deployment on an [Azure Arc-enabled Kubernetes](/azure/azure-arc/kubernetes/overview) cluster, specify `connectedClusters` value for `--cluster-type` parameter. Assuming your cluster has more than three nodes, you use a NodePort service type and HTTPS for inference workload support, run following Azure CLI command to deploy Azure Machine Learning extension:
   ```azurecli
   az k8s-extension create --name <extension-name> --extension-type Microsoft.AzureML.Kubernetes --config enableTraining=True enableInference=True inferenceRouterServiceType=nodePort sslCname=<ssl cname> installNvidiaDevicePlugin=True installDcgmExporter=True --config-protected sslCertPemFile=<file-path-to-cert-PEM> sslKeyPemFile=<file-path-to-cert-KEY> --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <your-RG-name> --scope cluster
   ```

### [Azure portal](#tab/portal)

The UI experience to deploy an extension is only available for **[Azure Arc-enabled Kubernetes](/azure/azure-arc/kubernetes/overview)**. If you have an AKS cluster without Azure Arc connection, you need to use CLI to deploy Azure Machine Learning extension.

1. In the [Azure portal](https://portal.azure.com/#home), go to **Kubernetes - Azure Arc** and select your cluster.
1. Select **Extensions** (under **Settings**), and then select **+ Add**.

   :::image type="content" source="media/how-to-attach-kubernetes-to-workspace/deploy-extension-from-ui.png" alt-text="Screenshot of adding new extension to the Arc-enabled Kubernetes cluster from Azure portal.":::

1. From the list of available extensions, select **Azure Machine Learning extension** to deploy the latest version of the extension.

   :::image type="content" source="media/how-to-attach-kubernetes-to-workspace/deploy-extension-from-ui-extension-list.png" alt-text="Screenshot of selecting Azure Machine Learning extension from Azure portal.":::

1. Follow the prompts to deploy the extension. You can customize the installation by configuring the installation in the tab of **Basics**, **Configurations**, and **Advanced**. For a detailed list of Azure Machine Learning extension configuration settings, see [Azure Machine Learning extension configuration settings](#review-azure-machine-learning-extension-configuration-settings).

   :::image type="content" source="media/how-to-attach-kubernetes-to-workspace/deploy-extension-from-ui-settings.png" alt-text="Screenshot of configuring Azure Machine Learning extension settings from Azure portal.":::
1. On the **Review + create** tab, select **Create**.
   
   :::image type="content" source="media/how-to-attach-kubernetes-to-workspace/deploy-extension-from-ui-create.png" alt-text="Screenshot of deploying new extension to the Arc-enabled Kubernetes cluster from Azure portal.":::

1. After the deployment completes, you can see the Azure Machine Learning extension in **Extension** page. If the extension installation succeeds, you see **Installed** for the **Install status**.

   :::image type="content" source="media/how-to-attach-kubernetes-to-workspace/deploy-extension-from-ui-extension-detail.png" alt-text="Screenshot of installed Azure Machine Learning extensions listing in Azure portal.":::

---

### Verify Azure Machine Learning extension deployment

1. Run the applicable CLI command to check the Azure Machine Learning extension details:

   **AKS**

   ```azurecli
   az k8s-extension show --name <extension-name> --cluster-type managedClusters --cluster-name <your-AKS-cluster-name> --resource-group <resource-group>
   ```

   **Azure Arc-enabled Kubernetes**

   ```azurecli
   az k8s-extension show --name <extension-name> --cluster-type connectedClusters --cluster-name <your-connected-cluster-name> --resource-group <resource-group>
   ```

1. In the response, look for `"name"` and `"provisioningState": "Succeeded"`. It might show `"provisioningState": "Pending"` for the first few minutes.

1. If the provisioningState shows Succeeded, run the following command on your machine with the kubeconfig file pointed to your cluster to check that all pods under `azureml` namespace are in `Running` state:

   ```bash
    kubectl get pods -n azureml
   ```

## Review Azure Machine Learning extension component

When the Azure Machine Learning extension deployment finishes, use `kubectl get deployments -n azureml` to see the list of resources created in the cluster. The list usually consists of a subset of the following resources, depending on the configuration settings you specify. 

   |Resource name  |Resource type |Training |Inference |Training and Inference| Description | Communication with cloud|
   |--|--|--|--|--|--|--|
   |relayserver|Kubernetes deployment|**&check;**|**&check;**|**&check;**|The deployment creates the relay server only for Azure Arc-enabled Kubernetes clusters, and **not** in AKS clusters. Relay server works with Azure Relay to communicate with the cloud services.|Receive the request of job creation, model deployment from cloud service; sync the job status with cloud service.|
   |gateway|Kubernetes deployment|**&check;**|**&check;**|**&check;**|The gateway is used to communicate and send data back and forth.|Send nodes and cluster resource information to cloud services.|
   |aml-operator|Kubernetes deployment|**&check;**|N/A|**&check;**|Manage the lifecycle of training jobs.| Token exchange with the cloud token service for authentication and authorization of Azure Container Registry.|
   |metrics-controller-manager|Kubernetes deployment|**&check;**|**&check;**|**&check;**|Manage the configuration for Prometheus|N/A|
   |{EXTENSION-NAME}-kube-state-metrics|Kubernetes deployment|**&check;**|**&check;**|**&check;**|Export the cluster-related metrics to Prometheus.|N/A|
   |{EXTENSION-NAME}-prometheus-operator|Kubernetes deployment|Optional|Optional|Optional| Provide Kubernetes native deployment and management of Prometheus and related monitoring components.|N/A|
   |amlarc-identity-controller|Kubernetes deployment|N/A|**&check;**|**&check;**|Request and renew Azure Blob/Azure Container Registry token through managed identity.|Token exchange with the cloud token service for authentication and authorization of Azure Container  Registry and Azure Blob used by inference/model deployment.|
   |amlarc-identity-proxy|Kubernetes deployment|N/A|**&check;**|**&check;**|Request and renew Azure Blob/Azure Container Registry token  through managed identity.|Token exchange with the cloud token service for authentication and authorization of Azure Container  Registry and Azure Blob used by inference/model deployment.|
   |azureml-fe-v2|Kubernetes deployment|N/A|**&check;**|**&check;**|The front-end component that routes incoming inference requests to deployed services.|Send service logs to Azure Blob.|
   |inference-operator-controller-manager|Kubernetes deployment|N/A|**&check;**|**&check;**|Manage the lifecycle of inference endpoints. |N/A|
   |volcano-admission|Kubernetes deployment|Optional|N/A|Optional|Volcano admission webhook.|N/A|
   |volcano-controllers|Kubernetes deployment|Optional|N/A|Optional|Manage the lifecycle of Azure Machine Learning training job pods.|N/A|
   |volcano-scheduler |Kubernetes deployment|Optional|N/A|Optional|Used to perform in-cluster job scheduling.|N/A|
   |fluent-bit|Kubernetes daemonset|**&check;**|**&check;**|**&check;**|Gather the components' system log.| Upload the components' system log to cloud.|
   |{EXTENSION-NAME}-dcgm-exporter|Kubernetes daemonset|Optional|Optional|Optional|dcgm-exporter exposes GPU metrics for Prometheus.|N/A|
   |nvidia-device-plugin-daemonset|Kubernetes daemonset|Optional|Optional|Optional|nvidia-device-plugin-daemonset exposes GPUs on each node of your cluster| N/A|
   |prometheus-prom-prometheus|Kubernetes statefulset|**&check;**|**&check;**|**&check;**|Gather and send job metrics to cloud.|Send job metrics like cpu/gpu/memory utilization to cloud.|

> [!IMPORTANT]
   > * The Azure Relay resource is in the same resource group as the Arc cluster resource. It's used to communicate with the Kubernetes cluster. Modifying it breaks attached compute targets.
   > * By default, the deployment resources are randomly deployed to one or more nodes of the cluster, and daemonset resources are deployed to all nodes. To restrict the extension deployment to specific nodes, use the `nodeSelector` configuration setting described in the [configuration settings table](#review-azure-machine-learning-extension-configuration-settings).

> [!NOTE]
   > * **{EXTENSION-NAME}:** is the extension name you specify by using the `az k8s-extension create --name` CLI command. 


### Manage Azure Machine Learning extension

Update, list, show, and delete an Azure Machine Learning extension.

- For AKS clusters without Azure Arc connected, see [Deploy and manage cluster extensions](/azure/aks/deploy-extensions-az-cli).
- For Azure Arc-enabled Kubernetes, see [Deploy and manage Azure Arc-enabled Kubernetes cluster extensions](/azure/azure-arc/kubernetes/extensions).


## Next steps

- [Step 2: Attach Kubernetes cluster to workspace](how-to-attach-kubernetes-to-workspace.md)
- [Create and manage instance types](./how-to-manage-kubernetes-instance-types.md)
- [Azure Machine Learning inference router and connectivity requirements](./how-to-kubernetes-inference-routing-azureml-fe.md)
- [Secure AKS inferencing environment](./how-to-secure-kubernetes-inferencing-environment.md)
