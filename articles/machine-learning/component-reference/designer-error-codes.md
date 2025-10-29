---
title: Troubleshoot designer component errors
titleSuffix: "Azure Machine Learning"
description: Learn how you can read and troubleshoot automated component error codes in Azure Machine Learning designer.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: reference
author: likebupt
ms.author: keli19
ms.date: 03/25/2021
ms.custom:
  - troubleshooting
  - sfi-image-nochange
---
# Exceptions and error codes for the designer

This article describes the error messages and exception codes in Azure Machine Learning designer to help you troubleshoot your machine learning pipelines.

You can find the error message in the designer following these steps:  

- Select the failed component, go to the **Outputs+logs** tab, you can find the detailed log in the **70_driver_log.txt** file under the **azureml-logs** category.

- For detailed component error, you can check it in the error_info.json under **module_statistics** category.

Following are error codes of components in the designer.

## Error 0001  
 Exception occurs if one or more specified columns of data set couldn't be found.  

 You'll receive this error if a column selection is made for a component, but the selected column(s) don't exist in the input data set. This error may occur if you have manually typed in a column name or if the column selector has provided a suggested column that didn't exist in your dataset when you ran the pipeline.  

**Resolution:**
 Revisit the component throwing this exception and validate that the column name or names are correct and that all referenced columns do exist.  

|Exception Messages|
|------------------------|
|One or more specified columns were not found.|
|Column with name or index "{column_id}" not found.|
|Column with name or index "{column_id}" does not exist in "{arg_name_missing_column}".|
|Column with name or index "{column_id}" does not exist in "{arg_name_missing_column}", but exists in "{arg_name_has_column}".|
|Columns with name or index "{column_names}" not found.|
|Columns with name or index "{column_names}" does not exist in "{arg_name_missing_column}".|
|Columns with name or index "{column_names}" does not exist in "{arg_name_missing_column}", but exists in "{arg_name_has_column}".|


## Error 0002  
 Exception occurs if one or more parameters couldn't be parsed or converted from specified type into required by target method type.  

 This error occurs in Azure Machine Learning when you specify a parameter as input and the value type is different from the type that is expected, and implicit conversion can't be performed.  

**Resolution:**
 Check the component requirements and determine which value type is required (string, integer, double, etc.)  

|Exception Messages|
|------------------------|
|Failed to parse parameter.|
|Failed to parse "{arg_name_or_column}" parameter.|
|Failed to convert "{arg_name_or_column}" parameter to "{to_type}".|
|Failed to convert "{arg_name_or_column}" parameter from "{from_type}" to "{to_type}".|
|Failed to convert "{arg_name_or_column}" parameter value "{arg_value}" from "{from_type}" to "{to_type}".|
|Failed to convert value "{arg_value}" in column "{arg_name_or_column}" from "{from_type}" to "{to_type}" with usage of the format "{fmt}" provided.|


## Error 0003  
 Exception occurs if one or more of inputs are null or empty.  

 You'll receive this error in Azure Machine Learning if any inputs or parameters to a component are null or empty.  This error might occur, for example, when you didn't type in any value for a parameter. It can also happen if you chose a dataset that has missing values, or an empty dataset.  

**Resolution:**

+ Open the component that produced the exception and verify that all inputs have been specified. Ensure that all required inputs are specified. 
+ Make sure that data that is loaded from Azure storage is accessible, and that the account name or key hasn't changed.  
+ Check the input data for missing values, or nulls.
+ If using a query on a data source, verify that data is being returned in the format you expect. 
+ Check for typos or other changes in the specification of data.
  
|Exception Messages|
|------------------------|
|One or more of inputs are null or empty.|
|Input "{name}" is null or empty.|


## Error 0004  
 Exception occurs if parameter is less than or equal to specific value.  

 You'll receive this error in Azure Machine Learning if the parameter in the message is below a boundary value required for the component to process the data.  

**Resolution:**
 Revisit the component throwing the exception and modify the parameter to be greater than the specified value.  

|Exception Messages|
|------------------------|
|Parameter should be greater than boundary value.|
|Parameter "{arg_name}" value should be greater than {lower_boundary}.|
|Parameter "{arg_name}" has value "{actual_value}" which should be greater than {lower_boundary}.|


## Error 0005  
 Exception occurs if parameter is less than a specific value.  

 You'll receive this error in Azure Machine Learning if the parameter in the message is below or equal to a boundary value required for the component to process the data.  

**Resolution:**
 Revisit the component throwing the exception and modify the parameter to be greater than or equal to the specified value.  

|Exception Messages|
|------------------------|
|Parameter should be greater than or equal to boundary value.|
|Parameter "{arg_name}" value should be greater than or equal to {lower_boundary}.|
|Parameter "{arg_name}" has value "{value}" which should be greater than or equal to {lower_boundary}.|


## Error 0006  
 Exception occurs if parameter is greater than or equal to the specified value.  

 You'll receive this error in Azure Machine Learning if the parameter in the message is greater than or equal to a boundary value required for the component to process the data.  

**Resolution:**
 Revisit the component throwing the exception and modify the parameter to be less than the specified value.  

|Exception Messages|
|------------------------|
|Parameters mismatch. One of the parameters should be less than another.|
|Parameter "{arg_name}" value should be less than parameter "{upper_boundary_parameter_name}" value.|
|Parameter "{arg_name}" has value "{value}" which should be less than {upper_boundary_parameter_name}.|


## Error 0007  
 Exception occurs if parameter is greater than a specific value.  

 You'll receive this error in Azure Machine Learning if, in the properties for the component, you specified a value that is greater than is allowed. For example, you might specify a data that is outside the range of supported dates, or you might indicate that five columns be used when only three columns are available. 

 You might also see this error if you're specifying two sets of data that need to match in some way. For example, if you're renaming columns, and specify the columns by index, the number of names you supply must match the number of column indices. Another example might be a math operation that uses two columns, where the columns must have the same number of rows. 

**Resolution:**

 + Open the component in question and review any numeric property settings.
 + Ensure that any parameter values fall within the supported range of values for that property.
 + If the component takes multiple inputs, ensure that inputs are of the same size.
<!-- + If the component has multiple properties that can be set, ensure that related properties have appropriate values. For example, when using [Group Data into Bins](group-data-into-bins.md), if you use the option to specify custom bin edges, the number of bins must match the number of values you provide as bin boundaries.-->
 + Check whether the dataset or data source has changed. Sometimes a value that worked with a previous version of the data will fail after the number of columns, the column data types, or the size of the data has changed.  

|Exception messages|
|------------------------|
|Parameters mismatch. One of the parameters should be less than or equal to another.|
|Parameter "{arg_name}" value should be less than or equal to parameter "{upper_boundary_parameter_name}" value.|
|Parameter "{arg_name}" has value "{actual_value}" which should be less than or equal to {upper_boundary}.|
|Parameter "{arg_name}" value {actual_value} should be less than or equal to parameter "{upper_boundary_parameter_name}" value {upper_boundary}.|
|Parameter "{arg_name}" value {actual_value} should be less than or equal to {upper_boundary_meaning} value {upper_boundary}.|


## Error 0008  
 Exception occurs if parameter isn't in range.  

 You'll receive this error in Azure Machine Learning if the parameter in the message is outside the bounds required for the component to process the data.  

 For example, this error is displayed if you try to use [Add Rows](add-rows.md) to combine two datasets that have a different number of columns.  

**Resolution:**
 Revisit the component throwing the exception and modify the parameter to be within the specified range.  

|Exception Messages|
|------------------------|
|Parameter value is not in the specified range.|
|Parameter "{arg_name}" value is not in range.|
|Parameter "{arg_name}" value should be in the range of [{lower_boundary}, {upper_boundary}].|
|Parameter "{arg_name}" value is not in range. {reason}|


## Error 0009  
 Exception occurs when the Azure storage account name or container name is specified incorrectly.  

This error occurs in Azure Machine Learning designer when you specify parameters for an Azure storage account, but the name or password can't be resolved. Errors on passwords or account names can happen for many reasons:

 + The account is the wrong type. Some new account types aren't supported for use with Machine Learning designer. See [Import Data](import-data.md) for details.
 + You entered the incorrect account name
 + The account no longer exists
 + The password for the storage account is wrong or has changed
 + You didn't specify the container name, or the container doesn't exist
 + You didn't fully specify the file path (path to the blob)
   

**Resolution:**

Such problems often occur when you try to manually enter the account name, password, or container path. We recommend that you use the new wizard for the [Import Data](import-data.md) component, which helps you look up and check names.

Also check whether the account, container, or blob has been deleted. Use another Azure storage utility to verify that the account name and password have been entered correctly, and that the container exists. 

Some newer account types aren't supported by Azure Machine Learning. For example, the new "hot" or "cold" storage types can't be used for machine learning. Both classic storage accounts and storage accounts created as "General purpose" work fine.

If the complete path to a blob was specified, verify that the path is specified as **container/blobname**, and that both the container and the blob exist in the account.  

 The path shouldn't contain a leading slash. For example **/container/blob** is incorrect and should be entered as **container/blob**.  


|Exception Messages|
|------------------------|
|The Azure storage account name or container name is incorrect.|
|The Azure storage account name "{account_name}" or container name "{container_name}" is incorrect; a container name of the format container/blob was expected.|


