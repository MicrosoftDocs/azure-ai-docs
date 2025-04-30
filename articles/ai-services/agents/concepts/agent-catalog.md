---
title: How to get started with an AI agent template
titleSuffix: Azure AI Foundry
description: This article provides instructions on how to use an AI agent template to get started with Azure AI Foundry Agent Service.
manager: nitinme
ms.service: azure-ai-agent-service
ms.topic: how-to
ms.date: 04/29/2025
ms.author: aahi
author: aahill
#customer intent: As a developer, I want to jump start my journey with an AI template.
---

# Get started with an agent template

Streamline your agentic system development with prebuilt, task-specific agent templates. Benefit from a quick deployment for a variety of tasks. For example, translation, sales prep, computer use, and more.

<!--
Available templates include:

* [Get started with AI chat](https://github.com/Azure-Samples/get-started-with-ai-chat)
* [Get started with AI agents](https://github.com/Azure-Samples/get-started-with-ai-agents)
* [Unlock insights from conversational data](https://github.com/microsoft/Conversation-Knowledge-Mining-Solution-Accelerator)
-->
[!INCLUDE [feature-preview](../../../ai-foundry/includes/feature-preview.md)]

## Prerequisites

- [Azure subscription](https://azure.microsoft.com/free)
- An [Azure AI Foundry project](../../../ai-foundry/how-to/create-projects.md).

## Start with a sample application

1. Go to [Azure AI Foundry portal](https://ai.azure.com).
1. Open your project in Azure AI Foundry portal.
1. On the left pane, select **Templates** (preview).
1. Find the solution template you want to use. For example, **Get started with AI Agents**.

    :::image type="content" source="../media/agent-catalog.png" alt-text="A screenshot of the model catalog." lightbox="../media/agent-catalog.png":::

1. Select **Open in Github** to view the entire sample application.
1. In some cases, you can also view a step-by-step tutorial that explains the AI code.

## Explore the sample application

Once you're looking at the GitHub repository for your sample, refer to the README for more instructions and information on how to deploy your own version of the application.

Instructions vary by sample, but most include how to:

* Open the solution in the location of your choice:
  * GitHub Codespaces
  * VS Code Dev Containers
  * Your local IDE
* Deploy the application to Azure
* How to test the app

The README also includes information about the application, such as the use case, architecture, and pricing information.

## Available templates

| Agent Template | Description | Tools used |
|----------------|-------------|------------|
| Claim Buddy | Simplifies the claims process for patients, ensuring they understand their benefits, and helping them efficiently navigate the often-complex claim submission and resolution process. | File Search, Code Interpreter, Form-Fill tool (OpenAPI Specified Tool) |
| Trusty Link | Trusty Link enhances client relationships by providing timely, personalized support for financial decision-making. Acting as a digital relationship manager, the agent offers relevant product advice, answers financial inquiries, and ensures each client gets tailored assistance aligned with their goals. | File Search, Grounding with Bing, MorningStar |
| Home Loan Genie | Streamlines the mortgage application journey, empowering users to make informed decisions about their home loan options while simplifying the documentation and application process. | File Search, Code Interpreter |
| Revenue Max | Revenue Max empowers consumer goods companies with data-driven insights, enabling them to make informed decisions on pricing and product placement to drive sustainable revenue growth. | File Search, Grounding with Bing, Code Interpreter |
| Ticket Expert Pro | Ticket Expert Pro provides a seamless ticketing experience, helping users find and book the best travel options across flights, trains, and accommodations—while ensuring a smooth, informed, and personalized experience. | Tripadvisor, Skyscanner (OpenAPI) Tool, Code Interpreter |
| Sales Prep Agent | Ensures you're always prepared for your external meetings by scanning your calendar, identifying external participants, researching them, and delivering a concise summary in Teams so you can walk in informed and confident. | Azure Logic Apps (ALA), Grounding with Bing |
| Email Support Agent | Drafts high-quality, AI-generated replies to customer questions using your internal knowledge base—helping you stay responsive while maintaining accuracy and tone. | File Search, Azure Logic Apps (Outlook Connector) |
| Outreach Agent | Helps you scale personalized outbound sales by studying a lead's public profile and writing tailored emails that reflect their role, company, and goals—while avoiding duplicate outreach and managing your sales pipeline records automatically. | File Search, Azure Logic Apps, Grounding with Bing, Outlook/Gmail connector (via ALA) |
| Logi Track | Logi Track (Logistics Agent) enhances supply chain visibility and efficiency by providing real-time data, predictive insights, and operational recommendations—ensuring timely deliveries and optimal inventory management. | Azure Maps API (OpenAPI Tool), Azure Table Storage Tool (OpenAPI Tool), Power BI (Logic Apps Connector) Tool |
| Store Ops Guide | Store Ops Guide acts as a virtual consultant, helping retailers optimize their physical store environments to enhance efficiency, improve customer experience, and streamline daily operations. | File Search, Image Analysis Tool (OpenAPI tool), Code Interpreter, Grounding with Bing |
| Red Teaming Agent | Semantic Kernel Agent |  |
| Tumor Board Biomed Agent |  | |
| Patient data agent |  | |
| Radiology agent | | |
| Translation | | |
| Intent routing | | |
| Exact question answering | | |
| Voice live agent | | |
| Insurance Claim Processing | Processes insurance claims by extracting data, redacting PII, and assessing risk and severity. It boosts efficiency, accuracy, and privacy, and adapts to industries like finance, legal, and healthcare. | Document Intelligence, PII Redaction |
| Contract analysis | Compare two different versions of a contract and extract the key fields and clauses. Compare the extracted values to identify the difference between the two version and generate a report on the changes for a reviewer to follow up on. | File Search, Content Understanding |
| SOP (Standard Operating Procedure) Forge | SOP Forge turns any short instructional video into a fully formatted Standard Operating Procedure that matches your corporate template. Upload the footage and the agent automatically transcribes it, identifies each step, adds or generates crisp images, and delivers a structured Markdown file ready for distribution. Need tweaks?—just ask in chat to merge steps, adjust tone, or swap visuals and get an updated SOP in seconds, freeing you from documentation drudgery. | Content Understanding, File Search, Image Gen | 
| Ads Reconciliation agent | | |
| Video Translation | Video Translation Agent enables seamless multilingual adaptation of video content. It localizes training materials, product demos, and corporate communications by generating dubbed and subtitled versions in the user’s target languages—expanding global reach while preserving tone, emotion, and original context. | Video Translation API, Azure Blob Storage |
| Fidelity Saifir Agent | | |
| Sight Machine Agent | | |
| Marquee Insights Agent | | |