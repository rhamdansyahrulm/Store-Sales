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