## Error 0010  
 Exception occurs if input datasets have column names that should match but do not.  

 You'll receive this error in Azure Machine Learning if the column index in the message has different column names in the two input datasets.  

**Resolution:**
 Use [Edit Metadata](edit-metadata.md) or modify the original dataset to have the same column name for the specified column index.  

|Exception Messages|
|------------------------|
|Columns with corresponding index in input datasets have different names.|
|Column names are not the same for column {col_index} (zero-based) of input datasets ({dataset1} and {dataset2} respectively).|


## Error 0011  
 Exception occurs if passed column set argument doesn't apply to any of dataset columns.  

 You'll receive this error in Azure Machine Learning if the specified column selection doesn't match any of the columns in the given dataset.  

 You can also get this error if you haven't selected a column and at least one column is required for the component to work.  

**Resolution:**
 Modify the column selection in the component so that it applies to the columns in the dataset.  

 If the component requires that you select a specific column, such as a label column, verify that the right column is selected.  

 If inappropriate columns are selected, remove them and rerun the pipeline.  

|Exception Messages|
|------------------------|
|Specified column set does not apply to any of dataset columns.|
|Specified column set "{column_set}" does not apply to any of dataset columns.|


## Error 0012  
 Exception occurs if instance of class couldn't be created with passed set of arguments.  

**Resolution:**
 This error isn't actionable by the user and will be deprecated in a future release.  

|Exception Messages|
|------------------------|
|Untrained model, please train model first.|
|Untrained model ({arg_name}), use trained model.|


## Error 0013  
 Exception occurs if the learner passed to the component is an invalid type.  

 This error occurs whenever a trained model is incompatible with the connected scoring component. <!--For example, connecting the output of [Train Matchbox Recommender](train-matchbox-recommender.md) to [Score Model](score-model.md) (instead of [Score Matchbox Recommender](score-matchbox-recommender.md)) will generate this error when the pipeline is run.  -->

**Resolution:**

Determine the type of learner that is produced by the training component, and determine the scoring component that is appropriate for the learner. 

If the model was trained using any of the specialized training components, connect the trained model only to the corresponding specialized scoring component. 


|Model type|Training component| Scoring component|
|----|----|----|
|any classifier|[Train Model](train-model.md) |[Score Model](score-model.md)|
|any regression model|[Train Model](train-model.md) |[Score Model](score-model.md)|

<!--| clustering models| [Train Clustering Model](train-clustering-model.md) or [Sweep Clustering](sweep-clustering.md)| [Assign Data to Clusters](assign-data-to-clusters.md)|
| anomaly detection - One-Class SVM | [Train Anomaly Detection Model](train-anomaly-detection-model.md) |[Score Model](score-model.md)|
| anomaly detection - PCA |[Train Model](train-model.md) |[Score Model](score-model.md) </br> Some additional steps are required to evaluate the model. |
| anomaly detection - time series|  [Time Series Anomaly Detection](time-series-anomaly-detection.md) |Model trains from data and generates scores. The component does not create a trained learner and no additional scoring is required. |
| recommendation model| [Train Matchbox Recommender](train-matchbox-recommender.md) | [Score Matchbox Recommender](score-matchbox-recommender.md) |
| image classification | [Pretrained Cascade Image Classification](pretrained-cascade-image-classification.md) | [Score Model](score-model.md) |
|Vowpal Wabbit models| [Train Vowpal Wabbit Version 7-4 Model](train-vowpal-wabbit-version-7-4-model.md) | [Score Vowpal Wabbit Version 7-4 Model](score-vowpal-wabbit-version-7-4-model.md) |   
|Vowpal Wabbit models| [Train Vowpal Wabbit Version 7-10 Model](train-vowpal-wabbit-version-7-10-model.md) | [Score Vowpal Wabbit Version 7-10 Model](score-vowpal-wabbit-version-7-10-model.md) |
|Vowpal Wabbit models| [Train Vowpal Wabbit Version 8 Model](score-vowpal-wabbit-version-8-model.md) | [Score Vowpal Wabbit Version 8 Model](score-vowpal-wabbit-version-8-model.md) |-->

|Exception Messages|
|------------------------|
|Learner of invalid type is passed.|
|Learner "{arg_name}" has invalid type.|
|Learner "{arg_name}" has invalid type "{learner_type}".|
|Learner of invalid type is passed. Exception message: {exception_message}|


## Error 0014  
 Exception occurs if the count of column unique values is greater than allowed.  

 This error occurs when a column contains too many unique values, like an ID column or text column. You might see this error if you specify that a column be handled as categorical data, but there are too many unique values in the column to allow processing to complete. You might also see this error if there's a mismatch between the number of unique values in two inputs.   

The error of unique values is greater than allowed will occur if meeting **both** following conditions:

- More than 97% instances of one column are unique values, which means nearly all categories are different from each other.
- One column has more than 1,000 unique values.

**Resolution:**

Open the component that generated the error, and identify the columns used as inputs. For some components, you can right-click the dataset input and select **Visualize** to get statistics on individual columns, including the number of unique values and their distribution.

For columns that you intend to use for grouping or categorization, take steps to reduce the number of unique values in columns. You can reduce in different ways, depending on the data type of the column. 

For ID columns which isn't meaningful features during training a model, you can use [Edit Metadata](../algorithm-module-reference/edit-metadata.md) to mark that column as **Clear feature** and it will not be used during training a model. 

For text columns, you can use [Feature Hashing](../algorithm-module-reference/feature-hashing.md) or [Extract N-Gram Features from Text component](../algorithm-module-reference/extract-n-gram-features-from-text.md) to preprocess text columns.
<!--
+ For text data, you might be able to use [Preprocess Text](preprocess-text.md) to collapse similar entries. 
+ For numeric data, you can create a smaller number of bins using [Group Data into Bins](group-data-into-bins.md), remove or truncate values using [Clip Values](clip-values.md), or use machine learning methods such as [Principal Component Analysis](principal-component-analysis.md) or [Learning with Counts](data-transformation-learning-with-counts.md) to reduce the dimensionality of the data.  
-->
> [!TIP]
> Unable to find a resolution that matches your scenario? You can provide feedback on this topic that includes the name of the component that generated the error, and the data type and cardinality of the column. We will use the information to provide more targeted troubleshooting steps for common scenarios.   

|Exception Messages|
|------------------------|
|Amount of column unique values is greater than allowed.|
|Number of unique values in column: "{column_name}" is greater than allowed.|
|Number of unique values in column: "{column_name}" exceeds tuple count of {limitation}.|


## Error 0015  
 Exception occurs if database connection has failed.  

 You'll receive this error if you enter an incorrect SQL account name, password, database server, or database name, or if a connection with the database can't be established due to problems with the database or server.  

**Resolution:**
 Verify that the account name, password, database server, and database have been entered correctly, and that the specified account has the correct level of permissions. Verify that the database is currently accessible.  

|Exception Messages|
|------------------------|
|Error making database connection.|
|Error making database connection: {connection_str}.|


## Error 0016  
 Exception occurs if input datasets passed to the component should have compatible column types but don't.  

 You'll receive this error in Azure Machine Learning if the types of the columns passed in two or more datasets aren't compatible with each other.  

**Resolution:**
 Use [Edit Metadata](edit-metadata.md) or modify the original input dataset<!--, or use [Convert to Dataset](convert-to-dataset.md)--> to ensure that the types of the columns are compatible.  

|Exception Messages|
|------------------------|
|Columns with corresponding index in input datasets do have incompatible types.|
|Columns '{first_col_names}' are incompatible between train and test data.|
|Columns '{first_col_names}' and '{second_col_names}' are incompatible.|
|Column element types aren't compatible for column '{first_col_names}' (zero-based) of input datasets ({first_dataset_names} and {second_dataset_names} respectively).|


## Error 0017  
 Exception occurs if a selected column uses a data type that isn't supported by the current component.  

 For example, you might receive this error in Azure Machine Learning if your column selection includes a column with a data type that can't be processed by the component, such as a string column for a math operation, or a score column where a categorical feature column is required.  

**Resolution:**
 1. Identify the column that is the problem.
 2. Review the requirements of the component.
 3. Modify the column to make it conform to requirements. You might need to use several of the following components to make changes, depending on the column and the conversion you're attempting:
    + Use [Edit Metadata](edit-metadata.md) to change the data type of columns, or to change the column usage from feature to numeric, categorical to noncategorical, and so forth.
<!--    + Use [Convert to Dataset](convert-to-dataset.md) to ensure that all included columns use data types that are supported by Azure Machine Learning.  If you cannot convert the columns, consider removing them from the input dataset.
    + Use the [Apply SQL Transformation](apply-sql-transformation.md) or [Execute R Script](execute-r-script.md) components to cast or convert any columns that cannot be modified using [Edit Metadata](edit-metadata.md). These components provide more flexibility for working with datetime data types.
    + For numeric data types, you can use the [Apply Math Operation](apply-math-operation.md) component to round or truncate values, or use the [Clip Values](clip-values.md) component to remove out of range values.  -->
 4. As a last resort, you might need to modify the original input dataset.

> [!TIP]
> Unable to find a resolution that matches your scenario? You can provide feedback on this topic that includes the name of the component that generated the error, and the data type and cardinality of the column. We will use the information to provide more targeted troubleshooting steps for common scenarios. 

