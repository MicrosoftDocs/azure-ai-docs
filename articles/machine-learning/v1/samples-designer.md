---
title: Example Pipelines & Datasets for the Designer
titleSuffix: Azure Machine Learning
description: Learn how to use samples in Azure Machine Learning designer to jumpstart your machine learning pipelines.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: sample
ms.reviewer: lgayhardt
author: likebupt
ms.author: keli19
ms.date: 06/05/2025
ms.custom: UpdateFrequency5, designer
---

# Example pipelines & datasets for Azure Machine Learning designer

[!INCLUDE [v1 deprecation](../includes/sdk-v1-deprecation.md)]

You can use the built-in examples in Azure Machine Learning designer to quickly get started building your own machine learning pipelines. The Azure Machine Learning designer [GitHub repository](https://github.com/Azure/MachineLearningDesigner) contains detailed documentation to help you understand some common machine learning scenarios.

## Prerequisites

* An Azure subscription. If you don't have an Azure subscription, create a [free account](https://azure.microsoft.com/free/).
* An Azure Machine Learning workspace.

> [!IMPORTANT]
> If you don't see graphical elements mentioned in this article, such as buttons in studio or designer, you might not have the right level of permissions for the workspace. Contact your Azure subscription administrator to verify that you have been granted the correct level of access. For more information, see [Manage users and roles](../how-to-assign-roles.md).

## Use sample pipelines

The designer saves a copy of the sample pipelines to your studio workspace. You can edit the pipeline to adapt it to your needs and save it as your own. Use them as a starting point to jumpstart your projects.

Here's how to use a designer sample:

1. Sign in to the [Azure Machine Learning studio](https://ml.azure.com), and select the workspace you want to use.

1. Select **Designer** from the sidebar menu.

1. Select **Create a new pipeline using classic prebuilt components** to create a new pipeline.

1. To the left of the pipeline canvas, select the **Component** tab for a complete list of sample pipelines in various categories.

1. To run a pipeline, you first need to set a default compute target to run the pipeline on.

   1. Select **Pipeline interface** to the right of the canvas to open the **Settings** pane. Select **+** next to **Inputs**, then choose **Compute target** from the dropdown list.

   1. In the dialog that appears, select an existing compute target or create a new one. Select **Save**.

   1. Select **Configure & Submit** at the top of the canvas to submit a pipeline job.

   Depending on the sample pipeline and compute settings, jobs might take some time to complete. The default compute settings have a minimum node size of 0, which means that the designer must allocate resources after being idle. Repeated pipeline jobs take less time since the compute resources are already allocated. Additionally, the designer uses cached results for each component to further improve efficiency.

1. After the pipeline finishes running, you can review the pipeline and view the output for each component to learn more. Use the following steps to view component outputs:

   1. Right-click the component in the canvas whose output you'd like to see.

   1. Select **Preview data**.

   Use the samples as starting points for some of the most common machine learning scenarios.

## Regression

Explore these built-in regression samples.

| Sample title | Description | 
| --- | --- |
| [Basic: Use regression to predict car prices with Azure Machine Learning designer](https://github.com/Azure/MachineLearningDesigner/blob/master/articles/samples/regression-automobile-price-prediction-basic.md) | Predict car prices using linear regression. |
| [Advanced: Train & compare multiple regression models to predict car prices with Azure Machine Learning designer](https://github.com/Azure/MachineLearningDesigner/blob/master/articles/samples/regression-automobile-price-prediction-compare-algorithms.md) | Predict car prices using decision forest and boosted decision tree regressors. Compare models to find the best algorithm.

## Classification

Explore these built-in classification samples. Open the samples to learn more and view the component comments in the designer.

| Sample title | Description | 
| --- | --- |
| [Predict income by using binary classification with feature selection](https://github.com/Azure/MachineLearningDesigner/blob/master/articles/samples/binary-classification-feature-selection-income-prediction.md) | Predict income as high or low, using a two-class boosted decision tree. Use Pearson correlation to select features. |
| [Predict credit risk by using binary classification with custom Python script](https://github.com/Azure/MachineLearningDesigner/blob/master/articles/samples/binary-classification-python-credit-prediction.md) | Classify credit applications as high or low risk. Use the Execute Python Script component to weight your data. |
| [Predict customer churn by using boosted decision tree](https://github.com/Azure/MachineLearningDesigner/blob/master/articles/samples/binary-classification-customer-relationship-prediction.md) | Predict customer churn using two-class boosted decision trees. Use SMOTE to sample biased data. |
| [Predict company category by using text classification](https://github.com/Azure/MachineLearningDesigner/blob/master/articles/samples/text-classification-wiki.md) | Classify company types from Wikipedia articles with multiclass logistic regression. |
| Multiclass classification with letter recognition | Create an ensemble of binary classifiers to classify written letters. |

## Computer vision

Explore these built-in computer vision samples. Open the samples to learn more and view the component comments in the designer.

| Sample title | Description | 
| --- | --- |
| Image classification using DenseNet | Use computer vision components to build image classification model based on PyTorch DenseNet.| 

## Recommender

Explore these built-in recommender samples. Open the samples to learn more and view the component comments in the designer.

| Sample title | Description | 
| --- | --- |
| Predict restaurant rating by using wide & deep-based recommendation | Build a restaurant recommender engine from restaurant/user features and ratings.|
| Rate movie rating tweets | Build a movie recommender engine from movie/user features and ratings.|

## Utility

Learn more about the samples that demonstrate machine learning utilities and features. Open the samples to learn more and view the component comments in the designer.

| Sample title | Description | 
| --- | --- |
| Predict adult income by using binary classification with the Vowpal Wabbit Model | Vowpal Wabbit is a machine learning system that pushes the frontier of machine learning with techniques such as online, hashing, allreduce, reductions, learning2search, active, and interactive learning. This sample shows how to use Vowpal Wabbit model to build binary classification model. |
| Predict flight delays by using [custom R script](https://github.com/Azure/MachineLearningDesigner/blob/master/articles/samples/r-script-flight-delay-prediction.md) | Use customized R script to predict if a scheduled passenger flight will be delayed by more than 15 minutes. |
| Predict adult income by using cross validation for binary classification | Use cross validation to build a binary classifier for adult income. |
| Permutation feature importance | Use permutation feature importance to compute importance scores for the test dataset.  |
| Predict adult income by using tune parameters for binary classification | Use Tune Model Hyperparameters to find optimal hyperparameters to build a binary classifier. |

## Datasets

When you create a new pipeline in Azure Machine Learning designer, many sample datasets are included by default. These sample datasets are used by the sample pipelines in the designer homepage. 

To the left of the pipeline canvas, in the **Component** tab, expand the **Sample data** node. You can use any of these datasets in your own pipeline by dragging it to the canvas.

| Dataset name | Dataset description |
|-------------|:--------------------|
| Adult Census Income Binary Classification dataset | A subset of the 1994 Census database, using working adults over the age of 16 with an adjusted income index of > 100.<br/>**Usage**: Classify people using demographics to predict whether a person earns over $50K a year.<br/> **Related research**: Kohavi, R., Becker, B., (1996). [UCI Machine Learning Repository](https://archive.ics.uci.edu/). Irvine, CA: University of California, School of Information and Computer Science. |
|Automobile price data (Raw)|Information about automobiles by make and model, including the price, features such as the number of cylinders and MPG, as well as an insurance risk score.<br/> The risk score is initially associated with auto price. It's then adjusted for actual risk in a process known to actuaries as symboling. A value of +3 indicates that the auto is risky, and a value of -3 that it's probably safe.<br/>**Usage**: Predict the risk score by features, using regression or multivariate classification.<br/>**Related research**: Schlimmer, J.C. (1987). [UCI Machine Learning Repository](https://archive.ics.uci.edu/). Irvine, CA: University of California, School of Information and Computer Science. |
| CRM Appetency Labels Shared |Labels from the KDD Cup 2009 customer relationship prediction challenge ([orange_small_train_appetency.labels](https://kdd.org/cupfiles/KDDCupData/2009/orange_small_train_appetency.labels)).|
|CRM Churn Labels Shared|Labels from the KDD Cup 2009 customer relationship prediction challenge ([orange_small_train_churn.labels](https://www.kdd.org/kdd-cup/view/kdd-cup-2009/Datas)).|
|CRM Dataset Shared | This data comes from the KDD Cup 2009 customer relationship prediction challenge ([orange_small_train.data.zip](https://kdd.org/cupfiles/KDDCupData/2009/orange_small_train.data.zip)). <br/>The dataset contains 50K customers from the French Telecom company Orange. Each customer has 230 anonymized features, 190 of which are numeric and 40 are categorical. The features are very sparse. |
|CRM Upselling Labels Shared|Labels from the KDD Cup 2009 customer relationship prediction challenge ([orange_large_train_upselling.labels](https://kdd.org/cupfiles/KDDCupData/2009/orange_small_train_upselling.labels)).|
|Flight Delays Data|Passenger flight on-time performance data taken from the TranStats data collection of the U.S. Department of Transportation ([On-Time](https://www.transtats.bts.gov/DL_SelectFields.asp?Table_ID=236&DB_Short_Name=On-Time)).<br/>The dataset covers the time period April-October 2013. Before uploading to the designer, the dataset was processed as follows: <br/>- The dataset was filtered to cover only the 70 busiest airports in the continental US <br/>- Canceled flights were labeled as delayed by more than 15 minutes <br/>- Diverted flights were filtered out <br/>- The following columns were selected: Year, Month, DayofMonth, DayOfWeek, Carrier, OriginAirportID, DestAirportID, CRSDepTime, DepDelay, DepDel15, CRSArrTime, ArrDelay, ArrDel15, Canceled|
|German Credit Card UCI dataset|The UCI Statlog (German Credit Card) dataset ([Statlog+German+Credit+Data](https://archive.ics.uci.edu/dataset/144/statlog+german+credit+data)), using the german.data file.<br/>The dataset classifies people, described by a set of attributes, as low or high credit risks. Each example represents a person. There are 20 features, both numerical and categorical, and a binary label (the credit risk value). High credit risk entries have label = 2, low credit risk entries have label = 1. The cost of misclassifying a low-risk example as high is 1, whereas the cost of misclassifying a high-risk example as low is 5.|
|IMDB Movie Titles|The dataset contains information about movies that were rated in X tweets: IMDB movie ID, movie name, genre, and production year. There are 17K movies in the dataset. The dataset was introduced in the paper "S. Dooms, T. De Pessemier and L. Martens. MovieTweetings: a Movie Rating Dataset Collected From Twitter. Workshop on Crowdsourcing and Human Computation for Recommender Systems, CrowdRec at RecSys 2013."|
|Movie Ratings|The dataset is an extended version of the Movie Tweetings dataset. The dataset has 170K ratings for movies, extracted from well-structured tweets on X. Each instance represents a tweet and is a tuple: user ID, IMDB movie ID, rating, timestamp, number of favorites for this tweet, and number of retweets of this tweet. The dataset was made available by A. Said, S. Dooms, B. Loni and D. Tikk for Recommender Systems Challenge 2014.|
|Restaurant Feature Data| A set of metadata about restaurants and their features, such as food type, dining style, and location. <br/>**Usage**: Use this dataset, in combination with the other two restaurant datasets, to train and test a recommender system.<br/> **Related research**: Bache, K. and Lichman, M. (2013). [UCI Machine Learning Repository](https://archive.ics.uci.edu/). Irvine, CA: University of California, School of Information and Computer Science.|
|Restaurant Ratings| Contains ratings given by users to restaurants on a scale from 0 to 2.<br/>**Usage**: Use this dataset, in combination with the other two restaurant datasets, to train and test a recommender system. <br/>**Related research**: Bache, K. and Lichman, M. (2013). [UCI Machine Learning Repository](https://archive.ics.uci.edu/). Irvine, CA: University of California, School of Information and Computer Science.|
|Restaurant Customer Data| A set of metadata about customers, including demographics and preferences. <br/>**Usage**: Use this dataset, in combination with the other two restaurant datasets, to train and test a recommender system. <br/> **Related research**: Bache, K. and Lichman, M. (2013). [UCI Machine Learning Repository](https://archive.ics.uci.edu/) Irvine, CA: University of California, School of Information and Computer Science.|
|Weather Dataset|Hourly land-based weather observations from NOAA (merged data from 201304 to 201310).<br/>The weather data covers observations made from airport weather stations, covering the time period April-October 2013. Before uploading to the designer, the dataset was processed as follows: <br/> - Weather station IDs were mapped to corresponding airport IDs  <br/> - Weather stations not associated with the 70 busiest airports were filtered out    <br/> - The Date column was split into separate Year, Month, and Day columns  <br/> - The following columns were selected: AirportID, Year, Month, Day, Time, TimeZone, SkyCondition, Visibility, WeatherType, DryBulbFarenheit, DryBulbCelsius, WetBulbFarenheit, WetBulbCelsius, DewPointFarenheit, DewPointCelsius, RelativeHumidity, WindSpeed, WindDirection, ValueForWindCharacter, StationPressure, PressureTendency, PressureChange, SeaLevelPressure, RecordType, HourlyPrecip, Altimeter|
|Wikipedia SP 500 Dataset|Data is derived from [Wikipedia](https://www.wikipedia.org) based on articles of each S&P 500 company, stored as XML data.  <br/>Before uploading to the designer, the dataset was processed as follows:    <br/> - Extract text content for each specific company    <br/> - Remove wiki formatting    <br/> - Remove nonalphanumeric characters    <br/> - Convert all text to lowercase    <br/> - Known company categories were added    <br/>Note that for some companies an article couldn't be found, so the number of records is less than 500.|

## Clean up resources

[!INCLUDE [aml-ui-cleanup](../includes/aml-ui-cleanup.md)]

## Related content

Learn the fundamentals of predictive analytics and machine learning with [Tutorial: Designer - train a no-code regression model](tutorial-designer-automobile-price-train-score.md)

