---
title:  "Apply SQL Transformation"
titleSuffix: Azure Machine Learning
description: Learn how to use the Apply SQL Transformation component in Azure Machine Learning to run a SQLite query on input datasets to transform the data.
services: machine-learning
ms.service: azure-machine-learning
ms.subservice: core
ms.topic: reference

author: likebupt
ms.author: keli19
ms.date: 08/11/2021
---

# Apply SQL Transformation

This article describes a component of Azure Machine Learning designer.

Using the Apply SQL Transformation component, you can:
  
-   Create tables for results and save the datasets in a portable database.  
  
-   Perform custom transformations on data types, or create aggregates.  
  
-   Execute SQL query statements to filter or alter data and return the query results as a data table.  

> [!IMPORTANT]
> The SQL engine used in this component is **SQLite**. For more information about SQLite syntax, see [SQL as Understood by SQLite](https://www.sqlite.org/index.html).
> This component will bump data to SQLite, which is in the memory DB, hence the component execution requires much more memory and may hit an `Out of memory` error. Make sure your computer has enough RAM.

## How to configure Apply SQL Transformation  

The component can take up to three datasets as inputs. When you reference the datasets connected to each input port, you must use the names `t1`, `t2`, and `t3`. The table number indicates the index of the input port.  

Following is sample code to show how to join two tables. t1 and t2 are two datasets connected to the left and middle input ports of **Apply SQL Transformation**:

```sql
SELECT t1.*
    , t3.Average_Rating
FROM t1 join
    (SELECT placeID
        , AVG(rating) AS Average_Rating
    FROM t2
    GROUP BY placeID
    ) as t3
on t1.placeID = t3.placeID
```
  
The remaining parameter is a SQL query, which uses the SQLite syntax. When typing multiple lines in the **SQL Script** text box, use a semi-colon to terminate each statement. Otherwise, line breaks are converted to spaces.  

This component supports all standard statements of the SQLite syntax. For a list of unsupported statements, see the [Technical Notes](#technical-notes) section.

##  Technical notes  

This section contains implementation details, tips, and answers to frequently asked questions.

-   An input is always required on port 1.  
  
-   For column identifiers that contain a space or other special characters, always enclose the column identifier in square brackets or double quotation marks when referring to the column in the `SELECT` or `WHERE` clauses.  

-   If you have used **Edit Metadata** to specify the column metadata (categorical or fields) before **Apply SQL Transformation**, the outputs of **Apply SQL Transformation** will not contain these attributes. You need to use **Edit Metadata** to edit the column after **Apply SQL Transformation**.
  
### Unsupported statements  

Although SQLite supports much of the ANSI SQL standard, it does not include many features supported by commercial relational database systems. For more information, see [SQL as Understood by SQLite](http://www.sqlite.org/lang.html). Also, be aware of the following restrictions when creating SQL statements:  
  
- SQLite uses dynamic typing for values, rather than assigning a type to a column as in most relational database systems. It is weakly typed, and allows implicit type conversion.  
  
- `LEFT OUTER JOIN` is implemented, but not `RIGHT OUTER JOIN` or `FULL OUTER JOIN`.  

- You can use `RENAME TABLE` and `ADD COLUMN` statements with the `ALTER TABLE` command, but other clauses are not supported, including `DROP COLUMN`, `ALTER COLUMN`, and `ADD CONSTRAINT`.  
  
- You can create a VIEW within SQLite, but thereafter views are read-only. You cannot execute a `DELETE`, `INSERT`, or `UPDATE` statement on a view. However, you can create a trigger that fires on an attempt to `DELETE`, `INSERT`, or `UPDATE` on a view and perform other operations in the body of the trigger.  
  

In addition to the list of non-supported functions provided on the official SQLite site, the following wiki provides a list of other unsupported features: [SQLite - Unsupported SQL](https://www.sqlite.org/omitted.html)  
    
## Next steps

See the [set of components available](component-reference.md) to Azure Machine Learning. 
