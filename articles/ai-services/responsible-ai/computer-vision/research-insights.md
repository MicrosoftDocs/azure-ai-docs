---
title: Research insights for Azure AI Vision spatial analysis
titleSuffix: Azure AI services
description: This document details research insights for a Azure AI Vision spatial analysis container deployment.
author: PatrickFarley
manager: nitinme
ms.author: pafarley
ms.service: azure-ai-vision
ms.topic: article
ms.date: 08/15/2022
---

# Research Insights for Azure AI Vision spatial analysis

This section summarizes research insights which apply to applications of AI systems that gather data from the environment to generate insights about how people behave. All sources for the references made in this article are listed in the [references section](#references).

## Research insights

**AI systems need to be designed to support effective human decision-making.**
AI systems are probabilistic in nature and can be computationally complex. In order to make it easier for users to be aware of system errors and other unintended outcomes and thereby support effective human decision-making(15), it is critical that these systems provide explanations about how the system works and be designed with the right level of human control.(16,17) The right level of human involvement needs to be evaluated on a per scenario/ context-of-use basis.(18,19)

**People prefer having the option to opt-in/out.**
In scenarios where technology is being used to monitor individuals' presence and behavior, many people expect to have the option to decide if they will participate.(4,20) Furthermore, some also expect that they would not be automatically enrolled into these scenarios. Some people will take actions to avoid interaction with technology when it is viewed as undesirable (i.e., having low perceptions on benefits).(21)

**Space Analysis metrics require clear explanations about what is NOT being recorded.**
People can have difficulty understanding how novel technology such as Space Analysis technology works. In the presence of monitoring technology, people's default position is that their personal data is being recorded.(20)

**People want to know what data is being processed and/or stored/recorded, how it is being used, and how it is secured.**
People care a lot about the data that systems collect about them.(4,8,21) Many people desire to understand the details of how data is used and secured. Furthermore, there is a need to know who would have access to the data, and what controls are in place to allow deletion of personal data, if applicable.(4,20,22,23)

**Concerns with workplace employee monitoring**
Recent external research shows that many people care about what organizations and employers are doing to ensure public safety with respect to COVID-19.(1,2,3) However, there is also research that shows people have less trust when the technology is used in a workplace environment for monitoring purposes. Across multiple studies, people have indicated discomfort in being monitored in the workplace.(4,5,6,7,8) The recommendations in this report consider the tension.

**Some workplace locations are expected to be more private.**
Research on space analysis technology indicates that the presence of space monitoring cameras is less welcome in personal workspaces, meeting spaces, conference rooms, and hallways (where people commonly have impromptu conversations).(4) Additionally, it is expected that restrooms should remain completely private and there may be additional legal considerations.

**Risk-benefit comparison**
For COVID-19 scenarios, the benefits of public health and safety need to be communicated.(2,3) Public polling shows that many are willing to make economic sacrifices in order to save lives(9), and place high importance on having safety conditions met before returning to normal activities.(10) However, trust in surveillance technology depends on perceived benefits. For example, there is generally trust in the use of surveillance technologies for building access as there is a clear perceived benefit (e.g. security & efficiency).(5)

**Trust in technology varies across demographic groups**
Careful considerations for marginalized groups should be taken when deploying technology. Some demographic groups have less trust in technology based on societal inequities and cultural norms.(5) For example, systematically marginalized groups often alter their behavior out of fear or intimidation when under surveillance (e.g., women, ethnic minorities, introverts).(13,14)

**People need time to weigh perceived benefits against perceived harms.**
In general, people do a cost-benefit analysis based on their perceptions of how a technology may impact them, but they are rarely capable of performing this analysis in the moment (especially if they are being observed).(5) In many scenarios this analysis can be
polarizing, where the perceived outcome is either primarily harmful or primarily beneficial. It is less common that both harms and benefits are perceived in equal magnitude. As a result, if benefits aren't clearly described and demonstrated, and if concerns and harms aren't proactively addressed, adoption may be put at risk because of the polarizing nature of this cost-benefit analysis.(23,24,25)

**Trust in surveillance technology increases when promoting efficiency, security, and safety.**
Public perceptions of surveillance technology become more favorable, and contribute to building trust, when there are clearly demonstrated benefits around efficiency, security, and safety.(5) Distrust in technology increases with perceptions of system
inaccuracies and the potential harmful consequences of errors. Additionally, people distrust technology when is perceived to infringe
on civil liberties. The public does not fully understand the nuance of identifiable monitoring systems, and de-identified systems.

**People tend to have greater trust in surveillance technology when used by official government agencies versus commercial entities.**
The public, generally, has more trust in in surveillance technology when it is used by official government agencies (e.g., law enforcement, airport security), compared to in the use of the technology by private and commercial organizations, due to concerns about data misuse.(5,6,7) Ongoing events with personal data hacks and misuse by corporations have contributed to this negative  perception.(26,27)

## References

1. Brenan, M. (2020). [Amid Slow Return to Workplaces, COVID-19 Precautions Abound](https://news.gallup.com/poll/312461/amid-slow-return-workplaces-covid-precautions-abound.aspx). Gallup.

2. Gandhi, V. (2020). [As COVID-19 Continues, Employees Are Feeling Less Prepared](https://www.gallup.com/workplace/313358/covid-continues-employees-feeling-less-prepared.aspx). Gallup.

3. Weber Shandwick, (2020). [Employee Perceptions on Returning to Work](https://www.webershandwick.com/news/employee-perceptions-on-returning-to-work/).

4. Noah, B., Sethumadhavan, A., Li, L., Pratt, K., (2019). [Real-Time Computer Vision Studio C Camera Installation-Community Jury](https://hits.microsoft.com/study/6014413). Microsoft Corporation - Confidential.

5. Noah, B., Simanto, M. H. S., Krones, J., Sethumadhavan, A., Bakkalbasioglu, E. (2019). [Trust in Facial Recognition Technology-International Survey](https://hits.microsoft.com/study/6014413). Microsoft Corporation -- Confidential.

6. Smith, A., (2019). [More Than Half of U.S. Adults Trust Law Enforcement to Use Facial Recognition Responsibly](https://www.pewresearch.org/internet/2019/09/05/more-than-half-of-u-s-adults-trust-law-enforcement-to-use-facial-recognition-responsibly/). Pew Research Center.

7. Ada Lovelace Institute (2019). [Beyond Face Value: Public Attitudes to Facial Recognition Technology](https://www.adalovelaceinstitute.org/wp-content/uploads/2019/09/Public-attitudes-to-facial-recognition-technology_v.FINAL_.pdf). Nuffield Foundation.

8. Madden, M., (2014). [Public Perceptions of Privacy and Security in the Post-Snowden Era](https://www.pewresearch.org/internet/2014/11/12/public-privacy-perceptions/). Pew Research Center.

9. Chamier, P. von, Noel, N., Angell, E., (2020). [Public Opinion, Trust, and the COVID-19 Pandemic](https://cic.nyu.edu/sites/default/files/public-opinion-trust-and-covid19.pdf). Center on International Cooperation.

10. Brenan, M. (2020). [Targeted Quarantines Top U.S. Adults' Conditions for Normalcy](https://news.gallup.com/poll/310247/targeted-quarantines-top-u-s-adults-conditions-normalcy.aspx). Gallup.

11. Wang, Y., Norice, G., Cranor, L. F., (2011). [Who is concerned about what? A study of Chinese and Indian users' privacy concerns on social network sites](https://experts.syr.edu/en/publications/who-is-concerned-about-what-a-atudy-of-american-chinese-and-india). Syracuse University.

12. GDMA (2018). [Global data privacy: What the consumer really thinks](https://dma.org.uk/uploads/misc/5b0522b113a23-global-data-privacy-report---final-2_5b0522b11396e.pdf). Global Alliance of Data-Driven Marketing Associations.

13. Levulis, S., Sethumadhavan, A., Noah, B., (2018). [Chilling Effects of Intelligent Meeting Systems](https://hits.microsoft.com/study/6009651). Microsoft Corporation - Confidential.

14. Penney, J. W., (2017). [Internet surveillance, regulation, and chilling effects online: a comparative case study](https://policyreview.info/articles/analysis/internet-surveillance-regulation-and-chilling-effects-online-comparative-case). Internet Policy
Review.

15. Parasuraman, R., Wickens, C. D., (2008). [Humans: Still Vital After All These Years of Automation](https://journals.sagepub.com/doi/abs/10.1518/001872008X312198). Human Factors: The Journal of the Human Factors and Ergonomics Society.

16. Whittaker, M., Crawford, K., Dobbe, R., Fried, G., Kaziunas, E., Mathur, V., West, S. M., Richardson, R., Schultz, J., Schwartz, O., (2018). [AI Now Report 2018](https://ainowinstitute.org/publication/ai-now-2018-report-2). AI Now Institute.

17. Parasuraman, R., Sheridan, T., Wickens, C. D., (2000). [A Model for Types and Levels of Human Interaction with Automation](https://ieeexplore.ieee.org/abstract/document/844354). IEEE Transactions on Systems, Man, and Cybernetics.

18. [Human Information Processing](https://web.archive.org/web/20170608105318/https://www.ergonomicsblog.uk/human-information-processing/). Ergonomics Blog.

19. Jones, D. G., Endsley, M. R., Bolstad, M., Estes, G. (2004). [The designer's situation awareness toolkit: Support for user-centered design](https://www.researchgate.net/publication/237460827_The_Designer%27s_Situation_Awareness_Toolkit_Support_for_User-Centered_Design). Human Factors and Ergonomics Society Annual Meeting Proceedings.

20. Madden, M., Raine, L., (2015). [Americans' Attitudes About Privacy, Security, and Surveillance](https://www.pewresearch.org/internet/2015/05/20/americans-attitudes-about-privacy-security-and-surveillance/). Pew Research Center.

21. Bakkalbasioglu, E., Sethumadhavan, A., (2020). [Surveillance and AI](https://hits.microsoft.com/Collection/7001443). Microsoft Corporation - Confidential.

22. Bakkalbasioglu, E., Sethumadhavan, A., (2020). [Enrollment Flow Evaluation: Frictionless Access Program](https://hits.microsoft.com/Study/6018123). Microsoft Corporation - Confidential.

23. Kropp, B., (2019). [The Future of Employee Monitoring](https://www.gartner.com/smarterwithgartner/the-future-of-employee-monitoring/). Gartner.

24. Bakkalbasioglu, E., Sethumadhavan, A., (2019). [Use of Facial Recognition Technology in Grocery Stores: Co-Creation](https://hits.microsoft.com/Study/6012953). Microsoft Corporation - Confidential.

25. Bakkalbasioglu, E., Sethumadhavan, A., (2019). [Use of Facial Recognition Technology in Building Access: Co-Creation](https://hits.microsoft.com/Study/6013092). Microsoft Corporation - Confidential.

26. Perrin, A., (2018). [Americans are changing their relationship with Facebook](https://www.pewresearch.org/fact-tank/2018/09/05/americans-are-changing-their-relationship-with-facebook/). Pew Research Center.

27. Doherty, C., Kiley, J., (2019). [Americans have become much less positive about tech companies' impact on the U.S.](https://www.pewresearch.org/fact-tank/2019/07/29/americans-have-become-much-less-positive-about-tech-companies-impact-on-the-u-s/). Pew Research Center.
