# Datasets Description

## 1. Train-Test Dataset

Training data consists of time series features:

- **store_nbr**: Identifies the store at which the products are sold.
- **family**: Identifies the type of product sold.
- **onpromotion**: Indicates the total number of items in a product family that were being promoted at a store on a given date.

**Target:**
- **Sales**: Total sales for a product family at a particular store on a given date. Fractional values are possible since products can be sold in fractional units (e.g., 1.5 kg of cheese).

| index |  id  |    date    | store_nbr |   family   |  sales  | onpromotion |
|:-----:|:----:|:----------:|:---------:|------------|:-------:|:-----------:|
|   0   |  0   | 2019-04-01 |     1     | AUTOMOTIVE |   0.0   |      0      |
|   1   |  1   | 2019-04-01 |     1     | BABY CARE  |   0.0   |      0      |
|   2   |  2   | 2019-04-01 |     1     |   BEAUTY   |   0.0   |      0      |
|   3   |  3   | 2019-04-01 |     1     | BEVERAGES  |   0.0   |      0      |
|   4   |  4   | 2019-04-01 |     1     |   BOOKS    |   0.0   |      0      |

## 2. Stores Dataset

Store metadata includes:

- **city**: City location information (22 Cities).
- **state**: State location information (16 States).
- **type**: Store type (5 Types).
- **cluster**: Grouping of similar stores (17 Clusters).

|index|store_nbr|city|state|type|cluster|
|:-----:|:-----:|---|---|:-----:|:-----:|
|0|1|Quito|Pichincha|D|13|
|1|2|Quito|Pichincha|D|13|
|2|3|Quito|Pichincha|D|8|
|3|4|Quito|Pichincha|D|9|
|4|5|Santo Domingo|Santo Domingo de los Tsachilas|D|4|

## 3. Holidays Events Dataset

- **Note**:
  - **transferred**: Some holidays officially fall on specific dates but are moved by the government.
  - **Bridge days**: Extra days added to holidays for extended breaks.
  - **Work Day**: Compensates for Bridge days, not normally scheduled workdays.

|index|date|type|locale|locale_name|description|transferred|
|:-----:|:-----:|:-----:|---|---|---|:-----:|
|0|2018-05-31|Holiday|Local|Manta|Fundacion de Manta|false|
|1|2018-06-30|Holiday|Regional|Cotopaxi|Provincializacion de Cotopaxi|false|
|2|2018-07-11|Holiday|Local|Cuenca|Fundacion de Cuenca|false|
|3|2018-07-13|Holiday|Local|Libertad|Cantonizacion de Libertad|false|
|4|2018-07-20|Holiday|Local|Riobamba|Cantonizacion de Riobamba|false|

## 4. Oil Dataset

Daily oil price, including values during both the train and test data timeframes. (Ecuador is an oil-dependent country, and its economic health is highly vulnerable to shocks in oil prices).

|index|date|dcoilwtico|
|:-----:|:-----:|:-----:|
|0|2019-04-01|NaN|
|1|2019-04-02|93.14|
|2|2019-04-03|92.97|
|3|2019-04-04|93.12|
|4|2019-04-07|93.20|

Dengan tampilan ini, informasi mengenai dataset akan lebih mudah dipahami oleh pengguna GitHub Anda. Anda dapat menyalin teks di atas dan memasukkannya ke dalam `readme.md` di repositori GitHub Anda.
