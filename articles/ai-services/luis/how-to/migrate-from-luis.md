---
title: Conversational Language Understanding backwards compatibility
titleSuffix: Foundry Tools
description: Learn about backwards compatibility between Language Understanding (LUIS) and Conversational Language Understanding
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: how-to
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-clu
---
# Migrate from Language Understanding (LUIS) to conversational language understanding (CLU)

Conversational language understanding (CLU) is a cloud-based AI offering in Azure Language in Foundry Tools. It's the newest generation of Language Understanding (LUIS) and offers backwards compatibility with previously created LUIS applications. CLU employs state-of-the-art machine learning intelligence to allow users to build a custom natural language understanding model for predicting intents and entities in conversational utterances.

CLU offers the following advantages over `LUIS`:

- Improved accuracy with state-of-the-art machine learning models for better intent classification and entity extraction. LUIS required more examples to generalize certain concepts in intents and entities, while CLU's more advanced machine learning reduces the burden on customers by requiring less data.
- Multilingual support for model learning and training. Train projects in one language and immediately predict intents and entities across 96 languages.
- Ease of integration with different CLU and custom question answering projects using orchestration workflow.
- The ability to add testing data within the experience using Language Studio and APIs for model performance evaluation before deployment.

To get started, you can use CLU directly or migrate your LUIS application.

## Comparison between LUIS and CLU

The following table presents a side-by-side comparison between the features of LUIS and CLU. It also highlights the changes to your LUIS application after migrating to CLU. Select the linked concept to learn more about the changes.

