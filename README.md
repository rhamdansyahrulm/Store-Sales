# Datasets Description

## 1. Train-Test Dataset

Training data consists of time series features:

- **store_nbr**: Identifies the store at which the products are sold.
- **family**: Identifies the type of product sold.
- **onpromotion**: Indicates the total number of items in a product family that were being promoted at a store on a given date.

**Target:**
- **Sales**: Total sales for a product family at a particular store on a given date. Fractional values are possible since products can be sold in fractional units (e.g., 1.5 kg of cheese).

<div align="center">
  <table>
    <tr>
      <th>index</th>
      <th>id</th>
      <th>date</th>
      <th>store_nbr</th>
      <th>family</th>
      <th>sales</th>
      <th>onpromotion</th>
    </tr>
    <tr>
      <td>0</td>
      <td>0</td>
      <td>2019-04-01</td>
      <td>1</td>
      <td>AUTOMOTIVE</td>
      <td>0.0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>1</td>
      <td>1</td>
      <td>2019-04-01</td>
      <td>1</td>
      <td>BABY CARE</td>
      <td>0.0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2</td>
      <td>2019-04-01</td>
      <td>1</td>
      <td>BEAUTY</td>
      <td>0.0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>3</td>
      <td>3</td>
      <td>2019-04-01</td>
      <td>1</td>
      <td>BEVERAGES</td>
      <td>0.0</td>
      <td>0</td>
    </tr>
    <tr>
      <td>4</td>
      <td>4</td>
      <td>2019-04-01</td>
      <td>1</td>
      <td>BOOKS</td>
      <td>0.0</td>
      <td>0</td>
    </tr>
  </table>
</div>


## 2. Stores Dataset

Store metadata includes:

- **city**: City location information (22 Cities).
- **state**: State location information (16 States).
- **type**: Store type (5 Types).
- **cluster**: Grouping of similar stores (17 Clusters).

<div align="center">
  <table>
    <tr>
      <th>index</th>
      <th>store_nbr</th>
      <th>city</th>
      <th>state</th>
      <th>type</th>
      <th>cluster</th>
    </tr>
    <tr>
      <td>0</td>
      <td>1</td>
      <td>Quito</td>
      <td>Pichincha</td>
      <td>D</td>
      <td>13</td>
    </tr>
    <tr>
      <td>1</td>
      <td>2</td>
      <td>Quito</td>
      <td>Pichincha</td>
      <td>D</td>
      <td>13</td>
    </tr>
    <tr>
      <td>2</td>
      <td>3</td>
      <td>Quito</td>
      <td>Pichincha</td>
      <td>D</td>
      <td>8</td>
    </tr>
    <tr>
      <td>3</td>
      <td>4</td>
      <td>Quito</td>
      <td>Pichincha</td>
      <td>D</td>
      <td>9</td>
    </tr>
    <tr>
      <td>4</td>
      <td>5</td>
      <td>Santo Domingo</td>
      <td>Santo Domingo de los Tsachilas</td>
      <td>D</td>
      <td>4</td>
    </tr>
  </table>
</div>


## 3. Holidays Events Dataset

- **Note**:
  - **transferred**: Some holidays officially fall on specific dates but are moved by the government.
  - **Bridge days**: Extra days added to holidays for extended breaks.
  - **Work Day**: Compensates for Bridge days, not normally scheduled workdays.

<div align="center">
  <table>
    <tr>
      <th>index</th>
      <th>date</th>
      <th>type</th>
      <th>locale</th>
      <th>locale_name</th>
      <th>description</th>
      <th>transferred</th>
    </tr>
    <tr>
      <td>0</td>
      <td>2018-05-31</td>
      <td>Holiday</td>
      <td>Local</td>
      <td>Manta</td>
      <td>Fundacion de Manta</td>
      <td>false</td>
    </tr>
    <tr>
      <td>1</td>
      <td>2018-06-30</td>
      <td>Holiday</td>
      <td>Regional</td>
      <td>Cotopaxi</td>
      <td>Provincializacion de Cotopaxi</td>
      <td>false</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2018-07-11</td>
      <td>Holiday</td>
      <td>Local</td>
      <td>Cuenca</td>
      <td>Fundacion de Cuenca</td>
      <td>false</td>
    </tr>
    <tr>
      <td>3</td>
      <td>2018-07-13</td>
      <td>Holiday</td>
      <td>Local</td>
      <td>Libertad</td>
      <td>Cantonizacion de Libertad</td>
      <td>false</td>
    </tr>
    <tr>
      <td>4</td>
      <td>2018-07-20</td>
      <td>Holiday</td>
      <td>Local</td>
      <

## 4. Oil Dataset

Daily oil price, including values during both the train and test data timeframes. (Ecuador is an oil-dependent country, and its economic health is highly vulnerable to shocks in oil prices).

<div align="center">
  <table>
    <tr>
      <th>index</th>
      <th>date</th>
      <th>dcoilwtico</th>
    </tr>
    <tr>
      <td>0</td>
      <td>2019-04-01</td>
      <td>NaN</td>
    </tr>
    <tr>
      <td>1</td>
      <td>2019-04-02</td>
      <td>93.14</td>
    </tr>
    <tr>
      <td>2</td>
      <td>2019-04-03</td>
      <td>92.97</td>
    </tr>
    <tr>
      <td>3</td>
      <td>2019-04-04</td>
      <td>93.12</td>
    </tr>
    <tr>
      <td>4</td>
      <td>2019-04-07</td>
      <td>93.20</td>
    </tr>
  </table>
</div>

