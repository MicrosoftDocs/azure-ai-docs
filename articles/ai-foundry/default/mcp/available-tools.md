---
title:  Explore available tools and example prompts for Foundry MCP Server (preview) 
description: Reference guide for all Foundry MCP Server tools, including dataset management, evaluation, model deployment, and monitoring, with example prompts for each tool.
keywords: mcp, model context protocol, foundry mcp server
author: sdgilley
ms.author: sgilley
ms.reviewer: sehan
ms.date: 11/04/2025
ms.topic: reference
ms.service: azure-ai-foundry
ai-usage: ai-assisted
---

# Available tools and example prompts for Foundry MCP Server (preview) 

Foundry MCP Server exposes a set of tools that let you manage datasets, run evaluations, deploy and monitor models, and more — all through conversational prompts instead of API calls. Use this reference to explore each tool and try the example prompts in your own project.

> [!TIP]
> Before using these tools, complete the [Foundry MCP Server setup](get-started.md).

[!INCLUDE [preview-feature](../../openai/includes/preview-feature.md)]

## Dataset management

**evaluation_dataset_create (write)**

Create or update a dataset version in a Foundry project.

Example prompts include:

- "Upload my customer support Q&A dataset from this Azure Blob Storage URL."
- "Create a new dataset version 2.0 for my training data located at `<blob-storage-account-url>`."
- "Register a new evaluation dataset called `product-reviews-v1` from my blob storage." 

**evaluation_dataset_get (read)**

Get a dataset by name and version, or list all datasets in the project.

Example prompts include:

- "Show me all datasets in my Foundry project" 
- "Get details for the 'customer-support-qa' dataset version 2" 
- "List all available datasets I can use for evaluation" 

## Evaluation operations 

**evaluation_create (write)**

Create an evaluation run for a dataset using one or more evaluators.

Example prompts include:

- "Create an evaluation run for my customer service dataset using Relevance, Groundedness, and Coherence evaluators." 
- "Run an evaluation on dataset-456 with Violence, HateUnfairness, and ContentSafety evaluators for my chatbot model." 
- "Evaluate my QA model using the F1Score, BleuScore, and RougeScore metrics on the test dataset."

**evaluation_get (read)**

List evaluation runs in the Azure AI Project.

Example prompts include:

- "Show me all evaluation runs in my Foundry project" 
- "List the recent evaluations I've run this week" 
- "Get the status of all my model evaluations" 

**evaluation_comparison_create (write)**

Create comparison results of evaluations within a group.

Example prompts include:

- "Compare the performance of my baseline model against the two new fine-tuned versions."
- "Create a comparison between run-baseline-123 and treatment runs run-124, run-125 for evaluation eval-456."
- "I want to compare Model A vs Model B performance on the same evaluation metrics."

**evaluation_comparison_get (read)**

Get or list comparison results of evaluations within a group.

Example prompts include:

- "Get the results of comparison insight-789."
- "Show me the comparison results I created yesterday."
- "Retrieve all evaluation comparison insights from my project."

## Model catalog and details 

**model_catalog_list (read)**

List models from the Foundry model catalog.

Example prompts include:

- "Show me all GPT-4 models available in the catalog."
- "List all Microsoft-published models with MIT license."
- "Find models I can use for free in the playground."
- "What models are available for text generation from OpenAI?"

**model_details_get (read)**

Get full model details and code sample from Foundry.

Example prompts include:

- "Get detailed information and code samples for GPT-4o-mini."
- "Show me the specifications and usage examples for the Llama-2-70b model."
- "I need the documentation and sample code for the text-embedding-ada-002 model."

## Model deployment management 

**model_deploy (write)**

Create or update a model deployment in the specified Foundry account.

Example prompts include:

- "Deploy GPT-4o-mini as 'production-chatbot' with 20 capacity units"
- "Create a new deployment called 'content-generator' using the GPT-4o model."
- "Deploy the latest version of GPT-4o for my application."

**model_deployment_get (read)**

Get one or more model deployments from a Foundry account.

Example prompts include:

- "Show me all my current model deployments."
- "Get details for my 'production-chatbot' deployment."
- "List all deployments in my Foundry account."

**model_deployment_delete (write)**

Delete a specific model deployment by name.

Example prompts include:

- "Delete the 'old-test-deployment' that I'm no longer using." 
- "Remove my staging deployment to free up quota." 
- "Clean up that deprecated model deployment from my Foundry account `<account-name>`." 

## Model analytics and recommendations 

**model_benchmark_get (read)**

Fetch benchmark data for Foundry models.

Example prompts include:

- "Show me benchmark data for all available models."
- "Get performance comparisons across different model families."
- "I want to see accuracy and cost metrics for various models."

**model_benchmark_subset_get (read)**

Get benchmark data for specific model name and version pairs.

Example prompts include:

- "Compare benchmark performance between GPT-4 and GPT-3.5-turbo."
- "Get benchmark data for Claude-3 vs Llama-2-70b models."
- "Show me performance metrics for the specific model versions I'm considering."

**model_similar_models_get (read)**

Returns a list of similar models based on deployment or model details.

Example prompts include:

- "Find models similar to my current GPT-4 deployment."
- "What alternatives are there to the model I'm currently using?"
- "Show me models with similar capabilities to my production deployment."

**model_switch_recommendations_get (read)**

Get model switch recommendations based on benchmark data.

Example prompts include:

- "Recommend better models based on my current deployment's performance."
- "Should I switch from my current model to something more cost-effective?"
- "Get optimization recommendations for my production model deployment."
- "What models would give me better quality/cost ratio than what I'm using now?"

## Model monitoring and operations 

**model_monitoring_metrics_get (read)**

Get monitoring metrics for a model deployment.

Example prompts include:

- "Show me the request metrics for my production-chatbot deployment."
- "Get latency statistics for my GPT-4o deployment over the last week."
- "Check the quota usage for my text-embedding deployment."
- "What are the error rates for my content-generator model?"

**model_deprecation_info_get (read)**

Get deployment info enriched with deprecation data.

Example prompts include:

- "Check if my production deployment is using a deprecated model version."
- "Get deprecation information for my legacy-chatbot deployment."
- "Are any of my current deployments scheduled for retirement?"

**model_quota_list (read)**

List available deployment quota and usage for a subscription in a region.

Example prompts include:

- "Check my available quota in East US region."
- "How much capacity do I have left for new deployments in West Europe?"
- "Show me quota usage across all regions for my subscription."

## Example workflows 

**Complete Model Evaluation Workflow:**

- "Upload my evaluation dataset from this blob storage URL."
- "Run an evaluation using Relevance, Groundedness, and Safety evaluators."
- "Compare my baseline model against the new fine-tuned version."
- "Show me the comparison results with statistical significance."

**Model Deployment & Optimization:**

- "Show me all GPT-4 models available in the catalog."
- "Deploy GPT-4o as 'customer-service-bot' with 15 capacity units."
- "Monitor the request latency for my new deployment."
- "Recommend more cost-effective alternatives based on current usage."

**Resource Management & Cleanup:**

- "List all my current deployments and their usage."
- "Check which deployments are using deprecated model versions."
- "Show me my quota usage across all regions."
- "Delete unused test deployments to free up capacity."

## Related content

- Get started with [Foundry MCP Server](get-started.md)
- Learn how to [build your own MCP server](build-your-own-mcp-server.md)
- Review [security best practices for MCP servers](security-best-practices.md)