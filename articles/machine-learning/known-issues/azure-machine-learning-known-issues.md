---
title: Azure Machine Learning known issues
description: Identify issues that are affecting Azure Machine Learning features. 
author: s-polly
ms.author: scottpolly
ms.topic: troubleshooting    
ms.service: azure-machine-learning
ms.subservice: core
ms.date: 11/07/2025
ms.update-cycle: 365-days
ms.custom:  
---

# Azure Machine Learning known issues

This article lists known issues for Azure Machine Learning features. Before submitting a support request, review this list to see if the issue that you're experiencing is already known and being addressed. 


## Currently active known issues

The following table lists known issues that currently affect Azure Machine Learning features.

| Issue ID | Category | Title | Description | Workaround | Issue Publish Date |
|----------|----------|-------|-------------|------------|-------------------|
| 1001 | Inferencing | Invalid certificate error during deployment with an AKS cluster | During machine learning deployments using an AKS cluster, you might receive an invalid certificate error, such as this. This error occurs because the certificate for AKS clusters created before Jan 2021 doesn't include the Subject Key Identifier value, which prevents the required Authority Key Identifier value from being generated. | Rotate the AKS certificate for the cluster. See [Certificate Rotation in Azure Kubernetes Services (AKS)](/azure/aks/certificate-rotation) for more information. Wait for 5 hours for the certificate to be automatically updated, and the issue should be resolved. | September 26, 2023 |
| 1002 | Inferencing | Existing Kubernetes compute can't be updated with `az ml compute attached` command | Updating a Kubernetes attached compute instance by using the `az ml compute attached` command appears to succeed but doesn't. When running the command `az ml compute attached --resource-group <resource-group-name> --workspace-name <workspace-name> --type Kubernetes --name <existing-attached-compute-name> --resource-id "<cluster-resource-id>" --namespace <kubernetes-namespace>`, The CLI returns a success message indicating that the compute has been successfully updated. However, the compute isn't updated. | No workaround. The `az ml compute attached` command currently doesn't support updating existing Kubernetes compute. | September 26, 2023 |
| 1003 | Azure Container Registry | Can't remove ACR reference from Microsoft Foundry or Azure Machine Learning config once configured | ACR (Azure Container Registry) is an optional dependent resource. Foundry or Azure Machine Learning workspace doesn't require an ACR to be created or attached while the workspace is created. The default value is set to null. However, if you attach an ACR or create an ACR for the given workspace, you can't remove it. If you try to update the workspace using CLI to set the Container Registry as null, the command doesn't throw any error, but it won't reset the configuration of ACR reference to null. | No workaround. This isn't supported. You can create a workspace with null ACR, but once it's updated you can't set it back to null. | September 25, 2025 |
| 1004 | Prompt Flow | Missing trace info in LLM tool output | When you configure prompt flow from studio UI with LLM tool, you notice that the tracing tab is empty. This issue occurs because tracing is disabled in the PF by default since tracing causes issues due to OpenAI API changes on how and where to pull token information from | Enable the PF in the flow.diag.yaml by setting environment variable pF_DISABLE_TRACING to False. Follow steps here and here. | September 25, 2025 |
| 1005 | Prompt Flow | PFAzure always uses Default Azure Credential | While using the prompt flow CLI pfazure, it doesn't pick up the authentication of az login user credentials. It always uses first the default Azure credential despite using az login. This issue can break authentication if the default Azure credentials or managed identity is misconfigured and it never falls back to the az login credentials that the user provides. | Pfazure relies on defaultAzureCredential for authentication and this issue is by design. One of the steps in this chain uses user credential from az login. Please ensure no other auth method before that is used. One possible case could be the environment variables, as they might interfere with the credential chain: EnvironmentCredential. Please check if any of the environment variables listed in the documentation are set, and remove them if necessary. Learn more here. | September 25, 2025 |
| 1006 | Terraform | Timeouts adding FQDN outbound rules with Terraform. | While using Terraform to provision workspaces with managed network with FQDN outbound rules, you might experience timeout if you try to bulk add the outbound rules using CSV. Previously, you were able to use comma separate values for your outbound rules. | The Azure Machine Learning workspace API supports multiple outbound rules, but this support isn't currently available in the `azurerm_machine_learning_workspace` resource. We suggest adding azapi_update_resource with type "Microsoft.MachineLearningServices/workspaces@2024-04-01" resource to make an update call to add all the outbound rules. Steps for doing this are here. | September 25, 2025 |
| 1007 | Networking | Azure Load Balancer rule for Managed VNET AOAO isn't supported | When you try to add a service tag rule for Allow Approved Outbound (AOAO) in managed VNet for Azure load balancer, it fails with the following error "Service tag AzureLoadBalancer not supported with FQDN Rules. Please remove the invalid servicetag rule test-datadog and retry". | This issue is by design. The service tag for AzureLoadBalancer isn't supported here. Relevant documentation is here. There are no workarounds. | September 25, 2025 |
 


## Next steps


- [See Azure service level outages](https://azure.status.microsoft/status)
- [Get your questions answered by the Azure Machine Learning community](/answers/tags/75/azure-machine-learning)
- 