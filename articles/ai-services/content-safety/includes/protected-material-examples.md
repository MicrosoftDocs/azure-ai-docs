---
title: "Protected Material Detection examples"
description: "Details about Protected material detection."
author: PatrickFarley
ms.date: 05/08/2025
ms.topic: include
ms.author: pafarley
---

[!INCLUDE [code-indexer](code-indexer.md)]

By detecting and preventing the display of protected material, organizations can ensure compliance with intellectual property laws, maintain content originality, and protect their reputations.

This guide provides details about the kinds of content that the protected material API detects.

## User scenarios

#### [Protected text](#tab/text)

### Content generation platforms for creative writing
- Scenario: A content generation platform that uses generative AI for creative writing (for example, blog posts, stories, marketing copy) integrates the Protected Material for Text feature to prevent the generation of content that closely matches known copyrighted material.
- User: Platform administrators and content creators.
- Action: The platform uses Azure AI Content Safety to scan AI-generated content before it's provided to users. If the generated text matches protected material, the content is flagged and either blocked or revised.
- Outcome: The platform avoids potential copyright infringements and ensures that all generated content is original and compliant with intellectual property laws.

### Automated social media content creation
- Scenario: A digital marketing agency uses generative AI to automate social media content creation. The agency integrates the Protected Material for Text feature to avoid publishing AI-generated content that includes copyrighted text, such as song lyrics or excerpts from books.
- User: Digital marketers and social media managers.
- Action: The agency employs Azure AI Content Safety to check all AI-generated social media content for matches against a database of protected material. Content that matches is flagged for revision or blocked from posting.
- Outcome: The agency maintains compliance with copyright laws and avoids reputation risks associated with posting unauthorized content.

### AI-assisted news writing
- Scenario: A news outlet uses generative AI to assist journalists in drafting articles and reports. To ensure the content does not unintentionally replicate protected news articles or other copyrighted material, the outlet uses the Protected Material for Text feature.
- User: Journalists, editors, and compliance officers.
- Action: The news outlet integrates Azure AI Content Safety into its content creation workflow. AI-generated drafts are automatically scanned for protected content before submission for editorial review.
- Outcome: The news outlet prevents accidental copyright violations and maintains the integrity and originality of its reporting.

### E-learning platforms using AI for content generation
- Scenario: An e-learning platform employs generative AI to generate educational content, such as summaries, quizzes, and explanatory text. The platform uses the Protected Material for Text feature to ensure the generated content does not include protected material from textbooks, articles, or academic papers.
- User: Educational content creators and compliance officers.
- Action: The platform integrates the feature to scan AI-generated educational materials. If any content matches known protected academic material, it's flagged for revision or automatically removed.
- Outcome: The platform maintains educational content quality and complies with copyright laws, avoiding the use of protected material in AI-generated learning resources.

### AI-powered recipe generators
- Scenario: A food and recipe website uses generative AI to generate new recipes based on user preferences. To avoid generating content that matches protected recipes from famous cookbooks or websites, the website integrates the Protected Material for Text feature.
- User: Content managers and platform administrators.
- Action: The website uses Azure AI Content Safety to check AI-generated recipes against a database of known protected content. If a generated recipe matches a protected one, it's flagged and revised or blocked.
- Outcome: The website ensures that all AI-generated recipes are original, reducing the risk of copyright infringement.

#### [Protected code](#tab/code)

### Software Development Platforms
- Scenario: A software development platform that utilizes generative AI to help developers write code integrates the Protected Material for Code feature to prevent the generation of code that replicates material from existing GitHub repositories.
- User: Platform administrators, developers.
- Action: The platform uses Azure AI Content Safety to scan AI-generated code. If any code matches protected material, it's flagged for review, revised, or blocked.
- Outcome: The platform ensures that all AI-generated code is original and complies with licensing agreements, reducing legal and compliance risks.

### Automated Code Writing Tools
- Scenario: A development team uses generative AI to automate parts of their code writing. The team integrates the Protected Material for Code feature to prevent the accidental use of code snippets that match content from existing GitHub repositories, including open-source code with restrictive licenses.
- User: Software developers, DevOps teams.
- Action: Azure AI Content Safety checks the generated code against known material from GitHub repositories. If a match is found, the code is flagged and revised before it's incorporated into the project.
- Outcome: The team avoids potential copyright infringement and ensures the AI-generated code adheres to appropriate licenses.

