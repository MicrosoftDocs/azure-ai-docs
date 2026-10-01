---
title: include file
description: include file
author: alvinashcraft
ms.author: aashcraft
ms.service: microsoft-foundry
ms.topic: include
ms.date: 03/19/2026
ms.custom: include, classic-and-new
ai-usage: ai-assisted
---

[!INCLUDE [non-english-translation](non-english-translation.md)]

As part of Microsoft's commitment to responsible AI, we have designed and operate Foundry Models sold by Azure (as defined in the [Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage)) with the intention of respecting the rights of individuals and society and fostering transparent human-computer interaction. For this reason, certain Models sold by Azure (or versions of them) are designated as Limited Access Services, and access and use are subject to eligibility criteria determined by Microsoft. Unless otherwise indicated in the service, all Azure customers are eligible for access to Models sold by Azure, and all uses consistent with the Product Terms and Code of Conduct are permitted, so customers are not required to submit a registration form unless they are: (a) accessing a model sold by Azure designated as a Limited Access Service, or (b) requesting approval to modify Guardrails (previously content filters) and/or abuse monitoring for a model sold by Azure. 

Models sold by Azure are made available to customers under the terms governing their subscription to Microsoft Azure Services, including [Product Terms](https://www.microsoft.com/licensing/terms/welcome/welcomepage) such as the Universal License Terms applicable to Microsoft Generative AI Services and the product offering terms for Models sold by Azure. Please review these terms carefully as they contain important conditions and obligations governing your use. 

Azure OpenAI Service is made available to customers under the terms governing their subscription to Microsoft Azure Services, including such as the Universal License Terms applicable to Microsoft Generative AI Services and the product offering terms for Azure OpenAI. Please review these terms carefully as they contain important conditions and obligations governing your use of Azure OpenAI Service.

## Registration for modified Guardrails and/or abuse monitoring 

All customers have the ability to configure severity thresholds on Guardrails (previously content filters), however, the modified Guardrails approval process is required to turn the Guardrails partially or fully off. Customers who wish to modify Guardrails and/or modify abuse monitoring are subject to additional eligibility criteria and requirements. At this time, modified Guardrails (previously content filters) and/or modified abuse monitoring for Models sold by Azure are available only to customers and partners managed by a Microsoft account team or under an eligible program, and are subject to additional requirements. Customers meeting these requirements can request approval for modified Guardrails and/or modified abuse monitoring using the following forms:

- [Modified Guardrails (previously content filters)](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUMlBQNkZMR0lFRldORTdVQzQ0TEI5Q1ExOSQlQCN0PWcu)  
- [Modified abuse monitoring](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUOE9MUTFMUlpBNk5IQlZWWkcyUEpWWEhGOCQlQCN0PWcu)

## Biosecurity and cybersecurity exception requests

When you use Azure OpenAI models, cybersecurity safeguards might block an API request and return a `cyber_policy` error.

This section explains what this error means and how to request an exception when your legitimate biosecurity or cybersecurity use case requires changes to these safeguards.

### When this error occurs

An API request sent to the model might be blocked when it's flagged for potential cybersecurity risk. In this case, the response includes the `cyber_policy` error code and a message such as:

```text
This request has been flagged for potentially high-risk cyber activity.
```

Or:

```text
This content was flagged for possible cybersecurity risk.
```

In these messages, "request" refers to the API request sent to the model.

### What an exception request covers

An exception request asks for a review of your use case and the changes to biosecurity or cybersecurity safeguards needed to support legitimate research or security-related activities.

Approval for modified Guardrails (previously modified content filters) or modified abuse monitoring does not, by itself, authorize changes to biosecurity or cybersecurity safeguards.

### How to request an exception

To request an exception, contact [responsibleainotifications@microsoft.com](mailto:responsibleainotifications@microsoft.com) directly.

Include the following information in your email:

- Your business purpose.
- Your specific use case.
- The safeguards you want to modify and why the changes are necessary.

Follow the guidance provided by the team regarding any required application forms or additional information.

## Important links

- [Register to modify Guardrails (previously content filters)](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUMlBQNkZMR0lFRldORTdVQzQ0TEI5Q1ExOSQlQCN0PWcu) (if needed)
- [Register to modify abuse monitoring](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUOE9MUTFMUlpBNk5IQlZWWkcyUEpWWEhGOCQlQCN0PWcu) (if needed)

Some advanced Models sold by Azure may have more stringent criteria for turning off abuse monitoring.  

## Help and support

Frequently asked questions about Limited Access can be found on the [Foundry Tools Limited Access](/azure/ai-services/cognitive-services-limited-access) page. If you need help with Azure OpenAI, see the [Foundry Tools support options](/azure/ai-services/cognitive-services-support-options) page. Report abuse of Azure OpenAI [here](https://aka.ms/reportabuse).

## See also

- [Code of conduct for Azure OpenAI Service integrations](/legal/ai-code-of-conduct?context=%2Fazure%2Fcognitive-services%2Fopenai%2Fcontext%2Fcontext)
- [Transparency note for Azure OpenAI Service](../openai/transparency-note.md)
- [Data, privacy, and security for Azure OpenAI Service](../openai/data-privacy.md)
