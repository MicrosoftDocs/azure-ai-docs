---
# Required metadata
# For more information, see https://review.learn.microsoft.com/en-us/help/platform/learn-editor-add-metadata?branch=main
# For valid values of ms.service, ms.prod, and ms.topic, see https://review.learn.microsoft.com/en-us/help/platform/metadata-taxonomies?branch=main

title: Manage traffic with spillover for Provisioned deployments
description: Article outlining how to use the spillover feature to manage traffic bursts for Azure OpenAI Service provisioned deployments
author:      sydneemayers # GitHub alias
ms.author: sydneemayers
ms.service: azure-ai-openai
ms.topic: how-to
ms.date:     03/05/2025
---

# Manage traffic with spillover for provisioned deployments (Preview)

Spillover is a capability that automates the process of sending overage traffic from provisioned deployments to standard deployments when a 429 response is received. Spillover is an optional capability that can be set for all requests on a given deployment or can be managed on a per-request basis. When spillover is enabled, Azure OpenAI service will take care of sending any overage traffic from your provisioned deployment to a designated standard deployment to be processed.

## Prerequisites
- A global provisioned or data zone provisioned deployment to be used as your primary deployment.
- A global or data zone standard deployment to be used as your spillover deployment. The data processing level of your standard deployment must match your provisioned deployment (e.g. global provisioned deployment must be used with a global standard spillover deployment).

## When to enable spillover on provisioned deployments
To maximize the utilization of your provisioned deployment, it is recommended to enable 

## When does spillover come into effect?

## How does spillover impact cost?

## How do I monitor my spillover usage?