|LUIS features | CLU features | Post migration |
|:------------:|:----------------------------------------------:|:--------------:|
|Machine-learned and Structured ML entities| Learned entity components |Machine-learned entities without subentities are transferred as CLU entities. Structured ML entities only transfer leaf nodes (lowest level subentities that don't have their own subentities) as entities in CLU. The name of the entity in CLU is the name of the subentity concatenated with the parent. For example, _Order.Size_|
|List, regex, and prebuilt entities| List, regex, and prebuilt entity components | List, regex, and prebuilt entities are transferred as entities in CLU with a populated entity component based on the entity type.|
|`Pattern.Any` entities| Not currently available | `Pattern.Any` entities are removed.|
|Single culture for each application|Multilingual models enable multiple languages for each project. |The primary language of your project is set as your LUIS application culture. Your project can be trained to extend to different languages.|
|Entity roles  |Roles are no longer needed. | Entity roles are transferred as entities.|
|Settings for: normalize punctuation, normalize diacritics, normalize word form, and use all training data.  |Settings are no longer needed. |Settings aren't transferred.  |
|Patterns and phrase list features|Patterns and Phrase list features are no longer needed. |Patterns and phrase list features aren't transferred.  |
|Entity features| Entity components| List or prebuilt entities added as features to an entity are transferred as added components to that entity. Entity features aren't transferred for intents. |
|Intents and utterances| Intents and utterances |All intents and utterances are transferred. Utterances are labeled with their transferred entities. |
|Application `GUID`s |Project names| A project is created for each migrating application with the application name. Any special characters in the application names are removed in CLU.|
|Versioning| Every time you train, a model is created and acts as a version of your project. | A project is created for the selected application version. |
|Evaluation using batch testing |Evaluation using testing sets | Adding your testing dataset is required.|
|Role-Based Access Control (RBAC) for LUIS resources |Role-Based Access Control (RBAC) available for Language resources |Language resource RBAC must be manually added after migration. |
|Single training mode| Standard and advanced training modes | Training is required after application migration. |
|Two publishing slots and version publishing |Ten deployment slots with custom naming | Deployment is required after the application's migration and training. |
|LUIS authoring APIs and SDK support in .NET, Python, Java, and Node.js |CLU Authoring REST APIs. | For more information, see the quickstart article for information on the CLU authoring APIs. Refactoring is necessary to use the CLU authoring APIs. |
|LUIS Runtime APIs and SDK support in .NET, Python, Java, and Node.js |CLU Runtime APIs. CLU Runtime SDK support for .NET and Python. | For more information, *see* how to call the API. Refactoring is necessary to use the CLU runtime API response. |

## Migrate your LUIS applications

Use the following steps to migrate your LUIS application using either the LUIS portal or REST API.

# [LUIS portal](#tab/luis-portal)

## Migrate your LUIS applications using the LUIS portal

Follow these steps to begin migration using the LUIS Portal:

1. After logging into the LUIS portal, select the button on the banner at the top of the screen to launch the migration wizard. The migration copies your selected LUIS applications to CLU. The migration overview tab provides a brief explanation of conversational language understanding and its benefits. Press Next to proceed.


1. Determine Azure Language resource that you wish to migrate your LUIS application to. If you created a Language resource, select your Azure subscription followed by your Language resource, and then select **Next**. If you don't have a Language resource, select the link to create a new Language resource. Afterwards, select the resource and select **Next**.


1. Select all your LUIS applications that you want to migrate, and specify each of their versions. Select **Next**. After selecting your application and version, you're prompted with a message informing you of any features that won't be carried over from your LUIS application.

    > [!NOTE]
    > Conversational language understanding currently doesn't support special characters. Any special characters in your selected LUIS application names are removed in your new migrated applications.

1. Review your Language resource and LUIS applications selections. Select **Finish** to migrate your applications.

1. A popup window lets you track the migration status of your applications. Applications that are successfully migrated have a status of **Not started**. Applications that are beginning migration have a status of **In progress**, and once migration completes the status is **Succeeded**. A **Failed** application means that you must repeat the migration process. Once the migration is completed for all applications, select **Done**.

1. After your applications are migrated, you can perform the following steps:

   * Train your model
   * Deploy your model
   * Call your deployed model

# [REST API](#tab/rest-api)

## Migrate your LUIS applications using REST APIs

Follow these steps to begin migration programmatically using the CLU Authoring REST APIs:

1. Export your LUIS application in JSON format. You can use the LUIS Portal to export your applications, or the LUIS programmatic APIs.

1. Submit a POST request using the following URL, headers, and JSON body to import LUIS application into your CLU project. CLU doesn't support names with special characters so remove any special characters from the project name.

    ### Request URL
    ```rest
    {ENDPOINT}/language/authoring/analyze-conversations/projects/{PROJECT-NAME}/:import?api-version={API-VERSION}&format=luis
    ```

    |Placeholder  |Value  | Example |
    |---------|---------|---------|
    |`{ENDPOINT}`     | The endpoint for authenticating your API request.   | `https://<your-custom-subdomain>.cognitiveservices.azure.com` |
    |`{PROJECT-NAME}`     | The name for your project. This value is case sensitive.   | `myProject` |
    |`{API-VERSION}`     | The version of the API you're calling. | `2023-04-01` |

    ### Headers

    Use the following header to authenticate your request.

    |Key|Value|
    |--|--|
    |`Ocp-Apim-Subscription-Key`| The key to your resource. Used for authenticating your API requests.|

    ### JSON body

    Use the exported LUIS JSON data as your body.

1. After your application migrates, you can perform the following steps:

   * Train your model
   * Deploy your model
   * Call your deployed model

---

## Frequently asked questions

### Does CLU support a specific LUIS version?

Yes, CLU supports the model JSON version 7.0.0. If the JSON format is older, it would need to be imported into LUIS first, then exported from LUIS with the most recent version.

### How are entities different in CLU?

In CLU, a single entity can have multiple entity components, which are different methods for extraction. Those components are then combined together using rules you can define. The available components are:
- Learned: Equivalent to ML entities in LUIS, labels are used to train a machine-learned model to predict an entity based on the content and context of the provided labels.
- List: Just like list entities in LUIS, list components exact match a set of synonyms and maps them back to a normalized value called a **list key**.
- Prebuilt: Prebuilt components allow you to define an entity with the prebuilt extractors for common types available in both LUIS and CLU.
- Regex: Regex components use regular expressions to capture custom defined patterns, exactly like regex entities in LUIS.

Entities in LUIS are transferred over as entities of the same name in CLU with the equivalent components transferred.

After migrating, your structured machine-learned leaf nodes and bottom-level subentities are transferred to the new CLU model while all the parent entities and higher-level entities are ignored. The name of the entity is the bottom-level entity's name concatenated with its parent entity.

#### Example:

LUIS entity:

* Pizza Order
   * Topping
   * Size

Migrated LUIS entity in CLU:

* Pizza Order.Topping
* Pizza Order.Size

You also can't label two different entities in CLU for the same span of characters. Learned components in CLU are mutually exclusive and don't provide overlapping predictions for learned components only. When you migrate your LUIS application, entity labels that overlap preserve the longest label and ignore any others.

For more information on entity components, see Entity components.

### How are entity roles transferred to CLU?

Your roles are transferred as distinct entities along with their labeled utterances. Each role's entity type determines which entity component is populated. For example, a list entity role is transferred as an entity with the same name as the role, with a populated list component.

### How do entity features get transferred in CLU?

Entities used as features for intents aren't transferred. Entities used as features for other entities populate the relevant component of the entity. For example, if a list entity named _SizeList_ was used as a feature to a machine-learned entity named _Size_, then the _Size_ entity is transferred to CLU. The list values from _SizeList_ are added to the list component of the _Size_ entity. The same is applied for prebuilt and regex entities.

### How are entity confidence scores different in CLU?

Any extracted entity has a 100% confidence score and therefore entity confidence scores shouldn't be used to make decisions between entities.

### How is conversational language understanding multilingual?

Conversational language understanding projects accept utterances in different languages. Furthermore, you can train your model in one language and extend it to predict in other languages.

#### Example:

Training utterance (English):  *How are you?*

Labeled intent: Greeting

Runtime utterance (French): *`Comment ça va?`*

Predicted intent: Greeting

### How is the accuracy of CLU better than LUIS?

CLU uses state-of-the-art models to enhance machine learning performance of different models of intent classification and entity extraction.

These models are insensitive to minor variations, removing the need for the following settings: _Normalize punctuation_, _normalize diacritics_, _normalize word form_, and _use all training data_.

Additionally, the new models don't support phrase list features as they no longer require supplementary information from the user to provide semantically similar words for better accuracy. Patterns were also used to provide improved intent classification using rule-based matching techniques that aren't necessary in the new model paradigm. The following question provides more detail.

### What do I do if the features I'm using in LUIS are no longer present?

There are several features that were present in LUIS that are no longer available in CLU. These features include the ability to do feature engineering, having patterns and pattern.any entities, and structured entities. If you had dependencies on these features in LUIS, use the following guidance:

- **Patterns**: Patterns were added in LUIS to assist the intent classification through defining regular expression template utterances. This feature includes the ability to define Pattern only intents (without utterance examples). CLU is capable of generalizing by using the state-of-the-art models. You can provide a few utterances that match a specific pattern to the intent in CLU. In many cases, CLU classifies these different patterns as the top intent without needing the pattern template utterance. This step simplifies the requirement to formulate these patterns, which was limited in LUIS, and provides a better intent classification experience.

- **Phrase list features**: The ability to associate features mainly occurred to assist the classification of intents by highlighting the key elements/features to use. This step is no longer required since the deep models used in CLU already possess the ability to identify the elements that are inherent in the language. In turn removing these features has no effect on the classification ability of the model.

- **Structured entities**: The ability to define structured entities was mainly to enable multilevel parsing of utterances. With the different possibilities of the subentities, LUIS needed all the different combinations of entities to be defined and presented to the model as examples. In CLU, these structured entities are no longer supported, since overlapping learned components aren't supported. There are a few possible approaches to handling these structured extractions:
    - **Non-ambiguous extractions**: In most cases the detection of the leaf entities is enough to understand the required items within a full span. For example, structured entity such as _Trip_ that fully spanned a source and destination (_London to New York_ or _Home to work_) can be identified with the individual spans predicted for source and destination. Their presence as individual predictions would inform you of the _Trip_ entity.
    - **Ambiguous extractions** occur when the boundaries of different subentities aren't clear. To illustrate, take the example "I want to order a pepperoni pizza and an extra cheese vegetarian pizza." While the different pizza types and the topping modifications can be extracted, extracting them without context would have a degree of ambiguity of where the extra cheese is added. In this case, the extent of the span is context based and would require ML to make a determination. For ambiguous extractions, you can use one of the following approaches:

1. Combine subentities into different entity components within the same entity.

#### Example:

LUIS Implementation:

* Pizza Order (entity)
   * Size (subentity)
   * Quantity (subentity)

CLU Implementation:

* Pizza Order (entity)
   * Size (list entity component: small, medium, large)
   * Quantity (prebuilt entity component: number)

In CLU, you would label the entire span for _Pizza Order_ inclusive of the size and quantity, which would return the pizza order with a list key for size, and a number value for quantity in the same entity object.

2. For more complex problems where entities contain several levels of depth, you can create a project for each level of depth in the entity structure. This process gives you the option to:
- Pass the utterance to each project.
- Combine the analyses of each project in the stage proceeding CLU.

For a detailed example of this concept, check out the pizza sample projects available on GitHub.

### How do I manage versions in CLU?

CLU saves the data assets used to train your model. You can export a model's assets or load them back into the project at any point. So models act as different versions of your project.

You can export your CLU projects using Language Studio or programmatically and store different versions of the assets locally.

### Why is CLU classification different from LUIS? How does None classification work?

CLU presents a different approach to training models by using multi-classification as opposed to binary classification. As a result, the interpretation of scores is different and also differs across training options. While you're likely to achieve better results, you have to observe the difference in scores and determine a new threshold for accepting intent predictions. You can easily add a confidence score threshold for the None intent in your project settings. This returns *None* as the top intent if the top intent didn't exceed the confidence score threshold provided.

### Do I need more data for CLU models than LUIS?

The new CLU models have better semantic understanding of language than in LUIS, and in turn help make models generalize with a significant reduction of data. You shouldn't aim to reduce the amount of data that you have. However, you can expect better performance and greater resilience to variations and synonyms in CLU compared to LUIS.

### If I don't migrate my LUIS apps, are they deleted?

Your current LUIS applications are accessible until March 31, 2025. After this date, you can't use these applications, the service endpoints don't function, and the applications are permanently removed. Starting October 31, 2025, you no longer have access to the LUIS portal online.

### Are .LU files supported on CLU?

CLU only supports JSON format. You can import your .LU files to LUIS and export them in JSON format, or you can follow the previous migration steps for your application.

### What are the service limits of CLU?

For more information, *see* service limits.

### Do I have to refactor my code if I migrate my applications from LUIS to CLU?

The API objects of CLU applications are different from LUIS and therefore code refactoring is necessary.

If you're using the LUIS programmatic and runtime APIs, you can replace them with their equivalent APIs.

CLU authoring APIs: Instead of LUIS's specific CRUD APIs for individual actions such as _add utterance_, _delete entity_, and _rename intent_, CLU offers an import API. This API replaces the full content of a project using the same name. If your service used LUIS programmatic APIs to provide a platform for other customers, you must consider this new design paradigm. All other APIs such as: _listing projects_, _training_, _deploying_, and _deleting_ are available. APIs for actions such as _importing_ and _deploying_ are asynchronous operations instead of synchronous as they were in LUIS.

CLU runtime APIs: The new API request and response includes many of the same parameters such as: _query_, _prediction_, _top intent_, _intents_, _entities_, and their values. The CLU response object offers a more straightforward approach. Entity predictions are provided as they are within the utterance text, and any additional information such as resolution or list keys are provided in extra parameters called `extraInformation` and `resolution`.

You can use the .NET or Python CLU runtime SDK to replace the LUIS runtime SDK. There's currently no authoring SDK available for CLU.

### How are the training times different in CLU? How is standard training different from advanced training?

CLU offers standard training, which trains and learns in English and is comparable to the training time of LUIS. It also offers advanced training, which takes a considerably longer duration as it extends the training to all other supported languages. The train API continues to be an asynchronous process, and you need to assess the change in the DevOps process you employ for your solution.

### How has the experience changed in CLU compared to LUIS? How is the development lifecycle different?

In LUIS you would Build-Train-Test-Publish, whereas in CLU you Build-Train-Evaluate-Deploy-Test.

1. **Build**: In CLU, you can define your intents, entities, and utterances before you train. CLU additionally offers you the ability to specify _test data_ as you build your application to be used for model evaluation. Evaluation assesses how well your model is performing on your test data and provides you with precision, recall, and F1 metrics.
2. **Train**: You create a model with a name each time you train. You can overwrite an already trained model. You can specify either _standard_ or _advanced_ training. Then determine if you would like to use your test data for evaluation, or a percentage of your training data to be left out from training and used as testing data. After training is complete, you can evaluate how well your model is doing on the outside.
3. **Deploy**: After training is complete and you have a model with a name, it can be deployed for predictions. A deployment is also named and has an assigned model. You could have multiple deployments for the same model. A deployment can be overwritten with a different model, or you can swap models with other deployments in the project.
4. **Test**: Once deployment is complete, you can use it for predictions through the deployment endpoint. You can also test it in the studio in the Test deployment page.

This process is in contrast to LUIS, where the application ID was attached to everything, and you deployed a version of the application in either the staging or production slots.

This influences the DevOps processes you use.

### Does CLU have container support?

No, you can't export CLU to containers.

### How are my LUIS applications named in CLU after migration?

Any special characters in the LUIS application name are removed. If the cleared name length is greater than 50 characters, the extra characters are removed. If the name after removing special characters is empty (for example, if the LUIS application name was `@@`), the new name is _untitled_. If there's already a conversational language understanding project with the same name, the migrated LUIS application is appended with `_1` for the first duplicate and increase by one for each subsequent duplicate. If the new name's length is 50 characters and it needs to be renamed, the last one or two characters are removed.

## Migration from LUIS git p

If you have any questions that were unanswered in this article, consider leaving your questions at our Microsoft `Q&A` thread.

## Next steps
* Quickstart: create a CLU project
* CLU language support
* CLU FAQ
