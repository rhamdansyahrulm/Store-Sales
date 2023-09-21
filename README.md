# Store Sales - Time Series Forecasting

https://public.tableau.com/views/EcuadorsStoreSales/Home?:language=en-US&:display_count=n&:origin=viz_share_link

**predict sales for the thousands of product families sold at Favorita stores located in Ecuador**. The training data includes dates, store and product information, whether that item was being promoted, as well as the sales numbers. Additional files include supplementary information that may be useful in building your models.

## Datasets Description
1. ### Train-Test Dataset
   Training data, comprising time series of features:
   - **store_nbr**<br> 
    Identifies the store at which the products are sold.
   - **family**<br>
    Identifies the type of product sold.
   - **onpromotion**<br>
    Gives the total number of items in a product family that were being promoted at a store at a given date.
  
    <br>Target : 
    - **Sales**<br> 
     Gives the total sales for a product family at a particular store at a given date. Fractional values are possible since products can be sold in fractional units (e.g., 1.5 kg of cheese).
        
     | index |  id  |    date    | store_nbr |   family   |  sales  | onpromotion |
     |:-----:|:----:|:----------:|:---------:|------------|:-------:|:-----------:|
     |   0   |  0   | 2019-04-01 |     1     | AUTOMOTIVE |   0.0   |      0      |
     |   1   |  1   | 2019-04-01 |     1     | BABY CARE  |   0.0   |      0      |
     |   2   |  2   | 2019-04-01 |     1     |   BEAUTY   |   0.0   |      0      |
     |   3   |  3   | 2019-04-01 |     1     | BEVERAGES  |   0.0   |      0      |
     |   4   |  4   | 2019-04-01 |     1     |   BOOKS    |   0.0   |      0      |


3. ### Stores Dataset
   - Store metadata including:
     - **city**&emsp; &ensp;&ensp;: City Location information. (22 Cities)
        - Quito, Santo Domingo, Cayambe, Latacunga, Riobamba, Ibarra,
        Guaranda, Puyo, Ambato, Guayaquil, Salinas, Daule, Babahoyo,
        Quevedo, Playas, Libertad, Cuenca, Loja, Machala, Esmeraldas,
        Manta, El Carmen
     - **state** &emsp;&ensp;: State Location information. (16 States)
       - Pichincha, Santo Domingo de los Tsachilas, Cotopaxi, Chimborazo,
        Imbabura, Bolivar, Pastaza, Tungurahua, Guayas, Santa Elena,
        Los Rios, Azuay, Loja, El Oro, Esmeraldas, Manabi
     - **type** &emsp; &ensp;: Store type. (5 Types)
       - A, B, C, D, E
     - **cluster** &ensp; : Grouping of similar stores. (17 Clusters)
       - 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17
     <center>
        
     |index|store\_nbr|city|state|type|cluster|
     |:-----:|:-----:|---|---|:-----:|:-----:|
     |0|1|Quito|Pichincha|D|13|
     |1|2|Quito|Pichincha|D|13|
     |2|3|Quito|Pichincha|D|8|
     |3|4|Quito|Pichincha|D|9|
     |4|5|Santo Domingo|Santo Domingo de los Tsachilas|D|4|
     </center>

4. ### Holidays Events Dataset
   - **Note**:
     - **transferred**&emsp;&ensp;: Some holidays officially fall on specific dates but are moved by the government.
     - **Bridge days**&ensp; &ensp;: Extra days added to holidays for extended breaks.
     - **Work Day**&emsp;&emsp;: Compensates for Bridge days, not normally scheduled workdays.
    <center>
       
   |index|date|type|locale|locale\_name|description|transferred|
   |:-----:|:-----:|:-----:|---|---|---|:-----:|
   |0|2018-05-31|Holiday|Local|Manta|Fundacion de Manta|false|
   |1|2018-06-30|Holiday|Regional|Cotopaxi|Provincializacion de Cotopaxi|false|
   |2|2018-07-11|Holiday|Local|Cuenca|Fundacion de Cuenca|false|
   |3|2018-07-13|Holiday|Local|Libertad|Cantonizacion de Libertad|false|
   |4|2018-07-20|Holiday|Local|Riobamba|Cantonizacion de Riobamba|false|

