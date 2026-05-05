---
title: Deploy open-source AI models with managed compute in Foundry
description: Learn how managed compute in Microsoft Foundry lets you deploy and serve open-source AI models on elastic GPU capacity without managing virtual machines, Kubernetes clusters, or model runtimes.
ms.service: microsoft-foundry
ms.subservice: foundry-model-inference
ms.custom:
  - build-2026
ms.topic: how-to
ms.date: 05/05/2026
ms.author: mopeakande
author: msakande
ms.reviewer: mabables
reviewer: ManojBableshwar
ai-usage: ai-assisted

#CustomerIntent: As an Azure AI developer, I want to use managed compute to deploy and serve open-source AI models on elastic GPU capacity without the operational burden of managing virtual machines, Kubernetes clusters, or model runtimes.
---

# Deploy open-source AI models with managed compute

<!-- Introduction: briefly explain what managed compute deployment is, why a developer would use it, and what this article covers (understanding the concept + completing a deployment). -->

## Prerequisites

<!-- List what the reader needs before they start: Azure subscription, Foundry project, required permissions (Cognitive Services Contributor or equivalent), Python version if code is shown, etc. -->

## What is managed compute deployment?

<!-- Explain the concept: managed compute as a deployment type in Foundry that handles infrastructure provisioning, GPU allocation, and model runtime management on behalf of the user. -->

## When to use managed compute

<!-- Describe the scenarios where managed compute is the right choice vs. other deployment types (serverless, provisioned). Include guidance on model types supported. -->

## Supported models

<!-- List or describe the categories of models that can be deployed with managed compute (HuggingFace, custom fine-tuned, etc.) and any restrictions. -->

## Deploy a model with managed compute

<!-- Procedural steps for creating a managed compute deployment in the Foundry portal and/or via the SDK/CLI. Use numbered steps. -->

## Send inference requests to the deployment

<!-- Procedural steps for invoking the deployed model endpoint. Include a code snippet (Python preferred). -->

## Manage and scale a deployment

<!-- Steps or guidance for updating deployment settings, scaling instance counts, monitoring utilization, and deleting a deployment when done. -->

## Pricing and billing

<!-- Explain the billing model for managed compute: pay-as-you-go vs. reserved capacity, what meters apply, link to pricing page. -->

## Troubleshooting

<!-- Cover common errors and failure scenarios: deployment provisioning failures, inference errors, quota exceeded, unhealthy endpoints, scaling issues. Include resolution steps for each. -->

## Related content

- [Deployment types for Microsoft Foundry Models](../foundry-models/concepts/deployment-types.md)
- [Managed compute pay-as-you-go](../../../foundry-classic/how-to/deploy-models-managed-pay-go.md)