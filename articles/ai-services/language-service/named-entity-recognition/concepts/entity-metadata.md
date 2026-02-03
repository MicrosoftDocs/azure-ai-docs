---
title: Entity Metadata provided by Named Entity Recognition (NER)
titleSuffix: Foundry Tools
description: View entity metadata values for named entity recognition (NER) named entities.
author: laujan
manager: nitinme
ms.service: azure-ai-language
ms.topic: concept-article
ms.date: 11/18/2025
ms.author: lajanuar
ms.custom: language-service-ner
---
# Entity Metadata

The entity metadata object stores optional supplementary details about detected entities, specifically providing standardized resolutions for numeric and temporal data. 

This attribute is only populated when extra information is available and may be empty or missing for some entities. 

Metadata resolutions convert various entity forms into consistent formats—for example, both "eighty" and "80" resolve to the integer 80. These NER resolutions enable downstream actions, such as extracting date and time entities for integration with a meeting scheduling system.


> [!NOTE]
>  Support for Entity Metadata is available with API `2023-04-15-preview` and later versions. For older API versions, see [Entity Resolutions](./entity-resolutions.md).

## Entities with metadata attributes

|Entities|Entities|Entities|Entities|Entities|Entities|
|:---:|:---:|:---:|:---:|:---:|:---:|
|[Age](#age)|[Area](#area)|[Currency](#currency)|[Date](#date)|[Datetime](#datetime)|[Information](#information)|
|[Length](#length)|[Number](#number)|[NumericRange](#numericrange)|[Ordinal](#ordinal)|[Set](#set)|[Speed](#speed)|
|[Temperature](#temperature)|[Time](#time)|[Volume](#volume)|[Weight](#weight)|||


### Age

|Metadata|Type|Description|
|---|---|---|
|**unit**|string|Unit of measurement for age.|
|**value**|number|Numeric value for age.|

```json
"metadata": {
                "unit": "Year",
                "value": 10
            }
```

**Possible values for *unit***:

* Day
* Month
* Week
* Year
* Unspecified


### Area

|Metadata|Type|Description|
|---|---|---|
|**unit**|string|Unit of measurement for area.|
|**value**|number|Numeric value for area.|


```JSON
"metadata": {
                "unit": "Acre",
                "value": 30
            }
```

**Possible values for *unit***:

* Acre
* SquareCentimeter
* SquareDecameter
* SquareDecimeter
* SquareFoot
* SquareHectometer
* SquareInch
* SquareKilometer
* SquareMeter
* SquareMile
* SquareMillimeter
* SquareYard
* Unspecified

### Currency

|Metadata|Type|Description|
|---|---|---|
|**unit**|string|Name of currency.|
|**value**|number|Numeric value for currency.|
|**ISO4217**|string|The ISO 4217 three-letter currency code uses the first two letters from the country's ISO 3166 code, and, when possible, the third letter is the first letter of the currency name.|

```json
"metadata": {
                "unit": "Egyptian pound",
                "value": 30,
                "ISO4217": "EGP"
            }
```

**Possible values for *ISO4217***:
- [ISO 4217 reference](https://docs.1010data.com/1010dataReferenceManual/DataTypesAndFormats/currencyUnitCodes.html).



### Date

|Metadata|Type|Description|
|---|---|---|
|**timex**|string|The ISO 8601 formatted date: `YYYY-MM-DD` (year, month, day). |
|**value**|string|The actual denoted date.|


Whenever an ambiguous date is provided, you're offered different options for your resolution. For example, "12 April" could refer to any year. Resolution provides this year and the next as options. The `timex` value `XXXX` indicates no year was specified in the query.

```json
"metadata": {
                "dateValues": [
                    {
                        "timex": "XXXX-04-12",
                        "value": "2022-04-12"
                    },
                    {
                        "timex": "XXXX-04-12",
                        "value": "2023-04-12"
                    }
                ]
            }
```

Ambiguity can occur even for a given day of the week. For example, saying "Monday" could refer to last Monday or this Monday. Once again the `timex` value indicates no year or month was specified, and uses a day of the week identifier (W) to indicate the first day of the week.

```json
"metadata" :{
                "dateValues": [
                    {
                        "timex": "XXXX-WXX-1",
                        "value": "2022-10-03"
                    },
                    {
                        "timex": "XXXX-WXX-1",
                        "value": "2022-10-10"
                    }
                ]
            }
```

### Datetime

|Metadata|Type|Description|
|---|---|---|
|timex|string|The ISO 8601 formatted date and time:<br>`YYYY-MM-DDTHH:MM:SS`(year, month, day, hour, minutes, seconds, milliseconds) with a `T` separator. |
|value|string|The actual denoted date and time.|

Similar to dates, you can have ambiguous datetime entities. Resolution provides this year and the next as options. The `timex` value **XXXX** indicates no year was specified.

```json
"metadata": {
                 "dateValues": [
                       {
                           "timex": "XXXX-05-03T12",
                           "value": "2022-05-03 12:00:00"
                       },
                       {
                           "timex": "XXXX-05-03T12",
                           "value": "2023-05-03 12:00:00"
                       }
                  ]
              }
```

### Information

|Metadata|Type|Description|
|---|---|---|
|**unit**|string|Unit of measurement for information (data).|
|**value**|number|Numeric value for information.|

```json

"metadata": {
                "unit": "Kilobit",
                "value": 30
            }

```

**Possible values for *unit***:

* Bit
* Byte
* Gigabit
* Gigabyte
* Kilobit
* Kilobyte
* Megabit
* Megabyte
* Petabit
* Petabyte
* Terabit
* Terabyte
* Unspecified

### Length

|Metadata|Type|Description|
|---|---|---|
|**unit**|string|Unit of measurement for length|
|**value**|number|Numeric value.|

```json

"metadata": {
                "unit": "Kilobit",
                "value": 30
            }

```
**Possible values for *unit***:

* Centimeter
* Decameter
* Decimeter
* Foot
* Hectometer
* Inch
* Kilometer
* LightYear
* Meter
* Micrometer
* Mile
* Millimeter
* Nanometer
* Picometer
* Point
* Yard
* Unspecified

### Number

|Metadata|Type|Description|
|---|---|---|
|**numberKind**|string|Number type.|
|**value**|number|Numeric value for number.|

```json

"metadata": {
                "numberKind": "Integer",
                "value": 30
            }

```

**Possible values for *numberKind***:

* Decimal
* Fraction
* Integer
* Percent
* Power
* Unspecified

### NumericRange

|Metadata|Type|Description|
|---|---|---|
|**rangeKind**|string|A supported numeric range.|
|**minimum**|number|The beginning value of  the interval.|
|**maximum**|number|The ending value of the interval.|

```json

"metadata": {
                "rangeKind": "length",
                "minimum": 30,
                "maximum": 100
            }

```
**Possible values for *rangeKind***:

* Age
* Area
* Currency
* Information
* Length
* Number
* Speed
* Temperature
* Volume
* Weight

### Ordinal

|Metadata|Type|Description|
|---|---|---|
|**offset**|string|The offset with respect to the reference (for example, offset = -1 indicates the second to last)|
|**relativeTo**|The reference point that the ordinal number denotes.|
|**value**|number|Numeric value for ordinal position.|

```json

"metadata": {
                "offset": -1,
                "relativeTo":"Current",
                "value": "first"
            }

```

**Possible values for *relativeTo***:

* Current
* End
* Start

### Set

A recurring datetime period (example: "every Monday at 6:00 PM.")

|Metadata|Type|Description|
|---|---|---|
|**timex**|string|The ISO 8601 formatted date and time:<br>`YYYY-MM-DDTHH:MM:SS`(year, month, day, hour, minutes, seconds, milliseconds) with a `T` separator. |
|**value**|string|Sets don't resolve to exact values, as they don't indicate an exact datetime.|


```json

"metadata": {
                "timex": "XXXX-WXX-1T18",
                "value": "not resolved"
            }

```

**Possible values for *type***:

* begin
* end
* duration
* modifier (example: `before`, `after`)
* timex


### Speed

|Metadata|Type|Description|
|---|---|---|
|**unit**|string|Unit of measurement for speed.|
|**value**|number|Numeric value for speed.|

```json

"metadata": {
                "unit": "Knots",
                "value": 50
            }

```

**Possible values for *unit***:

* CentimetersPerMillisecond
* FeetPerMinute
* FeetPerSecond
* KilometersPerHour
* KilometersPerMillisecond
* KilometersPerMinute
* KilometersPerSecond
* Knots
* MetersPerMillisecond
* MetersPerSecond
* MilesPerHour
* YardsPerMinute
* YardsPerSecond
* Unspecified

### Temperature

|Metadata|Type|Description|
|---|---|---|
|**unit**|string|Unit of measurement for temperature.|
|**value**|number|Numeric value.|

```json

"metadata": {
                "unit" "Kelvin",
                "value": 310
            }

```
**Possible values for *unit***:

* Celsius
* Fahrenheit
* Kelvin
* Rankine
* Unspecified



### Time

|Metadata|Type|Description|
|---|---|---|
|**timex**|string|The ISO 8601 formatted date time:<br>`[hh]:[mm]:[ss]`(hour, minutes, seconds).|
|**value**|number|Numeric value.|

```json

"metadata": {
                "timex":"T14:30:15",
                "value": "14:30:15"
            }

```

### Volume

|Metadata|Type|Description|
|---|---|---|
|**unit**|string|Unit of measurement for volume.|
|**value**|number|Numeric value for volume.|

```json

"metadata": {
                "unit": "Quart",
                "value": 4
            }

```
**Possible values for *unit***:

* Barrel
* Bushel
* Centiliter
* Cord
* CubicCentimeter
* CubicFoot
* CubicInch
* CubicMeter
* CubicMile
* CubicMillimeter
* CubicYard
* Cup
* Decaliter
* FluidDram
* FluidOunce
* Gill
* Hectoliter
* Hogshead
* Liter
* Milliliter
* Minim
* Peck
* Pinch
* Pint
* Quart
* Tablespoon
* Teaspoon
* Unspecified

### Weight

|Metadata|Type|Description|
|---|---|---|
|**unit**|string|Unit of measurement for weight.|
|**value**|number|Numeric value for weight.|

```json

"metadata": {
                "unit": "Ounce",
                "value": 16
            }

```
**Possible values for *unit***:

* Dram
* Gallon
* Grain
* Gram
* Kilogram
* LongTonBritish
* MetricTon
* Milligram
* Ounce
* PennyWeight
* Pound
* ShortHundredWeightUS
* ShortTonUS
* Stone
* Ton
* Unspecified


## Next steps


Learn [how to use NER](../how-to-call.md)