### AI-assisted Code Reviews
- Scenario: A software company integrates AI-assisted code review tools into its development process. To avoid introducing protected code from GitHub or external libraries, the company uses the Protected Material for Code feature.
- User: Code reviewers, software developers, compliance officers.
- Action: The company scans all AI-generated code for matches against protected material from GitHub repositories before final code review and deployment.
- Outcome: The company prevents the inclusion of protected material in their projects, maintaining compliance with intellectual property laws and internal standards.

### AI-generated Code for Educational Platforms
- Scenario: An e-learning platform uses generative AI to generate example code for programming tutorials and courses. The platform integrates the Protected Material for Code feature to ensure that generated examples do not duplicate code from existing GitHub repositories or other educational sources.
- User: Course creators, platform administrators.
- Action: Azure AI Content Safety checks all AI-generated code examples for protected content. Matches are flagged, reviewed, and revised.
- Outcome: The platform maintains the integrity and originality of its educational content while adhering to copyright laws.

### AI-powered Coding Assistants
- Scenario: A coding assistant tool powered by generative AI helps developers by generating code suggestions. To ensure that no suggestions infringe on code from GitHub repositories, the assistant tool uses the Protected Material for Code feature.
- User: Developers, tool administrators.
- Action: The tool scans all code suggestions for protected material from GitHub before presenting them to developers. If a suggestion matches protected code, it's flagged and not shown.
- Outcome: The coding assistant ensures that all code suggestions are free from protected content, fostering originality and reducing legal risks.
By integrating the Protected Material for Code feature, organizations can manage risks associated with AI-generated code, maintain compliance with intellectual property laws, and ensure the originality of their code outputs.

---

## Protected material text examples

Refer to this table for details of the major categories of protected material text detection. All four categories are applied when you call the API.

