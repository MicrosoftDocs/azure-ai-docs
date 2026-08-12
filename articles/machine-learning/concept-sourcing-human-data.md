---
title: Manually sourcing human data for AI development
description: Learn best practices for mitigating potential harm to people—especially in vulnerable groups—and building balanced datasets when collecting human data manually.
author: lgayhardt
ms.author: lagayhar
ms.service: azure-machine-learning
ms.subservice: responsible-ai
ms.reviewer: nhudo
ms.topic: concept-article 
ms.date: 06/30/2026
ms.custom: responsible-ml 
---
# What is human data and why is responsible sourcing important?

[!INCLUDE [SDK/cli v2](includes/machine-learning-dev-v2.md)]

Human data is data collected directly from, or about, people. Human data might include personal data such as names, age, images, or voice clips, and sensitive data such as genetic data, biometric data, gender identity, religious beliefs, or political affiliations. 

Collecting this data can be important to building AI systems that work for all users. But avoid certain practices, especially ones that can cause physical and psychological harm to data contributors.

The best practices in this article help you conduct manual data collection projects from volunteers where everyone involved is treated with respect, and potential harms - especially those faced by vulnerable groups - are anticipated and mitigated. This approach means that:

- People contributing data aren't coerced or exploited in any way, and they have control over what personal data is collected.
- People collecting and labeling data have adequate training.

These practices can also help ensure more balanced and higher-quality datasets and better stewardship of human data.

These practices are emerging, and we're continually learning. The best practices in the next section are a starting point as you begin your own responsible human data collections. These best practices are provided for informational purposes only and shouldn't be treated as legal advice. All human data collections should undergo specific privacy and legal reviews.

## General best practices

Follow these best practices when you manually collect human data directly from people.

:::row:::
        :::column span="":::
            **Best Practice**
        :::column-end:::
        :::column span="":::
            **Why?**
        :::column-end:::
    :::row-end:::

-----

:::row:::
    :::column span="":::
        **Obtain voluntary informed consent.**
    :::column-end:::

    :::column span="":::
        - Participants should understand and consent to data collection and how their data will be used.
        - Store, process, and use data only for purposes that are part of the original documented informed consent.
        - Properly store consent documentation and associate it with the collected data.
    :::column-end:::
:::row-end:::

-----

:::row:::
    :::column span="":::
        **Compensate data contributors appropriately.**
    :::column-end:::

    :::column span="":::
        - Don't pressure or coerce data contributors into data collections. Fairly compensate them for their time and data.
        - Inappropriate compensation can be exploitative or coercive.
    :::column-end:::

:::row-end:::

-----
 
:::row:::
    :::column span="":::
        **Let contributors self-identify demographic information.**
    :::column-end:::

    :::column span="":::
        - If data collectors assign demographic information instead of data contributors self-reporting it, it can 1) result in inaccurate metadata and 2) be disrespectful to data contributors.
    :::column-end:::

:::row-end:::

-----

:::row:::
    :::column span="":::
        **Anticipate harms when recruiting vulnerable groups.**
    :::column-end:::

    :::column span="":::
        - Collecting data from vulnerable population groups introduces risk to data contributors and your organization.
    :::column-end:::

:::row-end:::

-----

:::row:::
    :::column span="":::
        **Treat data contributors with respect.**
    :::column-end:::

    :::column span="":::
        - Improper interactions with data contributors at any phase of the data collection can negatively impact data quality, as well as the overall data collection experience for data contributors and data collectors.
    :::column-end:::

:::row-end:::

-----

:::row:::
    :::column span="":::
        **Qualify external suppliers carefully.**     
    :::column-end:::

    :::column span="":::
        - Data collections with unqualified suppliers might result in low-quality data, poor data management, unprofessional practices, and potentially harmful outcomes for data contributors and data collectors (including violations of human rights).
        - Annotation or labeling work (for example, audio transcription, image tagging) with unqualified suppliers might result in low-quality or biased datasets, insecure data management, unprofessional practices, and potentially harmful outcomes for data contributors (including violations of human rights).
    :::column-end:::

:::row-end:::

-----

