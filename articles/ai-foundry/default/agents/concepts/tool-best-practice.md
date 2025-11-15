---
title: "Best practices for using tools in foundry agent service"
description: "Best practices for using tools in foundry agent service"
author: aahill
ms.author: aahi
ms.date: 11/12/2025
ms.manager: nitinme
ms.topic: conceptual
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ai-usage: ai-assisted
---

# Best Practices for using tools in Microsoft Foundry Agent Service

> [!NOTE]
> We recommend you adding this to your agent to help it invoke the right tool(s): `You are a helpful assistant that MUST use the [name of the tool, such as GitHub MCP server, Fabric data agent] to answer all the questions from user. you MUST NEVER answer from your own knowledge UNDER ANY CIRCUMSTANCES. If you do not know the answer, or cannot find the answer in the provided Knowledge Base you MUST respond with "I don't know".`
> If you want it to generate citations, this instruction works well with Azure OpenAI models: `EVERY answer must ALWAYS provide citations for using the [name of the tool, such as GitHub MCP server, Fabric data agent] tool and render them as: `[message_idx:search_idx†source_name]` `

## Tools supported by models and regions
Tools are available in the following [regions](../../openai/how-to/responses.md#region-availability) with the following limitations. 
> [!NOTE]
> This region availability is only account for service availability, you need to make sure the model you want to use is also available in this region.

| Region Name        | A2A | Azure AI Search | Browser Automation | Code Interpreter | Computer Use | Fabric Data Agent | File Search | Function | Grounding with Bing Custom Search | Grounding with Bing Search | Image Generation | MCP | OpenAPI | SharePoint | Web Search |
|---------------------|-----|-----------------|---------------------|-------------------|--------------|--------------------|-------------|----------|------------------------------------|-----------------------------|-------------------|-----|---------|------------|------------|
| australiaeast       | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| brazilsouth         | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| canadacentral       | yes | yes             | yes                 | no                | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| canadaeast          | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| eastus              | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| eastus2             | yes | yes             | yes                 | yes               | yes          | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| francecentral       | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| germanywestcentral  | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| italynorth          | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| japaneast           | yes | yes             | yes                 | no                | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| koreacentral        | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| northcentralus      | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| norwayeast          | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| polandcentral       | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| southafricanorth    | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| southcentralus      | yes | yes             | yes                 | no                | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| southeastasia       | yes | yes             | yes                 | no                | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| southindia          | yes | yes             | yes                 | yes               | yes          | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| spaincentral        | yes | yes             | yes                 | no                | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| swedencentral       | yes | yes             | yes                 | yes               | yes          | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| switzerlandnorth    | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| uaenorth            | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| uksouth             | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| westus              | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |
| westus3             | yes | yes             | yes                 | yes               | no           | yes                | yes         | yes      | yes                                | yes                         | yes               | yes | yes     | yes        | yes        |

Tools are supported by the following models. 
> [!NOTE]
> For Image Generation tool, you need both the gpt-image-1 and the LLM as the orchestrator in the same Foundry project.

| Model | a2a | Azure AI Search | Browser Automation | Code Interpreter | Computer Use | Fabric Data Agent | File Search | Function | Grounding Bing Custom | Grounding Bing Search | Image Generation | MCP | OpenAPI | SharePoint | Web Search |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gpt-5 | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-5-mini | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-5-nano | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-5-chat | No | No | No | No | No | No | Yes | No | No | No | No | No | No | No | No |
| gpt-5-pro | Yes | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| o4-mini | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| o3 | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| o3-mini | Yes | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes |
| o1 | Yes | Yes | Yes | No | No | Yes | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes |
| computer-use-preview | No | No | No | No | Yes | No | No | No | No | No | No | No | No | No | No |
| gpt-4.1 | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-4.1-mini | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-4.1-nano | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-4o | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-4o-mini | Yes | Yes | Yes | Yes | No | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes | Yes |
| gpt-image-1 | No | No | No | No | No | No | No | No | No | No | Yes | No | No | No | No |
| DeepSeek-V3.0324 | No | Limited | No | Yes | No | Limited | Yes | Yes | Limited | Limited | No | Limited | No | Limited | No |
| DeepSeek-V3.1 | No | Limited | No | Yes | No | Limited | No | No | Limited | Limited | No | Limited | No | Limited | No |
| Llama-3.3-70B-Instruct | No | No | No | Yes | No | No | Yes | No | No | No | No | No | No | No | No |
| Llama-4-Maverick-178-128E-Instr | No | Limited | No | No | No | Limited | Yes | Yes | Limited | Limited | No | Limited | No | Limited | No |
| grok-3-mini | No | Limited | No | No | No | Limited | No | Yes | Limited | Limited | No | Limited | No | Limited | No |
| grok-4-fast-non-reasoning | No | Limited | No | No | No | Limited | No | Yes | Limited | Limited | No | Limited | No | Limited | No |
| grok-4-fast-reasoning | No | Limited | No | No | No | Limited | No | Yes | Limited | Limited | No | Limited | No | Limited | No || No | Limited | No | Limited | No |

## FaQ
**I dont think the model has invoked my tool, how I validate?**

In the Foundry Portal, you can go to tracing tab or click "debug" to verify if the tool is called and input/output if available.

**I verified the tool isn't called, how can I improve the agent's capability to invoke the call?**

There are various ways to influence how your AI agent invokes tools:

- The tool_choice parameter: Most deterministic way of controlling which (if any) tool is called by the model. By default, it is set to auto, which means the AI model will decide. If you want to force the model to call a specific tool, you can provide the specification of this tool, for example

```python
    response = openai_client.responses.create(
        conversation=conversation.id,
        input=openapi_language_query,
        extra_body={
            "agent": {"name": agent.name, "type": "agent_reference"},
            "tool_choice": "required",
            "stream": True
        },
    )
```
- The instructions parameter: Nondeterministic. Use the instructions to help the AI model understand your use case and the purposes of each tool. You want to tell the AI model what information or actions each tool can do. For example "use the AI Search tool <tool_name> for product related information, use the Fabric tool <tool_name> for sales related information." Sometimes the user query can be responded by the model's base knowledge or by the tools, you want to provide instructions like "use the tool outputs to generate a response, don't use your own knowledge."