| Category | Scope  | Considered acceptable  | Considered harmful    |
|---|-------|---|--------|--|
| Recipes     | Copyrighted content related to Recipes.   <br><br> Other harmful or sensitive text is out of scope for this task, unless it intersects with Recipes IP copyright harm. | <ul><li>Links to web pages that contain information about recipes  </li><li>Any content from recipes that have no or low IP/Copyright protections: <ul><li>Lists of ingredients</li><li>Basic instructions for combining and cooking ingredients</li></ul></li><li>Rejection or refusal to provide copyrighted content: <ul><li>Changing a topic to avoid sharing copyrighted content</li><li>Refusal to share copyrighted content</li><li>Providing nonresponsive information</li></ul></li></ul> | <ul><li>Other literary content in a recipe <ul><li>Matching anecdotes, stories, or personal commentary about the recipe (40 characters or more)</li><li>Creative names for the recipe that are not limited to the well-known name of the dish, or a plain descriptive summary of the dish indicating what the primary ingredient is (40 characters or more)</li><li>Creative descriptions of the ingredients or steps for combining or cooking ingredients, including descriptions that contain more information than needed to create the dish, rely on imprecise wording, or contain profanity (40 characters or more)</li></ul></li><li>Methods to access copyrighted content:<ul><li>Ways to bypass paywalls to access recipes</li></ul></li></ul> |
| Web Content | All websites that have `webmd.com` as their URL domain name. Only focuses on issues of copyrighted content around Selected Web Content. <br><br> Other harmful or sensitive text is out of scope for this task, unless it intersects Selected Web Content harm. | <ul><li>Links to web pages </li><li>Short excerpts or snippets of Selected Web Content as long as:<ul><li>They are relevant to the user's query</li><li>They are fewer than 200 characters</li></ul></li></ul>    | <ul><li>Substantial content of Selected Web Content  <ul><li>Response sections longer than 200 characters that bear substantial similarity to a block of text from the Selected Web Content</li><li>Excerpts from Selected Web Content that are longer than 200 characters</li><li>Quotes from Selected Web Content that are longer than 200 characters</li></ul></li><li>Methods to access copyrighted content:<ul><li>Ways to bypass paywalls or DRM protections to access copyrighted Selected Web Content</li></ul></li></ul>           |
| News        | Only focus on issues of copyrighted content around News. <br><br> Other harmful or sensitive text is out of scope for this task, unless it intersects News IP Copyright harm. | <ul><li>Links to web pages that host news or information about news, magazines, or blog articles as long as:<ul><li>They have legitimate permissions</li><li>They have licensed news coverage</li><li>They are authorized platforms</li></ul></li><li>Links to authorized web pages that contain embedded audio/video players as long as:<ul><li>They have legitimate permissions</li><li>They have licensed news coverage</li><li>They are authorized streaming platforms</li><li>They are official YouTube channels</li></ul></li><li>Short excerpts/snippets like headlines or captions from news articles as long as:<ul><li>They are relevant to the user's query</li><li>They are not a substantial part of the article</li><li>They are not the entire article</li></ul></li><li>Summary of news articles as long as:<ul><li>It is relevant to the user's query</li><li>It is brief and factual</li><li>It does not copy/paraphrase a substantial part of the article</li><li>It is clearly and visibly cited as a summary</li></ul></li><li>Analysis/Critique/Review of news articles as long as:<ul><li>It is relevant to the user's query</li><li>It is brief and factual</li><li>It does not copy/paraphrase a substantial part of the article</li><li>It is clearly and visibly cited as an analysis/critique/review</li></ul></li><li>Any news content that has no IP/Copyright protections:<ul><li>News/Magazines/Blogs that are in the public domain</li><li>News/Magazines/Blogs for which Copyright protection has elapsed, been surrendered, or never existed</li></ul></li><li>Rejection or refusal to provide copyrighted content:<ul><li>Changing topic to avoid sharing copyrighted content</li><li>Refusal to share copyrighted content</li><li>Providing nonresponsive information</li></ul></li></ul> | <ul><li>Links to pdf or any other file containing full text of news/magazine/blog articles, unless:<ul><li>They are sourced from authorized platforms with legitimate permissions and licenses</li></ul></li><li>News content<ul><li>More than 200 characters taken verbatim from any news article</li><li>More than 200 characters substantially similar to a block of text from any news article</li><li>Direct access to news/magazine/blog articles that are behind paywalls</li></ul></li><li>Methods to access copyrighted content:<ul><li>Steps to download news from an unauthorized website</li><li>Ways to bypass paywalls or DRM protections to access copyrighted news or videos</li></ul></li></ul>       |
| Lyrics      | Only focuses on issues of copyrighted content around Songs.     <br><br> Other harmful or sensitive text is out of scope for this task, unless it intersects Songs IP Copyright harm. | <ul><li>Links to web pages that contain information about songs such as:<ul><li>Lyrics of the songs</li><li>Chords or tabs of the associated music</li><li>Analysis or reviews of the song/music</li></ul></li><li>Links to authorized web pages that contain embedded audio/video players as long as:<ul><li>They have legitimate permissions</li><li>They have licensed music</li><li>They are authorized streaming platforms</li><li>They are official YouTube channels</li></ul></li><li>Short excerpts or snippets from lyrics of the songs as long as:<ul><li>They are relevant to the user's query</li><li>They are not a substantial part of the lyrics</li><li>They are not the entire lyrics</li><li>They are not more than 11 words long</li></ul></li><li>Short excerpts or snippets from chords/tabs of the songs as long as:<ul><li>They are relevant to the user's query</li><li>They are not a substantial part of the chords/tabs</li><li>They are not the entire chords/tabs</li></ul></li><li>Any content from songs that have no IP/Copyright protections:<ul><li>Songs/Lyrics/Chords/Tabs that are in the public domain</li><li>Songs/Lyrics/Chords/Tabs for which Copyright protection has elapsed, been surrendered, or never existed</li></ul></li><li>Rejection or refusal to provide copyrighted content:<ul><li>Changing topic to avoid sharing copyrighted content</li><li>Refusal to share copyrighted content</li><li>Providing nonresponsive information</li></ul></li></ul>         | <ul><li>Lyrics of a song<ul><li>Entire lyrics</li><li>Substantial part of the lyrics</li><li>Part of lyrics that contain more than 11 words</li></ul></li><li>Chords or Tabs of a song<ul><li>Entire chords/tabs</li><li>Substantial part of the chords/tabs</li></ul></li><li>Links to webpages that contain embedded audio/video players that:<ul><li>Do not have legitimate permissions</li><li>Do not have licensed music</li><li>Are not authorized streaming platforms</li><li>Are not official YouTube channels</li></ul></li><li>Methods to access copyrighted content:<ul><li>Steps to download songs from an unauthorized website</li><li>Ways to bypass paywalls or DRM protections to access copyrighted songs or videos</li></ul></li></ul>   |
