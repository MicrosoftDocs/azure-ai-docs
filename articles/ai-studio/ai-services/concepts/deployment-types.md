---
title: Understanding deployment types in Azure AI model inference
titleSuffix: Azure AI services
description: Learn how to use deployment types in Azure AI model deployments
author: mrbullwinkle
manager: nitinme
ms.service: azure-ai-studio
ms.topic: how-to
ms.date: 10/11/2024
ms.author: fasantia
ms.custom: ignite-2024, github-universe-2024
---

# Deployment types in Azure AI model inference

Azure AI model inference in Azure AI services provides customers with choices on the hosting structure that fits their business and usage patterns. The service offers two main types of deployment: **standard** and **provisioned**. Standard is offered with a global deployment option, routing traffic globally to provide higher throughput. Provisioned is also offered with a global deployment option, allowing customers to purchase and deploy provisioned throughput units across Azure global infrastructure.

All deployments can perform the exact same inference operations, however the billing, scale and performance are substantially different. As part of your solution design, you will need to make two key decisions:

- **Data residency needs**: global vs. regional resources  
- **Call volume**: standard vs. provisioned

Deployment types support varies by model and model provider. 

## Global versus regional deployment types

For standard and provisioned deployments, you have an option of two types of configurations within your resource – **global** or **regional**. Global standard is the recommended starting point. 

Global deployments leverage Azure's global infrastructure, dynamically route customer traffic to the data center with best availability for the customer’s inference requests. This means you will get the highest initial throughput limits and best model availability with Global while still providing our uptime SLA and low latency. For high volume workloads above the specified usage tiers on standard and global standard, you may experience increased latency variation. For customers that require the lower latency variance at large workload usage, we recommend purchasing provisioned throughput.

Our global deployments will be the first location for all new models and features. Customers with very large throughput requirements should consider our provisioned deployment offering.

## Standard

Standard deployments provide a pay-per-call billing model on the chosen model. Provides the fastest way to get started as you only pay for what you consume. Models available in each region as well as throughput may be limited.  

Standard deployments are optimized for low to medium volume workloads with high burstiness. Customers with high consistent volume may experience greater latency variability.

Only Azure OpenAI models support this deployment type.

## Global standard

Global deployments are available in the same Azure AI services resources as non-global deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center with best availability for each request.  Global standard provides the highest default quota and eliminates the need to load balance across multiple resources.  

Customers with high consistent volume may experience greater latency variability. The threshold is set per model.  For applications that require the lower latency variance at large workload usage, we recommend purchasing provisioned throughput if available.

## Global provisioned

Global deployments are available in the same Azure AI services resources as non-global deployment types but allow you to leverage Azure's global infrastructure to dynamically route traffic to the data center with best availability for each request. Global provisioned deployments provide reserved model processing capacity for high and predictable throughput using Azure global infrastructure.

Only Azure OpenAI models support this deployment type.
