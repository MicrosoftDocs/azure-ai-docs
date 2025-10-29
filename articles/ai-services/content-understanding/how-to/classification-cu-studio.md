# Classify and route your data using Content Understanding Studio

Content Understanding Studio offers the ability to create custom classification workflows that enable you to route your data to the proper custom analyzer. Routing allows you to input multiple different data streams into the same pipeline and ensures your data is always routed to the best analyzer. 

## Prerequisites

To get started, make sure you have the following resources and permissions:
* An Azure subscription. If you don't have an Azure subscription, [create a free account](https://azure.microsoft.com/pricing/purchase-options/azure-account?cid=msft_learn).

## Log in to Content Understanding Studio

Navigate to the [Content Understanding Studio portal]() and sign in using your credentials to get started. You may recognize the classic Azure AI Document Intelligence Studio experience; Content Understanding extends the same content and field extraction that you are familiar with in Document Intelligence across all modalities - document, image, video, and audio. Select the option to try out the new Content Understanding experience to get all of the multimodal capabilities of the service. 

[Insert photo of home page selection]

## Create your custom categories

Custom categories can allow you to route your data to a specific analyzer to get the best output based on the type of data. In this guide, we will show how to classify documents based on their country of origin. Documents for Australia, Canada, India, etc. may have different variations depending on where they originate, so this classification workflow ensures that the documents are analyzed with the correct context. To successfully route your data, you may want to create custom analyzers to route to depending on your scenario. For more information on building custom analyzers, check out [Create and improve your custom analyzer in Content Understanding Studio](./how-to/customization-in-cu-studio.md).

[Insert photo of sample data]

1.	**Start with a new project**: To get started with creating your custom classification workflow, select “Create project” on the home page. 

[Insert photo of home page]

2.	**Select your project type**: In this guide, we will select the option to `Classify and route with custom categories`. To learn more about creating custom analyzers for content and field extraction, check out [Create and improve your custom analyzer in Content Understanding Studio](./how-to/customization-in-cu-studio.md).

[Insert photo of selection screen]

3.	**Upload your data**: To get started with classifying, upload a piece of sample data.

4.	**Create routing rules**: Under the "Routing rule" tab, select `Add category`. Give the category a name and description, and select an analyzer to correspond to that route. For example, if you are analyzing a tax document from Australia, you would want to route to the analyzer that is built to focus on that document type.

[Insert photo of routing rules screen]

5.	**Preview analyzer settings**: Once analyzers are selected, you can preview the schema and configurations to ensure they match the scenario.

[Insert photo of analyzer settings]

6.	**Test your classification workflow**: Once you feel your custom routing rules are ready for testing, select “run analysis” to see the output of the rules on your data. You can optionally upload additional pieces of sample data for testing to see how it performs with multiple different rules.

[Insert photo of testing classification]

7. **Build your classification analyzer**: Once you’re satisfied with the output from your analyzer, select the “Build analyzer” button at the top of the page. Give the analyzer a name and select “Save”.

[Insert photo of building analyzer]

8. **Use your classification analyzer**: Now you have an analyzer endpoint that you can utilize in your own application via the REST API. This has been a walkthrough of how to use Content Understanding Studio to create custom categories.

## Next steps:
* Learn more about [Best practices for Azure AI Content Understanding](../concepts/best-practices.md)  