:::row:::
    :::column span="":::
        **Communicate expectations clearly in the Statement of Work (SOW) (contracts or agreements) with suppliers.**
    :::column-end:::

    :::column span="":::
        - A contract that lacks requirements for responsible data collection work might result in low-quality or poorly collected data.     
    :::column-end:::

:::row-end:::

-----

:::row:::
    :::column span="":::
        **Qualify geographies carefully.** 
    :::column-end:::

    :::column span="":::
        - When applicable, collecting data in areas of high geopolitical risk and/or unfamiliar geographies might result in unusable or low-quality data and might impact the safety of involved parties.
    :::column-end:::

:::row-end:::

-----

:::row:::
    :::column span="":::
        **Be a good steward of your datasets.**
    :::column-end:::

    :::column span="":::
        - Improper data management and poor documentation can result in data misuse.
    :::column-end:::

:::row-end:::

-----


>[!NOTE]
>This article focuses on recommendations for human data, including personal data and sensitive data such as biometric data, health data, racial or ethnic data, data collected manually from the general public or company employees, as well as metadata relating to human characteristics, such as age, ancestry, and gender identity, that may be created via annotation or labeling. 

[Download the full recommendations here](https://bit.ly/3FK8m8A)

## Best practices for collecting age, ancestry, and gender identity

For AI systems to work well for everyone, the datasets used for training and evaluation should reflect the diversity of people who use or are affected by those systems. In many cases, age, ancestry, and gender identity can help approximate the range of factors that might affect how well a product performs for various people. However, collecting this information requires special consideration.

If you collect this data, always let data contributors self-identify (choose their own responses) instead of having data collectors make assumptions, which might be incorrect. Also include a "prefer not to answer" option for each question. These practices show respect for the data contributors and yield more balanced and higher-quality data.
 
Microsoft developed these best practices based on three years of research with intended stakeholders and collaboration with many teams at Microsoft: [fairness and inclusiveness working groups](https://www.microsoft.com/ai/our-approach?activetab=pivot1:primaryr5), [Global Diversity & Inclusion](https://www.microsoft.com/diversity/default.aspx), [Global Readiness](https://www.microsoft.com/security/blog/2014/09/29/microsoft-global-readiness-diverse-cultures-multiple-languages-one-world/), [Office of Responsible AI](https://www.microsoft.com/ai/responsible-ai?activetab=pivot1:primaryr6), and others.   

To enable people to self-identify, consider using the following survey questions. 

### Age

**How old are you?**

*Select your age range*

[*Include appropriate age ranges as defined by project purpose, geographical region, and guidance from domain experts*]

- \# to # 
- \# to # 
- \# to # 
- Prefer not to answer


### Ancestry

**Select the categories that best describe your ancestry**

*You can select multiple options*

[*Include appropriate categories as defined by project purpose, geographical region, and guidance from domain experts*]

- Ancestry group 
- Ancestry group 
- Ancestry group 
- Multiple (multiracial, mixed ancestry) 
- Not listed, I describe myself as: _________________ 
- Prefer not to answer 


### Gender identity

**How do you identify?**

*You can select multiple options*

[*Include appropriate gender identities as defined by project purpose, geographical region, and guidance from domain experts*]

- Gender identity 
- Gender identity 
- Gender identity 
- Prefer to self-describe: _________________ 
- Prefer not to answer 


>[!CAUTION] 
>In some parts of the world, laws criminalize specific gender categories. It might be dangerous for data contributors to answer this question honestly. Always give people a way to opt out. Work with regional experts and attorneys to conduct a careful review of the laws and cultural norms of each place where you plan to collect data. If needed, avoid asking this question entirely. 

[Download the full guidance here.](https://bit.ly/3woCOAz)

## Next steps
For more information on how to work with your data, see: 

- [Secure data access in Azure Machine Learning](concept-data.md)
- [Data ingestion options for Azure Machine Learning workflows](concept-data-ingestion.md)
- [Optimize data processing with Azure Machine Learning](concept-optimize-data-processing.md)

To work with your data after you collect it, follow these how-to guides:

- [Set up image labeling](how-to-create-image-labeling-projects.md)
- [Label images and text](how-to-label-data.md)

