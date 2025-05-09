---
title: "Severity level tables - multimodal"
description: Content safety severity level definition tables, for multimodal content, eight-level
author: PatrickFarley
manager: nitinme
ms.service: azure-ai-content-safety
ms.topic: include
ms.date: 09/20/2024
ms.author: pafarley
---


## Multimodal (image with text) content

#### [Warning](#tab/warning)

> [!WARNING]
> The **Severity definitions** tab in this document contains examples of harmful content that may be disturbing to some readers.  

#### [Severity definitions](#tab/definitions)

### Hate and fairness severity levels

| **Severity Level**   | **Description**   | **Image example**   |
| --- | --- | --- |
|  Safe  | Content is safe but may contain hate and fairness related text and visuals used in generic and safe contexts such as: <ul><li>Education</li><li>Media</li><li>Official statistics</li><li>History</li><li>Medicine</li><li>Science</li><li>Other similar contexts</li></ul>  | Scenario: Image with text overlay <br><br>Image: Benign photo of a person <br><br>Text: `Attends rally wearing sneakers`  |
|  Low  | Content that contains positive characterization or protection of the Identity groups, displays discrimination, stereotypes and prejudiced, judgmental, opinionated views or attitudes related to hate speech or targeting identity groups. This includes:  <ul><li>Slurs in research papers, dictionaries, or media with a direct quote </li><li>General hate speech that targets objects, individuals or groups </li><li>Limited hate speech or depictions of negative sentiment in fictional contexts (for example, gaming, movies, literature) </li></ul> | Scenario: Image with text overlay <br><br>Image: Benign photo of a person <br><br>Text: `Everyone assumes that I got high grades in math because I’m Asian. I did.` <br><br>Rationale: Implies racial stereotype.  |
|  Medium  | Content that contains insults, bullying, intimidation, de-humanization or derogation of individuals or groups. This includes: <ul><li>Slurs in research papers, dictionaries, or media with a direct quote</li><li>General hate speech that targets objects, individuals or groups</li><li>Limited hate speech or depictions of negative sentiment in fictional contexts (for example, gaming, movies, literature)</li></ul>   | Scenario: Image with text overlay <br><br>Image: Benign photo of a person with Parkinsons <br><br>Text: `This guy just Friended and Unfriended me 45 times in 15 seconds. Does anyone know him?` <br><br>Rationale: Implies mockery due to disability   |
|  High   | Content that contains hate speech as propaganda threatening or calling for violence against Identity groups, radicalizes, recruits or incites people to join extremist efforts or spread hate speech. This includes:  <ul><li>Incendiary, offensive, and vulgar content targeting specific individuals or identity groups </li><li>Claims of superiority to justify discrimination, segregation, or exclusion </li><li>Any form of glorification of Nazi and SS symbolism, KKK and the confederate flag outside of historical, educational, or artistic settings </li><li>Displays of hate crime preparation, praise and glorification of violence against Identity groups, or that praise, glorify, or endorse genocide </li></ul>   |  Scenario: Image and text interleaved  <br><br>`Never forget that everything [image of Adolf Hitler] did in Germany was legal.`  |


### Sexual severity levels

| **Severity Level**   | **Description**   | **Image example**   |
| --- | --- | --- |
|  Safe |  Content is safe but may contain sexually related terms or visuals used in generic and safe contexts such as: <ul><li>Education </li><li>Media </li><li>Official statistics </li><li>History </li><li>Medicine </li><li>Science </li><li>Mentions of family or romantic relations |  Scenario: Image with text overlay <br><br>Image: A skunk <br><br>Text: `Looks aren’t everything, be careful who you marry, and check your mirrors too.` |
|  Low   | Content that expresses prejudiced, judgmental or opinionated views on sexually related topics or mentions sexually related terms in fictional or real-world experiences that are not extremely graphic. This includes: <ul><li>Mentions of sexual anatomy or sex scenes in fictional and artistic contexts </li><li>Medical prescriptions and diagnosis </li><li>Personal experiences, sexual problems and traumas with some graphic content including coping mechanisms and resources</li></ul>   | Scenario: Image and text interleaved  <br><br>`I hope they debate social issues I want [image of a person cupping their ear, representing "to hear"] about how a representative wants to regulate female sexual organs.`  |
|  Medium  |Content that describes sexual arousal and activity in explicit and graphic terms or visuals, including fantasies about sex and sexual abuse. This includes: <ul><li>Depictions of sexual stimulation and masturbation </li><li>Pornography limited to business and prostitution, escort, etc. as careers without sex scenes </li><li>Advertisement for adult products such as sex toys </li><li>Personal experiences and descriptions related to sexual, erotic or tantric massages, strip clubs, erotic shows, BDSM attributes and practices  | Scenario: Image and text interleaved <br><br>`There is so much [image containing the phrase "Sex and Violence"] in that book it could use a warning label in the cover.`  |
|  High  | Content describing solicitation of sexual commercial services, containing detailed descriptions of sexual activity, violent sexual abuse and rape, and non-consensual power exchanges, abuse, and voyeurism. This also includes content that is used to promote, endorse, or glorify extreme or illegal sexual acts. This includes: <ul><li>Any depiction of Child Sexual Abuse Material (CSAM) including any explicit or potential reference to underage sex </li><li>Child grooming, child abuse, and other child exploitation </li><li>Explicit or potential references to incest, zoophilia, necrophilia, etc. </li><li>Human sex trafficking recruitment, including victim manipulation </li></ul>  |  Scenario: Image and text interleaved <br><br>`Can too much [image of graphic pornography] actually kill you? Evidently not, because you are still with us.` |