5. ### Oil Dataset
   - **Daily oil price**. Includes values during both the train and test data timeframes. **(Ecuador is an oil-dependent country and it's economical health is highly vulnerable to shocks in oil prices.)** 
   <center>
      
    |index|date|dcoilwtico|
    |:-----:|:-----:|:-----:|
    |0|2019-04-01|NaN|
    |1|2019-04-02|93\.14|
    |2|2019-04-03|92\.97|
    |3|2019-04-04|93\.12|
    |4|2019-04-07|93\.2| 
   </center>
---
## Data Preprocessing

1. ### **Holidays Dataset**
    - **Event Handling with Transfer = True** : Events marked with transfer = True are similar to regular workdays and may not significantly affect prediction outcomes. Therefore, they can be safely removed from consideration.
    - **Shortened Event Descriptions** : Event descriptions are lengthy and verbose. To enhance clarity, it's recommended to truncate the descriptions to focus on essential information. For instance:
      - **Words to be removed**: puente, recupero, traslado
      - **Important words contain information** : fundacion, provincializacion, terremoto manabi, mundial de futbol brasil, fundacion, cantonizacion, primer dia del ano, independencia, navidad, dia de la madre
      <center>
         
      |index|date|type|locale|locale\_name|description|
      |---|---|---|---|---|---|
      |0|2018-05-31|Holiday|Local|Manta|fundacion|
      |1|2018-06-30|Holiday|Regional|Cotopaxi|provincializacion|
      |2|2018-07-11|Holiday|Local|Cuenca|fundacion|
      |3|2018-07-13|Holiday|Local|Libertad|cantonizacion|
      |4|2018-07-20|Holiday|Local|Riobamba|cantonizacion| 
      </center>
    -  The types of events are divided into three categories: local (city), regional (state), and national events. National events are likely to impact predictions across all locations, while on the other hand, local and regional events will only influence the city and state where the event occurs. Hence, when connecting the "Holidays" dataset with the train-test data, it's essential to consider both the location and type of each event.
  
2. ### **Oil Datasets**
    The list of oil price data available **does not have complete data for each day**; there are **missing dates** or **dates with null values for oil prices**. Therefore, there are several steps that need to be taken:
    
    -  Adding new rows for each missing date in the dataset.
    -  Performing null value imputation using **regression imputation**. This is because the price values correlate with dates, allowing us to utilize temporal information as a feature.
    <center> 
       
    ![image](https://github.com/rhamdansyahrulm/Store-Sales/assets/141615487/75785055-1683-449e-af14-363b3f40f48d)
    </center> 
3. ### **Merge Datasets & Selection Features**
    - The first datasets to be merged are the train-test data and the stores data. The purpose of this merging is to obtain information about the location (city and state), as well as the type and cluster of a store. The merging of these two datasets is carried out using the "store_nbr" column as the join key.
    <center>

    |index|date|store\_nbr|family|sales|onpromotion|city|state|type|cluster|
    |:-----:|:-----:|:-----:|---|:-----:|:-----:|---|---|:-----:|:-----:|
    |0|2019-04-01|1|AUTOMOTIVE|0\.0|0|Quito|Pichincha|D|13|
    |1|2019-04-02|1|BABY CARE|0\.0|0|Quito|Pichincha|D|13|
    |2|2019-04-03|1|BEAUTY|0\.0|0|Quito|Pichincha|D|13|
    |3|2019-04-04|1|BEVERAGES|0\.0|0|Quito|Pichincha|D|13|
    |4|2019-04-05|1|BOOKS|0\.0|0|Quito|Pichincha|D|13| 
    </center>

   - Once the store's location is known, the data will be split into separate tables for each store and the type of products sold.
   - Subsequently, the datasets are merged with the oil price data to understand the impact of daily oil prices on store revenue.
   - Following that, merging is performed with the dates of events, whether they are local, regional, or national, to understand the impact of significant events on store revenue.
   - Conduct column selection for unused features. This is because these features might have limited impact on making predictions. Some of these columns include "city", "state", "store_nbr", "family", "type", "cluster".
   - Perform label encoding on string-type features. Some of these columns include "case" dan "description"
   <center>

   |date|id|sales|onpromotion|dcoilwtico|case\_city|description\_city|case\_regional|description\_regional|case|description|
   |:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|:-----:|
   |2019-01-01|36|0\.0|0|93\.07|2|1|0|0|3|11|
   |2019-01-02|1818|396\.0|0|93\.14|2|1|0|0|6|16|
   |2019-01-03|3600|399\.0|0|92\.97|2|1|0|0|6|16|
   |2019-01-04|5382|460\.0|0|93\.12|2|1|0|0|6|16|
   |2019-01-05|7164|624\.0|0|93\.09|2|1|0|0|5|10| 
   </center>

   - Next, I will scale the values of all the features that I will use during the training process. It can help prevent numerical instability issues that may arise during computations, especially when dealing with large values or tiny differences between data points.
   - Finally, I create a windowed dataset with a window size of 7 and a stride of 1. It makes allows me to extract and structure temporal information from time series data, making it suitable for various analytical and modeling tasks.
   <center>

   |index|onpromotion|dcoilwtico|case\_Local|description\_Local|case\_Regional|description\_Regional|case\_National|description\_National|sales\_1|sales\_2|sales\_3|sales\_4|sales\_5|sales\_6|y|
   |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
   |0|0\.0|0\.792|1\.0|0\.0|0\.0|0\.0|0\.6|0\.733|0\.0|0\.254|0\.213|0\.158|0\.253|0\.268|0\.195|
   |1|0\.0|0\.793|1\.0|0\.0|0\.0|0\.0|1\.0|0\.0|0\.254|0\.213|0\.158|0\.253|0\.268|0\.195|0\.174|
   |2|0\.0|0\.791|1\.0|0\.0|0\.0|0\.0|1\.0|0\.0|0\.213|0\.158|0\.253|0\.268|0\.195|0\.174|0\.146|
   |3|0\.0|0\.793|1\.0|0\.0|0\.0|0\.0|1\.0|0\.0|0\.158|0\.253|0\.268|0\.195|0\.174|0\.146|0\.145|
   |4|0\.0|0\.792|1\.0|0\.0|0\.0|0\.0|1\.0|0\.667|0\.253|0\.268|0\.195|0\.174|0\.146|0\.145|0\.143|
   </center>

---
## **Create a Machine Learning Models (Using XGBRegressor)**

1. Split the data into **training data** (1554 samples), **testing data** (150 samples), and **prediction data** (16 samples) for each table that has been partitioned based on store number and product type.

<center>
   
![image](https://github.com/rhamdansyahrulm/Store-Sales/assets/141615487/572f0f0a-2776-4116-bde3-d0e5b1fe0c8d)
</center>

1. Create a machine learning model using the **XGBRegressor** technique with the following parameters:
   - **n_estimators** = 1000
   - **early_stopping_rounds** = 50
   - **evaluation metric** = root mean square error (RMSE).
2. Identify the features that have the most significant impact on the model.
<center>
   
![image](https://github.com/rhamdansyahrulm/Store-Sales/assets/141615487/a30f5c13-c03c-47b8-b7bb-6679bae74a95)
</center>
3. Evaluate the model by observing the error values at each epoch.
4. Compare the prediction results with the actual values.
