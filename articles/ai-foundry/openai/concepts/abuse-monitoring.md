---
title: Azure Direct Models abuse monitoring
titleSuffix: Azure OpenAI
description: Learn about the abuse monitoring capabilities of Azure OpenAI
author: mrbullwinkle
ms.author: mbullwin
ms.service: azure-ai-foundry
ms.subservice: azure-ai-foundry-openai
ms.topic: concept-article
ms.date: 12/6/2025
ms.custom: template-concept, ignite-2024
manager: nitinme
monikerRange: 'foundry-classic || foundry'

---

# Abuse Monitoring

Azure Direct Models detect and mitigate instances of recurring content and/or behaviors that suggest use of the service in a manner that might violate the [Code of Conduct](https://aka.ms/AI-CoC). Details on how data is handled can be found on the [Data, Privacy, and Security](/azure/ai-foundry/responsible-ai/openai/data-privacy) page. 


## Components of abuse monitoring

There are several components to abuse monitoring:

- **Content Classification**: Classifier models detect harmful text and/or images in user prompts (inputs) and completions (outputs). The system looks for categories of harms as defined in the [Content Requirements](/legal/ai-code-of-conduct?context=/azure/ai-foundry/openai/context/context), and assigns severity levels as described in more detail on the [Content Filtering](/azure/ai-foundry/openai/concepts/content-filter) page. The content classification signals contribute to pattern detection as described below.  
- **Abuse Pattern Capture**: The abuse monitoring system for Azure Direct Models looks at customer usage patterns and employs algorithms and heuristics to detect and score indicators of potential abuse. Detected patterns consider, for example, the frequency and severity at which harmful content is detected (as indicated in content classifier signals) in a customer’s prompts and completions, as well as the intentionality of the behavior. The trends and urgency of the detected pattern will also affect scoring of potential abuse severity.
    For example, a higher volume of harmful content classified as higher severity, or recurring conduct indicating intentionality (such as recurring jailbreak attempts) are both more likely to receive a high score indicating potential abuse. 
- **Review and Decision**: Prompts and completions that are flagged through content classification and/or identified as part of a potentially abusive pattern of use are subjected to another review process to help confirm the system’s analysis and inform actioning decisions for abuse monitoring. Such review is conducted through two methods: automated review and human review.
    - By default, if prompts and completions are flagged through content classification as harmful and/or identified to be part of a potentially abusive pattern of use, they might be sampled for review by using automated means including AI models such as LLMs instead of a human reviewer. The model used for this purpose processes prompts and completions only to confirm the system’s analysis and inform actioning decisions; prompts and completions that undergo such review are not stored by the abuse monitoring system or used to train the AI model or other systems.
    - In some cases, when automated review does not meet applicable confidence thresholds in complex contexts or if automated review systems are not available, human eyes-on review might be introduced to make an extra judgment. Authorized Microsoft employees may assess content flagged through content classification and/or identified as part of a potentially abusive pattern of use, and either confirm or correct the classification or determination based on predefined guidelines and policies. Such prompts and completions can be accessed for human review only by authorized Microsoft employees via Secure Access Workstations (SAWs) with Just-In-Time (JIT) request approval granted by team managers. For Azure Direct Model resources deployed in the European Economic Area, the authorized Microsoft employees are located in the European Economic Area. This human review abuse monitoring process will not take place if the customer has been approved for modified abuse monitoring. 
- **Notification and Action**: When a threshold of abusive behavior has been confirmed based on the preceding steps, the customer is informed of the determination by email. Except in cases of severe or recurring abuse, customers typically have an opportunity to explain or remediate—and implement mechanisms to prevent recurrence of—the abusive behavior. Failure to address the behavior—or recurring or severe abuse—may result in suspension or termination of the customer’s access to Azure Direct Model resources and/or capabilities.

## Modified abuse monitoring 

Some customers may want to use Azure Direct Models for a use case that involves the processing of highly sensitive or highly confidential data, or otherwise may conclude that they don't want or don't have the right to permit Microsoft to store and conduct human review on their prompts and completions for abuse detection. To address these concerns, Microsoft allows customers who meet additional Limited Access eligibility criteria to apply to modify abuse monitoring by completing [this form](https://customervoice.microsoft.com/Pages/ResponsePage.aspx?id=v4j5cvGGr0GRqy180BHbR7en2Ais5pxKtso_Pz4b1_xUOE9MUTFMUlpBNk5IQlZWWkcyUEpWWEhGOCQlQCN0PWcu). Some advanced models from Azure Direct Models may have more stringent criteria for turning off abuse monitoring. Learn more about applying for modified abuse monitoring at [Limited access to Azure Direct Models](/azure/ai-foundry/responsible-ai/openai/limited-access).    

> [!NOTE]
> When abuse monitoring is modified and human review is not performed, detection of potential abuse may be less accurate. Customers are notified of potential abuse detection as described above, and should be prepared to respond to such notification to avoid service interruption if possible.  

## Next steps

- Learn more about the [underlying models that power Azure OpenAI](../../foundry-models/concepts/models-sold-directly-by-azure.md).
- Learn more about understanding and mitigating risks associated with your application: [Overview of Responsible AI practices for Azure OpenAI models](/azure/ai-foundry/responsible-ai/openai/overview).
- Learn more about how data is processed in content filtering and abuse monitoring: [Data, privacy, and security for Azure OpenAI](/azure/ai-foundry/responsible-ai/openai/data-privacy#preventing-abuse-and-harmful-content-generation).