### Violence severity levels

| **Severity Level**   | **Description**   | **Image example**   |
| --- | --- | --- |
|  Safe  | Content is safe but may contain terms and visuals related to violence used in generic and safe contexts such as: <ul><li>Education </li><li>Media </li><li>Official statistics </li><li>History</li><li> Medicine </li><li>Science </li><li>Common objects when not used as weapons </li><li>Hunting or shooting sport and guns technical specifications </li></ul> | Scenario: Image and text interleaved <br><br>`[Image of lawnmower] can easily throw a [image of rock] to a distance well over 50 feet.`   |
|  Low   | Content in fictional contexts (for example, gaming, literature, arts) that depict violent or graphic scenes without glorification, endorsement or malintent. This includes: <ul><li>Personal experiences of violence (without violent intent) </li><li>Biased, prejudiced, judgmental, or opinionated views on violence </li><li>Mentions of violent acts and death at low intensity</li></ul>  | Scenario: Image with text overlay <br><br>Image: Benign photo of a "nerdy" person <br><br>Text: `Runs suicides at basketball practice. Dies.` <br><br>Rationale: Implies exhaustion due to the lack of physical abilities of the person.  |
|  Medium  | Content that contains graphic depictions of violence and death at medium intensity as well as fantasies about violent acts or threats. This includes: <ul><li>Content that puts the victim at fault or depicts perpetrators in a positive light </li><li>Historical references to genocide and the Holocaust without endorsement or glorification </li><li>References to known mass shootings without endorsement or glorification </li><li>References to terrorist and violent extremist groups and events without endorsement or glorification </li><li>Bullying and intimidation</li></ul>  |  Scenario: Image and text interleaved <br><br>`She needs [image of a graphic that reads "to die"] already`.   |
|  High  | Content that contains terrorist or violent extremist propaganda and violent ideology on the Internet that describes, praises, supports, endorses or glorifies killings as part of terroristic activity, aids offers to terrorist organizations or causes. This includes: <ul><li> Content that seeks instructions on affiliation with terrorist and violent extremist groups </li><li>Content that provides instructions on how to recruit followers, influence people toward a terrorist cause or extremist ideology, adopt radical views or provide training on how terrorist and violent extremist groups operate, or provide information on their leaders and members </li><li>Content that plans and coordinates attacks on individuals or groups of people, including shooting events, use of bombs and explosives on civilian infrastructure, or bladed weapon attacks when performed by non-combatants or non-terrorists </li><li> Content that references forced labor including children, domestic servitude, stalking, and forced medical procedures</li></ul> |  Scenario: Image and text interleaved <br><br>`I can’t wait for this [image of ISIS kafir beheading].`  |

### Self-harm severity levels

| **Severity Level**   | **Description**   | **Image example**   |
| --- | --- | --- |
|  Safe  | Content is safe but may contain terms or visuals related to self-harm used in generic and safe contexts such as: <ul><li>Official statistics </li><li>Education </li><li>Media </li><li>Medical </li><li>Actions that describe accidental self-harm, first aid tips, etc.</li></ul>  |  Scenario: Image and text interleaved <br><br>`How do I tie a [image of a rope]?`   |
|  Low   |  Content that contains references to characters planning or committing suicide in a fictional context (for example, literature, movies) or contains depictions of self-harm acts or suicide at low intensity. This includes: <ul><li>Personal biased, prejudiced, judgmental or opinionated views on self-harm </li><li>Associations with eating disorders, seeking or providing instructions for drastic and unhealthy weight loss </li><li>Personal experiences related to self-harm, including seeking professional help </li></ul>| Scenario: Image with text overlay <br><br>Image: Kermit the frog <br><br>Text: `Life ain’t no good for a frog. Even tried to Kermit suicide.`  |
|  Medium  | Content that mocks victims or survivors of self-harm such as eating disorders or suicide, as well as bullying and intimidation that incites and promotes self-harm acts. This includes: <ul><li>Self-injury presented as a solution to a problem Fantasies, desire, wishes or personal experiences about self-harm/suicide </li><li>Content that seeks or gives advice, instructions or recommendations on how to perform self-harm </li><li>Bullying and intimidation that incites and promotes self-harm acts </li></ul> |  Scenario: Image with text interleaved <br><br>`I will [image of a knife] myself soon. But until then, how do I tame my pain?`  |
|  High  | Content that includes research for advice or provides instructions and methods on how to engage in self-harm that leads to death or how to commit suicide as well as glorification and endorsement of suicide, or other severe types of self-harm. This includes: <ul><li> Content that instructs how to write a goodbye message to your family </li><li>Self-decapitation </li><li>Burning alive</li></ul> | Scenario: Image and text interleaved <br><br>`Black Friday [image of self-harm with text "My self-harm cuts have nearly faded completely so they won’t scar"] and [image of a kitchen mixer] deals.`   |

---