|Exception Messages|
|------------------------|
|Cannot process column of current type. The type is not supported by the component.|
|Cannot process column of type {col_type}. The type is not supported by the component.|
|Cannot process column "{col_name}" of type {col_type}. The type is not supported by the component.|
|Cannot process column "{col_name}" of type {col_type}. The type is not supported by the component. Parameter name: {arg_name}.|


## Error 0018  
 Exception occurs if input dataset isn't valid.  

**Resolution:**
 This error in Azure Machine Learning can appear in many contexts, so there isn't a single resolution. In general, the error indicates that the data provided as input to a component has the wrong number of columns, or that the data type doesn't match requirements of the component. For example:  

-   The component requires a label column, but no column is marked as a label, or you haven't selected a label column yet.  
  
-   The component requires that data be categorical but your data is numeric.  

<!---   The component requires a specific data type. For example, ratings provided to [Train Matchbox Recommender](train-matchbox-recommender.md) can be either numeric or categorical, but cannot be floating point numbers.  -->

-   The data is in the wrong format.  
  
-   Imported data contains invalid characters, bad values, or out of range values.  
-   The column is empty or contains too many missing values.  

 To determine the requirements and how your data might, review the help article for the component that will be consuming the dataset as input.  

 <!--We also recommend that you use [Summarize Data](summarize-data.md) or [Compute Elementary Statistics](compute-elementary-statistics.md) to profile your data, and use these components to fix metadata and clean values: [Edit Metadata](edit-metadata.md) and [Clean Missing Data](clean-missing-data.md), [Clip Values](clip-values.md)-->.  

|Exception Messages|
|------------------------|
|Dataset is not valid.|
|{dataset1} contains invalid data.|
|{dataset1} and {dataset2} should be consistent columnwise.|
|{dataset1} contains invalid data, {reason}.|
|{dataset1} contains {invalid_data_category}. {troubleshoot_hint}|
|{dataset1} is not valid, {reason}. {troubleshoot_hint}|


## Error 0019  
 Exception occurs if column is expected to contain sorted values, but it doesn't.  

 You'll receive this error in Azure Machine Learning if the specified column values are out of order.  

**Resolution:**
 Sort the column values by manually modifying the input dataset and rerun the component.  

|Exception Messages|
|------------------------|
|Values in column are not sorted.|
|Values in column "{col_index}" are not sorted.|
|Values in column "{col_index}" of dataset "{dataset}" are not sorted.|
|Values in argument "{arg_name}" are not sorted in "{sorting_order}" order.|


## Error 0020  
 Exception occurs if number of columns in some of the datasets passed to the component is too small.  

 You'll receive this error in Azure Machine Learning if not enough columns have been selected for a component.  

**Resolution:**
 Revisit the component and ensure that column selector has correct number of columns selected.  

|Exception Messages|
|------------------------|
|Number of columns in input dataset is less than allowed minimum.|
|Number of columns in input dataset "{arg_name}" is less than allowed minimum.|
|Number of columns in input dataset is less than allowed minimum of {required_columns_count} column(s).|
|Number of columns in input dataset "{arg_name}" is less than allowed minimum of {required_columns_count} column(s).|


