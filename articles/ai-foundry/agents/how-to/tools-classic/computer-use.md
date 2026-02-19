---
title: 'How to use Foundry Agent Service Computer Use Tool'
titleSuffix: Microsoft Foundry
description: Learn how to use Foundry Agent Service Computer Use Tool
services: cognitive-services
manager: nitinme
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-agent-service
ms.topic: how-to
ms.date: 12/16/2025
author: alvinashcraft
ms.author: aashcraft
ms.custom: references_regions
---

# Foundry Agent Service Computer Use Tool

> [!NOTE]
> This document refers to the classic version of the agents API. 
>
> 🔍 [View the new Computer Use documentation](../../../default/agents/how-to/tools/computer-use.md?view=foundry&preserve-view=true).


> [!WARNING]
> The Computer Use tool comes with additional significant security and privacy risks, including prompt injection attacks. Learn more about intended uses, capabilities, limitations, risks, and considerations when choosing a use case in the [Azure OpenAI transparency note](../../../responsible-ai/openai/transparency-note.md#risk-and-limitations-of-computer-use-preview).



Use this article to learn how to work with the Computer Use Tool in Foundry Agent Service. Computer Use is a specialized AI tool that uses a specialized model that can perform tasks by interacting with computer systems and applications through their user interfaces. With Computer Use, you can create an agent that can handle complex tasks and make decisions by interpreting visual elements and taking action based on on-screen content. 

## Features 

* Autonomous navigation: For example, Computer Use can open applications, click buttons, fill out forms, and navigate multi-page workflows. 

* Dynamic adaptation: Interpreting UI changes and adjusting actions accordingly. 

* Cross-application task execution: Can operate across web-based and desktop applications. 

* Natural language interface: Users can describe a task in plain language, and the Computer Use model determines which UI interactions to execute. 

## Request access 

For access to the `computer-use-preview` model, registration is required and access will be granted based on Microsoft's eligibility criteria. Customers who have access to other limited access models will still need to request access for this model. 

To request access, see the [application form](https://aka.ms/oai/cuaaccess).

Once access has been granted, you will need to create a deployment for the model. 

## Differences between Browser Automation and Computer Use

The following table lists some of the differences between the Computer Use Tool and [Browser Automation](./browser-automation.md) Tool.

| Feature                        | Browser Automation          | Computer Use Tool          |
|--------------------------------|-----------------------------|----------------------------|
| Model support                  | All GPT models              | `Computer-use-preview` model only |
| Can I visualize what's happening?     | No                          | Yes                        |
| How it understands the screen  | Parses the HTML or XML pages into DOM documents | Raw pixel data from screenshots |
| How it acts                    | A list of actions provided by the model | Virtual keyboard and mouse |
| Is it multi-step?                    | Yes                         | Yes                        |
| Interfaces                     | Browser                     | Computer and browser       |
| Do I need to bring my own resource?    | Your own Playwright resource with the keys stored as a connection. | No additional resource required but we highly recommend running this tool in a sandboxed environment.          |

## Regional support 

In order to use the Computer Use Tool, you need to have a [Computer Use model](../../../foundry-models/concepts/models-sold-directly-by-azure.md#computer-use-preview) deployment. The Computer Use model is available in the following regions: 
* `eastus2` 
* `swedencentral` 
* `southindia` 

## Understanding the Computer Use integration 

When working with the Computer Use tool, you typically would perform the following to integrate it into your application. 

1. Send a request to the model that includes a call to the Computer Use tool, and the display size and environment. You can also include a screenshot of the initial state of the environment in the first API request. 

1. Receive a response from the model. If the response has action items, those items contain suggested actions to make progress toward the specified goal. For example an action might be screenshot so the model can assess the current state with an updated screenshot, or click with X/Y coordinates indicating where the mouse should be moved. 

1. Execute the action using your application code on your computer or browser environment. 

1. After executing the action, capture the updated state of the environment as a screenshot. 

1. Send a new request with the updated state as a `tool_call_output`, and repeat this loop until the model stops requesting actions or you decide to stop. 

    > [!NOTE]
    > Before using the tool, you need to set up an environment that can capture screenshots and execute the recommended actions by the agent. We recommend using a sandboxed environment, such as Playwright for safety reasons.

## Handling conversation history 

You can use the `tool_call_id` parameter to link the current request to the previous response. Using this parameter is recommended if you don't want to manage the conversation history. 

If you don't use this parameter, you should make sure to include all the items returned in the response output of the previous request in your inputs array. This includes reasoning items if present. 

## Safety checks 

> [!WARNING] 
> Computer Use carries substantial security and privacy risks and user responsibility. Computer Use comes with significant security and privacy risks. Both errors in judgment by the AI and the presence of malicious or confusing instructions on web pages, desktops, or other operating environments which the AI encounters may cause it to execute commands you or others do not intend, which could compromise the security of your or other users’ browsers, computers, and any accounts to which AI has access, including personal, financial, or enterprise systems.
> 
> We strongly recommend using the Computer Use tool on virtual machines with no access to sensitive data or critical resources. Learn more about intended uses, capabilities, limitations, risks, and considerations when choosing a use case in the [Azure OpenAI transparency note](../../../responsible-ai/openai/transparency-note.md#risk-and-limitations-of-computer-use-preview).

The API has safety checks to help protect against prompt injection and model mistakes. These checks include: 

**Malicious instruction detection**: The system evaluates the screenshot image and checks if it contains adversarial content that might change the model's behavior. 

**Irrelevant domain detection**: The system evaluates the `current_url` parameter (if provided) and checks if the current domain is considered relevant given the conversation history. 

**Sensitive domain detection**: The system checks the `current_url` parameter (if provided) and raises a warning when it detects the user is on a sensitive domain. 

If one or more of the above checks is triggered, a safety check is raised when the model returns the next `computer_call` with the `pending_safety_checks` parameter. 

```json
"output": [ 
    { 
        "type": "reasoning", 
        "id": "rs_67cb...", 
        "summary": [ 
            { 
                "type": "summary_text", 
                "text": "Exploring 'File' menu option." 
            } 
        ] 
    }, 
    { 
        "type": "computer_call", 
        "id": "cu_67cb...", 
        "call_id": "call_nEJ...", 
        "action": { 
            "type": "click", 
            "button": "left", 
            "x": 135, 
            "y": 193 
        }, 
        "pending_safety_checks": [ 
            { 
                "id": "cu_sc_67cb...", 
                "code": "malicious_instructions", 
                "message": "We've detected instructions that may cause your application to perform malicious or unauthorized actions. Please acknowledge this warning if you'd like to proceed." 
            } 
        ], 
        "status": "completed" 
    } 
]
```

You need to pass the safety checks back as `acknowledged_safety_checks` in the next request in order to proceed. 

```json
"input":[ 
        { 
            "type": "computer_call_output", 
            "call_id": "<call_id>", 
            "acknowledged_safety_checks": [ 
                { 
                    "id": "<safety_check_id>", 
                    "code": "malicious_instructions", 
                    "message": "We've detected instructions that may cause your application to perform malicious or unauthorized actions. Please acknowledge this warning if you'd like to proceed." 
                } 
            ], 
            "output": { 
                "type": "computer_screenshot", 
                "image_url": "<image_url>" 
            } 
        } 
    ]
```

## Safety check handling 

In all cases where `pending_safety_checks` are returned, actions should be handed over to the end user to confirm proper model behavior and accuracy. 

`malicious_instructions` and `irrelevant_domain`: end users should review model actions and confirm that the model is behaving as intended. 

`sensitive_domain`: ensure an end user is actively monitoring the model actions on these sites. Exact implementation of this "watch mode" can vary by application, but a potential example could be collecting user impression data on the site to make sure there is active end user engagement with the application. 

## Next steps

* [Computer Use code samples](./computer-use-samples.md)