---
title: Vary MCP Tool Headers Per Request in Foundry Agent Service
description: Explains how to vary MCP tool headers by user or request in Foundry Agent Service by using structured inputs for per-user security trimming.
author: haileytap
ms.author: haileytapia
manager: mcleans
ms.service: microsoft-foundry
ms.topic: include
ms.date: 08/06/2026
ms.custom: include file
ai-usage: ai-assisted
---

To vary MCP headers per request, such as passing a different user's token on each call, declare a [structured input](../agents/how-to/structured-inputs.md#use-structured-inputs-with-mcp-servers) in the agent definition and reference it as a `{{placeholder}}` in the tool's `headers`. The caller supplies the value on each invocation. This approach works for MCP tools bound to a project connection.

For per-user authorization against an MCP server, you can also use [OAuth identity passthrough](../agents/how-to/mcp-authentication.md#oauth-identity-passthrough).