## Error 0021  
 Exception occurs if number of rows in some of the datasets passed to the component is too small.  

 This error in seen in Azure Machine Learning when there aren't enough rows in the dataset to perform the specified operation. For example, you might see this error if the input dataset is empty, or if you're trying to perform an operation that requires some minimum number of rows to be valid. Such operations can include (but aren't limited to) grouping or classification based on statistical methods, certain types of binning, and learning with counts.  

**Resolution:**

 + Open the component that returned the error, and check the input dataset and component properties. 
 + Verify that the input dataset isn't empty and that there are enough rows of data to meet the requirements described in component help.  
 + If your data is loaded from an external source, make sure that the data source is available and that there's no error or change in the data definition that would cause the import process to get fewer rows.
 + If you're performing an operation on the data upstream of the component that might affect the type of data or the number of values, such as cleaning, splitting, or join operations, check the outputs of those operations to determine the number of rows returned.  

|Exception Messages|
|------------------------|
|Number of rows in input dataset is less than allowed minimum.|
|Number of rows in input dataset is less than allowed minimum of {required_rows_count} row(s).|
|Number of rows in input dataset is less than allowed minimum of {required_rows_count} row(s). {reason}|
|Number of rows in input dataset "{arg_name}" is less than allowed minimum of {required_rows_count} row(s).|
|Number of rows in input dataset "{arg_name}" is {actual_rows_count}, less than allowed minimum of {required_rows_count} row(s).|
|Number of "{row_type}" rows in input dataset "{arg_name}" is {actual_rows_count}, less than allowed minimum of {required_rows_count} row(s).|


## Error 0022  
 Exception occurs if number of selected columns in input dataset doesn't equal to the expected number.  

 This error in Azure Machine Learning can occur when the downstream component or operation requires a specific number of columns or inputs, and you have provided too few or too many columns or inputs. For example:  

-   You specify a single label column or key column and accidentally selected multiple columns.  
  
-   You're renaming columns, but provided more or fewer names than there are columns.  
  
-   The number of columns in the source or destination has changed or doesn't match the number of columns used by the component.  
  
-   You have provided a comma-separated list of values for inputs, but the number of values doesn't match, or multiple inputs aren't supported.  

**Resolution:**
 Revisit the component and check the column selection to ensure that the correct number of columns is selected. Verify the outputs of upstream components, and the requirements of downstream operations.  

 If you used one of the column selection options that can select multiple columns (column indices, all features, all numeric, etc.), validate the exact number of columns returned by the selection.  

 <!--If you are trying to specify a comma-separated list of datasets as inputs to [Unpack Zipped Datasets](unpack-zipped-datasets.md), unpack only one dataset at a time. Multiple inputs are not supported.  -->

 Verify that the number or type of upstream columns hasn't changed.  

 If you're using a recommendation dataset to train a model, remember that the recommender expects a limited number of columns, corresponding to user-item pairs or user-item-rankings. Remove additional columns before training the model or splitting recommendation datasets. For more information, see [Split Data](split-data.md).  

|Exception Messages|
|------------------------|
|Number of selected columns in input dataset does not equal to the expected number.|
|Number of selected columns in input dataset does not equal to {expected_col_count}.|
|Column selection pattern "{selection_pattern_friendly_name}" provides number of selected columns in input dataset not equal to {expected_col_count}.|
|Column selection pattern "{selection_pattern_friendly_name}" is expected to provide {expected_col_count} column(s) selected in input dataset, but {selected_col_count} column(s) is/are actually provided.|


## Error 0023  

Exception occurs if target column of input dataset isn't valid for the current trainer component.  

This error in Azure Machine Learning  occurs if the target column (as selected in the component parameters) isn't of the valid data-type, contained all missing values, or wasn't categorical as expected.  

**Resolution:**
Revisit the component input to inspect the content of the label/target column. Make sure it doesn't have all missing values. If the component is expecting target column to be categorical, make sure that there are more than one distinct values in the target column.  

|Exception Messages|
|------------------------|
|Input dataset has unsupported target column.|
|Input dataset has unsupported target column "{column_index}".|
|Input dataset has unsupported target column "{column_index}" for learner of type {learner_type}.|


## Error 0024  
Exception occurs if dataset doesn't contain a label column.  

 This error in Azure Machine Learning occurs when the component requires a label column and the dataset doesn't have a label column. For example, evaluation of a scored dataset usually requires that a label column is present to compute accuracy metrics.  

It can also happen that a label column is present in the dataset, but not detected correctly by Azure Machine Learning.

**Resolution:**

+ Open the component that generated the error, and determine if a label column is present. The name or data type of the column doesn't matter, as long as the column contains a single outcome (or dependent variable) that you're trying to predict. If you aren't sure which column has the label, look for a generic name such as  *Class* or *Target*. 
+  If the dataset doesn't include a label column, it's possible that the label column was explicitly or accidentally removed upstream. It could also be that the dataset isn't the output of an upstream scoring component.
+ To explicitly mark the column as the label column, add the [Edit Metadata](edit-metadata.md) component and connect the dataset. Select only the label column, and select **Label** from the **Fields** dropdown list. 
+ If the wrong column is chosen as the label, you can select **Clear label** from the **Fields** to fix the metadata on the column. 
  
|Exception Messages|
|------------------------|
|There is no label column in dataset.|
|There is no label column in "{dataset_name}".|


## Error 0025  
 Exception occurs if dataset doesn't contain a score column.  

 This error in Azure Machine Learning occurs if the input to the evaluated model doesn't contain valid score columns. For example, the user attempts to evaluate a dataset before it was scored with a correct trained model, or the score column was explicitly dropped upstream. This exception also occurs if the score columns on the two datasets are incompatible. For example, you might be trying to compare the accuracy of a linear regressor with a binary classifier.  

**Resolution:**
 Revisit the input to the evaluated model and examine if it contains one or more score columns. If not, the dataset wasn't scored or the score columns were dropped in an upstream component.  

|Exception Messages|
|------------------------|
|There is no score column in dataset.|
|There is no score column in "{dataset_name}".|
|There is no score column in "{dataset_name}" that is produced by a "{learner_type}". Score the dataset using the correct type of learner.|


## Error 0026  
 Exception occurs if columns with the same name aren't allowed.  

 This error in Azure Machine Learning occurs if multiple columns have the same name. One way you may receive this error is if the dataset doesn't have a header row and column names are automatically assigned: Col0, Col1, etc.  

**Resolution:**
 If columns have same name, insert a [Edit Metadata](edit-metadata.md) component between the input dataset and the component. Use the column selector in [Edit Metadata](edit-metadata.md) to select columns to rename, typing the new names into the **New column names** textbox.  

|Exception Messages|
|------------------------|
|Equal column names are specified in arguments. Equal column names are not allowed by component.|
|Equal column names in arguments "{arg_name_1}" and "{arg_name_2}" are not allowed. Please specify different names.|


## Error 0027  
 Exception occurs in case when two objects have to be of the same size but aren't.  

 This is a common error in Azure Machine Learning and can be caused by many conditions.  

**Resolution:**
 There's no specific resolution. However, you can check for conditions such as  the following:  

-   If you're renaming columns, make sure that each list (the input columns and the list of new names) has the same number of items.  
  
-   If you're joining or concatenating two datasets, make sure they have the same schema.  
  
-   If you're joining two datasets that have multiple columns, make sure that the key columns have the same data type, and select the option **Allow duplicates and preserve column order in selection**.  

|Exception Messages|
|------------------------|
|The size of passed objects is inconsistent.|
|The size of "{friendly_name1}" is inconsistent with size of "{friendly_name2}".|


## Error 0028  
 Exception occurs in the case when column set contains duplicated column names and it isn't allowed.  

 This error in Azure Machine Learning occurs when column names are duplicated; that is, not unique.  

**Resolution:**
 If any columns have same name, add an instance of [Edit Metadata](edit-metadata.md) between the input dataset and the component raising the error. Use the Column Selector in [Edit Metadata](edit-metadata.md) to select columns to rename, and type the new columns names into the **New column names** textbox. If you're renaming multiple columns, ensure that the values you type in the **New column names** are unique.  

|Exception Messages|
|------------------------|
|Column set contains duplicated column name(s).|
|The name "{duplicated_name}" is duplicated.|
|The name "{duplicated_name}" is duplicated in "{arg_name}".|
|The name "{duplicated_name}" is duplicated. Details: {details}|


## Error 0029  
 Exception occurs in case when invalid URI is passed.  

 This error in Azure Machine Learning occurs in case when invalid URI is passed.  You'll receive this error if any of the following conditions are true:  

-   The Public or SAS URI provided for Azure Blob Storage for read or write contains an error.  
  
-   The time window for the SAS has expired.  
  
-   The Web URL via HTTP source represents a file or a loopback URI.  
  
-   The Web URL via HTTP contains an incorrectly formatted URL.  
  
-   The URL can't be resolved by the remote source.  

**Resolution:**
 Revisit the component and verify the format of the URI. If the data source is a Web URL via HTTP, verify that the intended source isn't a file or a loopback URI (localhost).  

|Exception Messages|
|------------------------|
|Invalid Uri is passed.|
|The Uri "{invalid_url}" is invalid.|


## Error 0030  
 Exception occurs in the case when it isn't possible to download a file.  

 This exception in Azure Machine Learning occurs when it isn't possible to download a file. You'll receive this exception when an attempted read from an HTTP source has failed after three (3) retry attempts.  

**Resolution:**
 Verify that the URI to the HTTP source is correct and that the site is currently accessible via the Internet.  

|Exception Messages|
|------------------------|
|Unable to download a file.|
|Error while downloading the file: {file_url}.|


## Error 0031  
 Exception occurs if number of columns in column set is less than needed.  

 This error in Azure Machine Learning occurs if the number of columns selected is less than needed.  You'll receive this error if the minimum required number of columns aren't selected.  

**Resolution:**
 Add additional columns to the column selection by using the **Column Selector**.  

|Exception Messages|
|------------------------|
|Number of columns in column set is less than required.|
|At least {required_columns_count} column(s) should be specified for input argument "{arg_name}".|
|At least {required_columns_count} column(s) should be specified for input argument "{arg_name}". The actual number of specified columns is {input_columns_count}.|


## Error 0032  
 Exception occurs if argument isn't a number.  

 You'll receive this error  in Azure Machine Learning if the argument is a double or NaN.  

**Resolution:**
 Modify the specified argument to use a valid value.  

|Exception Messages|
|------------------------|
|Argument is not a number.|
|"{arg_name}" is not a number.|


## Error 0033  
 Exception occurs if argument is Infinity.  

 This error in Azure Machine Learning occurs if the argument is infinite. You'll receive this error if the argument is either `double.NegativeInfinity` or `double.PositiveInfinity`.  

**Resolution:**
 Modify the specified argument to be a valid value.  

|Exception Messages|
|------------------------|
|Argument must be finite.|
|"{arg_name}" is not finite.|
|Column "{column_name}" contains infinite values.|


## Error 0034  
 Exception occurs if more than one rating exists for a given user-item pair.  

 This error in Azure Machine Learning occurs in recommendation if a user-item pair has more than one rating value.  

**Resolution:**
 Ensure that the user-item pair possesses one rating value only.  

|Exception Messages|
|------------------------|
|More than one rating exists for the value(s) in dataset.|
|More than one rating for user {user} and item {item} in rating prediction data table.|
|More than one rating for user {user} and item {item} in {dataset}.|


## Error 0035  
 Exception occurs if no features were provided for a given user or item.  

 This error in Azure Machine Learning occurs you're trying to use a recommendation model for scoring but a feature vector can't be found.  

**Resolution:**

The Matchbox recommender has certain requirements that must be met when using either item features or user features.  This error indicates that a feature vector is missing for a user or item that you provided as input. Ensure that a vector of features is available in the data for each user or item.  

 For example, if you trained a recommendation model using features such as the user's age, location, or income, but now want to create scores for new users who weren't seen during training, you must provide some equivalent set of features (namely, age, location, and income values) for the new users in order to make appropriate predictions for them. 

 If you don't have any features for these users, consider feature engineering to generate appropriate features.  For example, if you don't have individual user age or income values, you might generate approximate values to use for a group of users. 

<!--When you are scoring from a recommendation mode, you can use item or user features only if you previously used item or user features during training. For more information, see [Score Matchbox Recommender](score-matchbox-recommender.md).

For general information about how the Matchbox recommendation algorithm works, and how to prepare a dataset of item features or user features, see [Train Matchbox Recommender](train-matchbox-recommender.md).  -->

 > [!TIP]
 > Resolution not applicable to your case? You are welcome to send feedback on this article and provide information about the scenario, including the component and the number of rows in the column. We will use this information to provide more detailed troubleshooting steps in the future.

|Exception Messages|
|------------------------|
|No features were provided for a required user or item.|
|Features for {required_feature_name} required but not provided.|


## Error 0036  
 Exception occurs if multiple feature vectors were provided for a given user or item.  

 This error in Azure Machine Learning occurs if a feature vector is defined more than once.  

**Resolution:**
 Ensure that the feature vector isn't defined more than once.  

|Exception Messages|
|------------------------|
|Duplicate feature definition for a user or item.|


## Error 0037  
 Exception occurs if multiple label columns are specified and just one is allowed.  

 This error in Azure Machine Learning occurs if more than one column is selected to be the new label column. Most supervised learning algorithms require a single column to be marked as the target or label.  

**Resolution:**
 Make sure to select a single column as the new label column.  

|Exception Messages|
|------------------------|
|Multiple label columns are specified.|
|Multiple label columns are specified in "{dataset_name}".|


## Error 0039  
 Exception occurs if an operation has failed.  

 This error in Azure Machine Learning occurs when an internal operation can't be completed.  

**Resolution:**
 This error is caused by many conditions and there's no specific remedy.  
 The following table contains generic messages for this error, which are followed by a specific description of the condition. 

 If no details are available, [Microsoft Q&A question page for send feedback](/answers/topics/azure-machine-learning-studio-classic.html) and provide information about the components that generated the error and related conditions.

|Exception Messages|
|------------------------|
|Operation failed.|
|Error while completing operation: "{failed_operation}".|
|Error while completing operation: "{failed_operation}". Reason: "{reason}".|


## Error 0042  
 Exception occurs when it isn't possible to convert column to another type.  

 This error in Azure Machine Learning occurs when it isn't possible to convert column to the specified type.  You'll receive this error if a component requires a particular data type, such as datetime, text, a floating point number, or integer, but it isn't possible to convert an existing column to the required type.  

For example, you might select a column and try to convert it to a numeric data type for use in a math operation, and get this error if the column contained invalid data. 

Another reason you might get this error if you try to use a column containing floating point numbers or many unique values as a categorical column. 

**Resolution:**

+ Open the help page for the component that generated the error, and verify the data type requirements.
+ Review the data types of the columns in the input dataset.
+ Inspect data originating in so-called schema-less data sources.
+ Check the dataset for missing values or special characters that might block conversion to the desired data type. 
    + Numeric data types should be consistent: for example, check for floating point numbers in a column of integers.
    + Look for text strings or NA values in a number column. 
    + Boolean values can be converted to an appropriate representation depending on the required data type.
    + Examine text columns for nonunicode characters, tab characters, or control characters
    + Datetime data should be consistent to avoid modeling errors, but cleanup can be complex owing to the many formats. Consider using <!--the [Execute R Script](execute-r-script.md) or -->[Execute Python Script](execute-python-script.md) components to perform cleanup.  
+ If necessary, modify the values in the input dataset so that the column can be converted successfully. Modification might include binning, truncation or rounding operations, elimination of outliers, or imputation of missing values. See the following articles for some common data transformation scenarios in machine learning:
    + [Clean Missing Data](clean-missing-data.md)
    + [Normalize Data](normalize-data.md)
<!--+ [Clip Values](clip-values.md) 
    + [Group Data Into Bins](group-data-into-bins.md)
  -->

> [!TIP]
> Resolution unclear, or not applicable to your case? You are welcome to send feedback on this article and provide information about the scenario, including the component and the data type of the column. We will use this information to provide more detailed troubleshooting steps in the future.  

|Exception Messages|
|------------------------|
|Not allowed conversion.|
|Could not convert column of type {type1} to column of type {type2}.|
|Could not convert column "{col_name1}" of type {type1} to column of type {type2}.|
|Could not convert column "{col_name1}" of type {type1} to column "{col_name2}" of type {type2}.|


## Error 0044  
 Exception occurs when it isn't possible to derive element type of column from the existing values.  

 This error in Azure Machine Learning occurs when it isn't possible to infer the type of a column or columns in a dataset. This typically happens when concatenating two or more datasets with different element types. If Azure Machine Learning is unable to determine a common type that is able to represent all the values in a column or columns without loss of information, it generates this error.  

**Resolution:**
 Ensure that all values in a given column in both datasets being combined are either of the same type (numeric, Boolean, categorical, string, date, etc.) or can be coerced to the same type.  

|Exception Messages|
|------------------------|
|Cannot derive element type of the column.|
|Cannot derive element type for column "{column_name}" -- all the elements are null references.|
|Cannot derive element type for column "{column_name}" of dataset "{dataset_name}" -- all the elements are null references.|


## Error 0045  
 Exception occurs when it isn't possible to create a column because of mixed element types in the source.  

 This error in Azure Machine Learning is produced when the element types of two datasets being combined are different.  

**Resolution:**
 Ensure that all values in a given column in both datasets being combined are of the same type (numeric, Boolean, categorical, string, date, etc.).  

|Exception Messages|
|------------------------|
|Cannot create column with mixed element types.|
|Cannot create column with id "{column_id}" of mixed element types:<br />Type of data[{row_1}, {column_id}] is "{type_1}". <br />Type of data[{row_2}, {column_id}] is "{type_2}".|
|Cannot create column with id "{column_id}" of mixed element types:<br />Type in chunk {chunk_id_1} is "{type_1}". <br />Type in chunk {chunk_id_2} is "{type_2}" with chunk size: {chunk_size}.|


## Error 0046  
 Exception occurs when it isn't possible to create directory on specified path.  

 This error in Azure Machine Learning occurs when it isn't possible to create a directory on the specified path. You'll receive this error if any part of the path to the output directory for a Hive Query is incorrect or inaccessible.  

**Resolution:**
 Revisit the component and verify that the directory path is correctly formatted and that it's accessible with the current credentials.  

|Exception Messages|
|------------------------|
|Please specify a valid output directory.|
|Directory: {path} cannot be created. Please specify valid path.|


## Error 0047  
 Exception occurs if number of feature columns in some of the datasets passed to the component is too small.  

 This error in Azure Machine Learning occurs if the input dataset to training doesn't contain the minimum number of columns required by the algorithm. Typically either the dataset is empty or only contains training columns.  

**Resolution:**
 Revisit the input dataset to make sure there are one or more additional columns apart from the label column.  

|Exception Messages|
|------------------------|
|Number of feature columns in input dataset is less than allowed minimum.|
|Number of feature columns in input dataset is less than allowed minimum of {required_columns_count} column(s).|
|Number of feature columns in input dataset "{arg_name}" is less than allowed minimum of {required_columns_count} column(s).|


## Error 0048  
 Exception occurs in the case when it isn't possible to open a file.  

 This error in Azure Machine Learning occurs when it isn't possible to open a file for read or write. You might receive this error for these reasons:  

-   The container or the file (blob) doesn't exist  
  
-   The access level of the file or container doesn't allow you to access the file  
  
-   The file is too large to read or the wrong format  

**Resolution:**
 Revisit the component and the file you're trying to read.  

 Verify that the names of the container and file are correct.  

 Use the Azure classic portal or an Azure storage tool to verify that you have permission to access the file.  

  <!--If you are trying to read an image file, make sure that it meets the requirements for image files in terms of size, number of pixels, and so forth. For more information, see [Import Images](import-images.md).  -->

|Exception Messages|
|------------------------|
|Unable to open a file.|
|Error while opening the file: {file_name}.|
|Error while opening the file: {file_name}. Storage exception message: {exception}.|


## Error 0049  
 Exception occurs in the case when it isn't possible to parse a file.  

 This error in Azure Machine Learning occurs when it isn't possible to parse a file. You'll receive this error if the file format selected in the [Import Data](import-data.md) component doesn't match the actual format of the file, or if the file contains an unrecognizable character.  

**Resolution:**
 Revisit the component and correct the file format selection if it doesn't match the format of the file. If possible, inspect the file to confirm that it doesn't contain any illegal characters.  

|Exception Messages|
|------------------------|
|Unable to parse a file.|
|Error while parsing the {file_format} file.|
|Error while parsing the {file_format} file: {file_name}.|
|Error while parsing the {file_format} file. Reason: {failure_reason}.|
|Error while parsing the {file_format} file: {file_name}. Reason: {failure_reason}.|


## Error 0052  
 Exception occurs if Azure storage account key is specified incorrectly.  

 This error in Azure Machine Learning occurs if the key used to access the Azure storage account is incorrect. For example, you might see this error if the Azure storage key was truncated when copied and pasted, or if the wrong key was used.  

 For more information about how to get the key for an Azure storage account, see [View, copy, and regenerate storage access keys](/azure/storage/common/storage-account-create).  

**Resolution:**
 Revisit the component and verify that the Azure storage key is correct for the account; copy the key again from the Azure classic portal if necessary.  

|Exception Messages|
|------------------------|
|The Azure storage account key is incorrect.|


## Error 0053  
 Exception occurs in the case when there are no user features or items for matchbox recommendations.  

 This error in Azure Machine Learning is produced when a feature vector can't be found.  

**Resolution:**
 Ensure that a feature vector is present in the input dataset.  

|Exception Messages|
|------------------------|
|User features or/and items are required but not provided.|


## Error 0056  
 Exception occurs if the columns you selected for an operation violates requirements.  

 This error in Azure Machine Learning occurs when you're choosing columns for an operation that requires the column be of a particular data type. 

 This error can also happen if the column is the correct data type, but the component you're using requires that the column also be marked as a feature, label, or categorical column.  

  <!--For example, the [Convert to Indicator Values](convert-to-indicator-values.md) component requires that columns be categorical, and will raise this error if you select a feature column or label column.  -->

**Resolution:**

1.  Review the data type of the columns that are currently selected. 

2. Ascertain whether the selected columns are categorical, label, or feature columns.  
  
3.  Review the help topic for the component in which you made the column selection, to determine if there are specific requirements for data type or column usage.  
  
3.  Use [Edit Metadata](edit-metadata.md) to change the column type for the duration of this operation. Be sure to change the column type back to its original value, using another instance of [Edit Metadata](edit-metadata.md), if you need it for downstream operations.  

|Exception Messages|
|------------------------|
|One or more selected columns were not in an allowed category.|
|Column with name "{col_name}" is not in an allowed category.|


## Error 0057  
 Exception occurs when attempting to create a file or blob that already exists.  

 This exception occurs when you're using the [Export Data](export-data.md) component or other component to save  results of a pipeline in Azure Machine Learning to Azure blob storage, but you attempt to create a file or blob that already exists.   

**Resolution:**

 You'll receive this error only if you previously set the property **Azure blob storage write mode** to **Error**. By design, this component raises an error if you attempt to write a dataset to a blob that already exists.

 - Open the component properties and change the property **Azure blob storage write mode** to **Overwrite**.
 - Alternatively, you can type the name of a different destination blob or file and be sure to specify a blob that doesn't already exist.  

|Exception Messages|
|------------------------|
|File or Blob already exists.|
|File or Blob "{file_path}" already exists.|


## Error 0058  
 This error in Azure Machine Learning occurs if the dataset doesn't contain the expected label column.  

 This exception can also occur when the label column provided doesn't match the data or datatype expected by the learner, or has the wrong values. For example, this exception is produced when using a real-valued label column when training a binary classifier.  

**Resolution:**
 The resolution depends on the learner or trainer that you're using, and the data types of  the columns in your dataset. First, verify the requirements of the machine learning algorithm or training component.  

 Revisit the input dataset. Verify that the column you expect to be treated as the label has the right data type for the model you're creating.  

 Check inputs for missing values and eliminate or replace them if necessary.  

 If necessary, add the [Edit Metadata](edit-metadata.md) component and ensure that the label column is marked as a label.  

|Exception Messages|
|------------------------|
|The label column values and scored label column values are not comparable.|
|The label column is not as expected in "{dataset_name}".|
|The label column is not as expected in "{dataset_name}", {reason}.|
|The label column "{column_name}" is not expected in "{dataset_name}".|
|The label column "{column_name}" is not expected in "{dataset_name}", {reason}.|


## Error 0059  
 Exception occurs if a column index specified in a column picker can't be parsed.  

 This error in Azure Machine Learning occurs if a column index specified when using the Column Selector can't be parsed.  You'll receive this error when the column index is in an invalid format that can't be parsed.  

**Resolution:**
 Modify the column index to use a valid index value.  

|Exception Messages|
|------------------------|
|One or more specified column indexes or index ranges could not be parsed.|
|Column index or range "{column_index_or_range}" could not be parsed.|


## Error 0060  
 Exception occurs when an out of range column range is specified in a column picker.  

 This error in Azure Machine Learning occurs when an out-of-range column range is specified in the Column Selector. You'll receive this error if the column range in the column picker doesn't correspond to the columns in the dataset.  

**Resolution:**
 Modify the column range in the column picker to correspond to the columns in the dataset.  

|Exception Messages|
|------------------------|
|Invalid or out of range column index range specified.|
|Column range "{column_range}" is invalid or out of range.|


## Error 0061  
 Exception occurs when attempting to add a row to a DataTable that has a different number of columns than the table.  

 This error in Azure Machine Learning occurs when you attempt to add a row to a dataset that has a different number of columns than the dataset.  You'll receive this error if the row that is being added to the dataset has a different number of columns from the input dataset.  The row can't be appended to the dataset if the number of columns is different.  

**Resolution:**
 Modify the input dataset to have the same number of columns as the row added, or modify the row added to have the same number of columns as the dataset.  

|Exception Messages|
|------------------------|
|All tables must have the same number of columns.|
|Columns in chunk "{chunk_id_1}" is different with chunk "{chunk_id_2}" with chunk size: {chunk_size}.|
|Column count in file "{filename_1}" (count={column_count_1}) is different with file "{filename_2}" (count={column_count_2}).|


## Error 0062  
 Exception occurs when attempting to compare two models with different learner types.  

 This error in Azure Machine Learning is produced when evaluation metrics for two different scored datasets can't be compared. In this case, it isn't possible to compare the effectiveness of the models used to produce the two scored datasets.  

**Resolution:**
 Verify that the scored results are produced by the same kind of machine learning model (binary classification, regression, multi-class classification, recommendation, clustering, anomaly detection, etc.) All models that you compare must have the same learner type.  

|Exception Messages|
|------------------------|
|All models must have the same learner type.|
|Got incompatible learner type: "{actual_learner_type}". Expected learner types are: "{expected_learner_type_list}".|


## Error 0064  
 Exception occurs if Azure storage account name or storage key is specified incorrectly.  

 This error in Azure Machine Learning occurs if the Azure storage account name or storage key is specified incorrectly. You'll receive this error if you enter an incorrect account name or password for the storage account. This may occur if you manually enter the account name or password. It may also occur if the account has been deleted.  

**Resolution:**
 Verify that the account name and password have been entered correctly, and that the account exists.  

|Exception Messages|
|------------------------|
|The Azure storage account name or storage key is incorrect.|
|The Azure storage account name "{account_name}" or storage key for the account name is incorrect.|


## Error 0065  
 Exception occurs if Azure blob name is specified incorrectly.  

 This error in Azure Machine Learning occurs if the Azure blob name is specified incorrectly.  You'll receive the error if:  

-   The blob can't be found in the specified container.  

 <!---   The fully qualified name of the blob specified for output in one of the [Learning with Counts](data-transformation-learning-with-counts.md) components is greater than 512 characters.  -->

-   Only the container was specified as the source in a [Import Data](import-data.md) request when the format was Excel or CSV with encoding; concatenation of the contents of all blobs within a container isn't allowed with these formats.  
  
-   A SAS URI doesn't contain the name of a valid blob.  

**Resolution:**
 Revisit the component throwing the exception. Verify that the specified blob does exist in the container in the storage account and that permissions allow you to see the blob. Verify that the input is of the form **containername/filename** if you have Excel or CSV with encoding formats. Verify that a SAS URI contains the name of a valid blob.  

|Exception Messages|
|------------------------|
|The Azure storage blob name is incorrect.|
|The Azure storage blob name "{blob_name}" is incorrect.|
|The Azure storage blob name with prefix "{blob_name_prefix}" does not exist.|
|Failed to find any Azure storage blobs under container "{container_name}".|
|Failed to find any Azure storage blobs with wildcard path "{blob_wildcard_path}".|


## Error 0066  
 Exception occurs if a resource couldn't be uploaded to an Azure Blob.  

 This error in Azure Machine Learning occurs if a resource couldn't be uploaded to an Azure Blob.  <!--You will receive this message if [Train Vowpal Wabbit 7-4 Model](train-vowpal-wabbit-version-7-4-model.md) encounters an error attempting to save either the model or the hash created when training the model.--> Both are saved to the same Azure storage account as the account containing the input file.  

**Resolution:**
 Revisit the component. Verify that the Azure account name, storage key, and container are correct and that the account has permission to write to the container.  

|Exception Messages|
|------------------------|
|The resource could not be uploaded to Azure storage.|
|The file "{source_path}" could not be uploaded to Azure storage as "{dest_path}".|


## Error 0067  
 Exception occurs if a dataset has a different number of columns than expected.  

 This error in Azure Machine Learning occurs if a dataset has a different number of columns than expected.  You'll receive this error when the number of columns in the dataset are different from the number of columns that the component expects during execution.  

**Resolution:**
 Modify the input dataset or the parameters.  

|Exception Messages|
|------------------------|
|Unexpected number of columns in the datatable.|
|Unexpected number of columns in the dataset "{dataset_name}".|
|Expected "{expected_column_count}" column(s) but found "{actual_column_count}" column(s) instead.|
|In input dataset "{dataset_name}", expected "{expected_column_count}" column(s) but found "{actual_column_count}" column(s) instead.|


## Error 0068  
 Exception occurs if the specified Hive script isn't correct.  

 This error in Azure Machine Learning occurs if there are syntax errors in a Hive QL script, or if the Hive interpreter encounters an error while executing the query or script.  

**Resolution:**

The error message from Hive is normally reported back in the Error Log so that you can take action based on the specific error. 

+ Open the component and inspect the query for mistakes.  
+ Verify that the query works correctly outside of Azure Machine Learning by logging in to the Hive console of your Hadoop cluster and running the query.  
+ Try placing comments in your Hive script in a separate line as opposed to mixing executable statements and comments in a single line.  

### Resources

See the following articles for help with Hive queries for machine learning:

+ [Create Hive tables and load data from Azure Blob Storage](/azure/architecture/data-science-process/move-hive-tables)
+ [Explore data in tables with Hive queries](/azure/architecture/data-science-process/explore-data-hive-tables)
+ [Create features for data in a Hadoop cluster using Hive queries](/azure/architecture/data-science-process/create-features-hive)
+ [Hive for SQL Users Cheat Sheet (PDF)](http://hortonworks.com/wp-content/uploads/2013/05/hql_cheat_sheet.pdf)

  
|Exception Messages|
|------------------------|
|Hive script is incorrect.|


## Error 0069  
 Exception occurs if the specified SQL script isn't correct.  

 This error in Azure Machine Learning occurs if the specified SQL script has syntax problems, or if the columns or table specified in the script isn't valid. 

 You'll receive this error if the SQL engine encounters any error while executing the query or script. The SQL error message is normally reported back in the Error Log so that you can take action based on the specific error.  

**Resolution:**
 Revisit the component and inspect the SQL query for mistakes.  

 Verify that the query works correctly outside of Azure Machine Learning by logging in to the database server directly and running the query.  

 If there's a SQL generated message reported by the component exception, take action based on the reported error. For example, the error messages sometimes include specific guidance on the likely error:
+ *No such column or missing database*, indicating that you might have typed a column name wrong. If you're sure the column name is correct, try using brackets or quotation marks to enclose the column identifier.
+ *SQL logic error near \<SQL keyword\>*, indicating that you might have a syntax error before the specified keyword

  
|Exception Messages|
|------------------------|
|SQL script is incorrect.|
|SQL query "{sql_query}" is not correct.|
|SQL query "{sql_query}" is not correct. Exception message: {exception}.|


## Error 0070  
 Exception occurs when attempting to access nonexistent Azure table.  

 This error in Azure Machine Learning occurs when you attempt to access a nonexistent Azure table. You'll receive this error if you specify a table in Azure storage, which doesn't exist when reading from or writing to Azure Table Storage. This can happen if you mistype the name of the desired table, or you have a mismatch between the target name and the storage type. For example, you intended to read from a table but entered the name of a blob instead.  

**Resolution:**
 Revisit the component to verify that the name of the table is correct.  

|Exception Messages|
|------------------------|
|Azure table does not exist.|
|Azure table "{table_name}" does not exist.|


## Error 0072  
 Exception occurs in the case of connection timeout.  

 This error in Azure Machine Learning occurs when a connection times out. You'll receive this error if there are currently connectivity issues with the data source or destination, such as slow internet connectivity, or if the dataset is large and/or the SQL query to read in the data performs complicated processing.  

**Resolution:**
 Determine whether there are currently issues with slow connections to Azure storage or the internet.  

|Exception Messages|
|------------------------|
|Connection timeout occurred.|


## Error 0073  
 Exception occurs if an error occurs while converting a column to another type.  

 This error in Azure Machine Learning occurs when it isn't possible to convert column to another type.  You'll receive this error if a component requires a particular type and it isn't possible to convert the column to the new type.  

**Resolution:**
 Modify the input dataset so that the column can be converted based on the inner exception.  

|Exception Messages|
|------------------------|
|Failed to convert column.|
|Failed to convert column to {target_type}.|


## Error 0075  
Exception occurs when an invalid binning function is used when quantizing a dataset.  

This error in Azure Machine Learning occurs when you're trying to bin data using an unsupported method, or when the parameter combinations are invalid.  

**Resolution:**

Error handling for this event was introduced in an earlier version of Azure Machine Learning that allowed more customization of binning methods. Currently all binning methods are based on a selection from a dropdown list, so technically it should no longer be possible to get this error.

 <!--If you get this error when using the [Group Data into Bins](group-data-into-bins.md) component, consider reporting the issue in the [Microsoft Q&A question page for Azure Machine Learning](/answers/topics/azure-machine-learning-studio-classic.html), providing the data types, parameter settings, and the exact error message.  -->

|Exception Messages|
|------------------------|
|Invalid binning function used.|


## Error 0077  
 Exception occurs when unknown blob file writes mode passed.  

 This error in Azure Machine Learning occurs if an invalid argument is passed in the specifications for a blob file destination or source.  

**Resolution:**
 In almost all components that import or export data to and from Azure blob storage, parameter values controlling the write mode are assigned by using a dropdown list; therefore, it isn't possible to pass an invalid value, and this error shouldn't appear. This error is deprecated in a later release.  

|Exception Messages|
|------------------------|
|Unsupported blob write mode.|
|Unsupported blob write mode: {blob_write_mode}.|


## Error 0078  
 Exception occurs when the HTTP option for [Import Data](import-data.md) receives a 3xx status code indicating redirection.  

 This error in Azure Machine Learning occurs when the HTTP option for [Import Data](import-data.md) receives a 3xx (301, 302, 304, etc.) status code indicating redirection. You'll receive this error if you attempt to connect to an HTTP source that redirects the browser to another page. For security reasons, redirecting websites aren't allowed as data sources for Azure Machine Learning.  

**Resolution:**
 If the website is a trusted website, enter the redirected URL directly.  

|Exception Messages|
|------------------------|
|Http redirection not allowed.|


## Error 0079  
 Exception occurs if Azure storage container name is specified incorrectly.  

 This error in Azure Machine Learning occurs if the Azure storage container name is specified incorrectly. You'll receive this error if you haven't specified both the container and the blob (file) name using **the Path to blob beginning with container** option when writing to Azure Blob Storage.  

**Resolution:**
 Revisit the [Export Data](export-data.md) component and verify that the specified path to the blob contains both the container and the file name, in the format **container/filename**.  

|Exception Messages|
|------------------------|
|The Azure storage container name is incorrect.|
|The Azure storage container name "{container_name}" is incorrect; a container name of the format container/blob was expected.|


## Error 0080  
 Exception occurs when column with all values missing isn't allowed by component.  

 This error in Azure Machine Learning is produced when one or more of the columns consumed by the component contains all missing values. For example, if a component is computing aggregate statistics for each column, it can't operate on a column containing no data. In such cases, component execution is halted with this exception.  

**Resolution:**
 Revisit the input dataset and remove any columns that contain all missing values.  

|Exception Messages|
|------------------------|
|Columns with all values missing are not allowed.|
|Column {col_index_or_name} has all values missing.|


## Error 0081  
 Exception occurs in PCA component if number of dimensions to reduce to is equal to number of feature columns in input dataset, containing at least one sparse feature column.  

 This error in Azure Machine Learning is produced if the following conditions are met: (a) the input dataset has at least one sparse column and (b) the final number of dimensions requested is the same as the number of input dimensions.  

**Resolution:**
 Consider reducing the number of dimensions in the output to be fewer than the number of dimensions in the input. It's typical in applications of PCA.   <!--For more information, see [Principal Component Analysis](principal-component-analysis.md).  -->

|Exception Messages|
|------------------------|
|For dataset containing sparse feature columns number of dimensions to reduce to should be less than number of feature columns.|


## Error 0082  
 Exception occurs when a model can't be successfully deserialized.  

 This error in Azure Machine Learning occurs when a saved machine learning model or transform can't be loaded by a newer version of the Azure Machine Learning runtime as a result of a breaking change.  

**Resolution:**
 The training pipeline that produced the model or transform must be rerun and the model or transform must be resaved.  

|Exception Messages|
|------------------------|
|Model could not be deserialized because it is likely serialized with an older serialization format. Retrain and resave the model.|


## Error 0083  
 Exception occurs if dataset used for training can't be used for concrete type of learner.  

 This error in Azure Machine Learning is produced when the dataset is incompatible with the learner being trained. For example, the dataset might contain at least one missing value in each row, and as a result, the entire dataset would be skipped during training. In other cases, some machine learning algorithms such as anomaly detection don't expect labels to be present and can throw this exception if labels are present in the dataset.  

**Resolution:**
 Consult the documentation of the learner being used to check requirements for the input dataset. Examine the columns to see all required columns are present.  

|Exception Messages|
|------------------------|
|Dataset used for training is invalid.|
|{data_name} contains invalid data for training.|
|{data_name} contains invalid data for training. Learner type: {learner_type}.|
|{data_name} contains invalid data for training. Learner type: {learner_type}. Reason: {reason}.|
|Failed to apply "{action_name}" action on training data {data_name}. Reason: {reason}.|


## Error 0084  
 Exception occurs when scores produced from an R Script are evaluated. This is currently unsupported.  

 This error in Azure Machine Learning occurs if you try to use one of the components for evaluating a model with output from an R script that contains scores.  

**Resolution:**

|Exception Messages|
|------------------------|
|Evaluating scores produced by Custom Model is currently unsupported.|


## Error 0085  
 Exception occurs when script evaluation fails with an error.  

 This error in Azure Machine Learning occurs when you're running custom script that contains syntax errors.  

**Resolution:**
 Review your code in an external editor and check for errors.  

|Exception Messages|
|------------------------|
|Error during evaluation of script.|
|The following error occurred during script evaluation, please view the output log for more information:<br />---------- Start of error message from {script_language} interpreter ----------<br />{message}<br />---------- End of error message from {script_language}  interpreter  ----------|


## Error 0090  
 Exception occurs when Hive table creation fails.  

 This error in Azure Machine Learning occurs when you're using [Export Data](export-data.md) or another option to save data to an HDInsight cluster and the specified Hive table can't be created.  

**Resolution:**
 Check the Azure storage account name associated with the cluster and verify that you're using the same account in the component properties.  

|Exception Messages|
|------------------------|
|The Hive table could not be created. For a HDInsight cluster, please ensure the Azure storage account name associated with cluster is the same as what is passed in through the component parameter.|
|The Hive table "{table_name}" could not be created. For a HDInsight cluster, please ensure the Azure storage account name associated with cluster is the same as what is passed in through the component parameter.|
|The Hive table "{table_name}" could not be created. For a HDInsight cluster, ensure the Azure storage account name associated with cluster is "{cluster_name}".|


## Error 0102  
 Thrown when a ZIP file can't be extracted.  

 This error in Azure Machine Learning occurs when you're importing a zipped package with the .zip extension, but the package is either not a zip file, or the file doesn't use a supported zip format.  

**Resolution:**
 Make sure the selected file is a valid .zip file, and that it was compressed by using one of the supported compression algorithms.  

 If you get this error when importing datasets in compressed format, verify that all contained files use one of the supported file formats, and are in Unicode format.  <!--For more information, see [Unpack Zipped Datasets](unpack-zipped-datasets.md).  -->

 Try reading the desired files to a new compressed zipped folder and try to add the custom component again.  

|Exception Messages|
|------------------------|
|Given ZIP file is not in the correct format.|


## Error 0105  
 This error is displayed when a component definition file contains an unsupported parameter type.  
  
 This error in Azure Machine Learning is produced when you create a custom component xml definition and the type of a parameter or argument in the definition doesn't match a supported type.  
  
**Resolution:**
 Make sure that the type property of any **Arg** element in the custom component xml definition file is a supported type.  
  
|Exception Messages|  
|------------------------|  
|Unsupported parameter type.|  
|Unsupported parameter type '{0}' specified.|  


## Error 0107  
 Thrown when a component definition file defines an unsupported output type.  
  
 This error in Azure Machine Learning is produced when the type of an output port in a custom component xml definition doesn't match a supported type.  
  
**Resolution:**
 Make sure that the type property of an Output element in the custom component xml definition file is a supported type.  
  
|Exception Messages|  
|------------------------|  
|Unsupported output type.|  
|Unsupported output type '{output_type}' specified.|  


## Error 0125  
 Thrown when schema for multiple datasets doesn't match.  

**Resolution:**

|Exception Messages|
|------------------------|
|Dataset schema does not match.|


## Error 0127  
 Image pixel size exceeds allowed limit.  

 This error occurs if you're reading images from an image dataset for classification and the images are larger than the model can handle.  

 <!--**Resolution:**
 For more information about the image size and other requirements, see these topics:  

-   [Import Images](import-images.md)  
  
-   [Pretrained Cascade Image Classification](pretrained-cascade-image-classification.md)  -->

|Exception Messages|
|------------------------|
|Image pixel size exceeds allowed limit.|
|Image pixel size in the file '{file_path}' exceeds allowed limit: '{size_limit}'.|


## Error 0128  
 Number of conditional probabilities for categorical columns exceeds limit.  

**Resolution:**

|Exception Messages|
|------------------------|
|Number of conditional probabilities for categorical columns exceeds limit.|
|Number of conditional probabilities for categorical columns exceeds limit. Columns '{column_name_or_index_1}' and '{column_name_or_index_2}' are the problematic pair.|


## Error 0129  
 Number of columns in the dataset exceeds allowed limit.  

**Resolution:**

|Exception Messages|
|------------------------|
|Number of columns in the dataset exceeds allowed limit.|
|Number of columns in the dataset in '{dataset_name}' exceeds allowed.|
|Number of columns in the dataset in '{dataset_name}' exceeds allowed limit of '{component_name}'.|
|Number of columns in the dataset in '{dataset_name}' exceeds allowed '{limit_columns_count}' limit of '{component_name}'.|


## Error 0134
Exception occurs when label column is missing or has insufficient number of labeled rows.  

This error occurs when the component requires a label column, but you didn't include one in the column selection, or the label column is missing too many values.

This error can also occur when a previous operation changes the dataset such that insufficient rows are available to a downstream operation. For example, suppose you use an expression in the **Partition and Sample** component to divide a dataset by values. If no matches are found for your expression, one of the datasets resulting from the partition would be empty.

Resolution: 

 If you include a label column in the column selection but it isn't recognized, use the [Edit Metadata](edit-metadata.md) component to mark it as a label column.

  <!--Use the [Summarize Data](summarize-data.md) component to generate a report that shows how many values are missing in each column. -->
  Then, you can use the [Clean Missing Data](clean-missing-data.md) component to remove rows with missing values in the label column. 

 Check your input datasets to make sure that they contain valid data, and enough rows to satisfy the requirements of the operation. Many algorithms generate an error message if they require some minimum number rows of data, but the data contains only a few rows, or only a header.

|Exception Messages|
|------------------------|
|Exception occurs when label column is missing or has insufficient number of labeled rows.|
|Exception occurs when label column is missing or has less than {required_rows_count} labeled rows.|
|Exception occurs when label column in dataset {dataset_name} is missing or has less than {required_rows_count} labeled rows.|


## Error 0138  
 Memory has been exhausted, unable to complete running of component. Downsampling the dataset may help to alleviate the problem.  

 This error occurs when the component that is running requires more memory than is available in the Azure container. This can happen if you're working with a large dataset and the current operation can't fit into memory.  

**Resolution:**
 If you're trying to read a large dataset and the operation can't be completed, downsampling the dataset might help.  

  <!--If you use the visualizations on datasets to check the cardinality of columns, only some rows are sampled. To get a full report, use [Summarize Data](summarize-data.md). You can also use the [Apply SQL Transformation](apply-sql-transformation.md) to check for the number of unique values in each column.  

 Sometimes transient loads can lead to such error. Machine support also changes over time. 

 Try using [Principal Component Analysis](principal-component-analysis.md) or one of the provided feature selection methods to reduce your dataset to a smaller set of more feature-rich columns: [Feature Selection](feature-selection-modules.md)  -->

|Exception Messages|
|------------------------|
|Memory has been exhausted, unable to complete running of component.|
|Memory has been exhausted, unable to complete running of component. Details: {details}|


## Error 0141  
 Exception occurs if the number of the selected numerical columns and unique values in the categorical and string columns is too small.  

 This error in Azure Machine Learning occurs when there aren't enough unique values in the selected column to perform the operation.  

**Resolution:**
 Some operations perform statistical operations on feature and categorical columns, and if there aren't enough values, the operation might fail or return an invalid result. Check your dataset to see how many values there are in the feature and label columns, and determine whether the operation you're trying to perform is statistically valid.  

 If the source dataset is valid, you might also check whether some upstream data manipulation or metadata operation has changed the data and removed some values.  

 If upstream operations include splitting, sampling, or resampling, verify that the outputs contain the expected number of rows and values.  

|Exception Messages|
|------------------------|
|The number of the selected numerical columns and unique values in the categorical and string columns is too small.|
|The total number of the selected numerical columns and unique values in the categorical and string columns (currently {actual_num}) should be at least {lower_boundary}.|


## Error 0154  
 Exception occurs when user tries to join data on key columns with incompatible column type.

|Exception Messages|
|------------------------|
|Key column element types are not compatible.|
|Key column element types are not compatible.(left: {keys_left}; right: {keys_right})|


## Error 0155  
 Exception occurs when column names of dataset aren't string.

|Exception Messages|
|------------------------|
|The dataframe column name must be string type. Column names are not string.|
|The dataframe column name must be string type. Column names {column_names} are not string.|


## Error 0156  
 Exception occurs when failed to read data from Azure SQL Database.

|Exception Messages|
|------------------------|
|Failed to read data from Azure SQL Database.|
|Failed to read data from Azure SQL Database: {detailed_message} DB: {database_server_name}:{database_name} Query: {sql_statement}|


## Error 0157  
 Datastore not found.

|Exception Messages|
|------------------------|
|Datastore information is invalid.|
|Datastore information is invalid. Failed to get Azure Machine Learning datastore '{datastore_name}' in workspace '{workspace_name}'.|


## Error 0158
 Thrown when a transformation directory is invalid.

|Exception Messages|
|------------------------------------------------------------|
|Given TransformationDirectory is invalid.|
|TransformationDirectory "{arg_name}" is invalid. Reason: {reason}. Rerun training experiment, which generates the Transform file. If training experiment was deleted, please recreate and save the Transform file.|
|TransformationDirectory "{arg_name}" is invalid. Reason: {reason}. {troubleshoot_hint}|


## Error 0159
 Exception occurs if component model directory is invalid. 

|Exception Messages|
|------------------------------------------------------------|
|Given ModelDirectory is invalid.|
|ModelDirectory "{arg_name}" is invalid.|
|ModelDirectory "{arg_name}" is invalid. Reason: {reason}.|
|ModelDirectory "{arg_name}" is invalid. Reason: {reason}. {troubleshoot_hint}|


## Error 1000  
Internal library exception.  

This error is provided to capture otherwise unhandled internal engine errors. Therefore, the cause for this error might be different depending on the component that generated the error.  

To get more help, we recommend that you post the detailed message that accompanies the error to the [Azure Machine Learning forum](/answers/topics/azure-machine-learning.html), together with a description of the scenario, including the data used as inputs. This feedback helps us to prioritize errors and identify the most important issues for further work.  

|Exception Messages|
|------------------------|
|Library exception.|
|Library exception: {exception}.|
|Unknown library exception: {exception}. {customer_support_guidance}.|

## Troubleshooting guide

### Execute Python Script component error

Search **in azureml_main** in **70_driver_logs** of **Execute Python Script component** and you could find which line occurred error. For example, "File "/tmp/tmp01_ID/user_script.py", line 17, in azureml_main" indicates that the error occurred in the 17 line of your Python script.

### Distributed training

Currently designer supports distributed training for and [Train PyTorch Model](train-pytorch-model.md) component.

<!-- [Train Wide and Deep Recommender](train-wide-and-deep-recommender.md) component  -->

If the component enabled distributed training fails without any `70_driver` logs, you can check `70_mpi_log` for error details.

  The following example shows that the **Node count** of run settings is larger than available node count of compute cluster.
  
  [![Screenshot showing node count error.](./media/module/distributed-training-node-count-error.png)](./media/module/distributed-training-node-count-error.png#lightbox)

  The following example shows that **Process count per node** is larger than **Processing Unit** of the compute.

  [![Screenshot showing mpi log.](./media/module/distributed-training-error-mpi-log.png)](./media/module/distributed-training-error-mpi-log.png#lightbox)

Otherwise, you can check `70_driver_log` for each process. `70_driver_log_0` is for master process.

  [![Screenshot showing driver log.](./media/module/distributed-training-error-driver-log.png)](./media/module/distributed-training-error-driver-log.png#lightbox)

### Fail to mount sample data in pipeline

:::image type="content" source="./media/module/global-datasets-error.png" alt-text="Screenshot of error of sample datastore." lightbox = "./media/module/global-datasets-error.png":::

If you encounter above error, please follow the steps below to resolve the issue:

- Double click data node to go to detail page of datastore.
  :::image type="content" source="./media/module/sample-data-datastore.png" alt-text="Screenshot of datastore of sample data." lightbox = "./media/module/sample-data-datastore.png":::

- `Unregister` this `azureml_globaldatasets` data store.
  :::image type="content" source="./media/module/unregister-sample-datastore.png" alt-text="Screenshot of unregister sample datastore." lightbox = "./media/module/unregister-sample-datastore.png":::

- Drag and drop a new `Sample Data` node to the pipeline to have another try.
